/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : create_quality_rule_history.sql
Schema      : monitoring
Purpose     : Stores enterprise data quality execution history
Version     : 1.0.0
===============================================================================
*/

CREATE TABLE IF NOT EXISTS monitoring.quality_rule_history
(

    history_id BIGSERIAL PRIMARY KEY,

    execution_id UUID NOT NULL,

    rule_id VARCHAR(20) NOT NULL,

    rule_name VARCHAR(200) NOT NULL,

    category VARCHAR(100) NOT NULL,

    severity VARCHAR(50) NOT NULL,

    passed BOOLEAN NOT NULL,

    rows_checked BIGINT NOT NULL,

    rows_failed BIGINT NOT NULL,

    quality_score NUMERIC(5,2) NOT NULL,

    execution_time_ms NUMERIC(12,2) NOT NULL,

    message TEXT,

    executed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

);

CREATE INDEX IF NOT EXISTS idx_quality_history_execution
ON monitoring.quality_rule_history(execution_id);

CREATE INDEX IF NOT EXISTS idx_quality_history_rule
ON monitoring.quality_rule_history(rule_id);

CREATE INDEX IF NOT EXISTS idx_quality_history_date
ON monitoring.quality_rule_history(executed_at);