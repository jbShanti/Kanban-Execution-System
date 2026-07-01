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
    TaskStatus,
)

from tests.helper import create_task



def test_count_completed_tasks():
    tasks = [
        create_task(
            title="Task 1",
            status=TaskStatus.COMPLETED,
            section_title="Inbox",
        ),
        create_task(
            title="Task 2",
            status=TaskStatus.OPEN,
            section_title="Inbox",
        ),
    ]

    result = count_completed_tasks(tasks)

    assert result == 1


def test_count_open_tasks():
    tasks = [
        create_task(
            title="Task 1",
            status=TaskStatus.OPEN,
            section_title="Inbox",
        ),
        create_task(
            title="Task 2",
            status=TaskStatus.IN_PROGRESS,
            section_title="Inbox",
        ),
        create_task(
            title="Task 3",
            status=TaskStatus.COMPLETED,
            section_title="Inbox",
        ),
    ]

    result = count_open_tasks(tasks)

    assert result == 2


def test_group_tasks_by_section():
    tasks = [
        create_task(
            title="Task 1",
            status=TaskStatus.OPEN,
            section_title="Inbox",
        ),
        create_task(
            title="Task 2",
            status=TaskStatus.OPEN,
            section_title="Today",
        ),
        create_task(
            title="Task 3",
            status=TaskStatus.COMPLETED,
            section_title="Inbox",
        ),
    ]

    result = group_tasks_by_section(tasks)

    assert len(result["Inbox"]) == 2
    assert len(result["Today"]) == 1



def test_find_overdue_tasks():
    tasks = [
        create_task(
            title="Old task",
            status=TaskStatus.OPEN,
            section_title="Inbox",
            due=date(2025, 1, 1),
        ),
        create_task(
            title="Future task",
            status=TaskStatus.OPEN,
            section_title="Inbox",
            due=date(2099, 1, 1),
        ),
        create_task(
            title="Completed task",
            status=TaskStatus.COMPLETED,
            section_title="Inbox",
            due=date(2025, 1, 1),
        ),
    ]

    result = find_overdue_tasks(tasks)

    assert len(result) == 1
    assert result[0].title == "Old task"


def test_calculate_total_score():
    tasks = [
        create_task(
            title="Task 1",
            status=TaskStatus.OPEN,
            section_title="Inbox",
            score=10,
        ),
        create_task(
            title="Task 2",
            status=TaskStatus.OPEN,
            section_title="Inbox",
            score=25,
        ),
        create_task(
            title="Task 3",
            status=TaskStatus.OPEN,
            section_title="Inbox",
        ),
    ]

    result = calculate_total_score(tasks)

    assert result == 35


def test_calculate_section_scores():
    tasks = [
        create_task(
            title="Task 1",
            status=TaskStatus.OPEN,
            section_title="Inbox",
            score=10,
        ),
        create_task(
            title="Task 2",
            status=TaskStatus.OPEN,
            section_title="Inbox",
            score=20,
        ),
        create_task(
            title="Task 3",
            status=TaskStatus.OPEN,
            section_title="Today",
            score=50,
        ),
    ]

    result = calculate_section_scores(tasks)

    assert result["Inbox"] == 30
    assert result["Today"] == 50


def test_find_high_score_tasks():
    tasks = [
        create_task(
            title="Low",
            status=TaskStatus.OPEN,
            section_title="Inbox",
            score=10,
        ),
        create_task(
            title="High",
            status=TaskStatus.OPEN,
            section_title="Inbox",
            score=80,
        ),
    ]

    result = find_high_score_tasks(tasks, threshold=50)

    assert len(result) == 1
    assert result[0].title == "High"


def test_find_tasks_without_dates():
    tasks = [
        create_task(
            title="Undated",
            status=TaskStatus.OPEN,
            section_title="Inbox",
        ),
        create_task(
            title="Scheduled",
            status=TaskStatus.OPEN,
            section_title="Inbox",
            scheduled=date(2026, 1, 1),
        ),
        create_task(
            title="Completed",
            status=TaskStatus.COMPLETED,
            section_title="Inbox",
        ),
    ]

    result = find_tasks_without_dates(tasks)

    assert len(result) == 1
    assert result[0].title == "Undated"


def test_calculate_completion_rate():
    tasks = [
        create_task(
            title="Task 1",
            status=TaskStatus.COMPLETED,
            section_title="Inbox",
        ),
        create_task(
            title="Task 2",
            status=TaskStatus.OPEN,
            section_title="Inbox",
        ),
    ]

    result = calculate_completion_rate(tasks)

    assert result == 0.5


def test_find_empty_sections():
    tasks = [
        create_task(
            title="Task 1",
            status=TaskStatus.OPEN,
            section_title="Inbox",
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