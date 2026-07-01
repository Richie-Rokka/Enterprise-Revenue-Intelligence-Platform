/*
=============================================================
Enterprise Revenue Intelligence Platform

Monitoring Layer

Table:
    analytics.etl_run_history

Purpose
-------
Stores one record for every execution of the ETL pipeline.

Business Grain
--------------
One Row = One Pipeline Execution

=============================================================
*/

DROP TABLE IF EXISTS analytics.etl_run_history;

CREATE TABLE analytics.etl_run_history (

    run_id BIGSERIAL PRIMARY KEY,

    pipeline_name VARCHAR(100) NOT NULL,

    start_time TIMESTAMP NOT NULL,

    end_time TIMESTAMP,

    duration_seconds NUMERIC(10,2),

    status VARCHAR(20) NOT NULL,

    total_tables INTEGER,

    total_rows_loaded BIGINT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);