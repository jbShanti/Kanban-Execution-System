from datetime import datetime

from src.analytics.models import (
    AnalyticsReport,
    AnalyticsSnapshot,
)


def build_analytics_report(
    snapshot: AnalyticsSnapshot,
) -> AnalyticsReport:

    summary = snapshot.summary

    return AnalyticsReport(
        global_score=summary.total_score,
        corridor_distribution=summary.score_distribution,
        total_tasks=summary.total_tasks,
        scored_tasks=summary.scored_tasks,
        generated_at=datetime.now(),
    )