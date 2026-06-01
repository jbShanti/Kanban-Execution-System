from __future__ import annotations

from src.parser.models import Board
from src.analytics.models import SectionMetrics

def calculate_section_metrics(
    board: Board,
) -> dict[str, SectionMetrics]:
    """
    Calculate metrics grouped by section title.
    """

    metrics_by_section: dict[str, SectionMetrics] = {}

    for task in board.tasks:
        section_key = task.section.title

        if section_key not in metrics_by_section:
            metrics_by_section[section_key] = SectionMetrics(
                section=task.section,
                wip_limit=task.section.wip_limit,
            )

        metrics = metrics_by_section[section_key]

        metrics.total_tasks += 1

        if task.is_active:
            metrics.active_tasks += 1

        if task.is_actionable:
            metrics.actionable_tasks += 1

        if task.is_completed:
            metrics.completed_tasks += 1

        if task.is_cancelled:
            metrics.cancelled_tasks += 1

        if task.score is not None:
            metrics.scored_tasks += 1
            metrics.total_score += task.score

    return metrics_by_section