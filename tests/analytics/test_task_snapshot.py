from datetime import date

from src.analytics.task_snapshot import build_task_snapshot
from src.parser.models import Section, Task, SectionType, TaskStatus


def test_build_snapshot_for_active_task():
    section = Section(
        title="Doing",
        raw_title="## Doing",
        type=SectionType.EXECUTION,
    )

    task = Task(
        title="Implement snapshot builder",
        status=TaskStatus.OPEN,
        section=section,
        score=5,
    )

    snapshot = build_task_snapshot(
        task=task,
        today=date(2026, 6, 14),
    )

    assert snapshot.title == "Implement snapshot builder"
    assert snapshot.section == "Doing"
    assert snapshot.status == TaskStatus.OPEN

    assert snapshot.score == 5

    assert snapshot.is_active is True
    assert snapshot.is_completed is False
    assert snapshot.is_archived is False
    assert snapshot.is_overdue is False
    
    


def test_build_snapshot_for_overdue_task():
    section = Section(
        title="Doing",
        raw_title="## Doing",
        type=SectionType.EXECUTION,
    )

    task = Task(
        title="Overdue task",
        status=TaskStatus.OPEN,
        section=section,
        due=date(2026, 6, 10),
    )

    snapshot = build_task_snapshot(
        task=task,
        today=date(2026, 6, 14),
    )

    assert snapshot.is_active is True
    assert snapshot.is_completed is False
    assert snapshot.is_overdue is True
    

def test_completed_task_is_not_overdue():
    section = Section(
        title="Done",
        raw_title="## Done",
        type=SectionType.DONE,
    )

    task = Task(
        title="Completed task",
        status=TaskStatus.COMPLETED,
        section=section,
        due=date(2026, 6, 10),
        completed_at=date(2026, 6, 12),
    )

    snapshot = build_task_snapshot(
        task=task,
        today=date(2026, 6, 14),
    )

    assert snapshot.is_completed is True
    assert snapshot.is_active is False

    assert snapshot.is_overdue is False
    
    
def test_archived_task_snapshot():
    section = Section(
        title="Archive",
        raw_title="## Archive",
        type=SectionType.ARCHIVE,
    )

    task = Task(
        title="Archived task",
        status=TaskStatus.COMPLETED,
        section=section,
        archived=True,
    )

    snapshot = build_task_snapshot(
        task=task,
        today=date(2026, 6, 14),
    )

    assert snapshot.is_archived is True
    
    
def test_build_task_snapshot_with_analytics_ignore() -> None:
    section = Section(
        title="Doing",
        raw_title="## Doing",
        type=SectionType.EXECUTION,
    )

    task = Task(
        title="Ignored task",
        status=TaskStatus.OPEN,
        section=section,
        analytics={"ignore"},
    )

    snapshot = build_task_snapshot(
        task,
        today=date(2026, 6, 19),
    )

    assert snapshot.analytics_ignore is True
    
    
def test_build_task_snapshot_without_analytics_ignore() -> None:
    section = Section(
        title="Doing",
        raw_title="## Doing",
        type=SectionType.EXECUTION,
    )

    task = Task(
        title="Normal task",
        status=TaskStatus.OPEN,
        section=section,
    )

    snapshot = build_task_snapshot(
        task,
        today=date(2026, 6, 19),
    )

    assert snapshot.analytics_ignore is False