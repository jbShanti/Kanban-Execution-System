from datetime import datetime, timedelta

from src.analytics.stale_analytics import (
    calculate_stale_tasks,
)
from src.parser.models import (
    Section,
    SectionType,
    Task,
    TaskStatus,
)


def test_pipeline_stale_thresholds():
    section = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
    )

    now = datetime(2026, 5, 31, 12, 0, 0)

    healthy = Task(
        title="Healthy",
        status=TaskStatus.OPEN,
        section=section,
        updated_at=now - timedelta(days=10),
    )

    stale = Task(
        title="Stale",
        status=TaskStatus.OPEN,
        section=section,
        updated_at=now - timedelta(days=45),
    )

    critical = Task(
        title="Critical",
        status=TaskStatus.OPEN,
        section=section,
        updated_at=now - timedelta(days=120),
    )

    results = calculate_stale_tasks(
        [healthy, stale, critical],
        now=now,
    )

    assert len(results) == 2

    assert results[0].task.title == "Critical"
    assert results[0].is_stale is True
    assert results[0].is_critical is True

    assert results[1].task.title == "Stale"
    assert results[1].is_stale is True
    assert results[1].is_critical is False


def test_execution_stale_thresholds():
    section = Section(
        title="Doing",
        raw_title="Doing",
        type=SectionType.EXECUTION,
    )

    now = datetime(2026, 5, 31, 12, 0, 0)

    stale = Task(
        title="Stale",
        status=TaskStatus.IN_PROGRESS,
        section=section,
        updated_at=now - timedelta(days=10),
    )

    critical = Task(
        title="Critical",
        status=TaskStatus.IN_PROGRESS,
        section=section,
        updated_at=now - timedelta(days=45),
    )

    results = calculate_stale_tasks(
        [stale, critical],
        now=now,
    )

    assert len(results) == 2

    assert results[0].task.title == "Critical"
    assert results[0].is_critical is True

    assert results[1].task.title == "Stale"
    assert results[1].is_stale is True
    assert results[1].is_critical is False


def test_ignores_completed_tasks():
    section = Section(
        title="Doing",
        raw_title="Doing",
        type=SectionType.EXECUTION,
    )

    now = datetime(2026, 5, 31, 12, 0, 0)

    task = Task(
        title="Completed",
        status=TaskStatus.COMPLETED,
        section=section,
        updated_at=now - timedelta(days=365),
    )

    results = calculate_stale_tasks(
        [task],
        now=now,
    )

    assert len(results) == 0


def test_ignores_tasks_without_updated_at():
    section = Section(
        title="Doing",
        raw_title="Doing",
        type=SectionType.EXECUTION,
    )

    task = Task(
        title="No Update",
        status=TaskStatus.OPEN,
        section=section,
        updated_at=None,
    )

    results = calculate_stale_tasks(
        [task],
    )

    assert len(results) == 0


def test_ignores_waiting_tasks():
    section = Section(
        title="Waiting",
        raw_title="Waiting",
        type=SectionType.WAITING,
    )

    now = datetime(2026, 5, 31, 12, 0, 0)

    task = Task(
        title="Waiting task",
        status=TaskStatus.OPEN,
        section=section,
        updated_at=now - timedelta(days=365),
    )

    results = calculate_stale_tasks(
        [task],
        now=now,
    )

    assert len(results) == 0


def test_ignores_strategic_tasks():
    section = Section(
        title="Goals",
        raw_title="Goals",
        type=SectionType.STRATEGIC,
    )

    now = datetime(2026, 5, 31, 12, 0, 0)

    task = Task(
        title="Strategic task",
        status=TaskStatus.OPEN,
        section=section,
        updated_at=now - timedelta(days=365),
    )

    results = calculate_stale_tasks(
        [task],
        now=now,
    )

    assert len(results) == 0


def test_ignores_info_tasks():
    section = Section(
        title="Info",
        raw_title="Info",
        type=SectionType.INFO,
    )

    now = datetime(2026, 5, 31, 12, 0, 0)

    task = Task(
        title="Reference",
        status=TaskStatus.INFO,
        section=section,
        updated_at=now - timedelta(days=365),
    )

    results = calculate_stale_tasks(
        [task],
        now=now,
    )

    assert len(results) == 0