/*
=============================================================
Enterprise Revenue Intelligence Platform
Analytics Semantic Layer

File:
    vw_sales.sql

Purpose
-------
Create the master sales semantic view used by
Power BI and downstream analytical views.

Business Grain
--------------
One Row = One Order Item

Design Principles
-----------------
• Preserve the grain of fact_sales
• Expose business-friendly attributes
• Centralize row-level business metrics
• No aggregations
• No SELECT *
• Analytics schema only (no staging tables)

Source Tables
-------------
analytics.fact_sales
analytics.dim_customer
analytics.dim_product
analytics.dim_seller
analytics.dim_date

=============================================================
*/

CREATE OR REPLACE VIEW analytics.vw_sales AS

SELECT

    /*======================================================
      ORDER INFORMATION
    ======================================================*/

    fs.order_id,
    fs.order_item_id,
    fs.order_purchase_timestamp,
    fs.date,

    /*======================================================
      CUSTOMER
    ======================================================*/

    fs.customer_id,
    dc.customer_city,
    dc.customer_state,

    /*======================================================
      PRODUCT
    ======================================================*/

    fs.product_id,
    dp.product_category,

    /*======================================================
      SELLER
    ======================================================*/

    fs.seller_id,
    ds.seller_city,
    ds.seller_state,

    /*======================================================
      CALENDAR
    ======================================================*/

    dd.year,
    dd.quarter,
    dd.month_number,
    dd.month_name,
    dd.week,
    dd.day,
    dd.day_name,
    dd.day_of_week,
    dd.is_weekend,

    /*======================================================
      BASE FACTS
    ======================================================*/

    fs.price,
    fs.freight_value,

    /*======================================================
      BUSINESS METRICS
    ======================================================*/

    (fs.price + fs.freight_value) AS total_revenue,

    1 AS sales_line_count

FROM analytics.fact_sales AS fs

INNER JOIN analytics.dim_customer AS dc
    ON fs.customer_id = dc.customer_id

INNER JOIN analytics.dim_product AS dp
    ON fs.product_id = dp.product_id

INNER JOIN analytics.dim_seller AS ds
    ON fs.seller_id = ds.seller_id

INNER JOIN analytics.dim_date AS dd
    ON fs.date = dd.date;