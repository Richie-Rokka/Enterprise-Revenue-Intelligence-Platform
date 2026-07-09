/*
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : 010_quality_summary.sql
Schema      : analytics
Purpose     : Enterprise Data Quality Summary
Version     : 1.0.0

Description
-----------
Returns an enterprise summary of all executed quality rules.

NOTE
----
This script assumes the individual quality rule results have been persisted
to a metadata table (e.g. monitoring.quality_rule_history). Until that table
is implemented, this script serves as the enterprise contract.

===============================================================================
*/

SELECT

    COUNT(*) AS total_rules,

    COUNT(*) FILTER (
        WHERE passed
    ) AS rules_passed,

    COUNT(*) FILTER (
        WHERE NOT passed
    ) AS rules_failed,

    SUM(rows_checked) AS total_rows_checked,

    SUM(rows_failed) AS total_rows_failed,

    ROUND(

        100.0 *

        COUNT(*) FILTER (
            WHERE passed
        )

        /

        NULLIF(COUNT(*), 0),

        2

    ) AS quality_score,

    CASE

        WHEN COUNT(*) FILTER (WHERE passed) = COUNT(*)
            THEN 'A+'

        WHEN ROUND(
                100.0 *
                COUNT(*) FILTER (WHERE passed)
                /
                NULLIF(COUNT(*), 0),
                2
             ) >= 95
            THEN 'A'

        WHEN ROUND(
                100.0 *
                COUNT(*) FILTER (WHERE passed)
                /
                NULLIF(COUNT(*), 0),
                2
             ) >= 90
            THEN 'B'

        WHEN ROUND(
                100.0 *
                COUNT(*) FILTER (WHERE passed)
                /
                NULLIF(COUNT(*), 0),
                2
             ) >= 80
            THEN 'C'

        ELSE 'D'

    END AS grade,

    CURRENT_TIMESTAMP AS generated_at

FROM monitoring.quality_rule_history;