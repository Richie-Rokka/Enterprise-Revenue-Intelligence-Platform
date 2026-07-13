/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : executive_dashboard.sql
Schema      : analytics
Object      : analytics.executive_dashboard
Type        : Executive Dashboard View

Business Grain
--------------
One row per Calendar Date.

Purpose
-------
Provides the executive dashboard dataset by combining enterprise revenue
metrics with executive KPI snapshots. The view is optimized for Power BI
executive reporting and trend analysis.

Dependencies
------------
- analytics.revenue_kpis
- analytics.executive_kpis

Consumers
---------
- Executive Power BI Dashboard
- Executive Scorecards
- Executive Reporting

Notes
-----
- Trend metrics come from revenue_kpis.
- Enterprise snapshot KPIs come from executive_kpis.
- No direct dependency on warehouse or staging tables.
- Explicit projection only.
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.executive_dashboard AS

SELECT

    ----------------------------------------------------------------------------
    -- Calendar
    ----------------------------------------------------------------------------
    rk.calendar_date,
    rk.year_number,
    rk.quarter_number,
    rk.quarter_name,
    rk.month_number,
    rk.month_name,
    rk.year_month,
    rk.year_quarter,
    rk.week_of_year,
    rk.day_of_month,
    rk.day_name,
    rk.is_weekend,
    rk.is_business_day,

    ----------------------------------------------------------------------------
    -- Revenue Trend
    ----------------------------------------------------------------------------
    rk.gross_revenue,
    rk.net_revenue,
    rk.realized_revenue,

    rk.total_orders,
    rk.total_units_sold,

    rk.total_payment_value,

    rk.average_order_value,
    rk.average_payment_value,
    rk.average_item_price,
    rk.average_selling_price,

    rk.total_freight_value,
    rk.average_freight_value,
    rk.average_freight_percentage,

    rk.revenue_per_order,
    rk.revenue_per_unit,

    ----------------------------------------------------------------------------
    -- Enterprise Snapshot KPIs
    ----------------------------------------------------------------------------
    ek.active_customers,
    ek.active_products,
    ek.active_sellers,
    ek.product_categories,

    ek.total_gross_revenue,
    ek.total_net_revenue,
    ek.total_merchandise_sales,
    ek.total_freight_revenue,

    ek.average_order_value      AS enterprise_average_order_value,
    ek.average_item_price       AS enterprise_average_item_price,
    ek.average_payment_value    AS enterprise_average_payment_value,

    ek.revenue_per_customer,
    ek.revenue_per_product,
    ek.revenue_per_seller,

    ----------------------------------------------------------------------------
    -- Metadata
    ----------------------------------------------------------------------------
    ek.snapshot_timestamp,
    ek.metrics_version

FROM analytics.revenue_kpis rk

CROSS JOIN analytics.executive_kpis ek;