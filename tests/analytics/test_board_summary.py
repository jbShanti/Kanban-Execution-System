from datetime import date

from src.analytics.board_metrics import (
    calculate_board_metrics,
)

from src.analytics.board_summary import build_board_summary

from src.parser.models import (
    Board,
    Section,
    SectionType,
    Task,
    TaskStatus,
)


def make_section(
    title: str = "Todo",
) -> Section:
    return Section(
        title=title,
        raw_title=title,
        type=SectionType.QUEUED,
    )


def test_empty_board():
    board = Board(tasks=[])

    summary = build_board_summary(board)

    assert summary.total_tasks == 0
    assert summary.active_tasks == 0
    assert summary.completed_tasks == 0
    assert summary.total_score == 0
    assert summary.average_score == 0.0


def test_counts_statuses():
    section = make_section()

    board = Board(
        tasks=[
            Task(
                title="Open",
                status=TaskStatus.OPEN,
                section=section,
            ),
            Task(
                title="Progress",
                status=TaskStatus.IN_PROGRESS,
                section=section,
            ),
            Task(
                title="Done",
                status=TaskStatus.COMPLETED,
                section=section,
            ),
            Task(
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


def test_score_distribution():
    section = make_section()

    board = Board(
        tasks=[
            Task(
                title="Critical",
                status=TaskStatus.OPEN,
                section=section,
                score=25,
            ),
            Task(
                title="High",
                status=TaskStatus.OPEN,
                section=section,
                score=18,
            ),
            Task(
                title="Medium",
                status=TaskStatus.OPEN,
                section=section,
                score=12,
            ),
            Task(
                title="Low",
                status=TaskStatus.OPEN,
                section=section,
                score=8,
            ),
            Task(
                title="Tiny",
                status=TaskStatus.OPEN,
                section=section,
                score=3,
            ),
            Task(
                title="No Score",
                status=TaskStatus.OPEN,
                section=section,
            ),
        ]
    )

    summary = build_board_summary(board)

    assert summary.scored_tasks == 5
    assert summary.unscored_tasks == 1

    assert summary.score_distribution["21-25"] == 1
    assert summary.score_distribution["16-20"] == 1
    assert summary.score_distribution["11-15"] == 1
    assert summary.score_distribution["6-10"] == 1
    assert summary.score_distribution["1-5"] == 1
    assert summary.score_distribution["no_score"] == 1


def test_overdue_detection():
    section = make_section()

    board = Board(
        tasks=[
            Task(
                title="Overdue",
                status=TaskStatus.OPEN,
                section=section,
                due=date(2026, 5, 1),
            ),
            Task(
                title="Future",
                status=TaskStatus.OPEN,
                section=section,
                due=date(2026, 7, 1),
            ),
            Task(
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
    todo = make_section("Todo")
    health = make_section("Health")

    board = Board(
        tasks=[
            Task(
                title="A",
                status=TaskStatus.OPEN,
                section=todo,
            ),
            Task(
                title="B",
                status=TaskStatus.OPEN,
                section=todo,
            ),
            Task(
                title="C",
                status=TaskStatus.OPEN,
                section=health,
            ),
        ]
    )

    summary = build_board_summary(board)

    assert summary.by_section == {
        "Todo": 2,
        "Health": 1,
    }


def test_average_score():
    section = make_section()

    board = Board(
        tasks=[
            Task(
                title="A",
                status=TaskStatus.OPEN,
                section=section,
                score=10,
            ),
            Task(
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
    
def test_board_summary_matches_board_metrics():
    section = Section(
        title="Inbox",
        raw_title="Inbox",
        type=SectionType.INBOX,
    )

    board = Board(
        tasks=[
            Task(
                title="Open",
                status=TaskStatus.OPEN,
                section=section,
                score=15,
                due=date(2026, 5, 29),
            ),
            Task(
                title="In Progress",
                status=TaskStatus.IN_PROGRESS,
                section=section,
                score=22,
            ),
            Task(
                title="Completed",
                status=TaskStatus.COMPLETED,
                section=section,
                score=8,
            ),
            Task(
                title="Cancelled",
                status=TaskStatus.CANCELLED,
                section=section,
                score=None,
            ),
            Task(
                title="Paused",
                status=TaskStatus.PAUSED,
                section=section,
                score=3,
            ),
            Task(
                title="Scheduled",
                status=TaskStatus.SCHEDULED,
                section=section,
                score=12,
            ),
            Task(
                title="Delegated",
                status=TaskStatus.DELEGATED,
                section=section,
                score=5,
            ),
            Task(
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

    assert (
        summary.score_distribution
        == metrics.score_distribution
    )