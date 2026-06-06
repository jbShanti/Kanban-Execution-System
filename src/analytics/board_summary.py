from __future__ import annotations

from datetime import date

from src.analytics.models import (
    BoardSummary,
    SectionMetrics,
    SectionSummary,
)
from src.parser.models import Board, Section


def build_board_summary(
    board: Board,
    today: date | None = None,
) -> BoardSummary:
    today = today or date.today()

    summary = BoardSummary(
        total_tasks=len(board.tasks),
    )

    for task in board.tasks:

        if task.is_active:
            summary.active_tasks += 1

        if task.is_actionable:
            summary.actionable_tasks += 1

        if task.is_completed:
            summary.completed_tasks += 1

        if task.is_cancelled:
            summary.cancelled_tasks += 1

        status_name = task.status.value

        summary.by_status[status_name] = (
            summary.by_status.get(status_name, 0) + 1
        )

        section_name = task.section.title

        if section_name not in summary.sections:
            summary.sections[section_name] = SectionSummary()

        section_summary = summary.sections[section_name]

        section_summary.total_tasks += 1

        if task.is_active:
            section_summary.active_tasks += 1

        if task.is_actionable:
            section_summary.actionable_tasks += 1

        if task.is_completed:
            section_summary.completed_tasks += 1

        if task.is_cancelled:
            section_summary.cancelled_tasks += 1

        if task.score is not None:
            section_summary.scored_tasks += 1
            section_summary.total_score += task.score

        if (
            task.is_active
            and task.due is not None
            and task.due < today
        ):
            summary.overdue_tasks += 1

        if task.score is None:
            summary.unscored_tasks += 1

            summary.score_corridors["no_score"].task_count += 1

            continue

        score = task.score

        summary.scored_tasks += 1
        summary.total_score += score

        corridor_name: str

        if 21 <= score <= 25:
            corridor_name = "21-25"

        elif 16 <= score <= 20:
            corridor_name = "16-20"

        elif 11 <= score <= 15:
            corridor_name = "11-15"

        elif 6 <= score <= 10:
            corridor_name = "6-10"

        elif 1 <= score <= 5:
            corridor_name = "1-5"

        else:
            corridor_name = "0"

        corridor = summary.score_corridors[corridor_name]

        corridor.task_count += 1
        corridor.scored_tasks += 1
        corridor.total_score += score

    return summary


def build_section_metrics(
    section: Section,
    summary: SectionSummary,
) -> SectionMetrics:
    return SectionMetrics(
        section=section,
        summary=summary,
    )