"""
===============================================================================
Enterprise Revenue Intelligence Platform (ERIP)
===============================================================================

Module      : scorecard.py
Package     : src.quality
Purpose     : Enterprise Data Quality Scorecard Engine
Author      : ERIP
Version     : 2.0.0

Description
-----------
Generates enterprise data quality scorecards from executed quality rules.

Responsibilities
----------------
- Generate enterprise quality score
- Calculate overall quality grade
- Aggregate quality rule execution
- Produce executive-ready scorecards

===============================================================================
"""

from __future__ import annotations

from src.observability import get_logger

from .models import (
    QualityCheckResult,
    QualityScorecard,
)
from .rules import RulesEngine


logger = get_logger(__name__)


# =============================================================================
# Scorecard Engine
# =============================================================================


class ScorecardEngine:
    """
    Enterprise Data Quality Scorecard Engine.
    """

    VERSION = "2.0.0"

    # -------------------------------------------------------------------------

    def __init__(self) -> None:

        self.rules = RulesEngine()

    # -------------------------------------------------------------------------

    def generate(self) -> QualityScorecard:
        """
        Generate enterprise quality scorecard.
        """

        logger.info("=" * 60)
        logger.info("Generating Enterprise Quality Scorecard")
        logger.info("=" * 60)

        results = self.rules.execute()

        scorecard = self._build_scorecard(results)

        logger.info(

            "Overall Quality Score: %.2f%% (%s)",

            scorecard.overall_score,

            scorecard.grade,

        )

        logger.info("=" * 60)

        return scorecard

    # -------------------------------------------------------------------------

    def _build_scorecard(
        self,
        results: list[QualityCheckResult],
    ) -> QualityScorecard:
        """
        Build scorecard from rule execution results.
        """

        if not results:

            return QualityScorecard(

                completeness_score=0.0,

                uniqueness_score=0.0,

                consistency_score=0.0,

                referential_integrity_score=0.0,

                freshness_score=0.0,

                overall_score=0.0,

                grade="F",

            )

        scores = {

            "Completeness": 100.0,

            "Uniqueness": 100.0,

            "Consistency": 100.0,

            "Referential Integrity": 100.0,

            "Freshness": 100.0,

        }

        for result in results:

            if not result.passed:

                scores[result.rule_name] = 0.0

        overall = sum(scores.values()) / len(scores)

        return QualityScorecard(

            completeness_score=scores["Completeness"],

            uniqueness_score=scores["Uniqueness"],

            consistency_score=scores["Consistency"],

            referential_integrity_score=scores["Referential Integrity"],

            freshness_score=scores["Freshness"],

            overall_score=overall,

            grade=self._grade(overall),

        )

    # -------------------------------------------------------------------------

    @staticmethod
    def _grade(score: float) -> str:
        """
        Convert numeric score into enterprise grade.
        """

        if score >= 98:
            return "A+"

        if score >= 95:
            return "A"

        if score >= 90:
            return "B"

        if score >= 80:
            return "C"

        if score >= 70:
            return "D"

        return "F"

    # -------------------------------------------------------------------------

    def version(self) -> str:
        """
        Framework version.
        """

        return self.VERSION