/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : seller_dashboard.sql
Schema      : analytics
Object      : analytics.seller_dashboard
Type        : Dashboard View

Business Grain
--------------
One row summarizing enterprise seller performance.

Purpose
-------
Provides the Seller Dashboard dataset for seller portfolio,
sales performance, customer reach, product diversity,
freight performance and seller performance analysis.

Dependencies
------------
- analytics.seller_kpis

Consumers
---------
- Power BI Seller Dashboard
- Executive Dashboard

===============================================================================
*/

CREATE OR REPLACE VIEW analytics.seller_dashboard AS

SELECT

    ---------------------------------------------------------------------------
    -- Seller Portfolio
    ---------------------------------------------------------------------------
    total_sellers,
    countries,
    regions,
    states,
    cities,

    ---------------------------------------------------------------------------
    -- Revenue
    ---------------------------------------------------------------------------
    gross_sales,
    total_sales,
    total_net_revenue,

    average_seller_revenue,
    highest_seller_revenue,

    ---------------------------------------------------------------------------
    -- Sales Activity
    ---------------------------------------------------------------------------
    total_orders,
    total_order_items,
    total_quantity_sold,

    average_orders_per_seller,
    average_quantity_per_seller,
    average_order_value,

    ---------------------------------------------------------------------------
    -- Freight
    ---------------------------------------------------------------------------
    total_freight,
    average_freight_percentage,

    ---------------------------------------------------------------------------
    -- Customer Reach
    ---------------------------------------------------------------------------
    average_customers_per_seller,

    ---------------------------------------------------------------------------
    -- Product Portfolio
    ---------------------------------------------------------------------------
    average_products_per_seller,
    average_categories_per_seller,

    ---------------------------------------------------------------------------
    -- Seller Performance
    ---------------------------------------------------------------------------
    elite_sellers,
    top_sellers,
    high_performers,
    standard_sellers,

    ---------------------------------------------------------------------------
    -- Seller Lifecycle
    ---------------------------------------------------------------------------
    earliest_sale_date,
    latest_sale_date,

    ---------------------------------------------------------------------------
    -- Productivity
    ---------------------------------------------------------------------------
    revenue_per_seller

FROM analytics.seller_kpis;