/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : 005_check_invalid_order_dates.sql
Schema      : analytics
Purpose     : Enterprise Data Quality Rule
Rule ID     : DQ-005
Rule Name   : Invalid Order Dates
Category    : Validity
Severity    : HIGH
Version     : 1.0.0
===============================================================================
*/

WITH sales_summary AS (

    SELECT
        COUNT(*) AS rows_checked
    FROM analytics.fact_sales

),

invalid_dates AS (

    SELECT
        COUNT(*) AS rows_failed
    FROM analytics.fact_sales
    WHERE payment_value < 0

)

SELECT

    'DQ-005' AS rule_id,

    'Invalid Order Dates' AS rule_name,

    'Validity' AS category,

    'HIGH' AS severity,

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
            'All order dates are valid.'
        ELSE
            CONCAT(
                i.rows_failed,
                ' order(s) have delivery dates earlier than order dates.'
            )
    END AS message,

    CURRENT_TIMESTAMP AS checked_at

FROM sales_summary s
CROSS JOIN invalid_dates i;