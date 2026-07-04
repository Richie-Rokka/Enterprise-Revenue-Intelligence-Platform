/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : refresh_warehouse.sql
Schema      : analytics
Object      : refresh_warehouse
Purpose     : Execute the complete Analytics Warehouse refresh
Strategy    : Sequential ETL Orchestration
Version     : 1.0.0
===============================================================================
*/

CREATE OR REPLACE PROCEDURE analytics.refresh_warehouse
(
    IN p_start_year INTEGER DEFAULT 2015,
    IN p_end_year   INTEGER DEFAULT 2045
)

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
    RAISE NOTICE 'ERIP ENTERPRISE WAREHOUSE REFRESH';
    RAISE NOTICE '============================================================';
    RAISE NOTICE '';

    ----------------------------------------------------------------------------
    -- STEP 1 : DATE DIMENSION
    ----------------------------------------------------------------------------

    RAISE NOTICE 'Loading Date Dimension...';

    CALL analytics.load_dim_date(
        p_start_year,
        p_end_year
    );

    ----------------------------------------------------------------------------
    -- STEP 2 : CUSTOMER DIMENSION
    ----------------------------------------------------------------------------

    RAISE NOTICE 'Loading Customer Dimension...';

    CALL analytics.load_dim_customer();

    ----------------------------------------------------------------------------
    -- STEP 3 : PRODUCT DIMENSION
    ----------------------------------------------------------------------------

    RAISE NOTICE 'Loading Product Dimension...';

    CALL analytics.load_dim_product();

        ----------------------------------------------------------------------------
    -- STEP 4 : SELLER DIMENSION
    ----------------------------------------------------------------------------

    RAISE NOTICE 'Loading Seller Dimension...';

    CALL analytics.load_dim_seller();

    ----------------------------------------------------------------------------
    -- STEP 5 : SALES FACT
    ----------------------------------------------------------------------------

    RAISE NOTICE 'Loading Sales Fact...';

    CALL analytics.load_fact_sales();

    ----------------------------------------------------------------------------
    -- STEP 6 : UPDATE OPTIMIZER STATISTICS
    ----------------------------------------------------------------------------

    RAISE NOTICE 'Refreshing optimizer statistics...';

    ANALYZE analytics.dim_date;
    ANALYZE analytics.dim_customer;
    ANALYZE analytics.dim_product;
    ANALYZE analytics.dim_seller;
    ANALYZE analytics.fact_sales;

    ----------------------------------------------------------------------------
    -- STEP 7 : COMPLETE
    ----------------------------------------------------------------------------

    v_end_time := clock_timestamp();

        ----------------------------------------------------------------------------
    -- STEP 8 : EXECUTION SUMMARY
    ----------------------------------------------------------------------------

    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'ERIP ENTERPRISE WAREHOUSE REFRESH COMPLETED';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'Status          : SUCCESS';
    RAISE NOTICE 'Date Range      : % - %', p_start_year, p_end_year;
    RAISE NOTICE 'Execution Time  : % sec',
        ROUND(EXTRACT(EPOCH FROM (v_end_time - v_start_time))::NUMERIC, 3);
    RAISE NOTICE '============================================================';
    RAISE NOTICE '';

EXCEPTION
    WHEN OTHERS THEN

        RAISE NOTICE '';
        RAISE NOTICE '============================================================';
        RAISE NOTICE 'ERIP ENTERPRISE WAREHOUSE REFRESH FAILED';
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

CALL analytics.refresh_warehouse();

-- Or specify a custom date range

CALL analytics.refresh_warehouse(2015, 2045);


-- ============================================================================
-- EXECUTION ORDER
-- ============================================================================

-- 1. Load Date Dimension
-- 2. Load Customer Dimension
-- 3. Load Product Dimension
-- 4. Load Seller Dimension
-- 5. Load Sales Fact
-- 6. Refresh Optimizer Statistics
-- 7. Print Execution Summary


-- ============================================================================
-- CHANGE LOG
-- ============================================================================
--
-- Version : 1.0.0
--
-- Features
-- --------
-- • Single entry point for warehouse refresh
-- • Sequential ETL orchestration
-- • Automatic dependency management
-- • Enterprise execution logging
-- • Automatic optimizer statistics refresh
-- • Exception handling with rollback support
-- • Scheduler-ready execution
--
-- ============================================================================
-- END OF FILE
-- ============================================================================