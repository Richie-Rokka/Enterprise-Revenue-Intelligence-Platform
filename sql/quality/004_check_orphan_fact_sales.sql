/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : 004_check_orphan_fact_sales.sql
Schema      : analytics
Purpose     : Enterprise Data Quality Rule
Rule ID     : DQ-004
Rule Name   : Orphan Fact Sales Detection
Category    : Referential Integrity
Severity    : CRITICAL
Version     : 1.0.0
===============================================================================
*/

WITH sales_summary AS (

    SELECT
        COUNT(*) AS rows_checked
    FROM analytics.fact_sales

),

orphan_sales AS (

    SELECT
        COUNT(*) AS rows_failed
    FROM analytics.fact_sales f
    LEFT JOIN analytics.dim_customer c
        ON f.customer_sk = c.customer_sk
    LEFT JOIN analytics.dim_product p
        ON f.product_sk = p.product_sk
    LEFT JOIN analytics.dim_seller s
        ON f.seller_sk = s.seller_sk
    LEFT JOIN analytics.dim_date d
        ON f.date_key = d.date_key
    WHERE
        c.customer_sk IS NULL
        OR p.product_sk IS NULL
        OR s.seller_sk IS NULL
        OR d.date_key IS NULL

)

SELECT

    'DQ-004' AS rule_id,

    'Orphan Fact Sales Detection' AS rule_name,

    'Referential Integrity' AS category,

    'CRITICAL' AS severity,

    (o.rows_failed = 0) AS passed,

    s.rows_checked,

    o.rows_failed,

    ROUND(
        (
            (s.rows_checked - o.rows_failed) * 100.0
        )
        /
        NULLIF(s.rows_checked, 0),
        2
    ) AS quality_score,

    CASE
        WHEN o.rows_failed = 0 THEN
            'No orphan fact records detected.'
        ELSE
            CONCAT(
                o.rows_failed,
                ' orphan fact_sales record(s) detected.'
            )
    END AS message,

    CURRENT_TIMESTAMP AS checked_at

FROM sales_summary s
CROSS JOIN orphan_sales o;