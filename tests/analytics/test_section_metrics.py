from src.analytics.board_summary import build_board_summary
from src.analytics.section_metrics import build_section_metrics_map, build_section_metrics
from src.parser.models import (
    Board,
    Section,
    SectionType,
    Task,
    TaskStatus,
)

from src.analytics.models import (
    SectionSummary,
)



def test_calculates_section_metrics():
    inbox = Section(
        title="Inbox",
        raw_title="Inbox",
        type=SectionType.INBOX,
    )

    focus = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
        wip_limit=2,
    )

    tasks = [
        Task(
            title="Task 1",
            status=TaskStatus.OPEN,
            section=inbox,
            score=10,
        ),
        Task(
            title="Task 2",
            status=TaskStatus.COMPLETED,
            section=inbox,
            score=20,
        ),
        Task(
            title="Task 3",
            status=TaskStatus.IN_PROGRESS,
            section=focus,
            score=15,
        ),
        Task(
            title="Task 4",
            status=TaskStatus.DELEGATED,
            section=focus,
            score=None,
        ),
    ]

    summary = build_board_summary(Board(tasks=tasks))

    metrics = build_section_metrics_map(
        Board(tasks=tasks),
        summary.sections,
    )

    assert len(metrics) == 2

    inbox_metrics = metrics["Inbox"]

    assert inbox_metrics.total_tasks == 2
    assert inbox_metrics.active_tasks == 1
    assert inbox_metrics.actionable_tasks == 1
    assert inbox_metrics.completed_tasks == 1
    assert inbox_metrics.cancelled_tasks == 0

    assert inbox_metrics.scored_tasks == 2
    assert inbox_metrics.total_score == 30
    assert inbox_metrics.average_score == 15.0

    assert inbox_metrics.wip_limit is None
    assert inbox_metrics.wip_usage is None

    focus_metrics = metrics["Focus"]

    assert focus_metrics.total_tasks == 2
    assert focus_metrics.active_tasks == 1
    assert focus_metrics.actionable_tasks == 2
    assert focus_metrics.completed_tasks == 0
    assert focus_metrics.cancelled_tasks == 0

    assert focus_metrics.scored_tasks == 1
    assert focus_metrics.total_score == 15
    assert focus_metrics.average_score == 15.0

    assert focus_metrics.wip_limit == 2
    assert focus_metrics.wip_usage == 0.5
    


def test_build_section_metrics_uses_summary():
    section = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
        wip_limit=3,
    )

    summary = SectionSummary(
        total_tasks=5,
        active_tasks=2,
        actionable_tasks=2,
        completed_tasks=1,
        cancelled_tasks=1,
        scored_tasks=2,
        total_score=30,
    )

    metrics = build_section_metrics(
        section=section,
        summary=summary,
    )

    assert metrics.section is section
    assert metrics.summary is summary

    assert metrics.total_tasks == 5
    assert metrics.active_tasks == 2
    assert metrics.actionable_tasks == 2

    assert metrics.completed_tasks == 1
    assert metrics.cancelled_tasks == 1

    assert metrics.scored_tasks == 2
    assert metrics.total_score == 30

    assert metrics.wip_limit == 3
    
    
def test_section_metrics_match_section_summary():
    inbox = Section(
        title="Inbox",
        raw_title="Inbox",
        type=SectionType.INBOX,
    )

    board = Board(
        tasks=[
            Task(
                title="Open",
                status=TaskStatus.OPEN,
                section=inbox,
                score=10,
            ),
            Task(
                title="Completed",
                status=TaskStatus.COMPLETED,
                section=inbox,
                score=20,
            ),
        ]
    )

    summary = build_board_summary(board)

    metrics_map = build_section_metrics_map(
        board,
        summary.sections,
    )

    metrics = metrics_map["Inbox"]
    section_summary = summary.sections["Inbox"]

    assert metrics.total_tasks == section_summary.total_tasks
    assert metrics.active_tasks == section_summary.active_tasks
    assert metrics.actionable_tasks == section_summary.actionable_tasks
    assert metrics.completed_tasks == section_summary.completed_tasks
    assert metrics.cancelled_tasks == section_summary.cancelled_tasks
    assert metrics.scored_tasks == section_summary.scored_tasks
    assert metrics.total_score == section_summary.total_score
    assert metrics.average_score == section_summary.average_score
    
    
    inbox = metrics_map["Inbox"]

    assert inbox.total_tasks == summary.sections["Inbox"].total_tasks
    assert inbox.active_tasks == summary.sections["Inbox"].active_tasks
    assert inbox.scored_tasks == summary.sections["Inbox"].scored_tasks
    assert inbox.total_score == summary.sections["Inbox"].total_score