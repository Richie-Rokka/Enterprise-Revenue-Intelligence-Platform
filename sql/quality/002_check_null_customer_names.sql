/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : 002_check_null_customer_names.sql
Schema      : analytics
Purpose     : Enterprise Data Quality Rule
Rule ID     : DQ-002
Rule Name   : Customer Name Completeness
Category    : Completeness
Severity    : HIGH
Version     : 1.0.0
===============================================================================
*/

WITH customer_summary AS (

    SELECT
        COUNT(*) AS rows_checked
    FROM analytics.dim_customer

),

invalid_rows AS (

    SELECT
        COUNT(*) AS rows_failed
    FROM analytics.dim_customer
    WHERE customer_city IS NULL
        OR TRIM(customer_city) = ''
        OR customer_state IS NULL

)

SELECT

    'DQ-002' AS rule_id,

    'Customer Name Completeness' AS rule_name,

    'Completeness' AS category,

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
        WHEN i.rows_failed = 0
            THEN 'All customer names are populated.'
        ELSE
            CONCAT(
                i.rows_failed,
                ' customer record(s) have missing names.'
            )
    END AS message,

    CURRENT_TIMESTAMP AS checked_at

FROM customer_summary s
CROSS JOIN invalid_rows i;