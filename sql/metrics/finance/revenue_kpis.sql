/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : revenue_kpis.sql
Schema      : analytics
Object      : analytics.revenue_kpis
Type        : Finance Metrics View

Business Grain
--------------
One row per Calendar Date.

Purpose
-------
Provides the canonical enterprise revenue metrics by calendar date.
Supports daily, weekly, monthly, quarterly and yearly reporting from a
single semantic metrics view.

Dependencies
------------
- analytics.vw_sales

Consumers
---------
- Executive Dashboard
- Finance Dashboard
- Power BI
- Revenue Analytics

Notes
-----
- Built exclusively from analytics.vw_sales
- Explicit projection only
- No SELECT *
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.revenue_kpis AS

WITH sales AS
(
    SELECT

        -----------------------------------------------------------------------
        -- Calendar
        -----------------------------------------------------------------------
        calendar_date,
        year_number,
        quarter_number,
        quarter_name,
        month_number,
        month_name,
        year_month,
        year_quarter,
        week_of_year,
        day_of_month,
        day_name,
        is_weekend,
        is_business_day,

        -----------------------------------------------------------------------
        -- Commercial Measures
        -----------------------------------------------------------------------
        order_id,
        quantity,
        item_price,
        freight_value,
        gross_sales_amount,
        net_sales_amount,
        payment_value,
        total_order_value,
        total_net_revenue,
        average_selling_price,
        freight_percentage

    FROM analytics.vw_sales
)

SELECT

    ---------------------------------------------------------------------------
    -- Calendar
    ---------------------------------------------------------------------------
    calendar_date,
    year_number,
    quarter_number,
    quarter_name,
    month_number,
    month_name,
    year_month,
    year_quarter,
    week_of_year,
    day_of_month,
    day_name,
    is_weekend,
    is_business_day,

    ---------------------------------------------------------------------------
    -- Revenue
    ---------------------------------------------------------------------------
    ROUND(
        SUM(gross_sales_amount),
        2
    ) AS gross_revenue,

    ROUND(
        SUM(net_sales_amount),
        2
    ) AS net_revenue,

    ROUND(
        SUM(total_net_revenue),
        2
    ) AS realized_revenue,

    ---------------------------------------------------------------------------
    -- Orders
    ---------------------------------------------------------------------------
    COUNT(DISTINCT order_id) AS total_orders,

    SUM(quantity) AS total_units_sold,

    ---------------------------------------------------------------------------
    -- Payments
    ---------------------------------------------------------------------------
    ROUND(
        SUM(payment_value),
        2
    ) AS total_payment_value,

    ROUND(
        AVG(payment_value),
        2
    ) AS average_payment_value,

    ---------------------------------------------------------------------------
    -- Order Value
    ---------------------------------------------------------------------------
    ROUND(
        AVG(total_order_value),
        2
    ) AS average_order_value,

    ROUND(
        MIN(total_order_value),
        2
    ) AS minimum_order_value,

    ROUND(
        MAX(total_order_value),
        2
    ) AS maximum_order_value,

    ---------------------------------------------------------------------------
    -- Pricing
    ---------------------------------------------------------------------------
    ROUND(
        AVG(item_price),
        2
    ) AS average_item_price,

    ROUND(
        AVG(average_selling_price),
        2
    ) AS average_selling_price,

    ---------------------------------------------------------------------------
    -- Freight
    ---------------------------------------------------------------------------
    ROUND(
        SUM(freight_value),
        2
    ) AS total_freight_value,

    ROUND(
        AVG(freight_value),
        2
    ) AS average_freight_value,

    ROUND(
        AVG(freight_percentage),
        2
    ) AS average_freight_percentage,

    ---------------------------------------------------------------------------
    -- Productivity
    ---------------------------------------------------------------------------
    ROUND(
        SUM(total_net_revenue)
        /
        NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS revenue_per_order,

    ROUND(
        SUM(total_net_revenue)
        /
        NULLIF(SUM(quantity), 0),
        2
    ) AS revenue_per_unit

FROM sales

GROUP BY

    calendar_date,
    year_number,
    quarter_number,
    quarter_name,
    month_number,
    month_name,
    year_month,
    year_quarter,
    week_of_year,
    day_of_month,
    day_name,
    is_weekend,
    is_business_day;