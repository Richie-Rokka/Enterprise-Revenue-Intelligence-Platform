/*
=============================================================
Enterprise Revenue Intelligence Platform

Monitoring Layer

Table:
    analytics.table_load_history

Purpose
-------
Stores one record for every table loaded
during a pipeline execution.

Business Grain
--------------
One Row = One Table Load

=============================================================
*/

DROP TABLE IF EXISTS analytics.table_load_history;

CREATE TABLE analytics.table_load_history (

    load_id BIGSERIAL PRIMARY KEY,

    run_id BIGINT NOT NULL,

    table_name VARCHAR(100) NOT NULL,

    rows_loaded BIGINT NOT NULL,

    load_status VARCHAR(20) NOT NULL,

    load_duration_seconds NUMERIC(10,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_table_load_run
        FOREIGN KEY (run_id)
        REFERENCES analytics.etl_run_history(run_id)

);