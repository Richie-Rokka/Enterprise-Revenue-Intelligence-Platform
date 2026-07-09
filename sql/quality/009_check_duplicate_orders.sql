/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : 009_check_duplicate_orders.sql
Schema      : analytics
Purpose     : Enterprise Data Quality Rule
Rule ID     : DQ-009
Rule Name   : Duplicate Order Detection
Category    : Uniqueness
Severity    : CRITICAL
Version     : 1.0.0
===============================================================================
*/

WITH order_summary AS (

    SELECT
        COUNT(*) AS rows_checked
    FROM analytics.fact_sales

),

duplicate_orders AS (

    SELECT
        order_id,
        COUNT(*) AS duplicate_count
    FROM analytics.fact_sales
    GROUP BY order_id
    HAVING COUNT(*) > 1

),

duplicate_summary AS (

    SELECT
        COUNT(*) AS rows_failed
    FROM duplicate_orders

)

SELECT

    'DQ-009' AS rule_id,

    'Duplicate Order Detection' AS rule_name,

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
            'No duplicate orders detected.'
        ELSE
            CONCAT(
                d.rows_failed,
                ' duplicate order(s) detected.'
            )
    END AS message,

    CURRENT_TIMESTAMP AS checked_at

FROM order_summary s
CROSS JOIN duplicate_summary d;