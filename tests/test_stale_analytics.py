from datetime import datetime, timedelta

from src.analytics.stale_analytics import analyze_stale_tasks
from src.parser.models import (
    Section,
    SectionType,
    Task,
    TaskStatus,
)


def test_detects_stale_and_critical_tasks():
    section = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
    )

    now = datetime(2026, 5, 31, 12, 0, 0)

    healthy_task = Task(
        title="Healthy",
        status=TaskStatus.OPEN,
        section=section,
        updated_at=now - timedelta(days=3),
    )

    stale_task = Task(
        title="Stale",
        status=TaskStatus.OPEN,
        section=section,
        updated_at=now - timedelta(days=10),
    )

    critical_task = Task(
        title="Critical",
        status=TaskStatus.IN_PROGRESS,
        section=section,
        updated_at=now - timedelta(days=45),
    )

    completed_task = Task(
        title="Completed",
        status=TaskStatus.COMPLETED,
        section=section,
        updated_at=now - timedelta(days=90),
    )

    results = analyze_stale_tasks(
        [
            healthy_task,
            stale_task,
            critical_task,
            completed_task,
        ],
        now=now,
    )

    assert len(results) == 3

    assert results[0].task.title == "Critical"
    assert results[0].age_days == 45
    assert results[0].is_stale is True
    assert results[0].is_critical is True

    assert results[1].task.title == "Stale"
    assert results[1].age_days == 10
    assert results[1].is_stale is True
    assert results[1].is_critical is False

    assert results[2].task.title == "Healthy"
    assert results[2].age_days == 3
    assert results[2].is_stale is False
    assert results[2].is_critical is False
    
def test_ignores_tasks_without_updated_timestamp():
    section = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
    )

    task = Task(
        title="Unknown age",
        status=TaskStatus.OPEN,
        section=section,
    )

    results = analyze_stale_tasks([task])

    assert results == []

def test_ignores_inactive_tasks():
    section = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
    )

    now = datetime(2026, 5, 31, 12, 0, 0)

    completed_task = Task(
        title="Completed",
        status=TaskStatus.COMPLETED,
        section=section,
        updated_at=now - timedelta(days=90),
    )

    cancelled_task = Task(
        title="Cancelled",
        status=TaskStatus.CANCELLED,
        section=section,
        updated_at=now - timedelta(days=90),
    )

    results = analyze_stale_tasks([completed_task, cancelled_task], now=now)

    assert results == []
    