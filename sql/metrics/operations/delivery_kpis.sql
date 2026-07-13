/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : delivery_kpis.sql
Schema      : analytics
Object      : delivery_kpis
Type        : Operations Metrics View

Business Grain
--------------
One row summarizing enterprise delivery performance.

Purpose
-------
Provides enterprise delivery KPIs for operational reporting and executive
monitoring.

Dependencies
------------
- analytics.vw_delivery_performance

Consumers
---------
- Operations Dashboard
- Executive Dashboard
- Power BI Operations Dashboard

===============================================================================
*/

CREATE OR REPLACE VIEW analytics.delivery_kpis AS

SELECT

    ---------------------------------------------------------------------------
    -- Delivery Volume
    ---------------------------------------------------------------------------
    COUNT(*)                                                   AS total_orders,

    COUNT(*) FILTER (
        WHERE is_delivered
    )                                                          AS delivered_orders,

    COUNT(*) FILTER (
        WHERE NOT is_delivered
    )                                                          AS undelivered_orders,

    ---------------------------------------------------------------------------
    -- On-Time Performance
    ---------------------------------------------------------------------------
    COUNT(*) FILTER (
        WHERE delivered_on_time
    )                                                          AS on_time_deliveries,

    COUNT(*) FILTER (
        WHERE delivered_late
    )                                                          AS late_deliveries,

    ROUND(
        100.0 *
        COUNT(*) FILTER (WHERE delivered_on_time)
        /
        NULLIF(
            COUNT(*) FILTER (WHERE is_delivered),
            0
        ),
        2
    )                                                          AS on_time_delivery_rate_pct,

    ROUND(
        100.0 *
        COUNT(*) FILTER (WHERE delivered_late)
        /
        NULLIF(
            COUNT(*) FILTER (WHERE is_delivered),
            0
        ),
        2
    )                                                          AS late_delivery_rate_pct,

    ---------------------------------------------------------------------------
    -- Delivery Performance
    ---------------------------------------------------------------------------
    ROUND(
        AVG(delivery_duration_days),
        2
    )                                                          AS avg_delivery_days,

    ROUND(
        MIN(delivery_duration_days),
        2
    )                                                          AS fastest_delivery_days,

    ROUND(
        MAX(delivery_duration_days),
        2
    )                                                          AS slowest_delivery_days,

    ROUND(
        AVG(delivery_delay_days),
        2
    )                                                          AS avg_delivery_delay_days,

    ROUND(
        MAX(delivery_delay_days),
        2
    )                                                          AS max_delivery_delay_days,

    ---------------------------------------------------------------------------
    -- Approval Performance
    ---------------------------------------------------------------------------
    ROUND(
        AVG(approval_duration_days),
        2
    )                                                          AS avg_order_approval_days,

    ---------------------------------------------------------------------------
    -- Carrier Performance
    ---------------------------------------------------------------------------
    ROUND(
        AVG(carrier_pickup_duration_days),
        2
    )                                                          AS avg_carrier_pickup_days,

    ---------------------------------------------------------------------------
    -- Estimated Delivery Accuracy
    ---------------------------------------------------------------------------
    ROUND(
        AVG(estimated_delivery_variance_days),
        2
    )                                                          AS avg_delivery_variance_days,

    ROUND(
        AVG(
            ABS(estimated_delivery_variance_days)
        ),
        2
    )                                                          AS avg_absolute_delivery_variance_days

FROM analytics.vw_delivery_performance;