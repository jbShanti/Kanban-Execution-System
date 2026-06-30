from datetime import UTC, datetime, timedelta

from src.analytics.wip import (
    WIP_LIMITS,
    calculate_stale_ratio,
    calculate_wip_pressure,
    count_tasks_by_section_type,
    detect_stale_tasks,
    detect_wip_violations,
    is_wip_overloaded,
)
from src.parser.models import (
    SectionType,
    Task,
    TaskStatus,
)
from tests.helper import create_section


def build_task(
    title: str,
    status: TaskStatus,
    section_type: SectionType,
    *,
    priority_weight: int = 3,
    wip_limit: int = 5,
) -> Task:
    return Task(
        title=title,
        status=status,
        section=create_section(
            title=section_type.value.title(),
            section_type=section_type,
            priority_weight=priority_weight,
            wip_limit=wip_limit,
        ),
        raw_line=f"- [ ] {title}",
        archived=False,
        metadata={},
        tags=[],
        score=None,
        due=None,
        time_estimate=None,
        updated_at=datetime.now(UTC),
    )


def test_count_wip_tasks():
    tasks = [
        build_task("Critical task", TaskStatus.OPEN, SectionType.TACTICAL),
        build_task("Execution task", TaskStatus.IN_PROGRESS, SectionType.EXECUTION),
        build_task("Waiting task", TaskStatus.DELEGATED, SectionType.WAITING),
        build_task("Completed task", TaskStatus.COMPLETED, SectionType.DONE),
    ]

    result = count_tasks_by_section_type(tasks)

    assert result == {
        SectionType.TACTICAL: 1,
        SectionType.EXECUTION: 1,
        SectionType.WAITING: 1,
    }


def test_count_wip_tasks_empty():
    assert count_tasks_by_section_type([]) == {}


def test_get_wip_by_section():
    tasks = [
        build_task("Critical task 1", TaskStatus.OPEN, SectionType.TACTICAL),
        build_task("Critical task 2", TaskStatus.OPEN, SectionType.TACTICAL),
        build_task("Execution task", TaskStatus.IN_PROGRESS, SectionType.EXECUTION),
        build_task("Waiting task", TaskStatus.DELEGATED, SectionType.WAITING),
        build_task("Done task", TaskStatus.COMPLETED, SectionType.DONE),
    ]

    result = count_tasks_by_section_type(tasks)

    assert result[SectionType.TACTICAL] == 2
    assert result[SectionType.EXECUTION] == 1
    assert result[SectionType.WAITING] == 1
    assert SectionType.DONE not in result


def test_get_wip_by_section_empty():
    assert count_tasks_by_section_type([]) == {}


def test_is_wip_overloaded_returns_true_when_limit_exceeded() -> None:
    tasks = [
        build_task(
            "Task",
            TaskStatus.OPEN,
            SectionType.EXECUTION,
            priority_weight=5,
            wip_limit=3,
        )
        for _ in range(5)
    ]

    assert is_wip_overloaded(tasks) is True


def test_detect_wip_violations_detects_overflow() -> None:
    tasks = [
        build_task(
            "Task",
            TaskStatus.OPEN,
            SectionType.EXECUTION,
            priority_weight=5,
            wip_limit=3,
        )
        for _ in range(5)
    ]

    result = detect_wip_violations(tasks)

    assert SectionType.EXECUTION in result


def test_calculate_wip_pressure_returns_float() -> None:
    tasks = [
        build_task(
            "Task",
            TaskStatus.OPEN,
            SectionType.EXECUTION,
            priority_weight=5,
            wip_limit=3,
        )
    ]

    result = calculate_wip_pressure(tasks)

    assert isinstance(result, float)


def test_wip_limits_contains_execution() -> None:
    assert SectionType.EXECUTION in WIP_LIMITS


def test_detect_stale_tasks_returns_old_tasks():
    now = datetime.now(UTC)

    stale_task = build_task(
        "Old task",
        TaskStatus.OPEN,
        SectionType.EXECUTION,
    )
    stale_task.updated_at = now - timedelta(days=10)

    fresh_task = build_task(
        "Fresh task",
        TaskStatus.OPEN,
        SectionType.EXECUTION,
    )
    fresh_task.updated_at = now - timedelta(hours=12)

    result = detect_stale_tasks(
        [stale_task, fresh_task],
        now=now,
    )

    assert len(result) == 1
    assert result[0].title == "Old task"


def test_calculate_stale_ratio():
    now = datetime.now(UTC)

    stale_task = build_task(
        "Old task",
        TaskStatus.OPEN,
        SectionType.EXECUTION,
    )
    stale_task.updated_at = now - timedelta(days=10)

    fresh_task = build_task(
        "Fresh task",
        TaskStatus.OPEN,
        SectionType.EXECUTION,
    )
    fresh_task.updated_at = now

    result = calculate_stale_ratio(
        [stale_task, fresh_task],
        now=now,
    )

    assert result == 0.5


def test_calculate_stale_ratio_empty():
    assert calculate_stale_ratio([]) == 0.0