from __future__ import annotations

from datetime import date

from src.analytics.models import AnalyticsTaskSnapshot
from src.parser.models import Task, Board


def build_task_snapshot(
    task: Task,
    today: date,
    average_score: float = 0.0,
) -> AnalyticsTaskSnapshot:
    """
    Converts a domain Task into an analytics snapshot.
    """

    time_estimate_minutes = (
        int(task.time_estimate.total_seconds() // 60)
        if task.time_estimate is not None
        else None
    )

    is_overdue = (
        task.due is not None
        and not task.is_completed
        and task.due < today
    )

    effective_score = task.score if task.score is not None else round(average_score)

    return AnalyticsTaskSnapshot(
        title=task.title,
        section=task.section.title,
        status=task.status,
        score=task.score,
        effective_score=effective_score,
        due_date=task.due,
        scheduled_date=task.scheduled,
        time_estimate_minutes=time_estimate_minutes,
        tags=tuple(task.tags),
        category=task.category,
        is_active=task.is_active,
        is_completed=task.is_completed,
        is_archived=task.archived,
        is_overdue=is_overdue,
        analytics_ignore=task.ignored,
        cost=task.cost,
        currency=task.currency,
    )
    
    
def build_task_snapshots(
    board: Board,
    today: date,
    average_score: float = 0.0,
) -> list[AnalyticsTaskSnapshot]:
    return [
        build_task_snapshot(
            task=task,
            today=today,
            average_score=average_score,
        )
        for task in board.tasks
    ]