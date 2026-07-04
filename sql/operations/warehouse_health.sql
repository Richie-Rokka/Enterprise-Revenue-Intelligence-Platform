/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : warehouse_health.sql
Schema      : analytics
Object      : warehouse_health
Purpose     : Enterprise Warehouse Health Report
Description : Provides a consolidated operational health report for the
              Enterprise Revenue Intelligence Platform including row counts,
              storage, latest ETL execution, audit metrics and warehouse
              readiness.

Business Process : Warehouse Monitoring
Platform         : PostgreSQL 18
Version          : 4.0.0
===============================================================================
*/

CREATE OR REPLACE PROCEDURE analytics.warehouse_health()
LANGUAGE plpgsql
AS
$$
DECLARE

    ----------------------------------------------------------------------------
    -- EXECUTION
    ----------------------------------------------------------------------------
    v_start_time             TIMESTAMPTZ := clock_timestamp();

    ----------------------------------------------------------------------------
    -- ROW COUNTS
    ----------------------------------------------------------------------------
    v_dim_date_rows          BIGINT;
    v_dim_customer_rows      BIGINT;
    v_dim_product_rows       BIGINT;
    v_dim_seller_rows        BIGINT;
    v_fact_sales_rows        BIGINT;

    ----------------------------------------------------------------------------
    -- STORAGE
    ----------------------------------------------------------------------------
    v_dim_date_size          TEXT;
    v_dim_customer_size      TEXT;
    v_dim_product_size       TEXT;
    v_dim_seller_size        TEXT;
    v_fact_sales_size        TEXT;

    ----------------------------------------------------------------------------
    -- AUDIT
    ----------------------------------------------------------------------------
    v_last_pipeline          TEXT;
    v_last_status            TEXT;
    v_last_started           TIMESTAMPTZ;
    v_last_completed         TIMESTAMPTZ;
    v_last_duration_ms       BIGINT;

    ----------------------------------------------------------------------------
    -- DATABASE
    ----------------------------------------------------------------------------
    v_database_size          TEXT;
    v_postgresql_version     TEXT;

BEGIN

    ----------------------------------------------------------------------------
    -- DATABASE INFORMATION
    ----------------------------------------------------------------------------
    SELECT version()
    INTO v_postgresql_version;

    SELECT pg_size_pretty(pg_database_size(current_database()))
    INTO v_database_size;

    ----------------------------------------------------------------------------
    -- ROW COUNTS
    ----------------------------------------------------------------------------
    SELECT COUNT(*) INTO v_dim_date_rows
    FROM analytics.dim_date;

    SELECT COUNT(*) INTO v_dim_customer_rows
    FROM analytics.dim_customer;

    SELECT COUNT(*) INTO v_dim_product_rows
    FROM analytics.dim_product;

    SELECT COUNT(*) INTO v_dim_seller_rows
    FROM analytics.dim_seller;

    SELECT COUNT(*) INTO v_fact_sales_rows
    FROM analytics.fact_sales;

    ----------------------------------------------------------------------------
    -- TABLE SIZES
    ----------------------------------------------------------------------------
    SELECT pg_size_pretty(pg_total_relation_size('analytics.dim_date'))
    INTO v_dim_date_size;

    SELECT pg_size_pretty(pg_total_relation_size('analytics.dim_customer'))
    INTO v_dim_customer_size;

    SELECT pg_size_pretty(pg_total_relation_size('analytics.dim_product'))
    INTO v_dim_product_size;

    SELECT pg_size_pretty(pg_total_relation_size('analytics.dim_seller'))
    INTO v_dim_seller_size;

    SELECT pg_size_pretty(pg_total_relation_size('analytics.fact_sales'))
    INTO v_fact_sales_size;

    ----------------------------------------------------------------------------
    -- LAST EXECUTION
    ----------------------------------------------------------------------------
    SELECT
        pipeline_name,
        status,
        started_at,
        completed_at,
        execution_time_ms
    INTO
        v_last_pipeline,
        v_last_status,
        v_last_started,
        v_last_completed,
        v_last_duration_ms
    FROM audit.etl_run_history
    ORDER BY run_id DESC
    LIMIT 1;

        ----------------------------------------------------------------------------
    -- HEALTH REPORT
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE '===========================================================';
    RAISE NOTICE 'ERIP Warehouse Health Report';
    RAISE NOTICE '===========================================================';

    ----------------------------------------------------------------------------
    -- DATABASE
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE '[DATABASE]';
    RAISE NOTICE 'Database           : %', current_database();
    RAISE NOTICE 'PostgreSQL Version : %', v_postgresql_version;
    RAISE NOTICE 'Database Size      : %', v_database_size;

    ----------------------------------------------------------------------------
    -- TABLE ROW COUNTS
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE '[ROW COUNTS]';
    RAISE NOTICE 'dim_date           : %', v_dim_date_rows;
    RAISE NOTICE 'dim_customer       : %', v_dim_customer_rows;
    RAISE NOTICE 'dim_product        : %', v_dim_product_rows;
    RAISE NOTICE 'dim_seller         : %', v_dim_seller_rows;
    RAISE NOTICE 'fact_sales         : %', v_fact_sales_rows;

    ----------------------------------------------------------------------------
    -- TABLE STORAGE
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE '[TABLE STORAGE]';
    RAISE NOTICE 'dim_date           : %', v_dim_date_size;
    RAISE NOTICE 'dim_customer       : %', v_dim_customer_size;
    RAISE NOTICE 'dim_product        : %', v_dim_product_size;
    RAISE NOTICE 'dim_seller         : %', v_dim_seller_size;
    RAISE NOTICE 'fact_sales         : %', v_fact_sales_size;

    ----------------------------------------------------------------------------
    -- LAST PIPELINE EXECUTION
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE '[LAST PIPELINE EXECUTION]';
    RAISE NOTICE 'Pipeline           : %', COALESCE(v_last_pipeline, 'N/A');
    RAISE NOTICE 'Status             : %', COALESCE(v_last_status, 'N/A');
    RAISE NOTICE 'Started            : %', COALESCE(v_last_started::TEXT, 'N/A');
    RAISE NOTICE 'Completed          : %', COALESCE(v_last_completed::TEXT, 'N/A');
    RAISE NOTICE 'Duration (ms)      : %', COALESCE(v_last_duration_ms, 0);

    ----------------------------------------------------------------------------
    -- WAREHOUSE STATUS
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE '[WAREHOUSE STATUS]';

    IF v_last_status = 'SUCCESS'
       AND v_fact_sales_rows > 0
    THEN
        RAISE NOTICE 'Status             : HEALTHY';
    ELSE
        RAISE NOTICE 'Status             : ATTENTION REQUIRED';
    END IF;

    RAISE NOTICE 'Checked At         : %', clock_timestamp();

    ----------------------------------------------------------------------------
    -- EXECUTION SUMMARY
    ----------------------------------------------------------------------------
    RAISE NOTICE '';
    RAISE NOTICE 'Execution Time     : %',
        clock_timestamp() - v_start_time;

EXCEPTION
    WHEN OTHERS THEN

        RAISE NOTICE '';
        RAISE NOTICE '===========================================================';
        RAISE NOTICE 'ERIP Warehouse Health Check Failed';
        RAISE NOTICE 'Error : %', SQLERRM;
        RAISE NOTICE '===========================================================';

        RAISE;

END;
$$;

-------------------------------------------------------------------------------
-- USAGE
-------------------------------------------------------------------------------

-- Display warehouse health report
-- CALL analytics.warehouse_health();

-------------------------------------------------------------------------------
-- SAMPLE OUTPUT
-------------------------------------------------------------------------------
--
-- ===========================================================
-- ERIP Warehouse Health Report
-- ===========================================================
--
-- [DATABASE]
-- Database           : erip
-- PostgreSQL Version : PostgreSQL 18.x
-- Database Size      : 186 MB
--
-- [ROW COUNTS]
-- dim_date           : 7,671
-- dim_customer       : 99,441
-- dim_product        : 32,951
-- dim_seller         : 3,095
-- fact_sales         : 112,650
--
-- [TABLE STORAGE]
-- dim_date           : 1 MB
-- dim_customer       : 22 MB
-- dim_product        : 16 MB
-- dim_seller         : 1 MB
-- fact_sales         : 58 MB
--
-- [LAST PIPELINE EXECUTION]
-- Pipeline           : refresh_warehouse
-- Status             : SUCCESS
-- Duration (ms)      : 4,812
--
-- [WAREHOUSE STATUS]
-- Status             : HEALTHY
--
-------------------------------------------------------------------------------
-- END OF FILE
-------------------------------------------------------------------------------