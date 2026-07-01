/*
=============================================================
Enterprise Revenue Intelligence Platform

Monitoring Layer

Table:
    analytics.data_quality_audit

Purpose
-------
Stores data quality metrics collected during
every ETL execution.

Business Grain
--------------
One Row = One Table Validation

=============================================================
*/

DROP TABLE IF EXISTS analytics.data_quality_audit;

CREATE TABLE analytics.data_quality_audit (

    audit_id BIGSERIAL PRIMARY KEY,

    run_id BIGINT NOT NULL,

    table_name VARCHAR(100) NOT NULL,

    row_count BIGINT,

    duplicate_count BIGINT,

    null_count BIGINT,

    quality_score NUMERIC(5,2),

    validation_status VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_quality_run
        FOREIGN KEY (run_id)
        REFERENCES analytics.etl_run_history(run_id)

);