from __future__ import annotations

from datetime import date

from src.parser.models import TaskStatus, Board
from src.analytics.models import BoardMetrics, BoardSummary

def build_board_metrics(
    summary: BoardSummary,
) -> BoardMetrics:
    return BoardMetrics(
        total_tasks=summary.total_tasks,
        active_tasks=summary.active_tasks,
        actionable_tasks=summary.actionable_tasks,
        completed_tasks=summary.completed_tasks,
        cancelled_tasks=summary.cancelled_tasks,
        overdue_tasks=summary.overdue_tasks,
        scored_tasks=summary.scored_tasks,
        unscored_tasks=summary.unscored_tasks,
        total_score=summary.total_score,
        
    )


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
            
        else:
            score = task.score

            metrics.scored_tasks += 1
            metrics.total_score += score


        if (
            task.is_active
            and task.due is not None
            and task.due < today
        ):
            metrics.overdue_tasks += 1

    return metrics