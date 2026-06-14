from datetime import date

from src.analytics.task_snapshot import (
    build_task_snapshots,
)
from src.parser.models import (
    Board,
    Section,
    Task,
    SectionType,
    TaskStatus,
)


def test_snapshot_count_equals_task_count():
    section = Section(
        title="Doing",
        raw_title="## Doing",
        type=SectionType.EXECUTION,
    )

    tasks = [
        Task(
            title="Task 1",
            status=TaskStatus.OPEN,
            section=section,
        ),
        Task(
            title="Task 2",
            status=TaskStatus.IN_PROGRESS,
            section=section,
        ),
        Task(
            title="Task 3",
            status=TaskStatus.COMPLETED,
            section=section,
        ),
    ]

    board = Board(tasks=tasks)

    snapshots = build_task_snapshots(
        board=board,
        today=date(2026, 6, 14),
    )

    assert len(snapshots) == len(board.tasks)
    
    
def test_snapshot_titles_preserved():
    section = Section(
        title="Doing",
        raw_title="## Doing",
        type=SectionType.EXECUTION,
    )

    board = Board(
        tasks=[
            Task(
                title="First task",
                status=TaskStatus.OPEN,
                section=section,
            ),
            Task(
                title="Second task",
                status=TaskStatus.IN_PROGRESS,
                section=section,
            ),
            Task(
                title="Third task",
                status=TaskStatus.COMPLETED,
                section=section,
            ),
        ]
    )

    snapshots = build_task_snapshots(
        board=board,
        today=date(2026, 6, 14),
    )

    assert [s.title for s in snapshots] == [
        "First task",
        "Second task",
        "Third task",
    ]