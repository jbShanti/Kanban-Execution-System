from collections import defaultdict
from datetime import date

from src.parser.models import (
    Task,
    TaskStatus,
)


OPEN_STATUSES = {
    TaskStatus.OPEN,
    TaskStatus.IN_PROGRESS,
    TaskStatus.SCHEDULED,
    TaskStatus.DELEGATED,
}


def count_completed_tasks(
    tasks: list[Task],
) -> int:
    return sum(
        1
        for task in tasks
        if task.status == TaskStatus.COMPLETED
    )


def count_open_tasks(
    tasks: list[Task],
) -> int:
    return sum(
        1
        for task in tasks
        if task.status in OPEN_STATUSES
    )


from collections import defaultdict

def group_tasks_by_section(
    tasks: list[Task],
) -> dict[str, list[Task]]:
    grouped: dict[str, list[Task]] = defaultdict(list)

    for task in tasks:
        grouped[task.section.title].append(task)

    return dict(grouped)


def find_overdue_tasks(
    tasks: list[Task],
) -> list[Task]:
    today = date.today()

    overdue_tasks: list[Task] = []

    for task in tasks:
        if (
            task.due is not None
            and task.due < today
            and task.status != TaskStatus.COMPLETED
        ):
            overdue_tasks.append(task)

    return overdue_tasks


def calculate_total_score(
    tasks: list[Task],
) -> int:
    return sum(
        task.score or 0
        for task in tasks
    )


def calculate_section_scores(
    tasks: list[Task],
) -> dict[str, int]:
    section_scores: dict[str, int] = defaultdict(int)

    for task in tasks:
        section_scores[task.section.title] += (
            task.score or 0
        )

    return dict(section_scores)


def find_high_score_tasks(
    tasks: list[Task],
    threshold: int = 50,
) -> list[Task]:
    high_score_tasks: list[Task] = []

    for task in tasks:
        if (
            task.score is not None
            and task.score >= threshold
        ):
            high_score_tasks.append(task)

    return high_score_tasks


def find_tasks_without_dates(
    tasks: list[Task],
) -> list[Task]:
    undated_tasks: list[Task] = []

    for task in tasks:
        if (
            task.due is None
            and task.scheduled is None
            and task.status in OPEN_STATUSES
        ):
            undated_tasks.append(task)

    return undated_tasks


def calculate_completion_rate(
    tasks: list[Task],
) -> float:
    if not tasks:
        return 0.0

    completed = count_completed_tasks(tasks)

    return completed / len(tasks)


def find_empty_sections(
    tasks: list[Task],
    known_sections: list[str],
) -> list[str]:
    grouped = group_tasks_by_section(tasks)

    empty_sections: list[str] = []

    for section in known_sections:
        if section not in grouped:
            empty_sections.append(section)

    return empty_sections