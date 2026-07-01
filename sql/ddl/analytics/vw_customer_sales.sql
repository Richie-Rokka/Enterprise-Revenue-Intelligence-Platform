/*
=============================================================
Enterprise Revenue Intelligence Platform
Analytics Semantic Layer

File:
    vw_customer_sales.sql

Purpose
-------
Summarize sales performance at the customer level.

Business Question
-----------------
How valuable is each customer?

Business Grain
--------------
One Row = One Customer

Source
------
analytics.vw_sales

=============================================================
*/

CREATE OR REPLACE VIEW analytics.vw_customer_sales AS

SELECT

    /*======================================================
      CUSTOMER
    ======================================================*/

    customer_id,

    customer_city,

    customer_state,

    /*======================================================
      CUSTOMER METRICS
    ======================================================*/

    COUNT(DISTINCT order_id) AS total_orders,

    SUM(sales_line_count) AS total_sales_lines,

    SUM(total_revenue) AS total_revenue,

    ROUND(
        (
        SUM(total_revenue)
        /
        NULLIF(COUNT(DISTINCT order_id), 0)
        )::numeric,
        2
    ) AS average_order_value

FROM analytics.vw_sales

GROUP BY

    customer_id,

    customer_city,

    customer_state;