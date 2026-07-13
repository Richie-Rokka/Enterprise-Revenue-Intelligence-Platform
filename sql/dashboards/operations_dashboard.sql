/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : operations_dashboard.sql
Schema      : analytics
Object      : analytics.operations_dashboard
Type        : Dashboard View

Business Grain
--------------
One row summarizing enterprise operational performance.

Purpose
-------
Provides the enterprise Operations Dashboard dataset by consolidating
delivery, logistics, payment and customer review KPIs.

Dependencies
------------
- analytics.delivery_kpis
- analytics.logistics_kpis
- analytics.payment_kpis
- analytics.review_kpis

Consumers
---------
- Power BI Operations Dashboard
- Executive Dashboard
- Operations Reporting

Notes
-----
- Built exclusively from validated Operations KPI views.
- No direct dependency on semantic or staging tables.
- Explicit projection only.
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.operations_dashboard AS

SELECT

    ----------------------------------------------------------------------------
    -- Delivery KPIs
    ----------------------------------------------------------------------------
    d.total_orders,
    d.delivered_orders,
    d.undelivered_orders,

    d.on_time_deliveries,
    d.late_deliveries,

    d.on_time_delivery_rate_pct,
    d.late_delivery_rate_pct,

    d.avg_delivery_days,
    d.fastest_delivery_days,
    d.slowest_delivery_days,

    d.avg_delivery_delay_days,
    d.max_delivery_delay_days,

    d.avg_order_approval_days,
    d.avg_carrier_pickup_days,

    d.avg_delivery_variance_days,
    d.avg_absolute_delivery_variance_days,

    ----------------------------------------------------------------------------
    -- Logistics KPIs
    ----------------------------------------------------------------------------
    l.total_order_items,
    l.active_sellers,
    l.active_products,

    l.avg_transit_days,
    l.avg_fulfillment_cycle_days,

    l.total_freight_cost,
    l.avg_freight_cost,

    l.total_product_value,
    l.avg_product_value,

    ----------------------------------------------------------------------------
    -- Payment KPIs
    ----------------------------------------------------------------------------
    p.total_payments,
    p.total_payment_value,
    p.average_payment_value,

    p.average_installments,

    p.credit_card_payments,
    p.debit_card_payments,
    p.boleto_payments,
    p.voucher_payments,

    p.credit_card_pct,
    p.debit_card_pct,
    p.boleto_pct,
    p.voucher_pct,

    ----------------------------------------------------------------------------
    -- Review KPIs
    ----------------------------------------------------------------------------
    r.total_reviews,
    r.average_review_score,

    r.positive_reviews,
    r.neutral_reviews,
    r.negative_reviews,

    r.positive_review_rate_pct,
    r.negative_review_rate_pct,

    r.average_review_response_days,
    r.average_days_to_review,

    r.review_comment_rate_pct,
    r.review_response_rate_pct

FROM analytics.delivery_kpis d

CROSS JOIN analytics.logistics_kpis l

CROSS JOIN analytics.payment_kpis p

CROSS JOIN analytics.review_kpis r;