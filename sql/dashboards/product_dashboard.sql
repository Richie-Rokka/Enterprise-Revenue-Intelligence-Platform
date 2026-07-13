/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : product_dashboard.sql
Schema      : analytics
Object      : analytics.product_dashboard
Type        : Dashboard View

Business Grain
--------------
One row summarizing enterprise product performance.

Purpose
-------
Provides the Product Dashboard dataset for product portfolio,
sales performance, pricing, freight, customer reach and
product performance analysis.

Dependencies
------------
- analytics.product_kpis

Consumers
---------
- Power BI Product Dashboard
- Executive Dashboard

===============================================================================
*/

CREATE OR REPLACE VIEW analytics.product_dashboard AS

SELECT

    ---------------------------------------------------------------------------
    -- Product Portfolio
    ---------------------------------------------------------------------------
    total_products,
    total_categories,
    size_classes,
    weight_classes,

    ---------------------------------------------------------------------------
    -- Revenue
    ---------------------------------------------------------------------------
    gross_product_sales,
    total_sales,
    total_net_revenue,

    average_product_revenue,
    highest_product_revenue,

    ---------------------------------------------------------------------------
    -- Sales Activity
    ---------------------------------------------------------------------------
    total_orders,
    total_order_items,
    total_quantity_sold,

    average_orders_per_product,
    average_quantity_per_product,

    ---------------------------------------------------------------------------
    -- Pricing
    ---------------------------------------------------------------------------
    average_unit_price,
    average_order_value,

    ---------------------------------------------------------------------------
    -- Freight
    ---------------------------------------------------------------------------
    total_freight,
    average_freight_percentage,

    ---------------------------------------------------------------------------
    -- Market Reach
    ---------------------------------------------------------------------------
    average_customers_per_product,
    average_sellers_per_product,

    ---------------------------------------------------------------------------
    -- Product Performance
    ---------------------------------------------------------------------------
    top_performers,
    high_performers,
    medium_performers,
    low_performers,

    ---------------------------------------------------------------------------
    -- Product Lifecycle
    ---------------------------------------------------------------------------
    earliest_sale_date,
    latest_sale_date,

    ---------------------------------------------------------------------------
    -- Productivity
    ---------------------------------------------------------------------------
    revenue_per_product

FROM analytics.product_kpis;