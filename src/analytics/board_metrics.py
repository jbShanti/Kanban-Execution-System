from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from src.parser.models import Task, TaskStatus


@dataclass(slots=True)
class BoardMetrics:
    total_tasks: int = 0

    active_tasks: int = 0
    actionable_tasks: int = 0

    open_tasks: int = 0
    in_progress_tasks: int = 0

    completed_tasks: int = 0
    cancelled_tasks: int = 0

    paused_tasks: int = 0
    scheduled_tasks: int = 0
    delegated_tasks: int = 0
    info_tasks: int = 0

    overdue_tasks: int = 0

    scored_tasks: int = 0
    unscored_tasks: int = 0

    total_score: int = 0

    score_distribution: dict[str, int] = field(
        default_factory=lambda: {
            "21-25": 0,
            "16-20": 0,
            "11-15": 0,
            "6-10": 0,
            "1-5": 0,
            "0": 0,
            "no_score": 0,
        }
    )


def calculate_board_metrics(
    tasks: list[Task],
    today: date | None = None,
) -> BoardMetrics:
    today = today or date.today()

    metrics = BoardMetrics(
        total_tasks=len(tasks),
    )

    for task in tasks:
        if task.is_active:
            metrics.active_tasks += 1

        if task.is_actionable:
            metrics.actionable_tasks += 1

        match task.status:
            case TaskStatus.OPEN:
                metrics.open_tasks += 1

            case TaskStatus.IN_PROGRESS:
                metrics.in_progress_tasks += 1

            case TaskStatus.COMPLETED:
                metrics.completed_tasks += 1

            case TaskStatus.CANCELLED:
                metrics.cancelled_tasks += 1

            case TaskStatus.PAUSED:
                metrics.paused_tasks += 1

            case TaskStatus.SCHEDULED:
                metrics.scheduled_tasks += 1

            case TaskStatus.DELEGATED:
                metrics.delegated_tasks += 1

            case TaskStatus.INFO:
                metrics.info_tasks += 1

        if task.score is None:
            metrics.unscored_tasks += 1
            metrics.score_distribution["no_score"] += 1

        else:
            score = task.score

            metrics.scored_tasks += 1
            metrics.total_score += score

            if 21 <= score <= 25:
                metrics.score_distribution["21-25"] += 1
            elif 16 <= score <= 20:
                metrics.score_distribution["16-20"] += 1
            elif 11 <= score <= 15:
                metrics.score_distribution["11-15"] += 1
            elif 6 <= score <= 10:
                metrics.score_distribution["6-10"] += 1
            elif 1 <= score <= 5:
                metrics.score_distribution["1-5"] += 1
            else:
                metrics.score_distribution["0"] += 1

        if (
            task.is_active
            and task.due is not None
            and task.due < today
        ):
            metrics.overdue_tasks += 1

    return metrics