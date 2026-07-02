/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

View        : analytics.vw_product_performance
Purpose     : Product Performance Analytics
Author      : ERIP
Version     : 2.2.0

Description
-----------
Provides product-level sales, revenue and performance metrics.

Grain
-----
One Row = One Product

Depends On
----------
analytics.vw_sales
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.vw_product_performance AS

SELECT

    ----------------------------------------------------------------------------
    -- Product
    ----------------------------------------------------------------------------

    product_id,

    product_category_name,

    product_category_english,

    product_size_class,

    product_weight_class,

    ----------------------------------------------------------------------------
    -- Sales Activity
    ----------------------------------------------------------------------------

    COUNT(DISTINCT order_id)              AS total_orders,

    COUNT(DISTINCT sales_sk)              AS total_order_items,

    SUM(quantity)                         AS total_quantity_sold,

    ----------------------------------------------------------------------------
    -- Revenue
    ----------------------------------------------------------------------------

    SUM(item_price)                       AS gross_product_sales,

    SUM(total_order_value)                AS total_sales,

    SUM(total_net_revenue)                AS total_net_revenue,

    AVG(item_price)                       AS average_unit_price,

    AVG(total_order_value)                AS average_order_value,

    ----------------------------------------------------------------------------
    -- Freight
    ----------------------------------------------------------------------------

    SUM(freight_value)                    AS total_freight,

    AVG(freight_percentage)               AS average_freight_percentage,

    ----------------------------------------------------------------------------
    -- Customer Reach
    ----------------------------------------------------------------------------

    COUNT(DISTINCT customer_id)           AS unique_customers,

    COUNT(DISTINCT seller_id)             AS unique_sellers,

    ----------------------------------------------------------------------------
    -- Product Lifecycle
    ----------------------------------------------------------------------------

    MIN(calendar_date)                    AS first_sale_date,

    MAX(calendar_date)                    AS last_sale_date,

    ----------------------------------------------------------------------------
    -- Performance Classification
    ----------------------------------------------------------------------------

    CASE

        WHEN SUM(total_net_revenue) >= 100000
            THEN 'Top Performer'

        WHEN SUM(total_net_revenue) >= 50000
            THEN 'High Performer'

        WHEN SUM(total_net_revenue) >= 10000
            THEN 'Medium Performer'

        ELSE 'Low Performer'

    END                                   AS product_performance_band

FROM analytics.vw_sales

GROUP BY

    product_id,

    product_category_name,

    product_category_english,

    product_size_class,

    product_weight_class;