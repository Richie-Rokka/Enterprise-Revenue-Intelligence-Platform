/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : 001_check_duplicate_customers.sql
Schema      : analytics
Purpose     : Enterprise Data Quality Rule
Rule ID     : DQ-001
Rule Name   : Duplicate Customer Detection
Category    : Uniqueness
Severity    : CRITICAL
Version     : 1.0.0

Description
-----------
Detect duplicate customer business keys in analytics.dim_customer.

Expected Result
---------------
rule_id
rule_name
category
severity
passed
rows_checked
rows_failed
message
checked_at

===============================================================================
*/

WITH customer_summary AS (

    SELECT
        COUNT(*) AS rows_checked
    FROM analytics.dim_customer

),

duplicate_customers AS (

    SELECT
        customer_id,
        COUNT(*) AS duplicate_count
    FROM analytics.dim_customer
    GROUP BY customer_id
    HAVING COUNT(*) > 1

),

duplicate_summary AS (

    SELECT
        COUNT(*) AS rows_failed
    FROM duplicate_customers

)

SELECT

    'DQ-001' AS rule_id,

    'Duplicate Customer Detection' AS rule_name,

    'Uniqueness' AS category,

    'CRITICAL' AS severity,

    CASE
        WHEN d.rows_failed = 0 THEN TRUE
        ELSE FALSE
    END AS passed,

    c.rows_checked,

    d.rows_failed,

    ROUND(
        (
            (c.rows_checked - d.rows_failed) * 100.0
        )
        /
        NULLIF(c.rows_checked, 0),
        2
    ) AS quality_score,

    CASE
        WHEN d.rows_failed = 0
            THEN 'No duplicate customer business keys detected.'
        ELSE
            CONCAT(
                d.rows_failed,
                ' duplicate customer business key(s) detected.'
            )
    END AS message,

    CURRENT_TIMESTAMP AS checked_at

FROM customer_summary c
CROSS JOIN duplicate_summary d;