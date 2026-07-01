/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : load_dim_seller.sql
Schema      : analytics
Object      : load_dim_seller
Purpose     : Load Seller Dimension (SCD Type 2)
Strategy    : Incremental / Idempotent
Source      : staging.seller
Version     : 3.1.0
===============================================================================
*/

CREATE OR REPLACE PROCEDURE analytics.load_dim_seller()

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
    -- STEP 1 : EXPIRE CHANGED SELLER RECORDS
    ----------------------------------------------------------------------------

    UPDATE analytics.dim_seller d
    SET
        effective_to = CURRENT_DATE - 1,
        is_current = FALSE,
        updated_timestamp = CURRENT_TIMESTAMP
    FROM staging.seller s
    WHERE d.seller_id = s.seller_id
      AND d.is_current = TRUE
      AND (
            d.seller_zip_code_prefix <> s.seller_zip_code_prefix
         OR d.seller_city <> s.seller_city
         OR d.seller_state <> s.seller_state
      );

    GET DIAGNOSTICS v_rows_updated = ROW_COUNT;

    ----------------------------------------------------------------------------
    -- STEP 2 : INSERT BRAND NEW SELLERS
    ----------------------------------------------------------------------------

    INSERT INTO analytics.dim_seller (
        seller_id, seller_zip_code_prefix, seller_city,
        seller_state, seller_region, seller_country,
        effective_from, effective_to, is_current,
        record_version, created_timestamp, updated_timestamp
    )

    SELECT
        s.seller_id,
        s.seller_zip_code_prefix,
        s.seller_city,
        s.seller_state,

        CASE
            WHEN s.seller_state IN ('SP','RJ','MG','ES') THEN 'Southeast'
            WHEN s.seller_state IN ('PR','SC','RS') THEN 'South'
            WHEN s.seller_state IN ('BA','PE','CE','RN','PB','AL','SE','PI','MA') THEN 'Northeast'
            WHEN s.seller_state IN ('GO','MT','MS','DF') THEN 'Central-West'
            WHEN s.seller_state IN ('AM','PA','RO','RR','AP','TO','AC') THEN 'North'
            ELSE 'Unknown'
        END,

        'Brazil',
        CURRENT_DATE,
        DATE '9999-12-31',
        TRUE,
        1,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP

    FROM staging.seller s

    WHERE NOT EXISTS (
        SELECT 1
        FROM analytics.dim_seller d
        WHERE d.seller_id = s.seller_id
    );

    GET DIAGNOSTICS v_rows_affected = ROW_COUNT;
    v_rows_inserted := v_rows_inserted + v_rows_affected;

    ----------------------------------------------------------------------------
    -- STEP 3 : INSERT NEW SELLER VERSIONS
    ----------------------------------------------------------------------------

    INSERT INTO analytics.dim_seller (
        seller_id, seller_zip_code_prefix, seller_city,
        seller_state, seller_region, seller_country,
        effective_from, effective_to, is_current,
        record_version, created_timestamp, updated_timestamp
    )

    SELECT
        s.seller_id,
        s.seller_zip_code_prefix,
        s.seller_city,
        s.seller_state,

        CASE
            WHEN s.seller_state IN ('SP','RJ','MG','ES') THEN 'Southeast'
            WHEN s.seller_state IN ('PR','SC','RS') THEN 'South'
            WHEN s.seller_state IN ('BA','PE','CE','RN','PB','AL','SE','PI','MA') THEN 'Northeast'
            WHEN s.seller_state IN ('GO','MT','MS','DF') THEN 'Central-West'
            WHEN s.seller_state IN ('AM','PA','RO','RR','AP','TO','AC') THEN 'North'
            ELSE 'Unknown'
        END,

        'Brazil',
        CURRENT_DATE,
        DATE '9999-12-31',
        TRUE,
        d.record_version + 1,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP

    FROM staging.seller s

    INNER JOIN analytics.dim_seller d
        ON s.seller_id = d.seller_id

    WHERE d.is_current = FALSE
      AND d.effective_to = CURRENT_DATE - 1
      AND NOT EXISTS (
            SELECT 1
            FROM analytics.dim_seller x
            WHERE x.seller_id = s.seller_id
              AND x.is_current = TRUE
      );

    GET DIAGNOSTICS v_rows_affected = ROW_COUNT;
    v_rows_inserted := v_rows_inserted + v_rows_affected;

    ----------------------------------------------------------------------------
    -- STEP 4 : UPDATE OPTIMIZER STATISTICS
    ----------------------------------------------------------------------------

    ANALYZE analytics.dim_seller;

    ----------------------------------------------------------------------------
    -- STEP 5 : EXECUTION SUMMARY
    ----------------------------------------------------------------------------

    SELECT COUNT(*)
    INTO v_rows_affected
    FROM analytics.dim_seller
    WHERE is_current = TRUE;

    v_end_time := clock_timestamp();

    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'ERIP ANALYTICS - SELLER DIMENSION LOAD';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'Status           : SUCCESS';
    RAISE NOTICE 'Target Table     : analytics.dim_seller';
    RAISE NOTICE 'Rows Updated     : %', v_rows_updated;
    RAISE NOTICE 'Rows Inserted    : %', v_rows_inserted;
    RAISE NOTICE 'Current Sellers  : %', v_rows_affected;
    RAISE NOTICE 'Execution Time   : % sec',
        ROUND(EXTRACT(EPOCH FROM (v_end_time - v_start_time))::NUMERIC, 3);
    RAISE NOTICE '============================================================';
    RAISE NOTICE '';

EXCEPTION
    WHEN OTHERS THEN

        RAISE NOTICE '';
        RAISE NOTICE '============================================================';
        RAISE NOTICE 'ERIP ANALYTICS - SELLER DIMENSION LOAD FAILED';
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

CALL analytics.load_dim_seller();


-- ============================================================================
-- VALIDATION QUERIES
-- ============================================================================

-- Current sellers

SELECT COUNT(*) AS current_sellers
FROM analytics.dim_seller
WHERE is_current = TRUE;


-- Seller history

SELECT
    seller_id,
    COUNT(*) AS versions
FROM analytics.dim_seller
GROUP BY seller_id
HAVING COUNT(*) > 1
ORDER BY versions DESC;


-- Duplicate current sellers (should return zero rows)

SELECT
    seller_id,
    COUNT(*) AS current_records
FROM analytics.dim_seller
WHERE is_current = TRUE
GROUP BY seller_id
HAVING COUNT(*) > 1;


-- Sellers by state

SELECT
    seller_state,
    COUNT(*) AS sellers
FROM analytics.dim_seller
WHERE is_current = TRUE
GROUP BY seller_state
ORDER BY sellers DESC;


-- Sellers by region

SELECT
    seller_region,
    COUNT(*) AS sellers
FROM analytics.dim_seller
WHERE is_current = TRUE
GROUP BY seller_region
ORDER BY seller_region;


-- Sample SCD history

SELECT
    seller_id,
    seller_city,
    seller_state,
    record_version,
    effective_from,
    effective_to,
    is_current
FROM analytics.dim_seller
ORDER BY seller_id, record_version
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
-- • Seller region derived during INSERT
-- • Removed unnecessary UPDATE pass
-- • Reduced table scans
-- • Improved execution metrics
-- • Cleaner SCD Type 2 implementation
-- • PostgreSQL optimizer refresh
-- • Improved readability and maintainability
--
-- ============================================================================
-- END OF FILE
-- ============================================================================