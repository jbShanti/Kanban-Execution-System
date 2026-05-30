from collections import defaultdict
from typing import DefaultDict

from src.parser.models import SectionType, Task, TaskStatus

from datetime import datetime, timedelta, UTC


WIP_LIMITS: dict[SectionType, int] = {
    SectionType.TACTICAL: 5,
    SectionType.EXECUTION: 3,
    SectionType.QUEUED: 20,
    SectionType.WAITING: 10,
    SectionType.STRATEGIC: 7,
    SectionType.UNKNOWN: 30,
}

SECTION_WEIGHTS = {
    SectionType.TACTICAL: 3.0,
    SectionType.EXECUTION: 2.0,
    SectionType.WAITING: 1.2,
    SectionType.QUEUED: 0.5,
    SectionType.STRATEGIC: 1.5,
    SectionType.UNKNOWN: 0.3,
}


def count_tasks_by_section_type(
    tasks: list[Task],
) -> dict[SectionType, int]:
    counts: DefaultDict[SectionType, int] = defaultdict(int)

    for task in tasks:
        if task.archived:
            continue

        if task.status == TaskStatus.COMPLETED:
            continue

        section_type = task.section.type

        if section_type not in WIP_LIMITS:
            continue

        counts[section_type] += 1

    return dict(counts)


def detect_wip_violations(
    tasks: list[Task],
) -> dict[SectionType, int]:
    violations: dict[SectionType, int] = {}

    counts = count_tasks_by_section_type(tasks)

    for section_type, limit in WIP_LIMITS.items():
        current = counts.get(section_type, 0)

        if current > limit:
            violations[section_type] = current - limit

    return violations


def is_wip_overloaded(
    tasks: list[Task],
) -> bool:
    violations = detect_wip_violations(tasks)

    return len(violations) > 0


def calculate_wip_pressure(
    tasks: list[Task],
) -> float:
    counts = count_tasks_by_section_type(tasks)

    total_ratio = 0.0
    sections = 0

    for section_type, limit in WIP_LIMITS.items():
        current = counts.get(section_type, 0)

        ratio = current / limit

        total_ratio += ratio
        sections += 1

    if sections == 0:
        return 0.0

    return round(total_ratio / sections, 2)

STALE_THRESHOLDS_DAYS: dict[SectionType, int] = {
    SectionType.TACTICAL: 1,
    SectionType.EXECUTION: 3,
    SectionType.WAITING: 7,
    SectionType.QUEUED: 30,
    SectionType.STRATEGIC: 14,
    SectionType.UNKNOWN: 30,
}

def detect_stale_tasks(
    tasks: list[Task],
    now: datetime | None = None,
) -> list[Task]:
    
    if now is None:
        now = datetime.now(UTC)

    stale_tasks: list[Task] = []

    for task in tasks:
        if task.archived:
            continue

        if task.status == TaskStatus.COMPLETED:
            continue

        threshold_days = STALE_THRESHOLDS_DAYS.get(
            task.section.type,
            30,
        )

        if task.updated_at is None:
            continue
        
  
        age = now - task.updated_at

        if age > timedelta(days=threshold_days):
            stale_tasks.append(task)

    return stale_tasks

def calculate_stale_ratio(
    tasks: list[Task],
    now: datetime | None = None,
) -> float:
    active_tasks = [
        task
        for task in tasks
        if not task.archived
        and task.status != TaskStatus.COMPLETED
    ]

    if not active_tasks:
        return 0.0

    stale_tasks = detect_stale_tasks(
        active_tasks,
        now=now,
    )

    ratio = len(stale_tasks) / len(active_tasks)

    return round(ratio, 2)