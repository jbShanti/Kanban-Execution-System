from __future__ import annotations

from src.analytics.models import (
    AnalyticsTaskSnapshot,
    FocusAttentionAnalytics,
)


HIGH_PRIORITY_SCORE_THRESHOLD = 17


def build_focus_attention_analytics(
    snapshots: list[AnalyticsTaskSnapshot],
) -> FocusAttentionAnalytics:
    """
    Builds focus-related attention metrics from task snapshots.
    """

    active_tasks = sum(
        1
        for task in snapshots
        if task.is_active
    )

    overdue_tasks = sum(
        1
        for task in snapshots
        if task.is_overdue
    )

    high_score_tasks = sum(
        1
        for task in snapshots
        if task.score >= HIGH_PRIORITY_SCORE_THRESHOLD
    )

    attention_by_tag: dict[str, int] = {}

    for task in snapshots:
        if not task.is_active:
            continue

        for tag in task.tags:
            attention_by_tag[tag] = (
                attention_by_tag.get(tag, 0)
                + task.score
            )

    return FocusAttentionAnalytics(
        active_tasks=active_tasks,
        overdue_tasks=overdue_tasks,
        high_score_tasks=high_score_tasks,
        attention_by_tag=attention_by_tag,
    )