/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : review_kpis.sql
Schema      : analytics
Object      : review_kpis
Type        : Operations Metrics View

Business Grain
--------------
One row summarizing enterprise customer review performance.

Purpose
-------
Provides enterprise customer satisfaction KPIs including review scores,
sentiment distribution, response performance, and review participation.

Dependencies
------------
- analytics.vw_review_performance

Consumers
---------
- Operations Dashboard
- Executive Dashboard
- Power BI Operations Dashboard

===============================================================================
*/

CREATE OR REPLACE VIEW analytics.review_kpis AS

SELECT

    ---------------------------------------------------------------------------
    -- Review Volume
    ---------------------------------------------------------------------------
    COUNT(*)                                                     AS total_reviews,

    COUNT(*) FILTER (
        WHERE review_answered
    )                                                            AS answered_reviews,

    COUNT(*) FILTER (
        WHERE NOT review_answered
    )                                                            AS unanswered_reviews,

    COUNT(*) FILTER (
        WHERE has_review_comment
    )                                                            AS reviews_with_comments,

    ---------------------------------------------------------------------------
    -- Review Scores
    ---------------------------------------------------------------------------
    ROUND(
        AVG(review_score),
        2
    )                                                            AS average_review_score,

    MIN(review_score)                                            AS minimum_review_score,

    MAX(review_score)                                            AS maximum_review_score,

    ---------------------------------------------------------------------------
    -- Review Rating Distribution
    ---------------------------------------------------------------------------
    COUNT(*) FILTER (
        WHERE review_rating = 'Excellent'
    )                                                            AS excellent_reviews,

    COUNT(*) FILTER (
        WHERE review_rating = 'Good'
    )                                                            AS good_reviews,

    COUNT(*) FILTER (
        WHERE review_rating = 'Average'
    )                                                            AS average_reviews,

    COUNT(*) FILTER (
        WHERE review_rating = 'Poor'
    )                                                            AS poor_reviews,

    COUNT(*) FILTER (
        WHERE review_rating = 'Very Poor'
    )                                                            AS very_poor_reviews,

    ---------------------------------------------------------------------------
    -- Sentiment Distribution
    ---------------------------------------------------------------------------
    COUNT(*) FILTER (
        WHERE review_sentiment = 'Positive'
    )                                                            AS positive_reviews,

    COUNT(*) FILTER (
        WHERE review_sentiment = 'Neutral'
    )                                                            AS neutral_reviews,

    COUNT(*) FILTER (
        WHERE review_sentiment = 'Negative'
    )                                                            AS negative_reviews,

    ROUND(
        100.0 *
        COUNT(*) FILTER (WHERE review_sentiment = 'Positive')
        /
        NULLIF(COUNT(*),0),
        2
    )                                                            AS positive_review_rate_pct,

    ROUND(
        100.0 *
        COUNT(*) FILTER (WHERE review_sentiment = 'Negative')
        /
        NULLIF(COUNT(*),0),
        2
    )                                                            AS negative_review_rate_pct,

    ---------------------------------------------------------------------------
    -- Response Performance
    ---------------------------------------------------------------------------
    ROUND(
        AVG(review_response_days),
        2
    )                                                            AS average_review_response_days,

    ROUND(
        AVG(days_to_review),
        2
    )                                                            AS average_days_to_review,

    ---------------------------------------------------------------------------
    -- Customer Engagement
    ---------------------------------------------------------------------------
    ROUND(
        100.0 *
        COUNT(*) FILTER (WHERE has_review_comment)
        /
        NULLIF(COUNT(*),0),
        2
    )                                                            AS review_comment_rate_pct,

    ROUND(
        100.0 *
        COUNT(*) FILTER (WHERE review_answered)
        /
        NULLIF(COUNT(*),0),
        2
    )                                                            AS review_response_rate_pct

FROM analytics.vw_review_performance;