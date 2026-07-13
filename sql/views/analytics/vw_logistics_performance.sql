/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : vw_logistics_performance.sql
Schema      : analytics
Object      : vw_logistics_performance
Type        : Operational Semantic View

Business Grain
--------------
One row per sales order item.

Purpose
-------
Provides the enterprise semantic layer for logistics and fulfillment
performance, exposing seller fulfillment, freight, shipping and delivery
metrics at the order-item level.

Dependencies
------------
- staging.sales_order
- staging.sales_order_item

Consumers
---------
- sql/metrics/operations/logistics_kpis.sql
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

CREATE OR REPLACE VIEW analytics.vw_logistics_performance AS

WITH logistics_base AS
(
    SELECT

        -----------------------------------------------------------------------
        -- Business Keys
        -----------------------------------------------------------------------
        soi.order_id,
        soi.order_item_id,
        soi.product_id,
        soi.seller_id,
        so.customer_id,

        -----------------------------------------------------------------------
        -- Order Status
        -----------------------------------------------------------------------
        so.order_status,

        -----------------------------------------------------------------------
        -- Lifecycle Dates
        -----------------------------------------------------------------------
        so.order_purchase_timestamp,
        so.order_approved_at,
        soi.shipping_limit_date,
        so.order_delivered_carrier_date,
        so.order_delivered_customer_date,
        so.order_estimated_delivery_date,

        -----------------------------------------------------------------------
        -- Commercial Values
        -----------------------------------------------------------------------
        soi.price,
        soi.freight_value

    FROM staging.sales_order_item AS soi

    INNER JOIN staging.sales_order AS so
        ON soi.order_id = so.order_id
),

logistics_metrics AS
(
    SELECT

        -----------------------------------------------------------------------
        -- Business Keys
        -----------------------------------------------------------------------
        lb.order_id,
        lb.order_item_id,
        lb.customer_id,
        lb.product_id,
        lb.seller_id,

        -----------------------------------------------------------------------
        -- Order Information
        -----------------------------------------------------------------------
        lb.order_status,

        -----------------------------------------------------------------------
        -- Timeline
        -----------------------------------------------------------------------
        lb.order_purchase_timestamp,
        lb.order_approved_at,
        lb.shipping_limit_date,
        lb.order_delivered_carrier_date,
        lb.order_delivered_customer_date,
        lb.order_estimated_delivery_date,

        -----------------------------------------------------------------------
        -- Commercial Values
        -----------------------------------------------------------------------
        lb.price,
        lb.freight_value,

        -----------------------------------------------------------------------
        -- Operational Metrics
        -----------------------------------------------------------------------
        CASE
            WHEN lb.order_approved_at IS NOT NULL
             AND lb.order_purchase_timestamp IS NOT NULL
            THEN ROUND(
                EXTRACT(
                    EPOCH FROM
                    (
                        lb.order_approved_at
                        - lb.order_purchase_timestamp
                    )
                ) / 86400.0,
                2
            )
        END AS approval_duration_days,

        CASE
            WHEN lb.order_delivered_carrier_date IS NOT NULL
             AND lb.order_approved_at IS NOT NULL
            THEN ROUND(
                EXTRACT(
                    EPOCH FROM
                    (
                        lb.order_delivered_carrier_date
                        - lb.order_approved_at
                    )
                ) / 86400.0,
                2
            )
        END AS carrier_pickup_duration_days,

        CASE
            WHEN lb.order_delivered_customer_date IS NOT NULL
             AND lb.order_delivered_carrier_date IS NOT NULL
            THEN ROUND(
                EXTRACT(
                    EPOCH FROM
                    (
                        lb.order_delivered_customer_date
                        - lb.order_delivered_carrier_date
                    )
                ) / 86400.0,
                2
            )
        END AS transit_duration_days,

        CASE
            WHEN lb.order_delivered_customer_date IS NOT NULL
             AND lb.order_purchase_timestamp IS NOT NULL
            THEN ROUND(
                EXTRACT(
                    EPOCH FROM
                    (
                        lb.order_delivered_customer_date
                        - lb.order_purchase_timestamp
                    )
                ) / 86400.0,
                2
            )
        END AS fulfillment_cycle_days,

        CASE
            WHEN lb.order_delivered_customer_date IS NOT NULL
             AND lb.order_estimated_delivery_date IS NOT NULL
            THEN ROUND(
                EXTRACT(
                    EPOCH FROM
                    (
                        lb.order_delivered_customer_date
                        - lb.order_estimated_delivery_date
                    )
                ) / 86400.0,
                2
            )
        END AS delivery_variance_days

    FROM logistics_base AS lb
)

SELECT

    ---------------------------------------------------------------------------
    -- Business Keys
    ---------------------------------------------------------------------------
    order_id,
    order_item_id,
    customer_id,
    product_id,
    seller_id,

    ---------------------------------------------------------------------------
    -- Order Information
    ---------------------------------------------------------------------------
    order_status,

    ---------------------------------------------------------------------------
    -- Timeline
    ---------------------------------------------------------------------------
    order_purchase_timestamp,
    order_approved_at,
    shipping_limit_date,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date,

    ---------------------------------------------------------------------------
    -- Commercial Values
    ---------------------------------------------------------------------------
    price,
    freight_value,

    ---------------------------------------------------------------------------
    -- Operational Metrics
    ---------------------------------------------------------------------------
    approval_duration_days,
    carrier_pickup_duration_days,
    transit_duration_days,
    fulfillment_cycle_days,
    delivery_variance_days,

    CASE
        WHEN delivery_variance_days > 0
        THEN delivery_variance_days
        ELSE 0
    END AS delivery_delay_days,

    ---------------------------------------------------------------------------
    -- Operational Flags
    ---------------------------------------------------------------------------
    CASE
        WHEN order_delivered_customer_date IS NOT NULL
        THEN TRUE
        ELSE FALSE
    END AS delivered_flag,

    CASE
        WHEN delivery_variance_days <= 0
         AND order_delivered_customer_date IS NOT NULL
        THEN TRUE
        ELSE FALSE
    END AS on_time_delivery_flag,

    CASE
        WHEN delivery_variance_days > 0
        THEN TRUE
        ELSE FALSE
    END AS delayed_delivery_flag

FROM logistics_metrics;