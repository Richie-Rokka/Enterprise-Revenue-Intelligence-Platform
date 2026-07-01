/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : validate_warehouse.sql
Schema      : analytics
Object      : validate_warehouse
Purpose     : Validate Enterprise Analytics Warehouse
Strategy    : Warehouse Health Checks
Version     : 1.0.0
===============================================================================
*/

CREATE OR REPLACE PROCEDURE analytics.validate_warehouse()

LANGUAGE plpgsql

AS
$$

DECLARE
    v_start_time TIMESTAMPTZ;
    v_end_time TIMESTAMPTZ;

    v_count INTEGER;

    v_tests INTEGER := 0;
    v_passed INTEGER := 0;
    v_failed INTEGER := 0;

BEGIN

    v_start_time := clock_timestamp();

    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'ERIP WAREHOUSE VALIDATION';
    RAISE NOTICE '============================================================';
    RAISE NOTICE '';

    ----------------------------------------------------------------------------
    -- TEST 1 : DATE DIMENSION
    ----------------------------------------------------------------------------

    v_tests := v_tests + 1;

    SELECT COUNT(*)
    INTO v_count
    FROM analytics.dim_date;

    IF v_count > 0 THEN

        v_passed := v_passed + 1;

        RAISE NOTICE '[PASS] Date Dimension (% rows)', v_count;

    ELSE

        v_failed := v_failed + 1;

        RAISE NOTICE '[FAIL] Date Dimension is empty';

    END IF;

    ----------------------------------------------------------------------------
    -- TEST 2 : CUSTOMER DIMENSION
    ----------------------------------------------------------------------------

    v_tests := v_tests + 1;

    SELECT COUNT(*)
    INTO v_count
    FROM analytics.dim_customer
    WHERE is_current = TRUE;

    IF v_count > 0 THEN

        v_passed := v_passed + 1;

        RAISE NOTICE '[PASS] Customer Dimension (% current rows)', v_count;

    ELSE

        v_failed := v_failed + 1;

        RAISE NOTICE '[FAIL] Customer Dimension is empty';

    END IF;

    ----------------------------------------------------------------------------
    -- TEST 3 : PRODUCT DIMENSION
    ----------------------------------------------------------------------------

    v_tests := v_tests + 1;

    SELECT COUNT(*)
    INTO v_count
    FROM analytics.dim_product
    WHERE is_current = TRUE;

    IF v_count > 0 THEN

        v_passed := v_passed + 1;

        RAISE NOTICE '[PASS] Product Dimension (% current rows)', v_count;

    ELSE

        v_failed := v_failed + 1;

        RAISE NOTICE '[FAIL] Product Dimension is empty';

    END IF;

        ----------------------------------------------------------------------------
    -- TEST 4 : SELLER DIMENSION
    ----------------------------------------------------------------------------

    v_tests := v_tests + 1;

    SELECT COUNT(*)
    INTO v_count
    FROM analytics.dim_seller
    WHERE is_current = TRUE;

    IF v_count > 0 THEN
        v_passed := v_passed + 1;
        RAISE NOTICE '[PASS] Seller Dimension (% current rows)', v_count;
    ELSE
        v_failed := v_failed + 1;
        RAISE NOTICE '[FAIL] Seller Dimension is empty';
    END IF;

    ----------------------------------------------------------------------------
    -- TEST 5 : SALES FACT
    ----------------------------------------------------------------------------

    v_tests := v_tests + 1;

    SELECT COUNT(*)
    INTO v_count
    FROM analytics.fact_sales;

    IF v_count > 0 THEN
        v_passed := v_passed + 1;
        RAISE NOTICE '[PASS] Sales Fact (% rows)', v_count;
    ELSE
        v_failed := v_failed + 1;
        RAISE NOTICE '[FAIL] Sales Fact is empty';
    END IF;

    ----------------------------------------------------------------------------
    -- TEST 6 : ORPHAN CUSTOMER KEYS
    ----------------------------------------------------------------------------

    v_tests := v_tests + 1;

    SELECT COUNT(*)
    INTO v_count
    FROM analytics.fact_sales f
    LEFT JOIN analytics.dim_customer c
        ON f.customer_sk = c.customer_sk
    WHERE c.customer_sk IS NULL;

    IF v_count = 0 THEN
        v_passed := v_passed + 1;
        RAISE NOTICE '[PASS] Customer foreign keys';
    ELSE
        v_failed := v_failed + 1;
        RAISE NOTICE '[FAIL] % orphan customer keys', v_count;
    END IF;

    ----------------------------------------------------------------------------
    -- TEST 7 : ORPHAN PRODUCT KEYS
    ----------------------------------------------------------------------------

    v_tests := v_tests + 1;

    SELECT COUNT(*)
    INTO v_count
    FROM analytics.fact_sales f
    LEFT JOIN analytics.dim_product p
        ON f.product_sk = p.product_sk
    WHERE p.product_sk IS NULL;

    IF v_count = 0 THEN
        v_passed := v_passed + 1;
        RAISE NOTICE '[PASS] Product foreign keys';
    ELSE
        v_failed := v_failed + 1;
        RAISE NOTICE '[FAIL] % orphan product keys', v_count;
    END IF;

    ----------------------------------------------------------------------------
    -- TEST 8 : ORPHAN SELLER KEYS
    ----------------------------------------------------------------------------

    v_tests := v_tests + 1;

    SELECT COUNT(*)
    INTO v_count
    FROM analytics.fact_sales f
    LEFT JOIN analytics.dim_seller s
        ON f.seller_sk = s.seller_sk
    WHERE s.seller_sk IS NULL;

    IF v_count = 0 THEN
        v_passed := v_passed + 1;
        RAISE NOTICE '[PASS] Seller foreign keys';
    ELSE
        v_failed := v_failed + 1;
        RAISE NOTICE '[FAIL] % orphan seller keys', v_count;
    END IF;

    ----------------------------------------------------------------------------
    -- TEST 9 : ORPHAN DATE KEYS
    ----------------------------------------------------------------------------

    v_tests := v_tests + 1;

    SELECT COUNT(*)
    INTO v_count
    FROM analytics.fact_sales f
    LEFT JOIN analytics.dim_date d
        ON f.date_key = d.date_key
    WHERE d.date_key IS NULL;

    IF v_count = 0 THEN
        v_passed := v_passed + 1;
        RAISE NOTICE '[PASS] Date foreign keys';
    ELSE
        v_failed := v_failed + 1;
        RAISE NOTICE '[FAIL] % orphan date keys', v_count;
    END IF;

        ----------------------------------------------------------------------------
    -- TEST 10 : DUPLICATE CURRENT CUSTOMERS
    ----------------------------------------------------------------------------

    v_tests := v_tests + 1;

    SELECT COUNT(*)
    INTO v_count
    FROM (
        SELECT customer_id
        FROM analytics.dim_customer
        WHERE is_current = TRUE
        GROUP BY customer_id
        HAVING COUNT(*) > 1
    ) t;

    IF v_count = 0 THEN
        v_passed := v_passed + 1;
        RAISE NOTICE '[PASS] Current customer uniqueness';
    ELSE
        v_failed := v_failed + 1;
        RAISE NOTICE '[FAIL] % duplicate current customers', v_count;
    END IF;

    ----------------------------------------------------------------------------
    -- TEST 11 : DUPLICATE CURRENT PRODUCTS
    ----------------------------------------------------------------------------

    v_tests := v_tests + 1;

    SELECT COUNT(*)
    INTO v_count
    FROM (
        SELECT product_id
        FROM analytics.dim_product
        WHERE is_current = TRUE
        GROUP BY product_id
        HAVING COUNT(*) > 1
    ) t;

    IF v_count = 0 THEN
        v_passed := v_passed + 1;
        RAISE NOTICE '[PASS] Current product uniqueness';
    ELSE
        v_failed := v_failed + 1;
        RAISE NOTICE '[FAIL] % duplicate current products', v_count;
    END IF;

    ----------------------------------------------------------------------------
    -- TEST 12 : DUPLICATE CURRENT SELLERS
    ----------------------------------------------------------------------------

    v_tests := v_tests + 1;

    SELECT COUNT(*)
    INTO v_count
    FROM (
        SELECT seller_id
        FROM analytics.dim_seller
        WHERE is_current = TRUE
        GROUP BY seller_id
        HAVING COUNT(*) > 1
    ) t;

    IF v_count = 0 THEN
        v_passed := v_passed + 1;
        RAISE NOTICE '[PASS] Current seller uniqueness';
    ELSE
        v_failed := v_failed + 1;
        RAISE NOTICE '[FAIL] % duplicate current sellers', v_count;
    END IF;

    ----------------------------------------------------------------------------
    -- EXECUTION SUMMARY
    ----------------------------------------------------------------------------

    v_end_time := clock_timestamp();

    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'ERIP WAREHOUSE VALIDATION SUMMARY';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'Tests Executed : %', v_tests;
    RAISE NOTICE 'Tests Passed   : %', v_passed;
    RAISE NOTICE 'Tests Failed   : %', v_failed;

    IF v_failed = 0 THEN
        RAISE NOTICE 'Overall Status : PASS';
    ELSE
        RAISE NOTICE 'Overall Status : FAIL';
    END IF;

    RAISE NOTICE 'Execution Time : % sec',
        ROUND(EXTRACT(EPOCH FROM (v_end_time - v_start_time))::NUMERIC, 3);

    RAISE NOTICE '============================================================';
    RAISE NOTICE '';

EXCEPTION
    WHEN OTHERS THEN

        RAISE NOTICE '';
        RAISE NOTICE '============================================================';
        RAISE NOTICE 'ERIP WAREHOUSE VALIDATION FAILED';
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

CALL analytics.validate_warehouse();


-- ============================================================================
-- VALIDATION COVERAGE
-- ============================================================================
--
-- 1. Date Dimension
-- 2. Customer Dimension
-- 3. Product Dimension
-- 4. Seller Dimension
-- 5. Sales Fact
-- 6. Customer Foreign Keys
-- 7. Product Foreign Keys
-- 8. Seller Foreign Keys
-- 9. Date Foreign Keys
-- 10. Current Customer Uniqueness
-- 11. Current Product Uniqueness
-- 12. Current Seller Uniqueness
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
-- • Enterprise warehouse health checks
-- • Referential integrity validation
-- • SCD Type 2 uniqueness validation
-- • Fact table validation
-- • Execution summary
-- • Scheduler-ready
--
-- ============================================================================
-- END OF FILE
-- ============================================================================