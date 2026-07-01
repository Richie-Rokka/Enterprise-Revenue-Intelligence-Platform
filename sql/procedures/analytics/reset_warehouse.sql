/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : reset_warehouse.sql
Schema      : analytics
Object      : reset_warehouse
Purpose     : Reset Analytics Warehouse (Development Only)
Strategy    : Dependency-Aware Data Reset
Version     : 1.0.1
===============================================================================
*/

CREATE OR REPLACE PROCEDURE analytics.reset_warehouse()

LANGUAGE plpgsql

AS
$$

DECLARE
    v_start_time TIMESTAMPTZ;
    v_end_time TIMESTAMPTZ;

BEGIN

    v_start_time := clock_timestamp();

    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'ERIP WAREHOUSE RESET';
    RAISE NOTICE '============================================================';
    RAISE NOTICE '';
    RAISE NOTICE 'WARNING: Development use only.';
    RAISE NOTICE '';

    ----------------------------------------------------------------------------
    -- STEP 1 : RESET WAREHOUSE TABLES
    ----------------------------------------------------------------------------

    RAISE NOTICE 'Clearing analytics warehouse tables...';

    TRUNCATE TABLE
        analytics.fact_sales,
        analytics.dim_customer,
        analytics.dim_product,
        analytics.dim_seller,
        analytics.dim_date
    RESTART IDENTITY CASCADE;

    RAISE NOTICE 'Warehouse tables cleared successfully.';

    ----------------------------------------------------------------------------
    -- STEP 2 : REFRESH OPTIMIZER STATISTICS
    ----------------------------------------------------------------------------

    RAISE NOTICE 'Refreshing optimizer statistics...';

    ANALYZE analytics.dim_date;
    ANALYZE analytics.dim_customer;
    ANALYZE analytics.dim_product;
    ANALYZE analytics.dim_seller;
    ANALYZE analytics.fact_sales;

    ----------------------------------------------------------------------------
    -- STEP 3 : COMPLETE
    ----------------------------------------------------------------------------

    v_end_time := clock_timestamp();

    ----------------------------------------------------------------------------
    -- STEP 4 : EXECUTION SUMMARY
    ----------------------------------------------------------------------------

    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'ERIP WAREHOUSE RESET COMPLETED';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'Status          : SUCCESS';
    RAISE NOTICE 'Warehouse       : Cleared';
    RAISE NOTICE 'Execution Time  : % sec',
        ROUND(EXTRACT(EPOCH FROM (v_end_time - v_start_time))::NUMERIC, 3);
    RAISE NOTICE '';
    RAISE NOTICE 'Next Step:';
    RAISE NOTICE 'CALL analytics.refresh_warehouse();';
    RAISE NOTICE '============================================================';
    RAISE NOTICE '';

EXCEPTION
    WHEN OTHERS THEN

        RAISE NOTICE '';
        RAISE NOTICE '============================================================';
        RAISE NOTICE 'ERIP WAREHOUSE RESET FAILED';
        RAISE NOTICE '============================================================';
        RAISE NOTICE 'SQLSTATE : %', SQLSTATE;
        RAISE NOTICE 'MESSAGE  : %', SQLERRM;
        RAISE NOTICE '============================================================';
        RAISE NOTICE '';

        RAISE;

END;

$$;


-- ============================================================================
-- EXAMPLE EXECUTION
-- ============================================================================

CALL analytics.reset_warehouse();


-- ============================================================================
-- RECOMMENDED EXECUTION ORDER
-- ============================================================================

-- 1. Reset Warehouse
-- CALL analytics.reset_warehouse();

-- 2. Refresh Warehouse
-- CALL analytics.refresh_warehouse();

-- 3. Validate Warehouse
-- CALL analytics.validate_warehouse();


-- ============================================================================
-- DEVELOPMENT NOTES
-- ============================================================================
--
-- • Development and integration testing only.
-- • Preserves schemas, indexes and constraints.
-- • Clears all warehouse data.
-- • Resets surrogate key sequences.
-- • Executes in dependency order.
--
-- ============================================================================


-- ============================================================================
-- CHANGE LOG
-- ============================================================================
--
-- Version : 1.0.0
--
-- Features
-- --------
-- • Dependency-aware warehouse reset
-- • Fast TRUNCATE operations
-- • Identity sequence reset
-- • Enterprise execution logging
-- • Scheduler-friendly output
-- • Safe development workflow
--
-- ============================================================================
-- END OF FILE
-- ============================================================================