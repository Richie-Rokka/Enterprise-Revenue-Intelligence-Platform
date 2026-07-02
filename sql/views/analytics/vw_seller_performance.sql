/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

View        : analytics.vw_seller_performance
Purpose     : Seller Performance Analytics
Author      : ERIP
Version     : 2.2.0

Description
-----------
Provides seller-level revenue and operational performance metrics.

Grain
-----
One Row = One Seller

Depends On
----------
analytics.vw_sales
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.vw_seller_performance AS

SELECT

    ----------------------------------------------------------------------------
    -- Seller
    ----------------------------------------------------------------------------

    seller_id,

    seller_city,

    seller_state,

    seller_region,

    seller_country,

    ----------------------------------------------------------------------------
    -- Sales Activity
    ----------------------------------------------------------------------------

    COUNT(DISTINCT order_id)              AS total_orders,

    COUNT(DISTINCT sales_sk)              AS total_order_items,

    SUM(quantity)                         AS total_quantity_sold,

    ----------------------------------------------------------------------------
    -- Revenue
    ----------------------------------------------------------------------------

    SUM(item_price)                       AS gross_sales,

    SUM(total_order_value)                AS total_sales,

    SUM(total_net_revenue)                AS total_net_revenue,

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

    ----------------------------------------------------------------------------
    -- Product Portfolio
    ----------------------------------------------------------------------------

    COUNT(DISTINCT product_id)            AS unique_products,

    COUNT(DISTINCT product_category_name)
                                          AS unique_categories,

    ----------------------------------------------------------------------------
    -- Sales Timeline
    ----------------------------------------------------------------------------

    MIN(calendar_date)                    AS first_sale_date,

    MAX(calendar_date)                    AS last_sale_date,

    ----------------------------------------------------------------------------
    -- Seller Classification
    ----------------------------------------------------------------------------

    CASE

        WHEN SUM(total_net_revenue) >= 250000
            THEN 'Elite Seller'

        WHEN SUM(total_net_revenue) >= 100000
            THEN 'Top Seller'

        WHEN SUM(total_net_revenue) >= 50000
            THEN 'High Performer'

        ELSE 'Standard Seller'

    END                                   AS seller_performance_band

FROM analytics.vw_sales

GROUP BY

    seller_id,

    seller_city,

    seller_state,

    seller_region,

    seller_country;