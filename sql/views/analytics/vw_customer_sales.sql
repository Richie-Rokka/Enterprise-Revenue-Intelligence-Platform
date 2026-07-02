/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

View        : analytics.vw_customer_sales
Purpose     : Customer Revenue & Sales Analytics
Author      : ERIP
Version     : 2.2.0

Description
-----------
Provides customer-level sales performance metrics for reporting,
segmentation and customer analytics.

Grain
-----
One Row = One Customer

Depends On
----------
analytics.vw_sales
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.vw_customer_sales AS

SELECT

    ----------------------------------------------------------------------------
    -- Customer
    ----------------------------------------------------------------------------

    customer_id,

    customer_city,

    customer_state,

    customer_region,

    customer_country,

    ----------------------------------------------------------------------------
    -- Customer Activity
    ----------------------------------------------------------------------------

    COUNT(DISTINCT order_id)          AS total_orders,

    COUNT(DISTINCT sales_sk)          AS total_order_items,

    ----------------------------------------------------------------------------
    -- Revenue
    ----------------------------------------------------------------------------

    SUM(quantity)                     AS total_quantity,

    SUM(item_price)                   AS total_item_sales,

    SUM(freight_value)                AS total_freight,

    SUM(total_order_value)            AS total_sales,

    SUM(total_net_revenue)            AS total_net_revenue,

    AVG(total_order_value)            AS average_order_value,

    ----------------------------------------------------------------------------
    -- Product Diversity
    ----------------------------------------------------------------------------

    COUNT(DISTINCT product_id)        AS unique_products,

    COUNT(DISTINCT product_category_name)
                                      AS unique_categories,

    ----------------------------------------------------------------------------
    -- Seller Reach
    ----------------------------------------------------------------------------

    COUNT(DISTINCT seller_id)         AS unique_sellers,

    ----------------------------------------------------------------------------
    -- Time Intelligence
    ----------------------------------------------------------------------------

    MIN(calendar_date)                AS first_purchase_date,

    MAX(calendar_date)                AS last_purchase_date,

    ----------------------------------------------------------------------------
    -- Customer Classification
    ----------------------------------------------------------------------------

    CASE

        WHEN SUM(total_net_revenue) >= 10000
            THEN 'VIP'

        WHEN SUM(total_net_revenue) >= 5000
            THEN 'High Value'

        WHEN SUM(total_net_revenue) >= 1000
            THEN 'Medium Value'

        ELSE 'Standard'

    END                               AS customer_segment

FROM analytics.vw_sales

GROUP BY

    customer_id,

    customer_city,

    customer_state,

    customer_region,

    customer_country;