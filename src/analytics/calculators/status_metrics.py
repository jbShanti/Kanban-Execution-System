from src.parser.models import Task, TaskStatus


def calculate_status_metrics(
    tasks: list[Task],
) -> dict[str, int]:
    active_tasks = 0
    completed_tasks = 0
    cancelled_tasks = 0
    delegated_tasks = 0
    scheduled_tasks = 0
    archived_tasks = 0

    for task in tasks:
        if task.archived:
            archived_tasks += 1
            continue

        if task.status in {
            TaskStatus.OPEN,
            TaskStatus.IN_PROGRESS,
        }:
            active_tasks += 1

        elif task.status == TaskStatus.COMPLETED:
            completed_tasks += 1

        elif task.status == TaskStatus.CANCELLED:
            cancelled_tasks += 1

        elif task.status == TaskStatus.DELEGATED:
            delegated_tasks += 1

        elif task.status == TaskStatus.SCHEDULED:
            scheduled_tasks += 1

    return {
        "active_tasks": active_tasks,
        "completed_tasks": completed_tasks,
        "cancelled_tasks": cancelled_tasks,
        "delegated_tasks": delegated_tasks,
        "scheduled_tasks": scheduled_tasks,
        "archived_tasks": archived_tasks,
    }