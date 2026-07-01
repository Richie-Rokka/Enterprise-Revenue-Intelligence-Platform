/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : load_dim_product.sql
Schema      : analytics
Object      : load_dim_product
Purpose     : Load Product Dimension (SCD Type 2)
Strategy    : Incremental / Idempotent
Source      : staging.product
              staging.product_category_translation
Version     : 3.1.0
===============================================================================
*/

CREATE OR REPLACE PROCEDURE analytics.load_dim_product()

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
    -- STEP 1 : EXPIRE CHANGED PRODUCT RECORDS
    ----------------------------------------------------------------------------

    UPDATE analytics.dim_product d
    SET
        effective_to = CURRENT_DATE - 1,
        is_current = FALSE,
        updated_timestamp = CURRENT_TIMESTAMP
    FROM staging.product p
    LEFT JOIN staging.product_category_translation t
        ON p.product_category_name = t.product_category_name
    WHERE d.product_id = p.product_id
      AND d.is_current = TRUE
      AND (
            COALESCE(d.product_category_name, '') <>
                COALESCE(p.product_category_name, '')
         OR COALESCE(d.product_category_english, '') <>
                COALESCE(t.product_category_name_english, '')
         OR COALESCE(d.product_weight_g, 0) <>
                COALESCE(p.product_weight_g, 0)
         OR COALESCE(d.product_length_cm, 0) <>
                COALESCE(p.product_length_cm, 0)
         OR COALESCE(d.product_height_cm, 0) <>
                COALESCE(p.product_height_cm, 0)
         OR COALESCE(d.product_width_cm, 0) <>
                COALESCE(p.product_width_cm, 0)
      );

    GET DIAGNOSTICS v_rows_updated = ROW_COUNT;

    ----------------------------------------------------------------------------
    -- STEP 2 : INSERT BRAND NEW PRODUCTS
    ----------------------------------------------------------------------------

    INSERT INTO analytics.dim_product (
        product_id, product_category_name, product_category_english,
        product_weight_g, product_length_cm, product_height_cm,
        product_width_cm, product_volume_cm3,
        product_size_class, product_weight_class,
        effective_from, effective_to, is_current,
        record_version, created_timestamp, updated_timestamp
    )

    SELECT
        src.product_id,
        src.product_category_name,
        src.product_category_english,
        src.product_weight_g,
        src.product_length_cm,
        src.product_height_cm,
        src.product_width_cm,
        src.product_volume_cm3,

        CASE
            WHEN src.product_volume_cm3 < 1000 THEN 'Small'
            WHEN src.product_volume_cm3 < 10000 THEN 'Medium'
            ELSE 'Large'
        END,

        CASE
            WHEN src.product_weight_g < 500 THEN 'Light'
            WHEN src.product_weight_g < 2000 THEN 'Medium'
            ELSE 'Heavy'
        END,

        CURRENT_DATE,
        DATE '9999-12-31',
        TRUE,
        1,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP

    FROM (
        SELECT
            p.product_id,
            p.product_category_name,
            t.product_category_name_english AS product_category_english,
            p.product_weight_g,
            p.product_length_cm,
            p.product_height_cm,
            p.product_width_cm,
            (
                COALESCE(p.product_length_cm, 0)
                * COALESCE(p.product_width_cm, 0)
                * COALESCE(p.product_height_cm, 0)
            ) AS product_volume_cm3
        FROM staging.product p
        LEFT JOIN staging.product_category_translation t
            ON p.product_category_name = t.product_category_name
    ) src

    WHERE NOT EXISTS (
        SELECT 1
        FROM analytics.dim_product d
        WHERE d.product_id = src.product_id
    );

    GET DIAGNOSTICS v_rows_affected = ROW_COUNT;
    v_rows_inserted := v_rows_inserted + v_rows_affected;

    ----------------------------------------------------------------------------
    -- STEP 3 : INSERT NEW PRODUCT VERSIONS
    ----------------------------------------------------------------------------

    INSERT INTO analytics.dim_product (
        product_id, product_category_name, product_category_english,
        product_weight_g, product_length_cm, product_height_cm,
        product_width_cm, product_volume_cm3,
        product_size_class, product_weight_class,
        effective_from, effective_to, is_current,
        record_version, created_timestamp, updated_timestamp
    )

    SELECT
        src.product_id,
        src.product_category_name,
        src.product_category_english,
        src.product_weight_g,
        src.product_length_cm,
        src.product_height_cm,
        src.product_width_cm,
        src.product_volume_cm3,

        CASE
            WHEN src.product_volume_cm3 < 1000 THEN 'Small'
            WHEN src.product_volume_cm3 < 10000 THEN 'Medium'
            ELSE 'Large'
        END,

        CASE
            WHEN src.product_weight_g < 500 THEN 'Light'
            WHEN src.product_weight_g < 2000 THEN 'Medium'
            ELSE 'Heavy'
        END,

        CURRENT_DATE,
        DATE '9999-12-31',
        TRUE,
        d.record_version + 1,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP

    FROM (
        SELECT
            p.product_id,
            p.product_category_name,
            t.product_category_name_english AS product_category_english,
            p.product_weight_g,
            p.product_length_cm,
            p.product_height_cm,
            p.product_width_cm,
            (
                COALESCE(p.product_length_cm, 0)
                * COALESCE(p.product_width_cm, 0)
                * COALESCE(p.product_height_cm, 0)
            ) AS product_volume_cm3
        FROM staging.product p
        LEFT JOIN staging.product_category_translation t
            ON p.product_category_name = t.product_category_name
    ) src

    INNER JOIN analytics.dim_product d
        ON src.product_id = d.product_id

    WHERE d.is_current = FALSE
      AND d.effective_to = CURRENT_DATE - 1
      AND NOT EXISTS (
            SELECT 1
            FROM analytics.dim_product x
            WHERE x.product_id = src.product_id
              AND x.is_current = TRUE
      );

    GET DIAGNOSTICS v_rows_affected = ROW_COUNT;
    v_rows_inserted := v_rows_inserted + v_rows_affected;

    ----------------------------------------------------------------------------
    -- STEP 4 : UPDATE OPTIMIZER STATISTICS
    ----------------------------------------------------------------------------

    ANALYZE analytics.dim_product;

    ----------------------------------------------------------------------------
    -- STEP 5 : EXECUTION SUMMARY
    ----------------------------------------------------------------------------

    SELECT COUNT(*)
    INTO v_rows_affected
    FROM analytics.dim_product
    WHERE is_current = TRUE;

    v_end_time := clock_timestamp();

    RAISE NOTICE '';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'ERIP ANALYTICS - PRODUCT DIMENSION LOAD';
    RAISE NOTICE '============================================================';
    RAISE NOTICE 'Status            : SUCCESS';
    RAISE NOTICE 'Target Table      : analytics.dim_product';
    RAISE NOTICE 'Rows Updated      : %', v_rows_updated;
    RAISE NOTICE 'Rows Inserted     : %', v_rows_inserted;
    RAISE NOTICE 'Current Products  : %', v_rows_affected;
    RAISE NOTICE 'Execution Time    : % sec',
        ROUND(EXTRACT(EPOCH FROM (v_end_time - v_start_time))::NUMERIC, 3);
    RAISE NOTICE '============================================================';
    RAISE NOTICE '';

EXCEPTION

    WHEN OTHERS THEN

        RAISE NOTICE '';
        RAISE NOTICE '============================================================';
        RAISE NOTICE 'ERIP ANALYTICS - PRODUCT DIMENSION LOAD FAILED';
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

CALL analytics.load_dim_product();


-- ============================================================================
-- VALIDATION QUERIES
-- ============================================================================

-- Current products

SELECT COUNT(*) AS current_products
FROM analytics.dim_product
WHERE is_current = TRUE;


-- Product history

SELECT
    product_id,
    COUNT(*) AS versions
FROM analytics.dim_product
GROUP BY product_id
HAVING COUNT(*) > 1
ORDER BY versions DESC;


-- Duplicate current products (should return zero rows)

SELECT
    product_id,
    COUNT(*) AS current_records
FROM analytics.dim_product
WHERE is_current = TRUE
GROUP BY product_id
HAVING COUNT(*) > 1;


-- Category distribution

SELECT
    product_category_english,
    COUNT(*) AS products
FROM analytics.dim_product
WHERE is_current = TRUE
GROUP BY product_category_english
ORDER BY products DESC;


-- Size distribution

SELECT
    product_size_class,
    COUNT(*) AS products
FROM analytics.dim_product
WHERE is_current = TRUE
GROUP BY product_size_class
ORDER BY product_size_class;


-- Weight distribution

SELECT
    product_weight_class,
    COUNT(*) AS products
FROM analytics.dim_product
WHERE is_current = TRUE
GROUP BY product_weight_class
ORDER BY product_weight_class;


-- Sample SCD history

SELECT
    product_id,
    product_category_english,
    record_version,
    effective_from,
    effective_to,
    is_current
FROM analytics.dim_product
ORDER BY product_id, record_version
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
-- • Single product volume calculation
-- • Derived attributes calculated during INSERT
-- • Reduced duplicate expressions
-- • Improved execution metrics
-- • PostgreSQL optimizer refresh
-- • Cleaner SCD Type 2 implementation
-- • Improved readability and maintainability
--
-- ============================================================================
-- END OF FILE
-- ============================================================================