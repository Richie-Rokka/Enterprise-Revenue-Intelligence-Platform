/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : payment_kpis.sql
Schema      : analytics
Object      : payment_kpis
Type        : Operations Metrics View

Business Grain
--------------
One row summarizing enterprise payment performance.

Purpose
-------
Provides enterprise payment KPIs covering payment volume, value,
payment methods, installments, and payment behavior.

Dependencies
------------
- staging.sales_order_payment

Consumers
---------
- Operations Dashboard
- Executive Dashboard
- Power BI Operations Dashboard

Notes
-----
- Payment metrics are sourced directly from the operational staging layer
  because no payment semantic view currently exists.
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.payment_kpis AS

SELECT

    ---------------------------------------------------------------------------
    -- Payment Volume
    ---------------------------------------------------------------------------
    COUNT(*)                                                    AS total_payments,

    COUNT(DISTINCT order_id)                                    AS total_orders,

    ---------------------------------------------------------------------------
    -- Payment Value
    ---------------------------------------------------------------------------
    ROUND(
        SUM(payment_value),
        2
    )                                                           AS total_payment_value,

    ROUND(
        AVG(payment_value),
        2
    )                                                           AS average_payment_value,

    ROUND(
        MIN(payment_value),
        2
    )                                                           AS minimum_payment_value,

    ROUND(
        MAX(payment_value),
        2
    )                                                           AS maximum_payment_value,

    ---------------------------------------------------------------------------
    -- Installments
    ---------------------------------------------------------------------------
    ROUND(
        AVG(payment_installments),
        2
    )                                                           AS average_installments,

    MAX(payment_installments)                                   AS maximum_installments,

    ---------------------------------------------------------------------------
    -- Payment Methods
    ---------------------------------------------------------------------------
    COUNT(*) FILTER (
        WHERE payment_type = 'credit_card'
    )                                                           AS credit_card_payments,

    COUNT(*) FILTER (
        WHERE payment_type = 'boleto'
    )                                                           AS boleto_payments,

    COUNT(*) FILTER (
        WHERE payment_type = 'voucher'
    )                                                           AS voucher_payments,

    COUNT(*) FILTER (
        WHERE payment_type = 'debit_card'
    )                                                           AS debit_card_payments,

    COUNT(*) FILTER (
        WHERE payment_type NOT IN
        (
            'credit_card',
            'boleto',
            'voucher',
            'debit_card'
        )
    )                                                           AS other_payment_methods,

    ---------------------------------------------------------------------------
    -- Payment Method Distribution
    ---------------------------------------------------------------------------
    ROUND(
        100.0 *
        COUNT(*) FILTER (WHERE payment_type = 'credit_card')
        /
        NULLIF(COUNT(*),0),
        2
    )                                                           AS credit_card_pct,

    ROUND(
        100.0 *
        COUNT(*) FILTER (WHERE payment_type = 'boleto')
        /
        NULLIF(COUNT(*),0),
        2
    )                                                           AS boleto_pct,

    ROUND(
        100.0 *
        COUNT(*) FILTER (WHERE payment_type = 'voucher')
        /
        NULLIF(COUNT(*),0),
        2
    )                                                           AS voucher_pct,

    ROUND(
        100.0 *
        COUNT(*) FILTER (WHERE payment_type = 'debit_card')
        /
        NULLIF(COUNT(*),0),
        2
    )                                                           AS debit_card_pct

FROM staging.sales_order_payment;