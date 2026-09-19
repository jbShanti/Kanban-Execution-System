"""
Unit tests for multiline task parsing.

Tests cover:
- Tasks with metadata on subsequent lines
- Multiple metadata fields across lines
- Single-line tasks (unchanged behavior)
- Mixed single-line and multiline tasks
- Edge cases: empty lines, immediate next task, section headers
"""

from pathlib import Path
from datetime import date

from src.parser.parser import parse_markdown_file
from src.parser.models import TaskStatus


def test_multiline_task_with_score():
    """Task with [score::10] on the next line should be parsed correctly."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    # Find the first task in Inbox section
    task = next(t for t in board.tasks if "Task with score on next line" in t.title)
    
    assert task.score == 10
    assert task.status == TaskStatus.OPEN
    assert task.section.title == "Inbox"


def test_multiline_task_with_multiple_metadata():
    """Task with multiple metadata fields on separate lines."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    task = next(t for t in board.tasks if "Task with multiple metadata" in t.title)
    
    assert task.score == 25
    assert task.due == date(2026, 10, 15)
    assert task.priority is not None
    assert task.priority.value == "high"


def test_multiline_completed_task_with_metadata():
    """Completed task with metadata on next line."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    task = next(t for t in board.tasks if "Completed task with metadata" in t.title)
    
    assert task.score == 50
    assert task.status == TaskStatus.COMPLETED


def test_multiline_in_progress_task_with_due():
    """In-progress task with due date on next line."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    task = next(t for t in board.tasks if "In progress task with due date" in t.title)
    
    assert task.due == date(2026, 11, 1)
    assert task.status == TaskStatus.IN_PROGRESS


def test_single_line_task_unchanged():
    """Single-line tasks should work exactly as before."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    task = next(t for t in board.tasks if "Single line task with all metadata" in t.title)
    
    assert task.score == 15
    assert task.due == date(2026, 9, 20)
    assert task.priority is not None
    assert task.priority.value == "normal"


def test_task_with_metadata_then_empty_line():
    """Task with metadata followed by empty line."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    task = next(t for t in board.tasks if "Task with metadata then empty line" in t.title)
    
    assert task.score == 30


def test_mixed_single_and_multiline_tasks():
    """File with combination of single-line and multiline tasks."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    # Count tasks in Today section
    today_tasks = [t for t in board.tasks if t.section.title == "Today"]
    assert len(today_tasks) == 3
    
    # Verify all have scores
    scores = [t.score for t in today_tasks]
    assert 15 in scores
    assert 30 in scores
    assert 5 in scores


def test_delegated_task_with_metadata():
    """Delegated task with metadata on next line."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    task = next(t for t in board.tasks if "Delegated task with metadata" in t.title)
    
    assert task.score == 100
    assert task.status == TaskStatus.DELEGATED
    assert task.metadata.get("owner") == "Alex"


def test_task_followed_immediately_by_another_task():
    """Task with metadata then immediately another task (no empty line)."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    task1 = next(t for t in board.tasks if "Task followed by another task immediately" in t.title)
    task2 = next(t for t in board.tasks if "Next task starts here" in t.title)
    
    assert task1.score == 40
    assert task2.score == 60


def test_task_with_three_metadata_lines():
    """Task with three metadata lines."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    task = next(t for t in board.tasks if "Task with three metadata lines" in t.title)
    
    assert task.score == 200
    assert task.time_estimate is not None
    assert task.time_estimate.total_seconds() == 7200  # 2h
    assert task.category == "research"


def test_task_with_continuation_text_not_metadata():
    """Continuation text without metadata pattern should not be treated as metadata."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    task = next(t for t in board.tasks if "Task with metadata and then continuation text" in t.title)
    
    assert task.score == 75
    # The continuation text should not affect parsing
    assert "continuation line" not in task.title.lower()


def test_task_with_metadata_then_section_header():
    """Task with metadata followed by section header."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    task = next(t for t in board.tasks if "Task with metadata then section header" in t.title)
    
    assert task.score == 90
    assert task.section.title == "Deep Work"


def test_task_in_new_section_after_header():
    """Task in new section after section header."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    task = next(t for t in board.tasks if "Task in new section" in t.title)
    
    assert task.score == 10
    assert task.section.title == "Another Section"


def test_no_orphan_tasks():
    """All tasks with metadata on subsequent lines should NOT be orphaned (score=None)."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    # Check all tasks that should have scores
    tasks_with_expected_scores = [
        ("Task with score on next line", 10),
        ("Task with multiple metadata", 25),
        ("Completed task with metadata", 50),
        ("In progress task with due date", None),  # No score, only due
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
        task = next(t for t in board.tasks if title_fragment in t.title)
        assert task.score == expected_score, f"Task '{title_fragment}': expected score {expected_score}, got {task.score}"


def test_multiline_preserves_tags_and_links():
    """Multiline parsing should preserve tags and links from the main task line."""
    path = Path("tests/parser/fixtures/multiline_tasks.md")
    board = parse_markdown_file(path)
    
    task = next(t for t in board.tasks if "Task with score on next line" in t.title)
    
    assert "MyGoals" in task.tags
    assert "MyGoals/2026" in task.tags
    assert "MyGoals/2026/Health" in task.tags
    assert task.due == date(2026, 9, 30)