/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : product_kpis.sql
Schema      : analytics
Object      : analytics.product_kpis
Type        : Product Metrics View

Business Grain
--------------
One row summarizing enterprise product performance.

Purpose
-------
Provides enterprise product KPIs covering product portfolio, sales,
revenue, customer reach, seller reach and product performance.

Dependencies
------------
- analytics.vw_product_performance

Consumers
---------
- Product Dashboard
- Executive Dashboard
- Power BI Product Dashboard

Notes
-----
- Built exclusively from analytics.vw_product_performance
- Explicit projection only
- No SELECT *
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.product_kpis AS

WITH product_sales AS
(
    SELECT

        product_id,
        product_category_name,
        product_category_english,
        product_size_class,
        product_weight_class,

        total_orders,
        total_order_items,
        total_quantity_sold,

        gross_product_sales,
        total_sales,
        total_net_revenue,

        average_unit_price,
        average_order_value,

        total_freight,
        average_freight_percentage,

        unique_customers,
        unique_sellers,

        first_sale_date,
        last_sale_date,

        product_performance_band

    FROM analytics.vw_product_performance
)

SELECT

    ---------------------------------------------------------------------------
    -- Product Portfolio
    ---------------------------------------------------------------------------
    COUNT(*)                                                    AS total_products,

    COUNT(DISTINCT product_category_name)                       AS total_categories,

    COUNT(DISTINCT product_size_class)                          AS size_classes,

    COUNT(DISTINCT product_weight_class)                        AS weight_classes,

    ---------------------------------------------------------------------------
    -- Revenue
    ---------------------------------------------------------------------------
    ROUND(
        SUM(gross_product_sales),
        2
    )                                                           AS gross_product_sales,

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
    )                                                           AS average_product_revenue,

    ROUND(
        MAX(total_net_revenue),
        2
    )                                                           AS highest_product_revenue,

    ---------------------------------------------------------------------------
    -- Sales Activity
    ---------------------------------------------------------------------------
    SUM(total_orders)                                           AS total_orders,

    SUM(total_order_items)                                      AS total_order_items,

    SUM(total_quantity_sold)                                    AS total_quantity_sold,

    ROUND(
        AVG(total_orders),
        2
    )                                                           AS average_orders_per_product,

    ROUND(
        AVG(total_quantity_sold),
        2
    )                                                           AS average_quantity_per_product,

    ---------------------------------------------------------------------------
    -- Pricing
    ---------------------------------------------------------------------------
    ROUND(
        AVG(average_unit_price),
        2
    )                                                           AS average_unit_price,

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
    -- Market Reach
    ---------------------------------------------------------------------------
    ROUND(
        AVG(unique_customers),
        2
    )                                                           AS average_customers_per_product,

    ROUND(
        AVG(unique_sellers),
        2
    )                                                           AS average_sellers_per_product,

    ---------------------------------------------------------------------------
    -- Performance Bands
    ---------------------------------------------------------------------------
    COUNT(*) FILTER (
        WHERE product_performance_band = 'Top Performer'
    )                                                           AS top_performers,

    COUNT(*) FILTER (
        WHERE product_performance_band = 'High Performer'
    )                                                           AS high_performers,

    COUNT(*) FILTER (
        WHERE product_performance_band = 'Medium Performer'
    )                                                           AS medium_performers,

    COUNT(*) FILTER (
        WHERE product_performance_band = 'Low Performer'
    )                                                           AS low_performers,

    ---------------------------------------------------------------------------
    -- Product Lifecycle
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
    )                                                           AS revenue_per_product,

    ---------------------------------------------------------------------------
    -- Metadata
    ---------------------------------------------------------------------------
    CURRENT_TIMESTAMP                                           AS snapshot_timestamp,

    '1.0.0'::TEXT                                               AS metrics_version

FROM product_sales;