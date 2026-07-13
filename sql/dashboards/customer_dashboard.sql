/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : customer_dashboard.sql
Schema      : analytics
Object      : analytics.customer_dashboard
Type        : Dashboard View

Business Grain
--------------
One row summarizing enterprise customer performance.

Purpose
-------
Provides the customer dashboard dataset for customer analytics,
segmentation, purchasing behaviour and geographic distribution.

Dependencies
------------
- analytics.customer_kpis

Consumers
---------
- Power BI Customer Dashboard
- Executive Dashboard

===============================================================================
*/

CREATE OR REPLACE VIEW analytics.customer_dashboard AS

SELECT

    ---------------------------------------------------------------------------
    -- Customer Base
    ---------------------------------------------------------------------------
    total_customers,
    countries_served,
    regions_served,
    states_served,
    cities_served,

    ---------------------------------------------------------------------------
    -- Revenue
    ---------------------------------------------------------------------------
    total_sales,
    total_net_revenue,
    total_item_sales,
    total_freight,

    average_customer_revenue,
    highest_customer_revenue,

    ---------------------------------------------------------------------------
    -- Purchasing Behaviour
    ---------------------------------------------------------------------------
    total_orders,
    total_order_items,
    total_quantity,

    average_orders_per_customer,
    average_order_items_per_customer,
    average_quantity_per_customer,

    average_order_value,

    ---------------------------------------------------------------------------
    -- Product Diversity
    ---------------------------------------------------------------------------
    average_unique_products,
    average_unique_categories,
    average_unique_sellers,

    ---------------------------------------------------------------------------
    -- Customer Segmentation
    ---------------------------------------------------------------------------
    high_value_customers,
    medium_value_customers,
    low_value_customers,

    ---------------------------------------------------------------------------
    -- Customer Lifecycle
    ---------------------------------------------------------------------------
    earliest_customer,
    latest_customer,

    ---------------------------------------------------------------------------
    -- Productivity
    ---------------------------------------------------------------------------
    revenue_per_customer,
    orders_per_customer

FROM analytics.customer_kpis;