from __future__ import annotations

from collections.abc import Sequence

from src.analytics.models import (
    AnalyticsTaskSnapshot,
    BoardHealth,
    BoardHealthStatus,
    OrphanTask,
    MissingMetadata,
)

def _build_sample_orphans(
    orphans: list[AnalyticsTaskSnapshot],
) -> tuple[OrphanTask, ...]:
    """Build prioritized sample of orphan tasks (top 5).
    
    Prioritization criteria (in order of importance):
      1. Total number of missing metadata fields (more = higher priority)
         A task missing BOTH score and tags is the most critical.
      2. Missing tag is MORE critical than missing score (at same missing count).
         Tags are essential for categorization and analytics; without tags
         a task is effectively "invisible" to the system.
      3. Alphabetical order by title (for deterministic output)
    """
    def prioritization_key(snapshot: AnalyticsTaskSnapshot) -> tuple[int, int, str]:
        missing_count: int = 0
        if snapshot.score is None:
            missing_count += 1
        if len(snapshot.tags) == 0:
            missing_count += 1
        
        # 0 = tag missing (higher priority), 1 = tag present (lower priority)
        tag_missing: int = 0 if len(snapshot.tags) == 0 else 1
        
        # Negative values → higher values come first when sorted ascending
        return (-missing_count, tag_missing, snapshot.title)
    
    sorted_orphans: list[AnalyticsTaskSnapshot] = sorted(
        orphans,
        key=prioritization_key,
    )
    
    result: list[OrphanTask] = []
    for snapshot in sorted_orphans[:5]:
        missing: list[MissingMetadata] = []
        if snapshot.score is None:
            missing.append(MissingMetadata.SCORE)
        if len(snapshot.tags) == 0:
            missing.append(MissingMetadata.TAG)
        
        result.append(
            OrphanTask(
                title=snapshot.title,
                is_active=snapshot.is_active,
                missing=tuple(missing),
            )
        )
    
    return tuple(result)

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
    """Build BoardHealth from task snapshots."""
    
    # ✅ Явная аннотация типа
    eligible_snapshots: list[AnalyticsTaskSnapshot] = [
        snapshot
        for snapshot in snapshots
        if not snapshot.analytics_ignore
    ]
    
    total_tasks: int = len(eligible_snapshots)
    
    active_tasks: int = sum(
        1 for snapshot in eligible_snapshots
        if snapshot.is_active
    )
    
    missing_score: int = sum(
        1
        for snapshot in eligible_snapshots
        if snapshot.score is None
    )
    
    missing_tag: int = sum(
        1
        for snapshot in eligible_snapshots
        if len(snapshot.tags) == 0
    )
    
    tasks_with_score: int = total_tasks - missing_score
    score_coverage: float = (
        tasks_with_score / total_tasks
        if total_tasks > 0
        else 1.0
    )
    
    tasks_with_tag: int = total_tasks - missing_tag
    tag_coverage: float = (
        tasks_with_tag / total_tasks
        if total_tasks > 0
        else 1.0
    )
    
    analytics_ready_tasks: int = sum(
        1
        for snapshot in eligible_snapshots
        if snapshot.score is not None
        and len(snapshot.tags) > 0
    )
    analytics_coverage: float = (
        analytics_ready_tasks / total_tasks
        if total_tasks > 0
        else 1.0
    )
    
    # ✅ Сироты = только АКТИВНЫЕ задачи с неполными метаданными
    orphans: list[AnalyticsTaskSnapshot] = [
        snapshot
        for snapshot in eligible_snapshots  # ← FIX: snapshots → eligible_snapshots
        if snapshot.is_active
        and (snapshot.score is None or len(snapshot.tags) == 0)
    ]
    
    orphan_tasks: int = len(orphans)
    sample_orphans: tuple[OrphanTask, ...] = _build_sample_orphans(orphans)
    
    status: BoardHealthStatus = evaluate_board_health_status(analytics_coverage)
    
    return BoardHealth(
        total_tasks=total_tasks,
        active_tasks=active_tasks,
        score_coverage=score_coverage,
        tag_coverage=tag_coverage,
        analytics_coverage=analytics_coverage,
        missing_score=missing_score,
        missing_tag=missing_tag,
        orphan_tasks=orphan_tasks,
        sample_orphans=sample_orphans,
        status=status,
)
    
    
def orphan_priority(
    orphan: OrphanTask,
) -> int:
    """
    Lower value means higher priority.

    Priority order:

    1. Missing score and tag
    2. Missing tag only
    3. Missing score only
    4. Any other orphan state
    """

    missing_score = (
        MissingMetadata.SCORE
        in orphan.missing
    )

    missing_tag = (
        MissingMetadata.TAG
        in orphan.missing
    )

    if missing_score and missing_tag:
        return 1

    if missing_tag:
        return 2

    if missing_score:
        return 3

    return 4