from datetime import date

from src.analytics.board_metrics import calculate_board_metrics
from src.analytics.board_summary import build_board_summary
from src.parser.models import SectionType, TaskStatus
from tests.helper import create_board, create_section, create_task


def test_empty_board():
    board = create_board(tasks=[])

    summary = build_board_summary(board)

    assert summary.total_tasks == 0
    assert summary.active_tasks == 0
    assert summary.completed_tasks == 0
    assert summary.total_score == 0
    assert summary.average_score == 0.0


def test_counts_statuses():
    section = create_section(
        title="Todo",
        section_type=SectionType.QUEUED,
    )

    board = create_board(
        tasks=[
            create_task(
                title="Open",
                status=TaskStatus.OPEN,
                section=section,
            ),
            create_task(
                title="Progress",
                status=TaskStatus.IN_PROGRESS,
                section=section,
            ),
            create_task(
                title="Done",
                status=TaskStatus.COMPLETED,
                section=section,
            ),
            create_task(
                title="Cancelled",
                status=TaskStatus.CANCELLED,
                section=section,
            ),
        ]
    )

    summary = build_board_summary(board)

    assert summary.total_tasks == 4
    assert summary.active_tasks == 2
    assert summary.actionable_tasks == 2
    assert summary.completed_tasks == 1
    assert summary.cancelled_tasks == 1


def test_board_summary_by_status_map():
    section = create_section(title="Inbox")

    tasks = [
        create_task(title="T1", status=TaskStatus.OPEN, section=section),
        create_task(title="T2", status=TaskStatus.OPEN, section=section),
        create_task(title="T3", status=TaskStatus.IN_PROGRESS, section=section),
        create_task(title="T4", status=TaskStatus.COMPLETED, section=section),
        create_task(title="T5", status=TaskStatus.CANCELLED, section=section),
        create_task(title="T6", status=TaskStatus.PAUSED, section=section),
        create_task(title="T7", status=TaskStatus.SCHEDULED, section=section),
        create_task(title="T8", status=TaskStatus.DELEGATED, section=section),
        create_task(title="T9", status=TaskStatus.INFO, section=section),
    ]

    summary = build_board_summary(create_board(tasks=tasks))

    assert summary.by_status == {
        "open": 2,
        "in_progress": 1,
        "completed": 1,
        "cancelled": 1,
        "paused": 1,
        "scheduled": 1,
        "delegated": 1,
        "info": 1,
    }


def test_overdue_detection():
    section = create_section(
        title="Todo",
        section_type=SectionType.QUEUED,
    )

    board = create_board(
        tasks=[
            create_task(
                title="Overdue",
                status=TaskStatus.OPEN,
                section=section,
                due=date(2026, 5, 1),
            ),
            create_task(
                title="Future",
                status=TaskStatus.OPEN,
                section=section,
                due=date(2026, 7, 1),
            ),
            create_task(
                title="Completed",
                status=TaskStatus.COMPLETED,
                section=section,
                due=date(2026, 5, 1),
            ),
        ]
    )

    summary = build_board_summary(
        board,
        today=date(2026, 6, 1),
    )

    assert summary.overdue_tasks == 1


def test_section_distribution():
    todo = create_section(title="Todo", section_type=SectionType.QUEUED)
    health = create_section(title="Health", section_type=SectionType.QUEUED)

    board = create_board(
        tasks=[
            create_task(
                title="A",
                status=TaskStatus.OPEN,
                section=todo,
            ),
            create_task(
                title="B",
                status=TaskStatus.OPEN,
                section=todo,
            ),
            create_task(
                title="C",
                status=TaskStatus.OPEN,
                section=health,
            ),
        ]
    )

    summary = build_board_summary(board)

    assert set(summary.sections.keys()) == {
        "Todo",
        "Health",
    }

    assert summary.sections["Todo"].total_tasks == 2
    assert summary.sections["Health"].total_tasks == 1
    assert summary.sections["Todo"].active_tasks == 2


def test_average_score():
    section = create_section(
        title="Todo",
        section_type=SectionType.QUEUED,
    )

    board = create_board(
        tasks=[
            create_task(
                title="A",
                status=TaskStatus.OPEN,
                section=section,
                score=10,
            ),
            create_task(
                title="B",
                status=TaskStatus.OPEN,
                section=section,
                score=20,
            ),
        ]
    )

    summary = build_board_summary(board)

    assert summary.total_score == 30
    assert summary.average_score == 15.0


def test_score_corridors_distribution():
    section = create_section(title="Inbox")

    tasks = [
        create_task(title="A", status=TaskStatus.OPEN, section=section, score=25),
        create_task(title="B", status=TaskStatus.OPEN, section=section, score=18),
        create_task(title="C", status=TaskStatus.OPEN, section=section, score=12),
        create_task(title="D", status=TaskStatus.OPEN, section=section, score=8),
        create_task(title="E", status=TaskStatus.OPEN, section=section, score=3),
        create_task(title="F", status=TaskStatus.OPEN, section=section, score=0),
        create_task(title="G", status=TaskStatus.OPEN, section=section, score=None),
    ]

    summary = build_board_summary(create_board(tasks=tasks))

    corridors = summary.score_corridors

    assert corridors["21-25"].task_count == 1
    assert corridors["21-25"].total_score == 25

    assert corridors["16-20"].task_count == 1
    assert corridors["16-20"].total_score == 18

    assert corridors["11-15"].task_count == 1
    assert corridors["11-15"].total_score == 12

    assert corridors["6-10"].task_count == 1
    assert corridors["6-10"].total_score == 8

    assert corridors["1-5"].task_count == 1
    assert corridors["1-5"].total_score == 3

    assert corridors["0"].task_count == 1
    assert corridors["0"].total_score == 0

    assert corridors["no_score"].task_count == 1
    assert corridors["no_score"].scored_tasks == 0
    assert corridors["no_score"].total_score == 0

    assert summary.scored_tasks == 6
    assert summary.unscored_tasks == 1
    assert summary.total_score == 66


def test_board_summary_matches_board_metrics():
    section = create_section()

    board = create_board(
        tasks=[
            create_task(
                title="Open",
                status=TaskStatus.OPEN,
                section=section,
                score=15,
                due=date(2026, 5, 29),
            ),
            create_task(
                title="In Progress",
                status=TaskStatus.IN_PROGRESS,
                section=section,
                score=22,
            ),
            create_task(
                title="Completed",
                status=TaskStatus.COMPLETED,
                section=section,
                score=8,
            ),
            create_task(
                title="Cancelled",
                status=TaskStatus.CANCELLED,
                section=section,
                score=None,
            ),
            create_task(
                title="Paused",
                status=TaskStatus.PAUSED,
                section=section,
                score=3,
            ),
            create_task(
                title="Scheduled",
                status=TaskStatus.SCHEDULED,
                section=section,
                score=12,
            ),
            create_task(
                title="Delegated",
                status=TaskStatus.DELEGATED,
                section=section,
                score=5,
            ),
            create_task(
                title="Info",
                status=TaskStatus.INFO,
                section=section,
                score=0,
            ),
        ]
    )

    summary = build_board_summary(
        board,
        today=date(2026, 5, 30),
    )

    metrics = calculate_board_metrics(
        board,
        today=date(2026, 5, 30),
    )

    assert summary.total_tasks == metrics.total_tasks
    assert summary.active_tasks == metrics.active_tasks
    assert summary.actionable_tasks == metrics.actionable_tasks

    assert summary.completed_tasks == metrics.completed_tasks
    assert summary.cancelled_tasks == metrics.cancelled_tasks

    assert summary.overdue_tasks == metrics.overdue_tasks

    assert summary.scored_tasks == metrics.scored_tasks
    assert summary.unscored_tasks == metrics.unscored_tasks

    assert summary.total_score == metrics.total_score


def test_section_summary_metrics():
    todo = create_section(
        title="Todo",
        section_type=SectionType.QUEUED,
    )

    board = create_board(
        tasks=[
            create_task(
                title="Open",
                status=TaskStatus.OPEN,
                section=todo,
                score=10,
            ),
            create_task(
                title="In Progress",
                status=TaskStatus.IN_PROGRESS,
                section=todo,
                score=20,
            ),
            create_task(
                title="Completed",
                status=TaskStatus.COMPLETED,
                section=todo,
                score=5,
            ),
            create_task(
                title="Cancelled",
                status=TaskStatus.CANCELLED,
                section=todo,
            ),
        ]
    )

    summary = build_board_summary(board)

    section = summary.sections["Todo"]

    assert section.total_tasks == 4
    assert section.active_tasks == 2
    assert section.actionable_tasks == 2
    assert section.completed_tasks == 1
    assert section.cancelled_tasks == 1
    assert section.scored_tasks == 3
    assert section.total_score == 35


def test_section_average_score():
    todo = create_section(
        title="Todo",
        section_type=SectionType.QUEUED,
    )

    board = create_board(
        tasks=[
            create_task(
                title="A",
                status=TaskStatus.OPEN,
                section=todo,
                score=10,
            ),
            create_task(
                title="B",
                status=TaskStatus.OPEN,
                section=todo,
                score=20,
            ),
            create_task(
                title="C",
                status=TaskStatus.OPEN,
                section=todo,
            ),
        ]
    )

    summary = build_board_summary(board)

    section = summary.sections["Todo"]

    assert section.total_tasks == 3
    assert section.scored_tasks == 2
    assert section.total_score == 30
    assert section.average_score == 15.0


def test_section_average_score_without_scores():
    todo = create_section(
        title="Todo",
        section_type=SectionType.QUEUED,
    )

    board = create_board(
        tasks=[
            create_task(
                title="A",
                status=TaskStatus.OPEN,
                section=todo,
            ),
            create_task(
                title="B",
                status=TaskStatus.OPEN,
                section=todo,
            ),
        ]
    )

    summary = build_board_summary(board)

    section = summary.sections["Todo"]

    assert section.scored_tasks == 0
    assert section.total_score == 0
    assert section.average_score == 0.0
