from datetime import date

from src.analytics.board_metrics import (
    calculate_board_metrics,
)

from src.analytics.board_summary import build_board_summary, build_section_metrics

from src.parser.models import (
    Board,
    Section,
    SectionType,
    Task,
    TaskStatus,
)

from src.analytics.models import SectionSummary, SectionMetrics

from src.analytics.section_metrics import (
    build_section_metrics_map,
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

    assert set(summary.sections.keys()) == {
    "Todo",
    "Health",
    }

    assert summary.sections["Todo"].total_tasks == 2
    assert summary.sections["Health"].total_tasks == 1
    assert summary.sections["Todo"].active_tasks == 2

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

    
def test_section_summary_metrics():
    todo = make_section("Todo")

    board = Board(
        tasks=[
            Task(
                title="Open",
                status=TaskStatus.OPEN,
                section=todo,
                score=10,
            ),
            Task(
                title="In Progress",
                status=TaskStatus.IN_PROGRESS,
                section=todo,
                score=20,
            ),
            Task(
                title="Completed",
                status=TaskStatus.COMPLETED,
                section=todo,
                score=5,
            ),
            Task(
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
    todo = make_section("Todo")

    board = Board(
        tasks=[
            Task(
                title="A",
                status=TaskStatus.OPEN,
                section=todo,
                score=10,
            ),
            Task(
                title="B",
                status=TaskStatus.OPEN,
                section=todo,
                score=20,
            ),
            Task(
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
    todo = make_section("Todo")

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
        ]
    )

    summary = build_board_summary(board)

    section = summary.sections["Todo"]

    assert section.scored_tasks == 0
    assert section.total_score == 0
    assert section.average_score == 0.0
    
    
def test_section_summary_matches_section_metrics():
    inbox = Section(
        title="Inbox",
        raw_title="Inbox",
        type=SectionType.INBOX,
    )

    board = Board(
        tasks=[
            Task(
                title="Task A",
                status=TaskStatus.OPEN,
                section=inbox,
                score=10,
            ),
            Task(
                title="Task B",
                status=TaskStatus.IN_PROGRESS,
                section=inbox,
                score=20,
            ),
            Task(
                title="Task C",
                status=TaskStatus.COMPLETED,
                section=inbox,
                score=15,
            ),
            Task(
                title="Task D",
                status=TaskStatus.CANCELLED,
                section=inbox,
            ),
        ]
    )

    summary = build_board_summary(board)

    metrics = build_section_metrics_map(board, summary.sections)

    section_summary = summary.sections["Inbox"]
    section_metrics = metrics["Inbox"]

    assert section_summary.total_tasks == section_metrics.total_tasks

    assert (
        section_summary.active_tasks
        == section_metrics.active_tasks
    )

    assert (
        section_summary.actionable_tasks
        == section_metrics.actionable_tasks
    )

    assert (
        section_summary.completed_tasks
        == section_metrics.completed_tasks
    )

    assert (
        section_summary.cancelled_tasks
        == section_metrics.cancelled_tasks
    )

    assert (
        section_summary.scored_tasks
        == section_metrics.scored_tasks
    )

    assert (
        section_summary.total_score
        == section_metrics.total_score
    )

    assert (
        section_summary.average_score
        == section_metrics.average_score
    )
    
    
def test_section_metrics_uses_summary():
    summary = SectionSummary(
        total_tasks=5,
        active_tasks=2,
        scored_tasks=2,
        total_score=30,
    )

    metrics = SectionMetrics(
        section=make_section(),
        summary=summary,
        wip_limit=3,
    )

    assert metrics.summary.total_tasks == 5
    assert metrics.summary.active_tasks == 2
    assert metrics.summary.average_score == 15.0
    
def test_build_section_metrics_from_summary():
    section = make_section()

    summary = SectionSummary(
        total_tasks=5,
        active_tasks=2,
        actionable_tasks=2,
        completed_tasks=1,
        scored_tasks=2,
        total_score=30,
    )

    metrics = build_section_metrics(
        section=section,
        summary=summary,
    )

    assert metrics.section is section
    assert metrics.summary is summary
    assert metrics.wip_limit == section.wip_limit