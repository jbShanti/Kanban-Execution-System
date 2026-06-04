from src.parser.analytics import (
    calculate_completion_rate,
    calculate_total_score,
    count_completed_tasks,
    count_open_tasks,
    find_high_score_tasks,
    find_overdue_tasks,
    find_tasks_without_dates,
    group_tasks_by_section,
)

from tests.helper import (
    load_test_board,
)

from src.parser.models import (
    TaskStatus,
)


def test_complex_board_parsing():


    tasks = load_test_board("complex_board.md").tasks

    assert len(tasks) > 10


def test_completed_tasks_detected():


    tasks = load_test_board("complex_board.md").tasks

    result = count_completed_tasks(tasks)

    assert result >= 3


def test_open_tasks_detected():


    tasks = load_test_board("complex_board.md").tasks

    result = count_open_tasks(tasks)

    assert result > 5


def test_sections_detected():


    tasks = load_test_board("complex_board.md").tasks

    grouped = group_tasks_by_section(tasks)

    assert "Inbox" in grouped
    assert "Today" in grouped
    assert "Waiting" in grouped
    assert "Deep Work" in grouped


def test_high_score_tasks_detected():


    tasks = load_test_board("complex_board.md").tasks

    result = find_high_score_tasks(
        tasks,
        threshold=200,
    )

    assert len(result) >= 2


def test_total_score_calculation():


    tasks = load_test_board("complex_board.md").tasks

    result = calculate_total_score(tasks)

    assert result > 1000


def test_overdue_detection():


    tasks = load_test_board("complex_board.md").tasks

    overdue = find_overdue_tasks(tasks)

    assert isinstance(overdue, list)


def test_tasks_without_dates():


    tasks = load_test_board("complex_board.md").tasks

    result = find_tasks_without_dates(tasks)

    assert len(result) > 0


def test_completion_rate():


    tasks = load_test_board("complex_board.md").tasks

    rate = calculate_completion_rate(tasks)

    assert 0 <= rate <= 1


def test_metadata_extraction():


    tasks = load_test_board("complex_board.md").tasks

    task = next(
        t
        for t in tasks
        if "Docker hardening" in t.title
    )

    assert task.metadata["owner"] == "Alex"


def test_tags_extraction():


    tasks = load_test_board("complex_board.md").tasks

    task = next(
        t
        for t in tasks
        if "execution intelligence engine" in t.title
    )

    assert "AI" in task.tags
    assert "Execution" in task.tags


def test_status_mapping():


    tasks = load_test_board("complex_board.md").tasks

    delegated_task = next(
        t
        for t in tasks
        if "Docker hardening" in t.title
    )

    assert delegated_task.status == TaskStatus.DELEGATED


def test_malformed_lines_ignored():


    tasks = load_test_board("complex_board.md").tasks

    titles = [
        task.title
        for task in tasks
    ]

    assert (
        "This line should be ignored completely"
        not in titles
    )

    assert (
        "invalid markdown task"
        not in titles
    )
    
def test_unicode_tags():


    tasks = load_test_board("complex_board.md").tasks

    task = next(
        t
        for t in tasks
        if "Unicode tags task" in t.title
    )

    assert "ИИ" in task.tags
    assert "Разработка" in task.tags
    assert "Execution" in task.tags


def test_malformed_dates():


    tasks = load_test_board("complex_board.md").tasks

    task = next(
        t
        for t in tasks
        if "Malformed date task" in t.title
    )

    assert task.due is None


def test_nested_tasks():


    tasks = load_test_board("complex_board.md").tasks

    titles = [
        task.title
        for task in tasks
    ]

    assert (
        "Nested subtask level 1"
        in titles
    )

    assert (
        "Completed nested subtask"
        in titles
    )

    assert (
        "Deep nested subtask"
        in titles
    )


def test_duplicate_metadata():


    tasks = load_test_board("complex_board.md").tasks

    task = next(
        t
        for t in tasks
        if "Duplicate metadata test" in t.title
    )

    assert task.metadata["score"] == "10"


def test_empty_sections():


    tasks = load_test_board("complex_board.md").tasks

    grouped = group_tasks_by_section(tasks)

    assert "Empty Section" not in grouped

    assert (
        "Another Empty Section"
        in grouped
    )