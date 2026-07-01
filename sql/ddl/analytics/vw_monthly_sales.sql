/*
=============================================================
Enterprise Revenue Intelligence Platform
Analytics Semantic Layer

File:
    vw_monthly_sales.sql

Purpose
-------
Summarize monthly sales performance.

Business Question
-----------------
How is the business performing each month?

Business Grain
--------------
One Row = One Month (per Year)

Source
------
analytics.vw_sales

=============================================================
*/

CREATE OR REPLACE VIEW analytics.vw_monthly_sales AS

SELECT

    /*======================================================
      CALENDAR
    ======================================================*/

    year,

    month_number,

    month_name,

    quarter,

    /*======================================================
      MONTHLY METRICS
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

    year,

    quarter,

    month_number,

    month_name

ORDER BY

    year,

    month_number;