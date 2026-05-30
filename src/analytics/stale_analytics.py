from __future__ import annotations

from datetime import datetime

from src.analytics.models import StaleTask
from src.parser.models import (
    SectionType,
    Task,
)


ACTIVE_EXECUTION_SECTION_TYPES = {
    SectionType.TACTICAL,
    SectionType.EXECUTION,
}

ACTIVE_PIPELINE_SECTION_TYPES = {
    SectionType.INBOX,
    SectionType.QUEUED,
    SectionType.FOCUS,
}


def _classify_staleness(
    task: Task,
    age_days: int,
) -> tuple[bool, bool]:
    """
    Returns:
        (is_stale, is_critical)
    """

    section_type = task.section.type

    if section_type in ACTIVE_EXECUTION_SECTION_TYPES:
        return (
            age_days >= 7,
            age_days >= 30,
        )

    if section_type in ACTIVE_PIPELINE_SECTION_TYPES:
        return (
            age_days >= 30,
            age_days >= 90,
        )

    return (
        False,
        False,
    )


def calculate_stale_tasks(
    tasks: list[Task],
    now: datetime | None = None,
) -> list[StaleTask]:
    """
    Identify stale actionable tasks.

    Execution zones:
        stale     >= 7 days
        critical  >= 30 days

    Pipeline zones:
        stale     >= 30 days
        critical  >= 90 days
    """

    now = now or datetime.now()

    results: list[StaleTask] = []

    for task in tasks:
        if not task.is_actionable:
            continue

        if task.updated_at is None:
            continue

        age_days = (
            now - task.updated_at
        ).days

        is_stale, is_critical = _classify_staleness(
            task,
            age_days,
        )

        if not is_stale:
            continue

        last_updated = task.updated_at

        age_days = (now - last_updated).days

        results.append(
            StaleTask(
                task=task,
                age_days=age_days,
                is_stale=is_stale,
                is_critical=is_critical,
                last_updated=last_updated,
            )
        )

    return sorted(
        results,
        key=lambda item: item.age_days,
        reverse=True,
    )