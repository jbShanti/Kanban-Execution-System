from __future__ import annotations

from datetime import date

from src.analytics.models import BoardSummary, SectionSummary, SectionMetrics
from src.parser.models import Section
from src.parser.models import Board


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
            summary.score_distribution["no_score"] += 1
            continue

        score = task.score

        summary.scored_tasks += 1
        summary.total_score += score

        if 21 <= score <= 25:
            summary.score_distribution["21-25"] += 1

        elif 16 <= score <= 20:
            summary.score_distribution["16-20"] += 1

        elif 11 <= score <= 15:
            summary.score_distribution["11-15"] += 1

        elif 6 <= score <= 10:
            summary.score_distribution["6-10"] += 1

        elif 1 <= score <= 5:
            summary.score_distribution["1-5"] += 1

        else:
            summary.score_distribution["0"] += 1

    return summary

def build_section_metrics(
    section: Section,
    summary: SectionSummary,
) -> SectionMetrics:

    return SectionMetrics(
    section=section,
    total_tasks=summary.total_tasks,
    active_tasks=summary.active_tasks,
    actionable_tasks=summary.actionable_tasks,
    completed_tasks=summary.completed_tasks,
    cancelled_tasks=summary.cancelled_tasks,
    scored_tasks=summary.scored_tasks,
    total_score=summary.total_score,
    wip_limit=section.wip_limit,
)