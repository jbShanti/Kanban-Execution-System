from src.analytics.service import build_analytics_snapshot
from src.parser.models import (
    SectionType,
    TaskStatus,
    )
from tests.helper import create_section, create_task, create_board


def test_builds_analytics_snapshot():
    inbox = create_section(
        title="Inbox",
        section_type=SectionType.INBOX,
    )

    focus = create_section(
        title="Focus",
        section_type=SectionType.FOCUS,
        wip_limit=2,
    )

    tasks = [
        create_task(
            title="Open task",
            status=TaskStatus.OPEN,
            section=inbox,
            score=10,
        ),
        create_task(
            title="Completed task",
            status=TaskStatus.COMPLETED,
            section=inbox,
            score=20,
        ),
        create_task(
            title="Focused task",
            status=TaskStatus.IN_PROGRESS,
            section=focus,
            score=15,
        ),
    ]


    board = create_board(tasks=tasks)
    
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