/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : load_dim_customer.sql
Schema      : analytics
Object      : load_dim_customer
Purpose     : Load Customer Dimension (SCD Type 2)
Strategy    : Incremental / Idempotent
Source      : staging.customer
Version     : 3.1.0
===============================================================================
*/

CREATE OR REPLACE PROCEDURE analytics.load_dim_customer()

LANGUAGE plpgsql

AS
$$

DECLARE
    v_start_time TIMESTAMPTZ;
    v_end_time TIMESTAMPTZ;

    v_rows_updated INTEGER := 0;
    v_rows_inserted INTEGER := 0;
    v_rows_affected INTEGER := 0;

BEGIN

    v_start_time := clock_timestamp();

    ----------------------------------------------------------------------------
    -- STEP 1 : EXPIRE CHANGED CUSTOMER RECORDS
    ----------------------------------------------------------------------------

    UPDATE analytics.dim_customer d
    SET
        effective_to = CURRENT_DATE - 1,
        is_current = FALSE,
        updated_timestamp = CURRENT_TIMESTAMP
    FROM staging.customer s
    WHERE d.customer_id = s.customer_id
      AND d.is_current = TRUE
      AND
      (
          d.customer_zip_code_prefix <> s.customer_zip_code_prefix
          OR d.customer_city <> s.customer_city
          OR d.customer_state <> s.customer_state
      );

    GET DIAGNOSTICS v_rows_updated = ROW_COUNT;

    ----------------------------------------------------------------------------
    -- STEP 2 : INSERT BRAND NEW CUSTOMERS
    ----------------------------------------------------------------------------

    INSERT INTO analytics.dim_customer (
        customer_id, customer_zip_code_prefix, customer_city,
        customer_state, customer_region, customer_country,
        effective_from, effective_to, is_current,
        record_version, created_timestamp, updated_timestamp
    )

    SELECT
        s.customer_id,
        s.customer_zip_code_prefix,
        s.customer_city,
        s.customer_state,

        CASE
            WHEN s.customer_state IN ('SP','RJ','MG','ES') THEN 'Southeast'
            WHEN s.customer_state IN ('PR','SC','RS') THEN 'South'
            WHEN s.customer_state IN ('BA','PE','CE','RN','PB','AL','SE','PI','MA') THEN 'Northeast'
            WHEN s.customer_state IN ('GO','MT','MS','DF') THEN 'Central-West'
            WHEN s.customer_state IN ('AM','PA','RO','RR','AP','TO','AC') THEN 'North'
            ELSE 'Unknown'
        END,

        'Brazil',
        CURRENT_DATE,
        DATE '9999-12-31',
        TRUE,
        1,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP

    FROM staging.customer s

    WHERE NOT EXISTS
    (
        SELECT 1
        FROM analytics.dim_customer d
        WHERE d.customer_id = s.customer_id
    );

    GET DIAGNOSTICS v_rows_affected = ROW_COUNT;

    v_rows_inserted := v_rows_inserted + v_rows_affected;

    ----------------------------------------------------------------------------
    -- STEP 3 : INSERT NEW VERSIONS FOR CHANGED CUSTOMERS
    ----------------------------------------------------------------------------

    INSERT INTO analytics.dim_customer (
        customer_id, customer_zip_code_prefix, customer_city,
        customer_state, customer_region, customer_country,
        effective_from, effective_to, is_current,
        record_version, created_timestamp, updated_timestamp
    )

    SELECT
        s.customer_id,
        s.customer_zip_code_prefix,
        s.customer_city,
        s.customer_state,

        CASE
            WHEN s.customer_state IN ('SP','RJ','MG','ES') THEN 'Southeast'
            WHEN s.customer_state IN ('PR','SC','RS') THEN 'South'
            WHEN s.customer_state IN ('BA','PE','CE','RN','PB','AL','SE','PI','MA') THEN 'Northeast'
            WHEN s.customer_state IN ('GO','MT','MS','DF') THEN 'Central-West'
            WHEN s.customer_state IN ('AM','PA','RO','RR','AP','TO','AC') THEN 'North'
            ELSE 'Unknown'
        END,

        'Brazil',
        CURRENT_DATE,
        DATE '9999-12-31',
        TRUE,
        d.record_version + 1,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP

    FROM staging.customer s

    INNER JOIN analytics.dim_customer d
        ON s.customer_id = d.customer_id

    WHERE d.is_current = FALSE
      AND d.effective_to = CURRENT_DATE - 1

      AND NOT EXISTS
      (
          SELECT 1
          FROM analytics.dim_customer x
          WHERE x.customer_id = s.customer_id
            AND x.is_current = TRUE
      );

    GET DIAGNOSTICS v_rows_affected = ROW_COUNT;

    v_rows_inserted := v_rows_inserted + v_rows_affected;

    ----------------------------------------------------------------------------
    -- STEP 4 : UPDATE OPTIMIZER STATISTICS
    ----------------------------------------------------------------------------

    ANALYZE analytics.dim_customer;

    ----------------------------------------------------------------------------
    -- EXECUTION SUMMARY
    ----------------------------------------------------------------------------

    SELECT COUNT(*)
    INTO v_rows_affected
    FROM analytics.dim_customer
    WHERE is_current = TRUE;

    v_end_time := clock_timestamp();

    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'ERIP ANALYTICS - CUSTOMER DIMENSION LOAD';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'Status            : SUCCESS';
    RAISE NOTICE 'Target Table      : analytics.dim_customer';
    RAISE NOTICE 'Rows Updated      : %', v_rows_updated;
    RAISE NOTICE 'Rows Inserted     : %', v_rows_inserted;
    RAISE NOTICE 'Current Customers : %', v_rows_affected;
    RAISE NOTICE 'Execution Time    : % sec',
        ROUND(EXTRACT(EPOCH FROM (v_end_time - v_start_time))::NUMERIC, 3);
    RAISE NOTICE '============================================================';
    RAISE NOTICE '';

EXCEPTION

    WHEN OTHERS THEN

        RAISE NOTICE '';
        RAISE NOTICE '============================================================';
        RAISE NOTICE 'ERIP ANALYTICS - CUSTOMER DIMENSION LOAD FAILED';
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

CALL analytics.load_dim_customer();


-- ============================================================================
-- VALIDATION QUERIES
-- ============================================================================

-- Current customers

SELECT COUNT(*) AS current_customers
FROM analytics.dim_customer
WHERE is_current = TRUE;


-- Historical versions

SELECT
    customer_id,
    COUNT(*) AS versions
FROM analytics.dim_customer
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY versions DESC;


-- Duplicate current customers (should return zero rows)

SELECT
    customer_id,
    COUNT(*) AS current_records
FROM analytics.dim_customer
WHERE is_current = TRUE
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- Customer distribution by state

SELECT
    customer_state,
    COUNT(*) AS customers
FROM analytics.dim_customer
WHERE is_current = TRUE
GROUP BY customer_state
ORDER BY customers DESC;


-- Customer distribution by region

SELECT
    customer_region,
    COUNT(*) AS customers
FROM analytics.dim_customer
WHERE is_current = TRUE
GROUP BY customer_region
ORDER BY customer_region;


-- Sample SCD history

SELECT
    customer_id,
    customer_city,
    customer_state,
    record_version,
    effective_from,
    effective_to,
    is_current
FROM analytics.dim_customer
ORDER BY customer_id, record_version
LIMIT 25;


-- ============================================================================
-- CHANGE LOG
-- ============================================================================
--
-- Version : 3.1.0
--
-- Improvements
-- ------------
-- • Compact enterprise SQL formatting
-- • Removed unnecessary UPDATE pass
-- • Customer region derived during INSERT
-- • Reduced table scans
-- • Improved execution metrics
-- • Cleaner SCD Type 2 implementation
-- • PostgreSQL optimizer refresh
-- • Improved readability and maintainability
--
-- ============================================================================
-- END OF FILE
-- ============================================================================