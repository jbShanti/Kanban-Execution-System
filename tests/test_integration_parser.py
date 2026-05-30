from pathlib import Path

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

from src.parser.parser import (
    parse_markdown_file,
)

from src.parser.models import (
    TaskStatus,
)


def test_complex_board_parsing():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    assert len(tasks) > 10


def test_completed_tasks_detected():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    result = count_completed_tasks(tasks)

    assert result >= 3


def test_open_tasks_detected():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    result = count_open_tasks(tasks)

    assert result > 5


def test_sections_detected():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    grouped = group_tasks_by_section(tasks)

    assert "Inbox" in grouped
    assert "Today" in grouped
    assert "Waiting" in grouped
    assert "Deep Work" in grouped


def test_high_score_tasks_detected():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    result = find_high_score_tasks(
        tasks,
        threshold=200,
    )

    assert len(result) >= 2


def test_total_score_calculation():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    result = calculate_total_score(tasks)

    assert result > 1000


def test_overdue_detection():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    overdue = find_overdue_tasks(tasks)

    assert isinstance(overdue, list)


def test_tasks_without_dates():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    result = find_tasks_without_dates(tasks)

    assert len(result) > 0


def test_completion_rate():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    rate = calculate_completion_rate(tasks)

    assert 0 <= rate <= 1


def test_metadata_extraction():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    task = next(
        t
        for t in tasks
        if "Docker hardening" in t.title
    )

    assert task.metadata["owner"] == "Alex"


def test_tags_extraction():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    task = next(
        t
        for t in tasks
        if "execution intelligence engine" in t.title
    )

    assert "AI" in task.tags
    assert "Execution" in task.tags


def test_status_mapping():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    delegated_task = next(
        t
        for t in tasks
        if "Docker hardening" in t.title
    )

    assert delegated_task.status == TaskStatus.DELEGATED


def test_malformed_lines_ignored():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

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
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    task = next(
        t
        for t in tasks
        if "Unicode tags task" in t.title
    )

    assert "ИИ" in task.tags
    assert "Разработка" in task.tags
    assert "Execution" in task.tags


def test_malformed_dates():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    task = next(
        t
        for t in tasks
        if "Malformed date task" in t.title
    )

    assert task.due is None


def test_nested_tasks():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

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
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    task = next(
        t
        for t in tasks
        if "Duplicate metadata test" in t.title
    )

    assert task.metadata["score"] == "10"


def test_empty_sections():
    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    grouped = group_tasks_by_section(tasks)

    assert "Empty Section" not in grouped

    assert (
        "Another Empty Section"
        in grouped
    )