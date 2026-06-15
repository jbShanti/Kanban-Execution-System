from __future__ import annotations

from collections.abc import Sequence

from src.analytics.models import (
    AnalyticsTaskSnapshot,
    BoardHealth,
    BoardHealthStatus,
)

def evaluate_board_health_status(
    analytics_coverage: float,
) -> BoardHealthStatus:

    if analytics_coverage >= 0.99:
        return BoardHealthStatus.EXCELLENT

    if analytics_coverage > 0.90:
        return BoardHealthStatus.GOOD

    if analytics_coverage > 0.75:
        return BoardHealthStatus.WARNING

    if analytics_coverage > 0.50:
        return BoardHealthStatus.POOR

    if analytics_coverage > 0.25:
        return BoardHealthStatus.AWFUL

    return BoardHealthStatus.CRITICAL



def build_board_health(
    snapshots: Sequence[AnalyticsTaskSnapshot],
) -> BoardHealth:
    total_tasks = len(snapshots)
 
    missing_score = sum(
        1
        for snapshot in snapshots
        if snapshot.score is None
    )
    
    missing_tag = sum(
        1
        for snapshot in snapshots
        if len(snapshot.tags) == 0
    )

    orphan_tasks = sum(
        1
        for snapshot in snapshots
        if snapshot.score is None
        or len(snapshot.tags) == 0
    )
    
    tasks_with_score = total_tasks - missing_score

    score_coverage = (
        tasks_with_score / total_tasks
        if total_tasks > 0
        else 1.0
    )
    
    tasks_with_tag = total_tasks - missing_tag

    tag_coverage = (
        tasks_with_tag / total_tasks
        if total_tasks > 0
        else 1.0
    )
    
    
    analytics_ready_tasks = sum(
        1
        for snapshot in snapshots
        if snapshot.score is not None
        and len(snapshot.tags) > 0
    )

    analytics_coverage = (
        analytics_ready_tasks / total_tasks
        if total_tasks > 0
        else 1.0
    )
    
    status = evaluate_board_health_status(
        analytics_coverage
    )
    
    return BoardHealth(
        total_tasks=total_tasks,

        score_coverage=score_coverage,
        tag_coverage=tag_coverage,
        analytics_coverage=analytics_coverage,

        missing_score=missing_score,
        missing_tag=missing_tag,

        orphan_tasks=orphan_tasks,

        sample_orphans=(),

        status=status,
    )