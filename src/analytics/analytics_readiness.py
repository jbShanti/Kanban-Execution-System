from __future__ import annotations

from collections.abc import Sequence

from src.analytics.models import (
    AnalyticsTaskSnapshot,
    BoardHealth,
    BoardHealthStatus,
)


def build_board_health(
    snapshots: Sequence[AnalyticsTaskSnapshot],
) -> BoardHealth:
    total_tasks = len(snapshots)
 
    missing_score = sum(
        1
        for snapshot in snapshots
        if snapshot.score is None
    )

    return BoardHealth(
        total_tasks=total_tasks,

        score_coverage=0.0,
        tag_coverage=0.0,
        analytics_coverage=0.0,

        missing_score=missing_score,
        missing_tag=0,

        orphan_tasks=0,

        sample_orphans=(),

        status=BoardHealthStatus.CRITICAL,
    )