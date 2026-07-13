/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : executive_kpis.sql
Schema      : analytics
Object      : analytics.executive_kpis
Purpose     : Enterprise Executive KPI Snapshot
Author      : ERIP
Version     : 1.0.0

Description
-----------
Enterprise one-row KPI snapshot for Executive Dashboards.

Grain
-----
One Row = Enterprise Snapshot

Dependencies
------------
analytics.vw_sales

Consumers
---------
• Executive Dashboard
• Power BI KPI Cards
• Executive Reporting
• Management Scorecards

Notes
-----
- Built exclusively from analytics.vw_sales
- Contains current enterprise-wide KPIs
- Designed for KPI cards and executive summaries

===============================================================================
*/

CREATE OR REPLACE VIEW analytics.executive_kpis AS

WITH base_sales AS (

    SELECT
        order_id,
        customer_id,
        product_id,
        seller_id,
        product_category_name,
        quantity,
        item_price,
        freight_value,
        gross_sales_amount,
        total_net_revenue,
        total_order_value,
        payment_value,
        freight_percentage
    FROM analytics.vw_sales

),

revenue_metrics AS (

    SELECT

        COALESCE(SUM(total_net_revenue), 0)::NUMERIC(18,2)
            AS total_net_revenue,

        COALESCE(SUM(gross_sales_amount), 0)::NUMERIC(18,2)
            AS total_gross_revenue,

        COALESCE(SUM(item_price), 0)::NUMERIC(18,2)
            AS total_merchandise_sales,

        COALESCE(SUM(freight_value), 0)::NUMERIC(18,2)
            AS total_freight_revenue

    FROM base_sales

),

order_metrics AS (

    SELECT

        COUNT(DISTINCT order_id)
            AS total_orders,

        COUNT(*)
            AS total_order_items,

        COALESCE(SUM(quantity), 0)
            AS total_quantity_sold

    FROM base_sales

),

customer_metrics AS (

    SELECT

        COUNT(DISTINCT customer_id)
            AS active_customers

    FROM base_sales

),

product_metrics AS (

    SELECT

        COUNT(DISTINCT product_id)
            AS active_products,

        COUNT(DISTINCT product_category_name)
            AS product_categories

    FROM base_sales

),

seller_metrics AS (

    SELECT

        COUNT(DISTINCT seller_id)
            AS active_sellers

    FROM base_sales

),

financial_metrics AS (

    SELECT

        COALESCE(AVG(total_order_value), 0)::NUMERIC(18,2)
            AS average_order_value,

        COALESCE(AVG(item_price), 0)::NUMERIC(18,2)
            AS average_item_price,

        COALESCE(AVG(payment_value), 0)::NUMERIC(18,2)
            AS average_payment_value,

        COALESCE(AVG(freight_percentage), 0)::NUMERIC(18,2)
            AS average_freight_percentage

    FROM base_sales

)

SELECT

    ---------------------------------------------------------------------------
    -- Revenue
    ---------------------------------------------------------------------------

    r.total_net_revenue,
    r.total_gross_revenue,
    r.total_merchandise_sales,
    r.total_freight_revenue,

    ---------------------------------------------------------------------------
    -- Orders
    ---------------------------------------------------------------------------

    o.total_orders,
    o.total_order_items,
    o.total_quantity_sold,

    ---------------------------------------------------------------------------
    -- Customers
    ---------------------------------------------------------------------------

    c.active_customers,

    ---------------------------------------------------------------------------
    -- Products
    ---------------------------------------------------------------------------

    p.active_products,
    p.product_categories,

    ---------------------------------------------------------------------------
    -- Sellers
    ---------------------------------------------------------------------------

    s.active_sellers,

    ---------------------------------------------------------------------------
    -- Financial
    ---------------------------------------------------------------------------

    f.average_order_value,
    f.average_item_price,
    f.average_payment_value,
    f.average_freight_percentage,

    ---------------------------------------------------------------------------
    -- Productivity
    ---------------------------------------------------------------------------

    ROUND(
        r.total_net_revenue
        / NULLIF(c.active_customers, 0),
        2
    ) AS revenue_per_customer,

    ROUND(
        r.total_net_revenue
        / NULLIF(p.active_products, 0),
        2
    ) AS revenue_per_product,

    ROUND(
        r.total_net_revenue
        / NULLIF(s.active_sellers, 0),
        2
    ) AS revenue_per_seller,

    ---------------------------------------------------------------------------
    -- Metadata
    ---------------------------------------------------------------------------

    CURRENT_TIMESTAMP AS snapshot_timestamp,

    '1.0.0'::TEXT AS metrics_version

FROM revenue_metrics r
CROSS JOIN order_metrics o
CROSS JOIN customer_metrics c
CROSS JOIN product_metrics p
CROSS JOIN seller_metrics s
CROSS JOIN financial_metrics f;