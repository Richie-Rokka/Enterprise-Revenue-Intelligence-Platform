/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : logistics_kpis.sql
Schema      : analytics
Object      : logistics_kpis
Type        : Operations Metrics View

Business Grain
--------------
One row summarizing enterprise logistics and fulfillment performance.

Purpose
-------
Provides enterprise logistics KPIs covering fulfillment, carrier
performance, freight, transit efficiency, and delivery execution.

Dependencies
------------
- analytics.vw_logistics_performance

Consumers
---------
- Operations Dashboard
- Executive Dashboard
- Power BI Operations Dashboard

===============================================================================
*/

CREATE OR REPLACE VIEW analytics.logistics_kpis AS

SELECT

    ---------------------------------------------------------------------------
    -- Logistics Volume
    ---------------------------------------------------------------------------
    COUNT(*)                                                        AS total_order_items,

    COUNT(DISTINCT order_id)                                        AS total_orders,

    COUNT(DISTINCT seller_id)                                       AS active_sellers,

    COUNT(DISTINCT product_id)                                      AS active_products,

    ---------------------------------------------------------------------------
    -- Fulfillment Performance
    ---------------------------------------------------------------------------
    ROUND(
        AVG(approval_duration_days),
        2
    )                                                               AS avg_order_approval_days,

    ROUND(
        AVG(carrier_pickup_duration_days),
        2
    )                                                               AS avg_carrier_pickup_days,

    ROUND(
        AVG(transit_duration_days),
        2
    )                                                               AS avg_transit_days,

    ROUND(
        AVG(fulfillment_cycle_days),
        2
    )                                                               AS avg_fulfillment_cycle_days,

    ---------------------------------------------------------------------------
    -- Delivery Performance
    ---------------------------------------------------------------------------
    ROUND(
        AVG(delivery_variance_days),
        2
    )                                                               AS avg_delivery_variance_days,

    ROUND(
        AVG(delivery_delay_days),
        2
    )                                                               AS avg_delivery_delay_days,

    ROUND(
        MAX(delivery_delay_days),
        2
    )                                                               AS max_delivery_delay_days,

    ---------------------------------------------------------------------------
    -- Freight Performance
    ---------------------------------------------------------------------------
    ROUND(
        SUM(freight_value),
        2
    )                                                               AS total_freight_cost,

    ROUND(
        AVG(freight_value),
        2
    )                                                               AS avg_freight_cost,

    ROUND(
        MIN(freight_value),
        2
    )                                                               AS minimum_freight_cost,

    ROUND(
        MAX(freight_value),
        2
    )                                                               AS maximum_freight_cost,

    ---------------------------------------------------------------------------
    -- Product Value
    ---------------------------------------------------------------------------
    ROUND(
        SUM(price),
        2
    )                                                               AS total_product_value,

    ROUND(
        AVG(price),
        2
    )                                                               AS avg_product_value,

    ---------------------------------------------------------------------------
    -- Delivery Success
    ---------------------------------------------------------------------------
    COUNT(*) FILTER (
        WHERE delivered_flag
    )                                                               AS delivered_items,

    COUNT(*) FILTER (
        WHERE on_time_delivery_flag
    )                                                               AS on_time_items,

    COUNT(*) FILTER (
        WHERE delayed_delivery_flag
    )                                                               AS delayed_items,

    ROUND(
        100.0 *
        COUNT(*) FILTER (WHERE on_time_delivery_flag)
        /
        NULLIF(
            COUNT(*) FILTER (WHERE delivered_flag),
            0
        ),
        2
    )                                                               AS on_time_delivery_rate_pct,

    ROUND(
        100.0 *
        COUNT(*) FILTER (WHERE delayed_delivery_flag)
        /
        NULLIF(
            COUNT(*) FILTER (WHERE delivered_flag),
            0
        ),
        2
    )                                                               AS delayed_delivery_rate_pct

FROM analytics.vw_logistics_performance;