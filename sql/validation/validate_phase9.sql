/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : validate_phase9.sql
Schema      : analytics
Purpose     : Phase 9 Regression Validation
Version     : 1.0.0

Description
-----------
Validates the successful deployment of all Phase 9 artifacts including:

• Commercial Semantic Views
• Operational Semantic Views
• Metrics Layer
• Dashboard Layer

Execution
---------
Run after Phase 9 deployment.

===============================================================================
*/

SET client_min_messages TO NOTICE;

DO
$$
DECLARE

    v_count BIGINT;

BEGIN

    RAISE NOTICE '';
    RAISE NOTICE '========================================================';
    RAISE NOTICE 'ERIP PHASE 9 REGRESSION VALIDATION';
    RAISE NOTICE '========================================================';
    RAISE NOTICE '';

    ----------------------------------------------------------------------------
    -- Commercial Semantic Views
    ----------------------------------------------------------------------------

    RAISE NOTICE 'Validating Commercial Semantic Views...';

    EXECUTE 'SELECT COUNT(*) FROM analytics.vw_sales'
        INTO v_count;
    RAISE NOTICE 'PASS - vw_sales (% rows)', v_count;

    EXECUTE 'SELECT COUNT(*) FROM analytics.vw_customer_sales'
        INTO v_count;
    RAISE NOTICE 'PASS - vw_customer_sales (% rows)', v_count;

    EXECUTE 'SELECT COUNT(*) FROM analytics.vw_product_performance'
        INTO v_count;
    RAISE NOTICE 'PASS - vw_product_performance (% rows)', v_count;

    EXECUTE 'SELECT COUNT(*) FROM analytics.vw_seller_performance'
        INTO v_count;
    RAISE NOTICE 'PASS - vw_seller_performance (% rows)', v_count;

    ----------------------------------------------------------------------------
    -- Operational Semantic Views
    ----------------------------------------------------------------------------

    RAISE NOTICE '';
    RAISE NOTICE 'Validating Operational Semantic Views...';

    EXECUTE 'SELECT COUNT(*) FROM analytics.vw_delivery_performance'
        INTO v_count;
    RAISE NOTICE 'PASS - vw_delivery_performance (% rows)', v_count;

    EXECUTE 'SELECT COUNT(*) FROM analytics.vw_review_performance'
        INTO v_count;
    RAISE NOTICE 'PASS - vw_review_performance (% rows)', v_count;

    EXECUTE 'SELECT COUNT(*) FROM analytics.vw_logistics_performance'
        INTO v_count;
    RAISE NOTICE 'PASS - vw_logistics_performance (% rows)', v_count;

    ----------------------------------------------------------------------------
    -- Executive Metrics
    ----------------------------------------------------------------------------

    RAISE NOTICE '';
    RAISE NOTICE 'Validating Executive Metrics...';

    EXECUTE 'SELECT COUNT(*) FROM analytics.executive_kpis'
        INTO v_count;
    RAISE NOTICE 'PASS - executive_kpis (% rows)', v_count;

    ----------------------------------------------------------------------------
    -- Finance Metrics
    ----------------------------------------------------------------------------

    EXECUTE 'SELECT COUNT(*) FROM analytics.revenue_kpis'
        INTO v_count;
    RAISE NOTICE 'PASS - revenue_kpis (% rows)', v_count;

    ----------------------------------------------------------------------------
    -- Customer Metrics
    ----------------------------------------------------------------------------

    EXECUTE 'SELECT COUNT(*) FROM analytics.customer_kpis'
        INTO v_count;
    RAISE NOTICE 'PASS - customer_kpis (% rows)', v_count;

    ----------------------------------------------------------------------------
    -- Product Metrics
    ----------------------------------------------------------------------------

    EXECUTE 'SELECT COUNT(*) FROM analytics.product_kpis'
        INTO v_count;
    RAISE NOTICE 'PASS - product_kpis (% rows)', v_count;

    ----------------------------------------------------------------------------
    -- Seller Metrics
    ----------------------------------------------------------------------------

    EXECUTE 'SELECT COUNT(*) FROM analytics.seller_kpis'
        INTO v_count;
    RAISE NOTICE 'PASS - seller_kpis (% rows)', v_count;

    ----------------------------------------------------------------------------
    -- Operations Metrics
    ----------------------------------------------------------------------------

    EXECUTE 'SELECT COUNT(*) FROM analytics.delivery_kpis'
        INTO v_count;
    RAISE NOTICE 'PASS - delivery_kpis (% rows)', v_count;

    EXECUTE 'SELECT COUNT(*) FROM analytics.review_kpis'
        INTO v_count;
    RAISE NOTICE 'PASS - review_kpis (% rows)', v_count;

    EXECUTE 'SELECT COUNT(*) FROM analytics.logistics_kpis'
        INTO v_count;
    RAISE NOTICE 'PASS - logistics_kpis (% rows)', v_count;

    EXECUTE 'SELECT COUNT(*) FROM analytics.payment_kpis'
        INTO v_count;
    RAISE NOTICE 'PASS - payment_kpis (% rows)', v_count;

    ----------------------------------------------------------------------------
    -- Dashboard Layer
    ----------------------------------------------------------------------------

    RAISE NOTICE '';
    RAISE NOTICE 'Validating Dashboard Layer...';

    EXECUTE 'SELECT COUNT(*) FROM analytics.executive_dashboard'
        INTO v_count;
    RAISE NOTICE 'PASS - executive_dashboard (% rows)', v_count;

    EXECUTE 'SELECT COUNT(*) FROM analytics.sales_dashboard'
        INTO v_count;
    RAISE NOTICE 'PASS - sales_dashboard (% rows)', v_count;

    EXECUTE 'SELECT COUNT(*) FROM analytics.customer_dashboard'
        INTO v_count;
    RAISE NOTICE 'PASS - customer_dashboard (% rows)', v_count;

    EXECUTE 'SELECT COUNT(*) FROM analytics.product_dashboard'
        INTO v_count;
    RAISE NOTICE 'PASS - product_dashboard (% rows)', v_count;

    EXECUTE 'SELECT COUNT(*) FROM analytics.seller_dashboard'
        INTO v_count;
    RAISE NOTICE 'PASS - seller_dashboard (% rows)', v_count;

    EXECUTE 'SELECT COUNT(*) FROM analytics.operations_dashboard'
        INTO v_count;
    RAISE NOTICE 'PASS - operations_dashboard (% rows)', v_count;

    ----------------------------------------------------------------------------
    -- Validation Complete
    ----------------------------------------------------------------------------

    RAISE NOTICE '';
    RAISE NOTICE '========================================================';
    RAISE NOTICE 'PHASE 9 VALIDATION PASSED';
    RAISE NOTICE 'All Semantic Views, Metrics and Dashboard Views compiled';
    RAISE NOTICE 'and executed successfully.';
    RAISE NOTICE '========================================================';
    RAISE NOTICE '';

END;
$$;