from datetime import date

from src.parser.analytics import (
    calculate_completion_rate,
    calculate_section_scores,
    calculate_total_score,
    count_completed_tasks,
    count_open_tasks,
    find_empty_sections,
    find_high_score_tasks,
    find_overdue_tasks,
    find_tasks_without_dates,
    group_tasks_by_section,
)

from src.parser.models import (
    Task,
    TaskStatus,
)

from tests.helper import create_section

def build_task(
    title: str,
    status: TaskStatus,
    section: str,
    score: int | None = None,
    due: date | None = None,
    scheduled: date | None = None,
) -> Task:
    return Task(
        title=title,
        status=status,
        section=create_section(title=section),
        score=score,
        due=due,
        scheduled=scheduled,
        tags=[],
        metadata={},
        raw_line=title,
    )


def test_count_completed_tasks():
    tasks = [
        build_task(
            "Task 1",
            TaskStatus.COMPLETED,
            "Inbox",
        ),
        build_task(
            "Task 2",
            TaskStatus.OPEN,
            "Inbox",
        ),
    ]

    result = count_completed_tasks(tasks)

    assert result == 1


def test_count_open_tasks():
    tasks = [
        build_task(
            "Task 1",
            TaskStatus.OPEN,
            "Inbox",
        ),
        build_task(
            "Task 2",
            TaskStatus.IN_PROGRESS,
            "Inbox",
        ),
        build_task(
            "Task 3",
            TaskStatus.COMPLETED,
            "Inbox",
        ),
    ]

    result = count_open_tasks(tasks)

    assert result == 2


def test_group_tasks_by_section():
    tasks = [
        build_task(
            "Task 1",
            TaskStatus.OPEN,
            "Inbox",
        ),
        build_task(
            "Task 2",
            TaskStatus.OPEN,
            "Today",
        ),
        build_task(
            "Task 3",
            TaskStatus.COMPLETED,
            "Inbox",
        ),
    ]
    
    result = group_tasks_by_section(tasks)

    assert len(result["Inbox"]) == 2
    assert len(result["Today"]) == 1



def test_find_overdue_tasks():
    tasks = [
        build_task(
            "Old task",
            TaskStatus.OPEN,
            "Inbox",
            due=date(2025, 1, 1),
        ),
        build_task(
            "Future task",
            TaskStatus.OPEN,
            "Inbox",
            due=date(2099, 1, 1),
        ),
        build_task(
            "Completed task",
            TaskStatus.COMPLETED,
            "Inbox",
            due=date(2025, 1, 1),
        ),
    ]

    result = find_overdue_tasks(tasks)

    assert len(result) == 1
    assert result[0].title == "Old task"


def test_calculate_total_score():
    tasks = [
        build_task(
            "Task 1",
            TaskStatus.OPEN,
            "Inbox",
            score=10,
        ),
        build_task(
            "Task 2",
            TaskStatus.OPEN,
            "Inbox",
            score=25,
        ),
        build_task(
            "Task 3",
            TaskStatus.OPEN,
            "Inbox",
        ),
    ]

    result = calculate_total_score(tasks)

    assert result == 35


def test_calculate_section_scores():
    tasks = [
        build_task(
            "Task 1",
            TaskStatus.OPEN,
            "Inbox",
            score=10,
        ),
        build_task(
            "Task 2",
            TaskStatus.OPEN,
            "Inbox",
            score=20,
        ),
        build_task(
            "Task 3",
            TaskStatus.OPEN,
            "Today",
            score=50,
        ),
    ]

    result = calculate_section_scores(tasks)

    assert result["Inbox"] == 30
    assert result["Today"] == 50


def test_find_high_score_tasks():
    tasks = [
        build_task(
            "Low",
            TaskStatus.OPEN,
            "Inbox",
            score=10,
        ),
        build_task(
            "High",
            TaskStatus.OPEN,
            "Inbox",
            score=80,
        ),
    ]

    result = find_high_score_tasks(
        tasks,
        threshold=50,
    )

    assert len(result) == 1
    assert result[0].title == "High"


def test_find_tasks_without_dates():
    tasks = [
        build_task(
            "Undated",
            TaskStatus.OPEN,
            "Inbox",
        ),
        build_task(
            "Scheduled",
            TaskStatus.OPEN,
            "Inbox",
            scheduled=date(2026, 1, 1),
        ),
        build_task(
            "Completed",
            TaskStatus.COMPLETED,
            "Inbox",
        ),
    ]

    result = find_tasks_without_dates(tasks)

    assert len(result) == 1
    assert result[0].title == "Undated"


def test_calculate_completion_rate():
    tasks = [
        build_task(
            "Task 1",
            TaskStatus.COMPLETED,
            "Inbox",
        ),
        build_task(
            "Task 2",
            TaskStatus.OPEN,
            "Inbox",
        ),
    ]

    result = calculate_completion_rate(tasks)

    assert result == 0.5


def test_find_empty_sections():
    tasks = [
        build_task(
            "Task 1",
            TaskStatus.OPEN,
            "Inbox",
        ),
    ]

    known_sections = [
        "Inbox",
        "Today",
        "Waiting",
    ]

    result = find_empty_sections(
        tasks,
        known_sections,
    )

    assert "Today" in result
    assert "Waiting" in result
    assert "Inbox" not in result