/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : create_validation_history.sql
Schema      : monitoring
Object      : validation_history
Purpose     : Enterprise Warehouse Validation History
Description : Stores the results of every warehouse validation execution,
              including validation rule, object validated, execution status,
              row counts, execution duration and error information.

Business Process : Enterprise Data Quality & Warehouse Validation
Owner            : Data Engineering
Platform         : PostgreSQL 18
Version          : 4.0.0
===============================================================================

TABLE GRAIN
-----------
One row per validation rule executed.

PRIMARY KEY
-----------
validation_id

FOREIGN KEY
-----------
run_id -> monitoring.etl_run_history(run_id)

POPULATED BY
------------
analytics.validate_warehouse()

Future Data Quality Framework

Deployment Validation Framework

===============================================================================
*/

DROP TABLE IF EXISTS monitoring.validation_history CASCADE;

CREATE TABLE monitoring.validation_history
(
    ----------------------------------------------------------------------------
    -- PRIMARY KEY
    ----------------------------------------------------------------------------
    validation_id               BIGINT
                                    GENERATED ALWAYS AS IDENTITY
                                    PRIMARY KEY,

    ----------------------------------------------------------------------------
    -- PIPELINE EXECUTION
    ----------------------------------------------------------------------------
    run_id                      BIGINT,

    ----------------------------------------------------------------------------
    -- VALIDATION INFORMATION
    ----------------------------------------------------------------------------
    validation_name             VARCHAR(150)    NOT NULL,

    validation_category         VARCHAR(100)    NOT NULL,

    target_object               VARCHAR(150)    NOT NULL,

    ----------------------------------------------------------------------------
    -- EXECUTION STATUS
    ----------------------------------------------------------------------------
    status                      VARCHAR(20)     NOT NULL,

    ----------------------------------------------------------------------------
    -- VALIDATION RESULTS
    ----------------------------------------------------------------------------
    rows_checked                BIGINT          NOT NULL
                                    DEFAULT 0,

    rows_failed                 BIGINT          NOT NULL
                                    DEFAULT 0,

    validation_score            NUMERIC(5,2),

    ----------------------------------------------------------------------------
    -- EXECUTION
    ----------------------------------------------------------------------------
    started_at                  TIMESTAMPTZ     NOT NULL
                                    DEFAULT clock_timestamp(),

    completed_at                TIMESTAMPTZ,

    execution_time_ms           BIGINT,

    ----------------------------------------------------------------------------
    -- DETAILS
    ----------------------------------------------------------------------------
    validation_message          TEXT,

    error_message               TEXT,

    ----------------------------------------------------------------------------
    -- AUDIT
    ----------------------------------------------------------------------------
    created_at                  TIMESTAMPTZ
                                    DEFAULT clock_timestamp(),

    ----------------------------------------------------------------------------
    -- FOREIGN KEY
    ----------------------------------------------------------------------------
    CONSTRAINT fk_validation_run
        FOREIGN KEY (run_id)
        REFERENCES monitoring.etl_run_history(run_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    ----------------------------------------------------------------------------
    -- CHECK CONSTRAINTS
    ----------------------------------------------------------------------------
    CONSTRAINT chk_validation_status
        CHECK
        (
            status IN
            (
                'PASSED',
                'FAILED',
                'WARNING',
                'SKIPPED'
            )
        ),

    CONSTRAINT chk_validation_score
        CHECK
        (
            validation_score IS NULL
            OR
            (
                validation_score >= 0
                AND
                validation_score <= 100
            )
        ),

    CONSTRAINT chk_rows_checked
        CHECK (rows_checked >= 0),

    CONSTRAINT chk_rows_failed
        CHECK (rows_failed >= 0),

    CONSTRAINT chk_execution_time
        CHECK
        (
            execution_time_ms IS NULL
            OR execution_time_ms >= 0
        )
);

-------------------------------------------------------------------------------
-- TABLE COMMENT
-------------------------------------------------------------------------------

COMMENT ON TABLE monitoring.validation_history IS
'Stores the outcome of every warehouse validation rule execution for data quality, referential integrity, deployment verification and operational monitoring.';

-------------------------------------------------------------------------------
-- COLUMN COMMENTS
-------------------------------------------------------------------------------

COMMENT ON COLUMN monitoring.validation_history.validation_id IS
'Unique identifier for each validation execution.';

COMMENT ON COLUMN monitoring.validation_history.run_id IS
'Associated ETL pipeline execution from monitoring.etl_run_history.';

COMMENT ON COLUMN monitoring.validation_history.validation_name IS
'Name of the validation rule executed.';

COMMENT ON COLUMN monitoring.validation_history.validation_category IS
'Validation category (Integrity, Data Quality, Referential Integrity, Business Rules, Deployment, etc.).';

COMMENT ON COLUMN monitoring.validation_history.target_object IS
'Warehouse object being validated.';

COMMENT ON COLUMN monitoring.validation_history.status IS
'Validation execution result.';

COMMENT ON COLUMN monitoring.validation_history.rows_checked IS
'Total records evaluated by the validation rule.';

COMMENT ON COLUMN monitoring.validation_history.rows_failed IS
'Number of records that failed validation.';

COMMENT ON COLUMN monitoring.validation_history.validation_score IS
'Validation success percentage (0-100).';

COMMENT ON COLUMN monitoring.validation_history.started_at IS
'Timestamp when validation execution started.';

COMMENT ON COLUMN monitoring.validation_history.completed_at IS
'Timestamp when validation execution completed.';

COMMENT ON COLUMN monitoring.validation_history.execution_time_ms IS
'Validation execution duration in milliseconds.';

COMMENT ON COLUMN monitoring.validation_history.validation_message IS
'Human-readable validation summary or recommendation.';

COMMENT ON COLUMN monitoring.validation_history.error_message IS
'Captured error message when validation execution fails.';

COMMENT ON COLUMN monitoring.validation_history.created_at IS
'Record creation timestamp.';

-------------------------------------------------------------------------------
-- INDEXES
-------------------------------------------------------------------------------

CREATE INDEX idx_validation_history_run_id
    ON monitoring.validation_history (run_id);

CREATE INDEX idx_validation_history_name
    ON monitoring.validation_history (validation_name);

CREATE INDEX idx_validation_history_category
    ON monitoring.validation_history (validation_category);

CREATE INDEX idx_validation_history_target
    ON monitoring.validation_history (target_object);

CREATE INDEX idx_validation_history_status
    ON monitoring.validation_history (status);

CREATE INDEX idx_validation_history_started
    ON monitoring.validation_history (started_at DESC);

CREATE INDEX idx_validation_history_completed
    ON monitoring.validation_history (completed_at DESC);

CREATE INDEX idx_validation_history_created
    ON monitoring.validation_history (created_at DESC);

CREATE INDEX idx_validation_history_run_status
    ON monitoring.validation_history
    (
        run_id,
        status
    );

CREATE INDEX idx_validation_history_target_status
    ON monitoring.validation_history
    (
        target_object,
        status
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
  AND table_name = 'validation_history';

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
  AND table_name = 'validation_history'
ORDER BY ordinal_position;

-------------------------------------------------------------------------------
-- VERIFY INDEXES
-------------------------------------------------------------------------------

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'monitoring'
  AND tablename = 'validation_history'
ORDER BY indexname;

-------------------------------------------------------------------------------
-- VERIFY CONSTRAINTS
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
  AND t.relname = 'validation_history'
ORDER BY conname;

-------------------------------------------------------------------------------
-- SAMPLE REPORT
-------------------------------------------------------------------------------

SELECT
    vh.validation_id,
    erh.pipeline_name,
    vh.validation_name,
    vh.validation_category,
    vh.target_object,
    vh.status,
    vh.rows_checked,
    vh.rows_failed,
    vh.validation_score,
    vh.execution_time_ms,
    vh.started_at,
    vh.completed_at
FROM monitoring.validation_history vh
LEFT JOIN monitoring.etl_run_history erh
       ON vh.run_id = erh.run_id
ORDER BY
    vh.validation_id DESC
LIMIT 20;

-------------------------------------------------------------------------------
-- END OF FILE
-------------------------------------------------------------------------------