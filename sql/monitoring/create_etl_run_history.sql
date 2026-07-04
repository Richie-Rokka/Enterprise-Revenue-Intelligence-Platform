/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : create_etl_run_history.sql
Schema      : monitoring
Object      : etl_run_history
Purpose     : Enterprise ETL Pipeline Execution History
Description : Stores execution metadata for every ETL pipeline run,
              including execution status, processing metrics, timing,
              and error information.

Business Process : Enterprise ETL Monitoring
Owner            : Data Engineering
Platform         : PostgreSQL 18
Version          : 4.0.0
===============================================================================

TABLE GRAIN
-----------
One row per ETL pipeline execution.

PRIMARY KEY
-----------
run_id

FOREIGN KEYS
------------
None

REFERENCED BY
-------------
monitoring.table_load_history

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

DROP TABLE IF EXISTS monitoring.etl_run_history CASCADE;

CREATE TABLE monitoring.etl_run_history
(
    ----------------------------------------------------------------------------
    -- PRIMARY KEY
    ----------------------------------------------------------------------------
    run_id                      BIGINT
                                    GENERATED ALWAYS AS IDENTITY
                                    PRIMARY KEY,

    ----------------------------------------------------------------------------
    -- PIPELINE INFORMATION
    ----------------------------------------------------------------------------
    pipeline_name               VARCHAR(150)    NOT NULL,

    target_table                VARCHAR(150)    NOT NULL,

    load_type                   VARCHAR(30)     NOT NULL,

    ----------------------------------------------------------------------------
    -- EXECUTION STATUS
    ----------------------------------------------------------------------------
    status                      VARCHAR(20)     NOT NULL
                                    DEFAULT 'RUNNING',

    ----------------------------------------------------------------------------
    -- EXECUTION TIMESTAMPS
    ----------------------------------------------------------------------------
    started_at                  TIMESTAMPTZ     NOT NULL
                                    DEFAULT clock_timestamp(),

    completed_at                TIMESTAMPTZ,

    ----------------------------------------------------------------------------
    -- EXECUTION METRICS
    ----------------------------------------------------------------------------
    rows_processed              BIGINT          NOT NULL
                                    DEFAULT 0,

    rows_inserted               BIGINT          NOT NULL
                                    DEFAULT 0,

    rows_updated                BIGINT          NOT NULL
                                    DEFAULT 0,

    rows_deleted                BIGINT          NOT NULL
                                    DEFAULT 0,

    execution_time_ms           BIGINT,

    ----------------------------------------------------------------------------
    -- ERROR HANDLING
    ----------------------------------------------------------------------------
    error_message               TEXT,

    ----------------------------------------------------------------------------
    -- AUDIT
    ----------------------------------------------------------------------------
    created_at                  TIMESTAMPTZ     NOT NULL
                                    DEFAULT clock_timestamp(),

    ----------------------------------------------------------------------------
    -- CONSTRAINTS
    ----------------------------------------------------------------------------
    CONSTRAINT chk_etl_run_status
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

    CONSTRAINT chk_etl_load_type
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

    CONSTRAINT chk_rows_processed
        CHECK (rows_processed >= 0),

    CONSTRAINT chk_rows_inserted
        CHECK (rows_inserted >= 0),

    CONSTRAINT chk_rows_updated
        CHECK (rows_updated >= 0),

    CONSTRAINT chk_rows_deleted
        CHECK (rows_deleted >= 0),

    CONSTRAINT chk_execution_time
        CHECK
        (
            execution_time_ms IS NULL
            OR execution_time_ms >= 0
        )
);

COMMENT ON TABLE monitoring.etl_run_history IS
'Enterprise ETL pipeline execution history capturing runtime metrics, execution status and audit information.';

-------------------------------------------------------------------------------
-- COLUMN COMMENTS
-------------------------------------------------------------------------------

COMMENT ON COLUMN monitoring.etl_run_history.run_id IS
'Unique identifier for each ETL pipeline execution.';

COMMENT ON COLUMN monitoring.etl_run_history.pipeline_name IS
'Name of the ETL pipeline or stored procedure executed.';

COMMENT ON COLUMN monitoring.etl_run_history.target_table IS
'Primary warehouse object being loaded.';

COMMENT ON COLUMN monitoring.etl_run_history.load_type IS
'Execution strategy (FULL_REFRESH, INCREMENTAL, INITIAL_LOAD, etc.).';

COMMENT ON COLUMN monitoring.etl_run_history.status IS
'Execution status of the ETL pipeline.';

COMMENT ON COLUMN monitoring.etl_run_history.started_at IS
'Timestamp when pipeline execution started.';

COMMENT ON COLUMN monitoring.etl_run_history.completed_at IS
'Timestamp when pipeline execution completed.';

COMMENT ON COLUMN monitoring.etl_run_history.rows_processed IS
'Total source records processed during execution.';

COMMENT ON COLUMN monitoring.etl_run_history.rows_inserted IS
'Number of rows inserted into the target object.';

COMMENT ON COLUMN monitoring.etl_run_history.rows_updated IS
'Number of existing rows updated.';

COMMENT ON COLUMN monitoring.etl_run_history.rows_deleted IS
'Number of rows deleted during execution.';

COMMENT ON COLUMN monitoring.etl_run_history.execution_time_ms IS
'Pipeline execution duration in milliseconds.';

COMMENT ON COLUMN monitoring.etl_run_history.error_message IS
'Error message returned if execution failed.';

COMMENT ON COLUMN monitoring.etl_run_history.created_at IS
'Record creation timestamp.';

-------------------------------------------------------------------------------
-- INDEXES
-------------------------------------------------------------------------------

CREATE INDEX idx_etl_run_history_pipeline
    ON monitoring.etl_run_history (pipeline_name);

CREATE INDEX idx_etl_run_history_target
    ON monitoring.etl_run_history (target_table);

CREATE INDEX idx_etl_run_history_status
    ON monitoring.etl_run_history (status);

CREATE INDEX idx_etl_run_history_load_type
    ON monitoring.etl_run_history (load_type);

CREATE INDEX idx_etl_run_history_started
    ON monitoring.etl_run_history (started_at DESC);

CREATE INDEX idx_etl_run_history_completed
    ON monitoring.etl_run_history (completed_at DESC);

CREATE INDEX idx_etl_run_history_created
    ON monitoring.etl_run_history (created_at DESC);

-------------------------------------------------------------------------------
-- VALIDATION
-------------------------------------------------------------------------------

-- Verify table exists
SELECT
    table_schema,
    table_name
FROM information_schema.tables
WHERE table_schema = 'monitoring'
  AND table_name = 'etl_run_history';

-------------------------------------------------------------------------------
-- Verify structure
-------------------------------------------------------------------------------

SELECT
    ordinal_position,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'monitoring'
  AND table_name = 'etl_run_history'
ORDER BY ordinal_position;

-------------------------------------------------------------------------------
-- Verify indexes
-------------------------------------------------------------------------------

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'monitoring'
  AND tablename = 'etl_run_history'
ORDER BY indexname;

-------------------------------------------------------------------------------
-- Verify constraints
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
  AND t.relname = 'etl_run_history'
ORDER BY conname;

-------------------------------------------------------------------------------
-- SAMPLE QUERY
-------------------------------------------------------------------------------

SELECT
    run_id,
    pipeline_name,
    target_table,
    load_type,
    status,
    rows_processed,
    rows_inserted,
    rows_updated,
    rows_deleted,
    execution_time_ms,
    started_at,
    completed_at
FROM monitoring.etl_run_history
ORDER BY run_id DESC
LIMIT 20;

-------------------------------------------------------------------------------
-- END OF FILE
-------------------------------------------------------------------------------