/*
=============================================================
Enterprise Revenue Intelligence Platform
Analytics Semantic Layer

File:
    vw_product_sales.sql

Purpose
-------
Summarize sales performance by product category.

Business Question
-----------------
How is each product category performing?

Business Grain
--------------
One Row = One Product Category

Source
------
analytics.vw_sales

=============================================================
*/

CREATE OR REPLACE VIEW analytics.vw_product_sales AS

SELECT

    /*======================================================
      PRODUCT
    ======================================================*/

    product_category,

    /*======================================================
      PRODUCT METRICS
    ======================================================*/

    COUNT(DISTINCT order_id) AS total_orders,

    SUM(sales_line_count) AS total_sales_lines,

    SUM(total_revenue) AS total_revenue,

    ROUND(
        (
            SUM(total_revenue)
            /
            NULLIF(
                COUNT(DISTINCT order_id),
                0
            )
        )::numeric,
        2
    ) AS average_order_value,

    ROUND(
        (
            SUM(total_revenue)
            /
            NULLIF(
                SUM(sales_line_count),
                0
            )
        )::numeric,
        2
    ) AS average_sales_line_value

FROM analytics.vw_sales

GROUP BY

    product_category

ORDER BY

    total_revenue DESC;