from __future__ import annotations

from datetime import date

from src.parser.models import TaskStatus, Board
from src.analytics.models import BoardMetrics


def calculate_board_metrics(
    board: Board,
    today: date | None = None,
) -> BoardMetrics:
    today = today or date.today()

    metrics = BoardMetrics(
        total_tasks=len(board.tasks),
    )

    for task in board.tasks:
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