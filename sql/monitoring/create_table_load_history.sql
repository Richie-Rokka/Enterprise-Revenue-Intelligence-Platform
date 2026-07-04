/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : create_table_load_history.sql
Schema      : monitoring
Object      : table_load_history
Purpose     : Enterprise Table Load Execution History
Description : Stores detailed execution metrics for every warehouse object
              loaded during an ETL pipeline execution. Each record is linked
              to a pipeline execution in monitoring.etl_run_history.

Business Process : Enterprise ETL Monitoring
Owner            : Data Engineering
Platform         : PostgreSQL 18
Version          : 4.0.0
===============================================================================

TABLE GRAIN
-----------
One row per warehouse object loaded during a pipeline execution.

PRIMARY KEY
-----------
load_history_id

FOREIGN KEY
-----------
run_id -> monitoring.etl_run_history(run_id)

POPULATED BY
------------
analytics.load_dim_date()

analytics.load_dim_customer()

analytics.load_dim_product()

analytics.load_dim_seller()

analytics.load_fact_sales()

analytics.refresh_warehouse()

analytics.refresh_metadata()

===============================================================================
*/

DROP TABLE IF EXISTS monitoring.table_load_history CASCADE;

CREATE TABLE monitoring.table_load_history
(
    ----------------------------------------------------------------------------
    -- PRIMARY KEY
    ----------------------------------------------------------------------------
    load_history_id             BIGINT
                                    GENERATED ALWAYS AS IDENTITY
                                    PRIMARY KEY,

    ----------------------------------------------------------------------------
    -- PIPELINE EXECUTION
    ----------------------------------------------------------------------------
    run_id                      BIGINT          NOT NULL,

    ----------------------------------------------------------------------------
    -- TARGET OBJECT
    ----------------------------------------------------------------------------
    target_table                VARCHAR(150)    NOT NULL,

    load_type                   VARCHAR(30)     NOT NULL,

    ----------------------------------------------------------------------------
    -- EXECUTION STATUS
    ----------------------------------------------------------------------------
    status                      VARCHAR(20)     NOT NULL,

    ----------------------------------------------------------------------------
    -- ROW METRICS
    ----------------------------------------------------------------------------
    rows_processed              BIGINT          NOT NULL
                                    DEFAULT 0,

    rows_inserted               BIGINT          NOT NULL
                                    DEFAULT 0,

    rows_updated                BIGINT          NOT NULL
                                    DEFAULT 0,

    rows_deleted                BIGINT          NOT NULL
                                    DEFAULT 0,

    ----------------------------------------------------------------------------
    -- EXECUTION TIMING
    ----------------------------------------------------------------------------
    started_at                  TIMESTAMPTZ     NOT NULL,

    completed_at                TIMESTAMPTZ,

    execution_time_ms           BIGINT,

    ----------------------------------------------------------------------------
    -- ERROR INFORMATION
    ----------------------------------------------------------------------------
    error_message               TEXT,

    ----------------------------------------------------------------------------
    -- AUDIT
    ----------------------------------------------------------------------------
    created_at                  TIMESTAMPTZ     NOT NULL
                                    DEFAULT clock_timestamp(),

    ----------------------------------------------------------------------------
    -- FOREIGN KEY
    ----------------------------------------------------------------------------
    

    ----------------------------------------------------------------------------
    -- CHECK CONSTRAINTS
    ----------------------------------------------------------------------------
    CONSTRAINT chk_table_load_status
        CHECK
        (
            status IN
            (
                'RUNNING',
                'SUCCESS',
                'FAILED',
                'WARNING',
                'CANCELLED'
            )
        ),

    CONSTRAINT chk_table_load_type
        CHECK
        (
            load_type IN
            (
                'FULL_REFRESH',
                'INCREMENTAL',
                'INITIAL_LOAD',
                'METADATA_REFRESH',
                'VALIDATION'
            )
        ),

    CONSTRAINT chk_table_rows_processed
        CHECK (rows_processed >= 0),

    CONSTRAINT chk_table_rows_inserted
        CHECK (rows_inserted >= 0),

    CONSTRAINT chk_table_rows_updated
        CHECK (rows_updated >= 0),

    CONSTRAINT chk_table_rows_deleted
        CHECK (rows_deleted >= 0),

    CONSTRAINT chk_table_execution_time
        CHECK
        (
            execution_time_ms IS NULL
            OR execution_time_ms >= 0
        )
);

-------------------------------------------------------------------------------
-- TABLE COMMENT
-------------------------------------------------------------------------------

COMMENT ON TABLE monitoring.table_load_history IS
'Detailed execution history for every warehouse object loaded during an ETL pipeline execution.';

-------------------------------------------------------------------------------
-- COLUMN COMMENTS
-------------------------------------------------------------------------------

COMMENT ON COLUMN monitoring.table_load_history.load_history_id IS
'Unique identifier for each table load execution.';

COMMENT ON COLUMN monitoring.table_load_history.run_id IS
'Foreign key to monitoring.etl_run_history identifying the parent pipeline execution.';

COMMENT ON COLUMN monitoring.table_load_history.target_table IS
'Warehouse table loaded during execution.';

COMMENT ON COLUMN monitoring.table_load_history.load_type IS
'Load strategy used for the table (FULL_REFRESH, INCREMENTAL, etc.).';

COMMENT ON COLUMN monitoring.table_load_history.status IS
'Execution status of the table load.';

COMMENT ON COLUMN monitoring.table_load_history.rows_processed IS
'Number of source rows processed.';

COMMENT ON COLUMN monitoring.table_load_history.rows_inserted IS
'Number of rows inserted into the target table.';

COMMENT ON COLUMN monitoring.table_load_history.rows_updated IS
'Number of rows updated in the target table.';

COMMENT ON COLUMN monitoring.table_load_history.rows_deleted IS
'Number of rows deleted from the target table.';

COMMENT ON COLUMN monitoring.table_load_history.started_at IS
'Timestamp when the table load started.';

COMMENT ON COLUMN monitoring.table_load_history.completed_at IS
'Timestamp when the table load completed.';

COMMENT ON COLUMN monitoring.table_load_history.execution_time_ms IS
'Execution duration in milliseconds.';

COMMENT ON COLUMN monitoring.table_load_history.error_message IS
'Captured error message when execution fails.';

COMMENT ON COLUMN monitoring.table_load_history.created_at IS
'Record creation timestamp.';

-------------------------------------------------------------------------------
-- INDEXES
-------------------------------------------------------------------------------

CREATE INDEX idx_table_load_history_run_id
    ON monitoring.table_load_history (run_id);

CREATE INDEX idx_table_load_history_target_table
    ON monitoring.table_load_history (target_table);

CREATE INDEX idx_table_load_history_status
    ON monitoring.table_load_history (status);

CREATE INDEX idx_table_load_history_load_type
    ON monitoring.table_load_history (load_type);

CREATE INDEX idx_table_load_history_started_at
    ON monitoring.table_load_history (started_at DESC);

CREATE INDEX idx_table_load_history_completed_at
    ON monitoring.table_load_history (completed_at DESC);

CREATE INDEX idx_table_load_history_created_at
    ON monitoring.table_load_history (created_at DESC);

CREATE INDEX idx_table_load_history_run_table
    ON monitoring.table_load_history
    (
        run_id,
        target_table
    );

CREATE INDEX idx_table_load_history_status_started
    ON monitoring.table_load_history
    (
        status,
        started_at DESC
    );

-------------------------------------------------------------------------------
-- VALIDATION
-------------------------------------------------------------------------------

-- Verify table exists
SELECT
    table_schema,
    table_name
FROM information_schema.tables
WHERE table_schema = 'monitoring'
  AND table_name = 'table_load_history';

-------------------------------------------------------------------------------
-- VERIFY STRUCTURE
-------------------------------------------------------------------------------

SELECT
    ordinal_position,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'monitoring'
  AND table_name = 'table_load_history'
ORDER BY ordinal_position;

-------------------------------------------------------------------------------
-- VERIFY INDEXES
-------------------------------------------------------------------------------

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'monitoring'
  AND tablename = 'table_load_history'
ORDER BY indexname;

-------------------------------------------------------------------------------
-- VERIFY FOREIGN KEY
-------------------------------------------------------------------------------

SELECT
    conname,
    pg_get_constraintdef(c.oid) AS constraint_definition
FROM pg_constraint c
INNER JOIN pg_class t
        ON c.conrelid = t.oid
INNER JOIN pg_namespace n
        ON n.oid = t.relnamespace
WHERE n.nspname = 'monitoring'
  AND t.relname = 'table_load_history'
ORDER BY conname;

-------------------------------------------------------------------------------
-- SAMPLE REPORT
-------------------------------------------------------------------------------

SELECT
    tlh.load_history_id,
    erh.pipeline_name,
    tlh.target_table,
    tlh.load_type,
    tlh.status,
    tlh.rows_processed,
    tlh.rows_inserted,
    tlh.rows_updated,
    tlh.rows_deleted,
    tlh.execution_time_ms,
    tlh.started_at,
    tlh.completed_at
FROM monitoring.table_load_history tlh
INNER JOIN monitoring.etl_run_history erh
        ON tlh.run_id = erh.run_id
ORDER BY tlh.load_history_id DESC
LIMIT 20;

-------------------------------------------------------------------------------
-- END OF FILE
-------------------------------------------------------------------------------