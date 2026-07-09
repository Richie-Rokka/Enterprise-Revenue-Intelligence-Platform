/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : 006_check_payment_totals.sql
Schema      : analytics
Purpose     : Enterprise Data Quality Rule
Rule ID     : DQ-006
Rule Name   : Payment Total Validation
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

invalid_payments AS (

    SELECT
        COUNT(*) AS rows_failed
    FROM analytics.fact_sales
    WHERE ABS(payment_value - net_sales_amount) > 0.01

)

SELECT

    'DQ-006' AS rule_id,

    'Payment Total Validation' AS rule_name,

    'Business Rule' AS category,

    'CRITICAL' AS severity,

    (i.rows_failed = 0) AS passed,

    s.rows_checked,

    i.rows_failed,

    ROUND(
        (
            (s.rows_checked - i.rows_failed) * 100.0
        )
        /
        NULLIF(s.rows_checked, 0),
        2
    ) AS quality_score,

    CASE
        WHEN i.rows_failed = 0 THEN
            'All payment totals match sales amounts.'
        ELSE
            CONCAT(
                i.rows_failed,
                ' payment total mismatch(es) detected.'
            )
    END AS message,

    CURRENT_TIMESTAMP AS checked_at

FROM sales_summary s
CROSS JOIN invalid_payments i;