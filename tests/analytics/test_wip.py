from src.analytics.wip import (
    WIP_LIMITS,
    calculate_wip_pressure,
    count_tasks_by_section_type,
    detect_wip_violations,
    is_wip_overloaded,
    calculate_stale_ratio,
    detect_stale_tasks,
)

from src.parser.models import (
    SectionType,
    Task,
    TaskStatus,
)

from datetime import UTC, datetime, timedelta

from src.parser.section_parser import build_section

def build_task(
    title: str,
    status: TaskStatus,
    section_type: SectionType,
) -> Task:

    section = build_section(
        f"{section_type.value.upper()} [P::3] (5)",
        section_type,
    )

    return Task(
        title=title,
        status=status,

        section=section,


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
        build_task(
            "Critical task",
            TaskStatus.OPEN,
            SectionType.TACTICAL,
        ),
        build_task(
            "Execution task",
            TaskStatus.IN_PROGRESS,
            SectionType.EXECUTION,
        ),
        build_task(
            "Waiting task",
            TaskStatus.DELEGATED,
            SectionType.WAITING,
        ),
        build_task(
            "Completed task",
            TaskStatus.COMPLETED,
            SectionType.DONE,
        ),
    ]

    result = count_tasks_by_section_type(tasks)

    assert result == {
        SectionType.TACTICAL: 1,
        SectionType.EXECUTION: 1,
        SectionType.WAITING: 1,
    }


def test_count_wip_tasks_empty():
    result = count_tasks_by_section_type([])

    assert result == {}


def test_get_wip_by_section():
    tasks = [
        build_task(
            "Critical task 1",
            TaskStatus.OPEN,
            SectionType.TACTICAL,
        ),
        build_task(
            "Critical task 2",
            TaskStatus.OPEN,
            SectionType.TACTICAL,
        ),
        build_task(
            "Execution task",
            TaskStatus.IN_PROGRESS,
            SectionType.EXECUTION,
        ),
        build_task(
            "Waiting task",
            TaskStatus.DELEGATED,
            SectionType.WAITING,
        ),
        build_task(
            "Done task",
            TaskStatus.COMPLETED,
            SectionType.DONE,
        ),
    ]

    result = count_tasks_by_section_type(tasks)

    assert result[SectionType.TACTICAL] == 2
    assert result[SectionType.EXECUTION] == 1
    assert result[SectionType.WAITING] == 1

    assert SectionType.DONE not in result


def test_get_wip_by_section_empty():
    result = count_tasks_by_section_type([])

    assert result == {}
    
def test_is_wip_overloaded_returns_true_when_limit_exceeded() -> None:
    tasks = [
        Task(
            title="Task",
            section=build_section(
                "DOING [P::5] (3)",
                SectionType.EXECUTION,
            ),
            raw_line="- [ ] Task",
              status=TaskStatus.OPEN,
        )
        for _ in range(5)
    ]

    result = is_wip_overloaded(tasks)

    assert result is True
    
def test_detect_wip_violations_detects_overflow() -> None:
    tasks = [
        Task(
            title="Task",
            section=build_section(
                "DOING [P::5] (3)",
                SectionType.EXECUTION,
            ),
            raw_line="- [ ] Task",
            status=TaskStatus.OPEN,
        )
        for _    in range(5)
    ]

    result = detect_wip_violations(tasks)

    assert SectionType.EXECUTION in result
    
def test_calculate_wip_pressure_returns_float() -> None:
    tasks = [
        Task(
            title="Task",
            section=build_section(
                "DOING [P::5] (3)",
                SectionType.EXECUTION,
            ),
            raw_line="- [ ] Task",
            status=TaskStatus.OPEN,
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
    result = calculate_stale_ratio([])

    assert result == 0.0