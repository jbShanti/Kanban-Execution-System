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

    corridors: list[ScoreCorridor] = []

    for (
        corridor_name,
        corridor_summary,
    ) in summary.score_corridors.items():

        average_score = 0.0

        if corridor_summary.scored_tasks > 0:
            average_score = (
                corridor_summary.total_score
                / corridor_summary.scored_tasks
            )

        percentage = 0.0

        if summary.total_tasks > 0:
            percentage = (
                corridor_summary.task_count
                / summary.total_tasks
                * 100
            )

        corridors.append(
            ScoreCorridor(
                name=corridor_name,
                task_count=corridor_summary.task_count,
                total_score=corridor_summary.total_score,
                average_score=average_score,
                percentage=percentage,
            )
        )

    return AnalyticsReport(
        global_score=summary.total_score,
        corridors=corridors,
        total_tasks=summary.total_tasks,
        scored_tasks=summary.scored_tasks,
        generated_at=datetime.now(),
    )