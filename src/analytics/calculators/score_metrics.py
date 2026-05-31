from src.parser.models import (
    Task,
    TaskStatus,
)


def calculate_score_metrics(
    tasks: list[Task],
) -> dict[str, int]:
    tasks_without_score = 0

    total_score = 0
    active_score = 0

    for task in tasks:
        if task.archived:
            continue

        if task.score is None:
            tasks_without_score += 1
            continue

        total_score += task.score

        if task.status in {
            TaskStatus.OPEN,
            TaskStatus.IN_PROGRESS,
        }:
            active_score += task.score

    return {
        "tasks_without_score": tasks_without_score,
        "total_score": total_score,
        "active_score": active_score,
    }