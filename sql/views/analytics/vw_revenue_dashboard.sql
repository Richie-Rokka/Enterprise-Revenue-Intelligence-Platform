/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

View        : analytics.vw_revenue_dashboard
Purpose     : Executive Revenue Dashboard
Author      : ERIP
Version     : 2.2.0

Description
-----------
Enterprise executive dashboard providing revenue KPIs by calendar period.

Grain
-----
One Row = Calendar Month

Depends On
----------
analytics.vw_sales

Consumers
---------
• Power BI Executive Dashboard
• Revenue Operations
• Finance
• Commercial Leadership
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.vw_revenue_dashboard AS

SELECT

    ----------------------------------------------------------------------------
    -- Calendar
    ----------------------------------------------------------------------------

    year_number,

    quarter_number,

    quarter_name,

    month_number,

    month_name,

    year_month,

    ----------------------------------------------------------------------------
    -- Revenue KPIs
    ----------------------------------------------------------------------------

    SUM(total_net_revenue) AS net_revenue,

    SUM(total_order_value) AS gross_revenue,

    SUM(item_price) AS merchandise_sales,

    SUM(freight_value) AS freight_revenue,

    ----------------------------------------------------------------------------
    -- Volume KPIs
    ----------------------------------------------------------------------------

    COUNT(DISTINCT order_id)               AS total_orders,

    COUNT(DISTINCT sales_sk)               AS total_order_items,

    SUM(quantity)                          AS total_quantity,

    ----------------------------------------------------------------------------
    -- Customer KPIs
    ----------------------------------------------------------------------------

    COUNT(DISTINCT customer_id)            AS total_customers,

    ----------------------------------------------------------------------------
    -- Product KPIs
    ----------------------------------------------------------------------------

    COUNT(DISTINCT product_id)             AS total_products,

    COUNT(DISTINCT product_category_name)  AS total_categories,

    ----------------------------------------------------------------------------
    -- Seller KPIs
    ----------------------------------------------------------------------------

    COUNT(DISTINCT seller_id)              AS total_sellers,

    ----------------------------------------------------------------------------
    -- Average KPIs
    ----------------------------------------------------------------------------

    AVG(total_order_value)                 AS average_order_value,

    AVG(total_net_revenue)                 AS average_order_item_revenue,

    ----------------------------------------------------------------------------
    -- Productivity KPIs
    ----------------------------------------------------------------------------

    SUM(total_net_revenue)
        / NULLIF(COUNT(DISTINCT customer_id),0)
        AS revenue_per_customer,

    SUM(total_net_revenue)
        / NULLIF(COUNT(DISTINCT seller_id),0)
        AS revenue_per_seller,

    SUM(total_net_revenue)
        / NULLIF(COUNT(DISTINCT product_id),0)
        AS revenue_per_product,

    ----------------------------------------------------------------------------
    -- Operational KPIs
    ----------------------------------------------------------------------------

    AVG(freight_percentage)                AS average_freight_percentage,

    ----------------------------------------------------------------------------
    -- Audit
    ----------------------------------------------------------------------------

    CURRENT_TIMESTAMP                      AS semantic_created_timestamp

FROM analytics.vw_sales

GROUP BY

    year_number,

    quarter_number,

    quarter_name,

    month_number,

    month_name,

    year_month

ORDER BY

    year_number,

    month_number;