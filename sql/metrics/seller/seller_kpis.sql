/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : seller_kpis.sql
Schema      : analytics
Object      : analytics.seller_kpis
Type        : Seller Metrics View

Business Grain
--------------
One row summarizing enterprise seller performance.

Purpose
-------
Provides enterprise seller KPIs covering seller portfolio, revenue,
sales activity, customer reach, product diversity and seller
performance classification.

Dependencies
------------
- analytics.vw_seller_performance

Consumers
---------
- Seller Dashboard
- Executive Dashboard
- Power BI Seller Dashboard

Notes
-----
- Built exclusively from analytics.vw_seller_performance
- Explicit projection only
- No SELECT *
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.seller_kpis AS

WITH seller_sales AS
(
    SELECT

        seller_id,
        seller_city,
        seller_state,
        seller_region,
        seller_country,

        total_orders,
        total_order_items,
        total_quantity_sold,

        gross_sales,
        total_sales,
        total_net_revenue,
        average_order_value,

        total_freight,
        average_freight_percentage,

        unique_customers,
        unique_products,
        unique_categories,

        first_sale_date,
        last_sale_date,

        seller_performance_band

    FROM analytics.vw_seller_performance
)

SELECT

    ---------------------------------------------------------------------------
    -- Seller Portfolio
    ---------------------------------------------------------------------------
    COUNT(*)                                                    AS total_sellers,

    COUNT(DISTINCT seller_country)                              AS countries,

    COUNT(DISTINCT seller_region)                               AS regions,

    COUNT(DISTINCT seller_state)                                AS states,

    COUNT(DISTINCT seller_city)                                 AS cities,

    ---------------------------------------------------------------------------
    -- Revenue
    ---------------------------------------------------------------------------
    ROUND(
        SUM(gross_sales),
        2
    )                                                           AS gross_sales,

    ROUND(
        SUM(total_sales),
        2
    )                                                           AS total_sales,

    ROUND(
        SUM(total_net_revenue),
        2
    )                                                           AS total_net_revenue,

    ROUND(
        AVG(total_net_revenue),
        2
    )                                                           AS average_seller_revenue,

    ROUND(
        MAX(total_net_revenue),
        2
    )                                                           AS highest_seller_revenue,

    ---------------------------------------------------------------------------
    -- Sales Activity
    ---------------------------------------------------------------------------
    SUM(total_orders)                                           AS total_orders,

    SUM(total_order_items)                                      AS total_order_items,

    SUM(total_quantity_sold)                                    AS total_quantity_sold,

    ROUND(
        AVG(total_orders),
        2
    )                                                           AS average_orders_per_seller,

    ROUND(
        AVG(total_quantity_sold),
        2
    )                                                           AS average_quantity_per_seller,

    ROUND(
        AVG(average_order_value),
        2
    )                                                           AS average_order_value,

    ---------------------------------------------------------------------------
    -- Freight
    ---------------------------------------------------------------------------
    ROUND(
        SUM(total_freight),
        2
    )                                                           AS total_freight,

    ROUND(
        AVG(average_freight_percentage),
        2
    )                                                           AS average_freight_percentage,

    ---------------------------------------------------------------------------
    -- Customer Reach
    ---------------------------------------------------------------------------
    ROUND(
        AVG(unique_customers),
        2
    )                                                           AS average_customers_per_seller,

    ---------------------------------------------------------------------------
    -- Product Portfolio
    ---------------------------------------------------------------------------
    ROUND(
        AVG(unique_products),
        2
    )                                                           AS average_products_per_seller,

    ROUND(
        AVG(unique_categories),
        2
    )                                                           AS average_categories_per_seller,

    ---------------------------------------------------------------------------
    -- Seller Performance
    ---------------------------------------------------------------------------
    COUNT(*) FILTER (
        WHERE seller_performance_band = 'Elite Seller'
    )                                                           AS elite_sellers,

    COUNT(*) FILTER (
        WHERE seller_performance_band = 'Top Seller'
    )                                                           AS top_sellers,

    COUNT(*) FILTER (
        WHERE seller_performance_band = 'High Performer'
    )                                                           AS high_performers,

    COUNT(*) FILTER (
        WHERE seller_performance_band = 'Standard Seller'
    )                                                           AS standard_sellers,

    ---------------------------------------------------------------------------
    -- Seller Lifecycle
    ---------------------------------------------------------------------------
    MIN(first_sale_date)                                        AS earliest_sale_date,

    MAX(last_sale_date)                                         AS latest_sale_date,

    ---------------------------------------------------------------------------
    -- Productivity
    ---------------------------------------------------------------------------
    ROUND(
        SUM(total_net_revenue)
        /
        NULLIF(COUNT(*), 0),
        2
    )                                                           AS revenue_per_seller,

    ---------------------------------------------------------------------------
    -- Metadata
    ---------------------------------------------------------------------------
    CURRENT_TIMESTAMP                                           AS snapshot_timestamp,

    '1.0.0'::TEXT                                               AS metrics_version

FROM seller_sales;