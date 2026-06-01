from src.analytics.section_metrics import calculate_section_metrics
from src.parser.models import (
    Board,
    Section,
    SectionType,
    Task,
    TaskStatus,
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

    metrics = calculate_section_metrics(Board(tasks=tasks))

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