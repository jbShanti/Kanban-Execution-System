from datetime import date, timedelta

from src.parser.models import Task


def calculate_time_metrics(
    tasks: list[Task],
) -> dict[str, int]:
    today = date.today()

    overdue_tasks = 0
    due_today_tasks = 0
    due_next_3_days_tasks = 0

    for task in tasks:
        if task.archived:
            continue

        if task.due is None:
            continue

        if task.due < today:
            overdue_tasks += 1

        if task.due == today:
            due_today_tasks += 1

        if (
            today
            <= task.due
            <= today + timedelta(days=3)
        ):
            due_next_3_days_tasks += 1

    return {
        "overdue_tasks": overdue_tasks,
        "due_today_tasks": due_today_tasks,
        "due_next_3_days_tasks": due_next_3_days_tasks,
    }