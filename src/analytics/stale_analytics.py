from __future__ import annotations

from datetime import datetime

from src.analytics.models import StaleTask
from src.parser.models import Task


STALE_THRESHOLD_DAYS = 7
CRITICAL_THRESHOLD_DAYS = 30


def analyze_stale_tasks(
    tasks: list[Task],
    now: datetime | None = None,
) -> list[StaleTask]:
    """
    Analyze active tasks and identify stale work.

    Rules:
    - only active tasks are analyzed
    - tasks without updated_at are ignored
    """

    now = now or datetime.now()

    results: list[StaleTask] = []

    for task in tasks:
        if not task.is_active:
            continue

        if task.updated_at is None:
            continue

        age_days = (now - task.updated_at).days

        results.append(
            StaleTask(
                task=task,
                age_days=age_days,
                is_stale=age_days >= STALE_THRESHOLD_DAYS,
                is_critical=age_days >= CRITICAL_THRESHOLD_DAYS,
                last_updated=task.updated_at,
            )
        )

    return sorted(
        results,
        key=lambda item: item.age_days,
        reverse=True,
    )