/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : vw_delivery_performance.sql
Schema      : analytics
Object      : vw_delivery_performance
Type        : Operational Semantic View

Business Grain
--------------
One row per sales order.

Purpose
-------
Provides the enterprise semantic layer for delivery lifecycle analytics,
including order approval, carrier pickup, delivery performance,
delivery variance, and on-time delivery metrics.

Dependencies
------------
- staging.sales_order

Consumers
---------
- sql/metrics/operations/delivery_kpis.sql
- sql/dashboards/operations_dashboard.sql
- Power BI Operations Dashboard

Notes
-----
- Operational semantic view.
- Does NOT depend on analytics.fact_sales.
- Explicit projection only.
- No SELECT *.
===============================================================================
*/

CREATE OR REPLACE VIEW analytics.vw_delivery_performance AS

WITH delivery_base AS
(
    SELECT

        -----------------------------------------------------------------------
        -- Business Keys
        -----------------------------------------------------------------------
        so.order_id,
        so.customer_id,

        -----------------------------------------------------------------------
        -- Order Status
        -----------------------------------------------------------------------
        so.order_status,

        -----------------------------------------------------------------------
        -- Lifecycle Timestamps
        -----------------------------------------------------------------------
        so.order_purchase_timestamp,
        so.order_approved_at,
        so.order_delivered_carrier_date,
        so.order_delivered_customer_date,
        so.order_estimated_delivery_date

    FROM staging.sales_order AS so
),

delivery_metrics AS
(
    SELECT

        -----------------------------------------------------------------------
        -- Business Keys
        -----------------------------------------------------------------------
        db.order_id,
        db.customer_id,

        -----------------------------------------------------------------------
        -- Status
        -----------------------------------------------------------------------
        db.order_status,

        -----------------------------------------------------------------------
        -- Lifecycle Dates
        -----------------------------------------------------------------------
        db.order_purchase_timestamp,
        db.order_approved_at,
        db.order_delivered_carrier_date,
        db.order_delivered_customer_date,
        db.order_estimated_delivery_date,

        -----------------------------------------------------------------------
        -- Operational Durations
        -----------------------------------------------------------------------
        CASE
            WHEN db.order_approved_at IS NOT NULL
            THEN ROUND(
                EXTRACT(EPOCH FROM
                    (db.order_approved_at - db.order_purchase_timestamp)
                ) / 86400.0,
                2
            )
        END AS approval_duration_days,

        CASE
            WHEN db.order_delivered_carrier_date IS NOT NULL
             AND db.order_approved_at IS NOT NULL
            THEN ROUND(
                EXTRACT(EPOCH FROM
                    (db.order_delivered_carrier_date - db.order_approved_at)
                ) / 86400.0,
                2
            )
        END AS carrier_pickup_duration_days,

        CASE
            WHEN db.order_delivered_customer_date IS NOT NULL
            THEN ROUND(
                EXTRACT(EPOCH FROM
                    (db.order_delivered_customer_date - db.order_purchase_timestamp)
                ) / 86400.0,
                2
            )
        END AS delivery_duration_days,

        CASE
            WHEN db.order_delivered_customer_date IS NOT NULL
             AND db.order_estimated_delivery_date IS NOT NULL
            THEN ROUND(
                EXTRACT(EPOCH FROM
                    (
                        db.order_delivered_customer_date
                      - db.order_estimated_delivery_date
                    )
                ) / 86400.0,
                2
            )
        END AS estimated_delivery_variance_days

    FROM delivery_base AS db
)

SELECT

    ---------------------------------------------------------------------------
    -- Business Keys
    ---------------------------------------------------------------------------
    dm.order_id,
    dm.customer_id,

    ---------------------------------------------------------------------------
    -- Status
    ---------------------------------------------------------------------------
    dm.order_status,

    ---------------------------------------------------------------------------
    -- Lifecycle Dates
    ---------------------------------------------------------------------------
    dm.order_purchase_timestamp,
    dm.order_approved_at,
    dm.order_delivered_carrier_date,
    dm.order_delivered_customer_date,
    dm.order_estimated_delivery_date,

    ---------------------------------------------------------------------------
    -- Operational Metrics
    ---------------------------------------------------------------------------
    dm.approval_duration_days,
    dm.carrier_pickup_duration_days,
    dm.delivery_duration_days,
    dm.estimated_delivery_variance_days,

    CASE
        WHEN dm.estimated_delivery_variance_days > 0
        THEN dm.estimated_delivery_variance_days
        ELSE 0
    END AS delivery_delay_days,

    ---------------------------------------------------------------------------
    -- Operational Flags
    ---------------------------------------------------------------------------
    CASE
        WHEN dm.order_delivered_customer_date IS NOT NULL
        THEN TRUE
        ELSE FALSE
    END AS is_delivered,

    CASE
        WHEN dm.order_delivered_customer_date IS NOT NULL
         AND dm.estimated_delivery_variance_days <= 0
        THEN TRUE
        ELSE FALSE
    END AS delivered_on_time,

    CASE
        WHEN dm.order_delivered_customer_date IS NOT NULL
         AND dm.estimated_delivery_variance_days > 0
        THEN TRUE
        ELSE FALSE
    END AS delivered_late

FROM delivery_metrics AS dm;