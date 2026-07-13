/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : customer_kpis.sql
Schema      : analytics
Object      : analytics.customer_kpis
Type        : Customer Metrics View

Business Grain
--------------
One row summarizing enterprise customer performance.

Purpose
-------
Provides enterprise customer KPIs covering customer base, purchasing
behavior, revenue contribution, product diversity, geographic coverage,
and customer segmentation.

Dependencies
------------
- analytics.vw_customer_sales

Consumers
---------
- Customer Dashboard
- Executive Dashboard
- Power BI Customer Dashboard

Notes
-----
- Built exclusively from analytics.vw_customer_sales
- Explicit projection only
- No SELECT *
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.customer_kpis AS

WITH customer_sales AS
(
    SELECT
        customer_id,
        customer_city,
        customer_state,
        customer_region,
        customer_country,

        total_orders,
        total_order_items,

        total_quantity,
        total_item_sales,
        total_freight,
        total_sales,
        total_net_revenue,
        average_order_value,

        unique_products,
        unique_categories,
        unique_sellers,

        first_purchase_date,
        last_purchase_date,

        customer_segment

    FROM analytics.vw_customer_sales
)

SELECT

    ---------------------------------------------------------------------------
    -- Customer Base
    ---------------------------------------------------------------------------
    COUNT(*)                                                    AS total_customers,

    COUNT(DISTINCT customer_country)                            AS countries_served,

    COUNT(DISTINCT customer_region)                             AS regions_served,

    COUNT(DISTINCT customer_state)                              AS states_served,

    COUNT(DISTINCT customer_city)                               AS cities_served,

    ---------------------------------------------------------------------------
    -- Revenue
    ---------------------------------------------------------------------------
    ROUND(
        SUM(total_sales),
        2
    )                                                           AS total_sales,

    ROUND(
        SUM(total_net_revenue),
        2
    )                                                           AS total_net_revenue,

    ROUND(
        SUM(total_item_sales),
        2
    )                                                           AS total_item_sales,

    ROUND(
        SUM(total_freight),
        2
    )                                                           AS total_freight,

    ROUND(
        AVG(total_net_revenue),
        2
    )                                                           AS average_customer_revenue,

    ROUND(
        MAX(total_net_revenue),
        2
    )                                                           AS highest_customer_revenue,

    ---------------------------------------------------------------------------
    -- Purchasing Behaviour
    ---------------------------------------------------------------------------
    SUM(total_orders)                                           AS total_orders,

    SUM(total_order_items)                                      AS total_order_items,

    SUM(total_quantity)                                         AS total_quantity,

    ROUND(
        AVG(total_orders),
        2
    )                                                           AS average_orders_per_customer,

    ROUND(
        AVG(total_order_items),
        2
    )                                                           AS average_order_items_per_customer,

    ROUND(
        AVG(total_quantity),
        2
    )                                                           AS average_quantity_per_customer,

    ROUND(
        AVG(average_order_value),
        2
    )                                                           AS average_order_value,

    ---------------------------------------------------------------------------
    -- Product Diversity
    ---------------------------------------------------------------------------
    ROUND(
        AVG(unique_products),
        2
    )                                                           AS average_unique_products,

    ROUND(
        AVG(unique_categories),
        2
    )                                                           AS average_unique_categories,

    ROUND(
        AVG(unique_sellers),
        2
    )                                                           AS average_unique_sellers,

    ---------------------------------------------------------------------------
    -- Customer Segmentation
    ---------------------------------------------------------------------------
    COUNT(*) FILTER (
        WHERE customer_segment = 'High Value'
    )                                                           AS high_value_customers,

    COUNT(*) FILTER (
        WHERE customer_segment = 'Medium Value'
    )                                                           AS medium_value_customers,

    COUNT(*) FILTER (
        WHERE customer_segment = 'Low Value'
    )                                                           AS low_value_customers,

    ---------------------------------------------------------------------------
    -- Customer Lifecycle
    ---------------------------------------------------------------------------
    MIN(first_purchase_date)                                    AS earliest_customer,

    MAX(last_purchase_date)                                     AS latest_customer,

    ---------------------------------------------------------------------------
    -- Revenue Productivity
    ---------------------------------------------------------------------------
    ROUND(
        SUM(total_net_revenue)
        /
        NULLIF(COUNT(*),0),
        2
    )                                                           AS revenue_per_customer,

    ROUND(
        SUM(total_orders)::NUMERIC
        /
        NULLIF(COUNT(*),0),
        2
    )                                                           AS orders_per_customer,

    ---------------------------------------------------------------------------
    -- Metadata
    ---------------------------------------------------------------------------
    CURRENT_TIMESTAMP                                           AS snapshot_timestamp,

    '1.0.0'::TEXT                                               AS metrics_version

FROM customer_sales;