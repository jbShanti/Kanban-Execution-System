from datetime import date

from src.analytics.board_metrics import (
    calculate_board_metrics,
)

from src.analytics.board_summary import build_board_summary, build_section_metrics

from src.parser.models import (
    SectionType,
    TaskStatus,
)

from tests.helper import create_task, create_section, create_board

from src.analytics.models import SectionSummary, SectionMetrics

from src.analytics.section_metrics import (
    build_section_metrics_map,
)

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
    
    
def test_section_summary_matches_section_metrics():
    inbox = create_section()

    board = create_board(
        tasks=[
            create_task(
                title="Task A",
                status=TaskStatus.OPEN,
                section=inbox,
                score=10,
            ),
            create_task(
                title="Task B",
                status=TaskStatus.IN_PROGRESS,
                section=inbox,
                score=20,
            ),
            create_task(
                title="Task C",
                status=TaskStatus.COMPLETED,
                section=inbox,
                score=15,
            ),
            create_task(
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
        section=create_section(),
        summary=summary,
        wip_limit=3,
    )

    assert metrics.summary.total_tasks == 5
    assert metrics.summary.active_tasks == 2
    assert metrics.summary.average_score == 15.0
    
def test_build_section_metrics_from_summary():
    section = create_section(
        title="Todo",
        section_type=SectionType.QUEUED,
    )

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