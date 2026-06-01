from src.analytics.analytics_service import build_analytics_snapshot
from src.parser.models import (
    Section,
    SectionType,
    Task,
    TaskStatus,
    Board,
)


def test_builds_analytics_snapshot():
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
            title="Open task",
            status=TaskStatus.OPEN,
            section=inbox,
            score=10,
        ),
        Task(
            title="Completed task",
            status=TaskStatus.COMPLETED,
            section=inbox,
            score=20,
        ),
        Task(
            title="Focused task",
            status=TaskStatus.IN_PROGRESS,
            section=focus,
            score=15,
        ),
    ]


    board = Board(tasks=tasks)
    
    snapshot = build_analytics_snapshot(board)

    assert snapshot.board.total_tasks == 3
    assert snapshot.board.active_tasks == 2
    assert snapshot.board.completed_tasks == 1

    assert len(snapshot.sections) == 2

    inbox_metrics = snapshot.sections["Inbox"]

    assert inbox_metrics.total_tasks == 2
    assert inbox_metrics.completed_tasks == 1
    assert inbox_metrics.total_score == 30

    focus_metrics = snapshot.sections["Focus"]

    assert focus_metrics.total_tasks == 1
    assert focus_metrics.active_tasks == 1
    assert focus_metrics.total_score == 15