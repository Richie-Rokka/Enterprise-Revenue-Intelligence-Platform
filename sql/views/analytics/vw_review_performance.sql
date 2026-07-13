/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : vw_review_performance.sql
Schema      : analytics
Object      : vw_review_performance
Type        : Operational Semantic View

Business Grain
--------------
One row per customer review.

Purpose
-------
Provides the enterprise semantic layer for customer review analytics,
including review scores, response times, and review lifecycle metrics.

Dependencies
------------
- staging.sales_order_review
- staging.sales_order

Consumers
---------
- sql/metrics/operations/review_kpis.sql
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

CREATE OR REPLACE VIEW analytics.vw_review_performance AS

WITH review_base AS
(
    SELECT

        -----------------------------------------------------------------------
        -- Business Keys
        -----------------------------------------------------------------------
        r.review_id,
        r.order_id,
        o.customer_id,

        -----------------------------------------------------------------------
        -- Review Attributes
        -----------------------------------------------------------------------
        r.review_score,
        r.review_comment_title,
        r.review_comment_message,

        -----------------------------------------------------------------------
        -- Review Timeline
        -----------------------------------------------------------------------
        r.review_creation_date,
        r.review_answer_timestamp,

        -----------------------------------------------------------------------
        -- Order Context
        -----------------------------------------------------------------------
        o.order_status,
        o.order_purchase_timestamp,
        o.order_delivered_customer_date

    FROM staging.sales_order_review AS r

    INNER JOIN staging.sales_order AS o
        ON r.order_id = o.order_id
),

review_metrics AS
(
    SELECT

        -----------------------------------------------------------------------
        -- Business Keys
        -----------------------------------------------------------------------
        rb.review_id,
        rb.order_id,
        rb.customer_id,

        -----------------------------------------------------------------------
        -- Review Attributes
        -----------------------------------------------------------------------
        rb.review_score,
        rb.review_comment_title,
        rb.review_comment_message,

        -----------------------------------------------------------------------
        -- Timeline
        -----------------------------------------------------------------------
        rb.review_creation_date,
        rb.review_answer_timestamp,

        rb.order_status,
        rb.order_purchase_timestamp,
        rb.order_delivered_customer_date,

        -----------------------------------------------------------------------
        -- Derived Metrics
        -----------------------------------------------------------------------
        CASE
            WHEN rb.review_answer_timestamp IS NOT NULL
             AND rb.review_creation_date IS NOT NULL
            THEN ROUND(
                EXTRACT(
                    EPOCH FROM
                    (
                        rb.review_answer_timestamp
                        - rb.review_creation_date
                    )
                ) / 86400.0,
                2
            )
        END AS review_response_days,

        CASE
            WHEN rb.review_creation_date IS NOT NULL
             AND rb.order_delivered_customer_date IS NOT NULL
            THEN ROUND(
                EXTRACT(
                    EPOCH FROM
                    (
                        rb.review_creation_date
                        - rb.order_delivered_customer_date
                    )
                ) / 86400.0,
                2
            )
        END AS days_to_review,

        CASE
            WHEN rb.review_score >= 4 THEN 'Positive'
            WHEN rb.review_score = 3 THEN 'Neutral'
            ELSE 'Negative'
        END AS review_sentiment

    FROM review_base AS rb
)

SELECT

    ---------------------------------------------------------------------------
    -- Business Keys
    ---------------------------------------------------------------------------
    review_id,
    order_id,
    customer_id,

    ---------------------------------------------------------------------------
    -- Review Information
    ---------------------------------------------------------------------------
    review_score,
    review_comment_title,
    review_comment_message,

    ---------------------------------------------------------------------------
    -- Review Classification
    ---------------------------------------------------------------------------
    review_sentiment,

    CASE
        WHEN review_score = 5 THEN 'Excellent'
        WHEN review_score = 4 THEN 'Good'
        WHEN review_score = 3 THEN 'Average'
        WHEN review_score = 2 THEN 'Poor'
        ELSE 'Very Poor'
    END AS review_rating,

    ---------------------------------------------------------------------------
    -- Order Context
    ---------------------------------------------------------------------------
    order_status,
    order_purchase_timestamp,
    order_delivered_customer_date,

    ---------------------------------------------------------------------------
    -- Review Timeline
    ---------------------------------------------------------------------------
    review_creation_date,
    review_answer_timestamp,

    ---------------------------------------------------------------------------
    -- Operational Metrics
    ---------------------------------------------------------------------------
    review_response_days,
    days_to_review,

    ---------------------------------------------------------------------------
    -- Operational Flags
    ---------------------------------------------------------------------------
    CASE
        WHEN review_answer_timestamp IS NOT NULL
        THEN TRUE
        ELSE FALSE
    END AS review_answered,

    CASE
        WHEN review_comment_message IS NOT NULL
         AND LENGTH(TRIM(review_comment_message)) > 0
        THEN TRUE
        ELSE FALSE
    END AS has_review_comment

FROM review_metrics;