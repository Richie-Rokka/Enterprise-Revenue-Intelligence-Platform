/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : create_pipeline_execution_history.sql
Schema      : monitoring
Object      : pipeline_execution_history
Purpose     : Enterprise Pipeline Execution History
Description : Stores execution metadata for complete orchestration pipelines
              including refresh_warehouse, deployment pipelines, scheduled
              jobs and future orchestration workflows.

Business Process : Enterprise Pipeline Monitoring
Owner            : Data Engineering
Platform         : PostgreSQL 18
Version          : 4.0.0
===============================================================================

TABLE GRAIN
-----------
One row per pipeline execution.

PRIMARY KEY
-----------
pipeline_execution_id

FOREIGN KEY
-----------
run_id -> monitoring.etl_run_history(run_id)

POPULATED BY
------------
analytics.refresh_warehouse()

Future Scheduler

Warehouse Deployment Framework

CI/CD Pipelines

===============================================================================
*/

DROP TABLE IF EXISTS monitoring.pipeline_execution_history CASCADE;

CREATE TABLE monitoring.pipeline_execution_history
(
    ----------------------------------------------------------------------------
    -- PRIMARY KEY
    ----------------------------------------------------------------------------
    pipeline_execution_id       BIGINT
                                    GENERATED ALWAYS AS IDENTITY
                                    PRIMARY KEY,

    ----------------------------------------------------------------------------
    -- PIPELINE
    ----------------------------------------------------------------------------
    run_id                      BIGINT,

    pipeline_name               VARCHAR(150)    NOT NULL,

    pipeline_version            VARCHAR(30),

    execution_mode              VARCHAR(30)     NOT NULL,

    environment                 VARCHAR(30)
                                    DEFAULT 'Development',

    ----------------------------------------------------------------------------
    -- EXECUTION STATUS
    ----------------------------------------------------------------------------
    status                      VARCHAR(20)
                                    NOT NULL,

    ----------------------------------------------------------------------------
    -- PIPELINE METRICS
    ----------------------------------------------------------------------------
    stages_total                INTEGER
                                    DEFAULT 0,

    stages_completed            INTEGER
                                    DEFAULT 0,

    stages_failed               INTEGER
                                    DEFAULT 0,

    tables_loaded               INTEGER
                                    DEFAULT 0,

    ----------------------------------------------------------------------------
    -- ROW METRICS
    ----------------------------------------------------------------------------
    total_rows_processed        BIGINT
                                    DEFAULT 0,

    total_rows_inserted         BIGINT
                                    DEFAULT 0,

    total_rows_updated          BIGINT
                                    DEFAULT 0,

    total_rows_deleted          BIGINT
                                    DEFAULT 0,

    ----------------------------------------------------------------------------
    -- EXECUTION
    ----------------------------------------------------------------------------
    started_at                  TIMESTAMPTZ
                                    NOT NULL
                                    DEFAULT clock_timestamp(),

    completed_at                TIMESTAMPTZ,

    execution_time_ms           BIGINT,

    ----------------------------------------------------------------------------
    -- EXECUTION DETAILS
    ----------------------------------------------------------------------------
    executed_by                 VARCHAR(100)
                                    DEFAULT CURRENT_USER,

    host_name                   VARCHAR(255),

    application_name            VARCHAR(255),

    ----------------------------------------------------------------------------
    -- MESSAGES
    ----------------------------------------------------------------------------
    execution_summary           TEXT,

    error_message               TEXT,

    ----------------------------------------------------------------------------
    -- AUDIT
    ----------------------------------------------------------------------------
    created_at                  TIMESTAMPTZ
                                    NOT NULL
                                    DEFAULT clock_timestamp(),

    ----------------------------------------------------------------------------
    -- FOREIGN KEY
    ----------------------------------------------------------------------------
    CONSTRAINT fk_pipeline_execution_run
        FOREIGN KEY (run_id)
        REFERENCES monitoring.etl_run_history(run_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    ----------------------------------------------------------------------------
    -- CHECK CONSTRAINTS
    ----------------------------------------------------------------------------
    CONSTRAINT chk_pipeline_status
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

    CONSTRAINT chk_execution_mode
        CHECK
        (
            execution_mode IN
            (
                'MANUAL',
                'SCHEDULED',
                'AUTOMATED',
                'DEPLOYMENT'
            )
        ),

    CONSTRAINT chk_stage_totals
        CHECK
        (
            stages_total >= 0
            AND stages_completed >= 0
            AND stages_failed >= 0
        ),

    CONSTRAINT chk_rows_processed
        CHECK (total_rows_processed >= 0),

    CONSTRAINT chk_rows_inserted
        CHECK (total_rows_inserted >= 0),

    CONSTRAINT chk_rows_updated
        CHECK (total_rows_updated >= 0),

    CONSTRAINT chk_rows_deleted
        CHECK (total_rows_deleted >= 0),

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

COMMENT ON TABLE monitoring.pipeline_execution_history IS
'Stores execution history for complete warehouse pipeline executions, including orchestration metrics, execution summaries and operational monitoring.';

-------------------------------------------------------------------------------
-- COLUMN COMMENTS
-------------------------------------------------------------------------------

COMMENT ON COLUMN monitoring.pipeline_execution_history.pipeline_execution_id IS
'Unique identifier for each pipeline execution.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.run_id IS
'Associated ETL execution from monitoring.etl_run_history.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.pipeline_name IS
'Name of the executed pipeline.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.pipeline_version IS
'Version of the pipeline executed.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.execution_mode IS
'Execution mode (MANUAL, SCHEDULED, AUTOMATED or DEPLOYMENT).';

COMMENT ON COLUMN monitoring.pipeline_execution_history.environment IS
'Execution environment (Development, Test or Production).';

COMMENT ON COLUMN monitoring.pipeline_execution_history.status IS
'Overall pipeline execution status.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.stages_total IS
'Total number of pipeline stages scheduled for execution.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.stages_completed IS
'Number of successfully completed stages.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.stages_failed IS
'Number of failed pipeline stages.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.tables_loaded IS
'Total warehouse tables successfully loaded.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.total_rows_processed IS
'Total rows processed by the pipeline.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.total_rows_inserted IS
'Total rows inserted by the pipeline.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.total_rows_updated IS
'Total rows updated by the pipeline.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.total_rows_deleted IS
'Total rows deleted by the pipeline.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.started_at IS
'Timestamp when pipeline execution started.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.completed_at IS
'Timestamp when pipeline execution completed.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.execution_time_ms IS
'Pipeline execution duration in milliseconds.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.executed_by IS
'Database user that initiated the pipeline execution.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.host_name IS
'Host server executing the pipeline.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.application_name IS
'Application or scheduler responsible for the execution.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.execution_summary IS
'Execution summary generated after pipeline completion.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.error_message IS
'Captured error message when pipeline execution fails.';

COMMENT ON COLUMN monitoring.pipeline_execution_history.created_at IS
'Record creation timestamp.';

-------------------------------------------------------------------------------
-- INDEXES
-------------------------------------------------------------------------------

CREATE INDEX idx_pipeline_execution_run_id
    ON monitoring.pipeline_execution_history (run_id);

CREATE INDEX idx_pipeline_execution_name
    ON monitoring.pipeline_execution_history (pipeline_name);

CREATE INDEX idx_pipeline_execution_status
    ON monitoring.pipeline_execution_history (status);

CREATE INDEX idx_pipeline_execution_mode
    ON monitoring.pipeline_execution_history (execution_mode);

CREATE INDEX idx_pipeline_execution_environment
    ON monitoring.pipeline_execution_history (environment);

CREATE INDEX idx_pipeline_execution_started
    ON monitoring.pipeline_execution_history (started_at DESC);

CREATE INDEX idx_pipeline_execution_completed
    ON monitoring.pipeline_execution_history (completed_at DESC);

CREATE INDEX idx_pipeline_execution_created
    ON monitoring.pipeline_execution_history (created_at DESC);

CREATE INDEX idx_pipeline_execution_status_started
    ON monitoring.pipeline_execution_history
    (
        status,
        started_at DESC
    );

CREATE INDEX idx_pipeline_execution_name_status
    ON monitoring.pipeline_execution_history
    (
        pipeline_name,
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
  AND table_name = 'pipeline_execution_history';

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
  AND table_name = 'pipeline_execution_history'
ORDER BY ordinal_position;

-------------------------------------------------------------------------------
-- VERIFY INDEXES
-------------------------------------------------------------------------------

SELECT
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname = 'monitoring'
  AND tablename = 'pipeline_execution_history'
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
  AND t.relname = 'pipeline_execution_history'
ORDER BY conname;

-------------------------------------------------------------------------------
-- SAMPLE REPORT
-------------------------------------------------------------------------------

SELECT
    peh.pipeline_execution_id,
    peh.pipeline_name,
    peh.pipeline_version,
    peh.execution_mode,
    peh.environment,
    peh.status,
    peh.stages_total,
    peh.stages_completed,
    peh.stages_failed,
    peh.tables_loaded,
    peh.total_rows_processed,
    peh.total_rows_inserted,
    peh.total_rows_updated,
    peh.total_rows_deleted,
    peh.execution_time_ms,
    peh.executed_by,
    peh.started_at,
    peh.completed_at
FROM monitoring.pipeline_execution_history peh
ORDER BY
    peh.pipeline_execution_id DESC
LIMIT 20;

-------------------------------------------------------------------------------
-- END OF FILE
-------------------------------------------------------------------------------