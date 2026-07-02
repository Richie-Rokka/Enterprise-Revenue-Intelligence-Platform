/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

View        : analytics.vw_sales
Purpose     : Enterprise Sales Semantic View
Author      : ERIP
Version     : 2.2

Description
-----------
Business-friendly semantic layer for sales analytics.

Grain
-----
One Row = One Order Item

Consumers
---------
• Power BI
• Executive Dashboards
• Customer Analytics
• Product Performance
• Seller Performance
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.vw_sales AS

SELECT

    ---------------------------------------------------------------------------
    -- Sales Identity
    ---------------------------------------------------------------------------

    fs.sales_sk,
    fs.order_id,
    fs.order_item_id,

    ---------------------------------------------------------------------------
    -- Technical Keys
    ---------------------------------------------------------------------------

    fs.customer_sk,
    fs.product_sk,
    fs.seller_sk,
    fs.date_key,

    ---------------------------------------------------------------------------
    -- Customer
    ---------------------------------------------------------------------------

    dc.customer_id,
    dc.customer_city,
    dc.customer_state,
    dc.customer_region,
    dc.customer_country,

    ---------------------------------------------------------------------------
    -- Product
    ---------------------------------------------------------------------------

    dp.product_id,
    dp.product_category_name,
    dp.product_category_english,
    dp.product_size_class,
    dp.product_weight_class,

    ---------------------------------------------------------------------------
    -- Seller
    ---------------------------------------------------------------------------

    ds.seller_id,
    ds.seller_city,
    ds.seller_state,
    ds.seller_region,
    ds.seller_country,

    ----------------------------------------------------------------------------
    -- Calendar
    ----------------------------------------------------------------------------

    dd.calendar_date,

    dd.year_number,

    dd.quarter_number,
    dd.quarter_name,

    dd.month_number,
    dd.month_name,

    dd.year_month,
    dd.year_quarter,

    dd.week_of_year,

    dd.day_of_month,
    dd.day_name,

    dd.is_weekend,
    dd.is_business_day,
    
    ---------------------------------------------------------------------------
    -- Sales Metrics
    ---------------------------------------------------------------------------

    fs.quantity,

    fs.item_price,

    fs.freight_value,

    fs.gross_sales_amount,

    fs.net_sales_amount,

    fs.payment_value,

    fs.average_selling_price,

    fs.freight_percentage,

    ---------------------------------------------------------------------------
    -- Order
    ---------------------------------------------------------------------------

    fs.payment_type,

    fs.order_status,

    ---------------------------------------------------------------------------
    -- Business Metrics
    ---------------------------------------------------------------------------

    (
        fs.item_price
        + fs.freight_value
    ) AS total_order_value,

    (
        fs.net_sales_amount
        * fs.quantity
    ) AS total_net_revenue,

    CASE

        WHEN fs.freight_percentage >= 20

        THEN 'High Freight'

        WHEN fs.freight_percentage >= 10

        THEN 'Medium Freight'

        ELSE 'Low Freight'

    END AS freight_band,

    CASE

        WHEN fs.quantity = 1

        THEN 'Single Item'

        ELSE 'Multiple Items'

    END AS order_size,

    CURRENT_TIMESTAMP AS semantic_created_timestamp

FROM analytics.fact_sales fs

INNER JOIN analytics.dim_customer dc

    ON fs.customer_sk = dc.customer_sk

INNER JOIN analytics.dim_product dp

    ON fs.product_sk = dp.product_sk

INNER JOIN analytics.dim_seller ds

    ON fs.seller_sk = ds.seller_sk

INNER JOIN analytics.dim_date dd

    ON fs.date_key = dd.date_key;