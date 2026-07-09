/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : 003_check_duplicate_products.sql
Schema      : analytics
Purpose     : Enterprise Data Quality Rule
Rule ID     : DQ-003
Rule Name   : Duplicate Product Detection
Category    : Uniqueness
Severity    : CRITICAL
Version     : 1.0.0
===============================================================================
*/

WITH product_summary AS (

    SELECT
        COUNT(*) AS rows_checked
    FROM analytics.dim_product

),

duplicate_products AS (

    SELECT
        product_id,
        COUNT(*) AS duplicate_count
    FROM analytics.dim_product
    GROUP BY product_id
    HAVING COUNT(*) > 1

),

duplicate_summary AS (

    SELECT
        COUNT(*) AS rows_failed
    FROM duplicate_products

)

SELECT

    'DQ-003' AS rule_id,

    'Duplicate Product Detection' AS rule_name,

    'Uniqueness' AS category,

    'CRITICAL' AS severity,

    (d.rows_failed = 0) AS passed,

    s.rows_checked,

    d.rows_failed,

    ROUND(
        (
            (s.rows_checked - d.rows_failed) * 100.0
        )
        /
        NULLIF(s.rows_checked, 0),
        2
    ) AS quality_score,

    CASE
        WHEN d.rows_failed = 0 THEN
            'No duplicate product business keys detected.'
        ELSE
            CONCAT(
                d.rows_failed,
                ' duplicate product business key(s) detected.'
            )
    END AS message,

    CURRENT_TIMESTAMP AS checked_at

FROM product_summary s
CROSS JOIN duplicate_summary d;