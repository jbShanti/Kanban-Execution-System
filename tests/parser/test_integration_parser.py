from datetime import date

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


from datetime import date

def test_overdue_detection():


    tasks = load_test_board("complex_board.md").tasks

    overdue = find_overdue_tasks(tasks, today=date(2026, 1, 15))

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


def test_multiline_task_parsing_integration():
    """Integration test for multiline task parsing with metadata on subsequent lines."""
    from pathlib import Path
    from src.parser.parser import parse_markdown_file
    
    tasks = parse_markdown_file(Path("tests/parser/fixtures/multiline_tasks.md")).tasks
    
    # Verify all tasks are parsed (not orphaned)
    assert len(tasks) > 10
    
    # Check specific multiline tasks
    task_with_score = next(t for t in tasks if "Task with score on next line" in t.title)
    assert task_with_score.score == 10
    assert task_with_score.due == date(2026, 9, 30)
    
    task_multiple_metadata = next(t for t in tasks if "Task with multiple metadata" in t.title)
    assert task_multiple_metadata.score == 25
    assert task_multiple_metadata.due == date(2026, 10, 15)
    assert task_multiple_metadata.priority is not None
    assert task_multiple_metadata.priority.value == "high"
    
    # Verify no tasks are orphaned (score=None when they should have score)
    tasks_with_expected_scores = [
        ("Task with score on next line", 10),
        ("Task with multiple metadata", 25),
        ("Completed task with metadata", 50),
        ("Single line task with all metadata", 15),
        ("Task with metadata then empty line", 30),
        ("Another single line task", 5),
        ("Delegated task with metadata", 100),
        ("Task followed by another task immediately", 40),
        ("Next task starts here", 60),
        ("Task with three metadata lines", 200),
        ("Task with metadata and then continuation text", 75),
        ("Task with metadata then section header", 90),
        ("Task in new section", 10),
    ]
    
    for title_fragment, expected_score in tasks_with_expected_scores:
        task = next(t for t in tasks if title_fragment in t.title)
        assert task.score == expected_score, f"Task '{title_fragment}': expected score {expected_score}, got {task.score}"


def test_multiline_tasks_not_marked_as_orphan():
    """Ensure multiline tasks with metadata are not treated as orphan (score=None)."""
    from pathlib import Path
    from src.parser.parser import parse_markdown_file
    
    tasks = parse_markdown_file(Path("tests/parser/fixtures/multiline_tasks.md")).tasks
    
    # All tasks that have score metadata should have score != None
    for task in tasks:
        if "score" in task.metadata:
            assert task.score is not None, f"Task '{task.title}' has score in metadata but score is None"