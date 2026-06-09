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

        average_score=corridor_summary.average_score

        percentage = corridor_summary.percentage_of(
            summary.total_tasks
        )

        score_share_percentage = 0.0

        if summary.total_score > 0:
            score_share_percentage = (
                corridor_summary.total_score
                / summary.total_score
                * 100
            )

        corridors.append(
            ScoreCorridor(
                name=corridor_name,
                task_count=corridor_summary.task_count,
                total_score=corridor_summary.total_score,
                average_score=average_score,
                percentage=percentage,
                score_share_percentage=score_share_percentage,
            )
        )
        
    high_value_tasks = sum(
        corridor.task_count
        for corridor in corridors
        if corridor.name in {"21-25", "16-20"}
    )

    high_value_percentage = 0.0

    if summary.total_tasks > 0:
        high_value_percentage = (
            high_value_tasks
            / summary.total_tasks
            * 100
        )

    focus_tasks = next(
    (
        corridor.task_count
        for corridor in corridors
        if corridor.name == "21-25"
    ),
    0,
)

    focus_percentage = 0.0

    if summary.total_tasks > 0:
        focus_percentage = (
            focus_tasks
            / summary.total_tasks
            * 100
        )
    
    return AnalyticsReport(
        global_score=summary.total_score,
        corridors=corridors,
        total_tasks=summary.total_tasks,
        scored_tasks=summary.scored_tasks,
        high_value_tasks=high_value_tasks,
        high_value_percentage=high_value_percentage,
        focus_tasks=focus_tasks,
        focus_percentage=focus_percentage,
        generated_at=datetime.now(),
    )