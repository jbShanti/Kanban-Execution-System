from __future__ import annotations

from src.analytics.models import (
    AttentionScore,
    BoardHealthReport,
    HealthWarning,
    PriorityScore,
    StaleTask,
    WipStatus,
    OverloadSignal
)
from src.analytics.stale_analytics import (
    ACTIVE_EXECUTION_SECTION_TYPES,
    ACTIVE_PIPELINE_SECTION_TYPES,
)


def build_board_health_report(
    priority_scores: list[PriorityScore],
    attention_scores: list[AttentionScore],
    stale_tasks: list[StaleTask],
    wip_statuses: list[WipStatus],
    overload_signals: list[OverloadSignal] | None = None,
) -> BoardHealthReport:
    score = 100.0

    warnings: list[HealthWarning] = []

    wip_violations = 0

    for status in wip_statuses:
        if not status.is_over_limit:
            continue

        wip_violations += 1

        score -= 10

        warnings.append(
            HealthWarning(
                category="wip",
                message=(
                    f"{status.section_name} exceeds "
                    f"WIP limit "
                    f"({status.active_tasks}/"
                    f"{status.wip_limit})"
                ),
            )
        )

    stale_task_count = 0

    for stale in stale_tasks:
        stale_task_count += 1

        section_type = stale.task.section.type

        if section_type in ACTIVE_EXECUTION_SECTION_TYPES:
            score -= 5 if stale.is_critical else 2

        elif section_type in ACTIVE_PIPELINE_SECTION_TYPES:
            score -= 1 if stale.is_critical else 0.5

        warnings.append(
            HealthWarning(
                category="stale",
                message=(
                    f"{stale.task.title} "
                    f"stale for {stale.age_days} days"
                ),
            )
        )

    score = max(score, 0.0)

    return BoardHealthReport(
        board_health_score=score,
        wip_violations=wip_violations,
        stale_task_count=stale_task_count,
        top_priority_tasks=priority_scores[:5],
        top_attention_tasks=attention_scores[:5],
        warnings=warnings,
        overload_signals=overload_signals
    )