from datetime import datetime

from src.analytics.models import (
    AnalyticsReport,
    AnalyticsSnapshot,
    ScoreCorridor,
)


def build_analytics_report(
    snapshot: AnalyticsSnapshot,
) -> AnalyticsReport:

    summary = snapshot.summary

    corridors = [
        ScoreCorridor(
            name=name,
            task_count=count,
            total_score=0,
            average_score=0.0,
            percentage=0.0,
        )
        for name, count in summary.score_distribution.items()
    ]

    return AnalyticsReport(
        global_score=summary.total_score,
        corridors=corridors,
        total_tasks=summary.total_tasks,
        scored_tasks=summary.scored_tasks,
        generated_at=datetime.now(),
    )