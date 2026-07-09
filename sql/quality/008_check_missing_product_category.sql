/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : 008_check_missing_product_category.sql
Schema      : analytics
Purpose     : Enterprise Data Quality Rule
Rule ID     : DQ-008
Rule Name   : Missing Product Category
Category    : Completeness
Severity    : HIGH
Version     : 1.0.0
===============================================================================
*/

WITH product_summary AS (

    SELECT
        COUNT(*) AS rows_checked
    FROM analytics.dim_product

),

missing_categories AS (

    SELECT
        COUNT(*) AS rows_failed
    FROM analytics.dim_product
    WHERE product_category_name IS NULL
        OR TRIM(product_category_name) = ''
        OR product_category_english IS NULL
        OR TRIM(product_category_english) = ''

)

SELECT

    'DQ-008' AS rule_id,

    'Missing Product Category' AS rule_name,

    'Completeness' AS category,

    'HIGH' AS severity,

    (m.rows_failed = 0) AS passed,

    s.rows_checked,

    m.rows_failed,

    ROUND(
        (
            (s.rows_checked - m.rows_failed) * 100.0
        )
        /
        NULLIF(s.rows_checked, 0),
        2
    ) AS quality_score,

    CASE
        WHEN m.rows_failed = 0 THEN
            'All products have valid categories.'
        ELSE
            CONCAT(
                m.rows_failed,
                ' product(s) have missing categories.'
            )
    END AS message,

    CURRENT_TIMESTAMP AS checked_at

FROM product_summary s
CROSS JOIN missing_categories m;