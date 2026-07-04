/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : refresh_metadata.sql
Schema      : analytics
Object      : refresh_metadata
Purpose     : Refresh Enterprise Warehouse Metadata
Description : Refreshes metadata, updates warehouse statistics, synchronizes
              audit information and optimizes query planner statistics after
              warehouse refresh operations.

Business Process : Metadata Management
Platform         : PostgreSQL 18
Version          : 4.0.0
===============================================================================
*/

CREATE OR REPLACE PROCEDURE analytics.refresh_metadata()
LANGUAGE plpgsql
AS
$$
DECLARE

    ----------------------------------------------------------------------------
    -- EXECUTION
    ----------------------------------------------------------------------------
    v_start_time              TIMESTAMPTZ := clock_timestamp();
    v_end_time                TIMESTAMPTZ;
    v_duration                INTERVAL;

    ----------------------------------------------------------------------------
    -- AUDIT
    ----------------------------------------------------------------------------
    v_run_id                  BIGINT;

BEGIN

    ----------------------------------------------------------------------------
    -- START AUDIT
    ----------------------------------------------------------------------------
    INSERT INTO monitoring.etl_run_history
    (
        pipeline_name,
        target_table,
        load_type,
        status,
        started_at
    )
    VALUES
    (
        'refresh_metadata',
        'analytics',
        'METADATA_REFRESH',
        'RUNNING',
        clock_timestamp()
    )
    RETURNING run_id
    INTO v_run_id;

    RAISE NOTICE '';
    RAISE NOTICE '===========================================================';
    RAISE NOTICE 'ERIP Metadata Refresh';
    RAISE NOTICE '===========================================================';

    ----------------------------------------------------------------------------
    -- ANALYZE TABLES
    ----------------------------------------------------------------------------
    RAISE NOTICE 'Refreshing planner statistics...';

    ANALYZE analytics.dim_date;
    ANALYZE analytics.dim_customer;
    ANALYZE analytics.dim_product;
    ANALYZE analytics.dim_seller;
    ANALYZE analytics.fact_sales;

    ----------------------------------------------------------------------------
    -- UPDATE TABLE STATISTICS
    ----------------------------------------------------------------------------
    RAISE NOTICE 'Updating relation statistics...';

    PERFORM pg_stat_reset_single_table_counters
    (
        'analytics.dim_date'::regclass
    );

    PERFORM pg_stat_reset_single_table_counters
    (
        'analytics.dim_customer'::regclass
    );

    PERFORM pg_stat_reset_single_table_counters
    (
        'analytics.dim_product'::regclass
    );

    PERFORM pg_stat_reset_single_table_counters
    (
        'analytics.dim_seller'::regclass
    );

    PERFORM pg_stat_reset_single_table_counters
    (
        'analytics.fact_sales'::regclass
    );

    ----------------------------------------------------------------------------
    -- REFRESH MATERIALIZED VIEWS (IF ANY)
    ----------------------------------------------------------------------------
    RAISE NOTICE 'Refreshing materialized views...';

        DO
    $refresh$
    DECLARE
        v_view RECORD;
    BEGIN
        FOR v_view IN
            SELECT
                schemaname,
                matviewname
            FROM pg_matviews
            WHERE schemaname = 'analytics'
        LOOP
            EXECUTE FORMAT
            (
                'REFRESH MATERIALIZED VIEW %I.%I',
                v_view.schemaname,
                v_view.matviewname
            );

            RAISE NOTICE
                'Refreshed Materialized View: %.%',
                v_view.schemaname,
                v_view.matviewname;
        END LOOP;
    END;
    $refresh$;

    ----------------------------------------------------------------------------
    -- COMPLETE AUDIT
    ----------------------------------------------------------------------------
    v_end_time := clock_timestamp();
    v_duration := v_end_time - v_start_time;

    UPDATE monitoring.etl_run_history
    SET
        status            = 'SUCCESS',
        completed_at      = v_end_time,
        execution_time_ms = ROUND(EXTRACT(EPOCH FROM v_duration) * 1000)
    WHERE run_id = v_run_id;

    INSERT INTO monitoring.table_load_history
    (
        run_id,
        target_table,
        load_type,
        status,
        started_at,
        completed_at,
        execution_time_ms
    )
    VALUES
    (
        v_run_id,
        'analytics',
        'METADATA_REFRESH',
        'SUCCESS',
        v_start_time,
        v_end_time,
        ROUND(EXTRACT(EPOCH FROM v_duration) * 1000)
    );

    RAISE NOTICE '';
    RAISE NOTICE '===========================================================';
    RAISE NOTICE 'Metadata Refresh Completed Successfully';
    RAISE NOTICE 'Duration : %', v_duration;
    RAISE NOTICE '===========================================================';

EXCEPTION
    WHEN OTHERS THEN

        v_end_time := clock_timestamp();
        v_duration := v_end_time - v_start_time;

        UPDATE monitoring.etl_run_history
        SET
            status            = 'FAILED',
            completed_at      = v_end_time,
            execution_time_ms = ROUND(EXTRACT(EPOCH FROM v_duration) * 1000),
            error_message     = SQLERRM
        WHERE run_id = v_run_id;

        INSERT INTO monitoring.table_load_history
        (
            run_id,
            target_table,
            load_type,
            status,
            error_message,
            started_at,
            completed_at,
            execution_time_ms
        )
        VALUES
        (
            v_run_id,
            'analytics',
            'METADATA_REFRESH',
            'FAILED',
            SQLERRM,
            v_start_time,
            v_end_time,
            ROUND(EXTRACT(EPOCH FROM v_duration) * 1000)
        );

        RAISE NOTICE '';
        RAISE NOTICE '===========================================================';
        RAISE NOTICE 'Metadata Refresh Failed';
        RAISE NOTICE 'Error     : %', SQLERRM;
        RAISE NOTICE 'Duration  : %', v_duration;
        RAISE NOTICE '===========================================================';

        RAISE;

END;
$$;

-------------------------------------------------------------------------------
-- USAGE
-------------------------------------------------------------------------------

-- Refresh warehouse metadata
-- CALL analytics.refresh_metadata();

-------------------------------------------------------------------------------
-- END OF FILE
-------------------------------------------------------------------------------