/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : sales_dashboard.sql
Schema      : analytics
Object      : analytics.sales_dashboard
Type        : Dashboard View

Business Grain
--------------
One row per Calendar Date.

Purpose
-------
Provides the Sales Dashboard dataset for sales trend analysis,
revenue performance, pricing, freight, and sales productivity.

Dependencies
------------
- analytics.revenue_kpis

Consumers
---------
- Power BI Sales Dashboard
- Executive Reporting
- Sales Analytics

Notes
-----
- Built exclusively from analytics.revenue_kpis
- Explicit projection only.
- No SELECT *.
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.sales_dashboard AS

SELECT

    ----------------------------------------------------------------------------
    -- Calendar
    ----------------------------------------------------------------------------
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

    ----------------------------------------------------------------------------
    -- Revenue
    ----------------------------------------------------------------------------
    gross_revenue,
    net_revenue,
    realized_revenue,

    ----------------------------------------------------------------------------
    -- Sales Activity
    ----------------------------------------------------------------------------
    total_orders,
    total_units_sold,

    ----------------------------------------------------------------------------
    -- Payments
    ----------------------------------------------------------------------------
    total_payment_value,
    average_payment_value,

    ----------------------------------------------------------------------------
    -- Order Value
    ----------------------------------------------------------------------------
    average_order_value,
    minimum_order_value,
    maximum_order_value,

    ----------------------------------------------------------------------------
    -- Pricing
    ----------------------------------------------------------------------------
    average_item_price,
    average_selling_price,

    ----------------------------------------------------------------------------
    -- Freight
    ----------------------------------------------------------------------------
    total_freight_value,
    average_freight_value,
    average_freight_percentage,

    ----------------------------------------------------------------------------
    -- Productivity
    ----------------------------------------------------------------------------
    revenue_per_order,
    revenue_per_unit

FROM analytics.revenue_kpis;