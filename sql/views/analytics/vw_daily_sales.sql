/*
=============================================================
Enterprise Revenue Intelligence Platform
Analytics Semantic Layer

File:
    vw_daily_sales.sql

Purpose
-------
Summarize daily sales performance.

Business Question
-----------------
How did the business perform each day?

Business Grain
--------------
One Row = One Calendar Date

Source
------
analytics.vw_sales

=============================================================
*/

CREATE OR REPLACE VIEW analytics.vw_daily_sales AS

SELECT

    /*======================================================
      DATE
    ======================================================*/

    date,

    year,

    quarter,

    month_number,

    month_name,

    week,

    day,

    day_name,

    day_of_week,

    is_weekend,

    /*======================================================
      DAILY METRICS
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

    date,

    year,

    quarter,

    month_number,

    month_name,

    week,

    day,

    day_name,

    day_of_week,

    is_weekend

ORDER BY

    date;