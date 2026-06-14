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

    return FocusAttentionAnalytics(
        active_tasks=active_tasks,
        overdue_tasks=overdue_tasks,
        high_score_tasks=high_score_tasks,
    )