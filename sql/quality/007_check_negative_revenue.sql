/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : 007_check_negative_revenue.sql
Schema      : analytics
Purpose     : Enterprise Data Quality Rule
Rule ID     : DQ-007
Rule Name   : Negative Revenue Detection
Category    : Business Rule
Severity    : CRITICAL
Version     : 1.0.0
===============================================================================
*/

WITH sales_summary AS (

    SELECT
        COUNT(*) AS rows_checked
    FROM analytics.fact_sales

),

negative_revenue AS (

    SELECT
        COUNT(*) AS rows_failed
    FROM analytics.fact_sales
    WHERE net_sales_amount < 0

)

SELECT

    'DQ-007' AS rule_id,

    'Negative Revenue Detection' AS rule_name,

    'Business Rule' AS category,

    'CRITICAL' AS severity,

    (n.rows_failed = 0) AS passed,

    s.rows_checked,

    n.rows_failed,

    ROUND(
        (
            (s.rows_checked - n.rows_failed) * 100.0
        )
        /
        NULLIF(s.rows_checked, 0),
        2
    ) AS quality_score,

    CASE
        WHEN n.rows_failed = 0 THEN
            'No negative revenue records detected.'
        ELSE
            CONCAT(
                n.rows_failed,
                ' record(s) with negative revenue detected.'
            )
    END AS message,

    CURRENT_TIMESTAMP AS checked_at

FROM sales_summary s
CROSS JOIN negative_revenue n;