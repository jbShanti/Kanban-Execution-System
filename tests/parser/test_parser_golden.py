from pathlib import Path
from datetime import datetime
from typing import Any, TypeAlias

from src.parser.models import (
    Section,
    Task,
    TaskStatus,
)

from src.parser.parser import (
    parse_markdown_file,
)

SerializedTask: TypeAlias = dict[str, Any]

def serialize_task(task: Task) -> SerializedTask:
    """
    Convert Task into deterministic snapshot structure.
    """

    return {
        "title": task.title,
        "status": task.status.value,

        "section": {
            "title": task.section.title,
            "raw_title": task.section.raw_title,
            "type": task.section.type.value,
            "priority_weight": task.section.priority_weight,
            "wip_limit": task.section.wip_limit,
        },

        "score": task.score,

        "due": (
            task.due.isoformat()
            if task.due is not None
            else None
        ),

        "scheduled": (
            task.scheduled.isoformat()
            if task.scheduled is not None
            else None
        ),

        "completed_at": (
            task.completed_at.isoformat()
            if task.completed_at is not None
            else None
        ),

        "updated_at": (
            task.updated_at.isoformat()
            if task.updated_at is not None
            else None
        ),

        "time_estimate": task.time_estimate,

        "tags": task.tags,

        "metadata": task.metadata,

        "archived": task.archived,
        "ignored": task.ignored,

        "raw_line": task.raw_line,
    }


def test_parse_complex_board_golden_snapshot():
    """
    Golden snapshot test for realistic board parsing.
    """

    path = Path(
        "tests/fixtures/complex_board.md"
    )

    tasks = parse_markdown_file(path)

    result: list[SerializedTask] = [
    serialize_task(task)
    for task in tasks
    ]   

    expected: list[SerializedTask] = [
        {
            "title": "Review parser architecture",
            "status": "open",

            "section": {
                "title": "Inbox",
                "raw_title": "Inbox",
                "type": "inbox",
                "priority_weight": None,
                "wip_limit": None,
            },

            "score": 15,

            "due": None,
            "scheduled": None,
            "completed_at": None,
            "updated_at": None,

            "time_estimate": None,

            "tags": [
                "Backend",
                "Parser",
        ],

            "metadata": {
                "score": "15",
            },

            "archived": False,
            "ignored": False,

            "raw_line": "- [ ] Review parser architecture #Backend #Parser [score::15]",
        },
    ]

    assert result[:1] == expected


def test_parse_pathological_board_does_not_crash():
    """
    Parser must tolerate malformed markdown
    without crashing.
    """

    path = Path(
        "tests/fixtures/pathological_board.md"
    )

    tasks = parse_markdown_file(path)

    assert isinstance(tasks, list)


def test_parse_pathological_board_extracts_valid_tasks():
    """
    Parser should still recover valid tasks
    from pathological input.
    """

    path = Path(
        "tests/fixtures/pathological_board.md"
    )

    tasks = parse_markdown_file(path)

    assert len(tasks) >= 10


def test_parsed_tasks_respect_domain_contracts():
    """
    All parsed tasks must satisfy
    domain invariants.
    """

    path = Path(
        "tests/fixtures/pathological_board.md"
    )

    tasks = parse_markdown_file(path)

    for task in tasks:

        assert isinstance(task, Task)

        assert isinstance(
            task.section,
            Section,
        )

        assert isinstance(
            task.status,
            TaskStatus,
        )

        assert isinstance(
            task.title,
            str,
        )

        assert isinstance(
            task.tags,
            list,
        )

        assert isinstance(
            task.metadata,
            dict,
        )

        assert task.section.title != ""

        if task.updated_at is not None:
            assert isinstance(
                task.updated_at,
                datetime,
            )

            assert (
                task.updated_at.tzinfo
                is not None
            )


def test_pathological_board_contains_known_tasks():
    path = Path(
        "tests/fixtures/pathological_board.md"
    )

    tasks = parse_markdown_file(path)

    titles = {
        task.title
        for task in tasks
    }

    assert "Normal task" in titles
    assert "Completed task" in titles
    assert "Emoji task 🚀" in titles

    assert "Valid task after malformed ones" in titles

    # parser successfully reaches EOF
    assert "Last valid task" in titles
    
def test_pathological_board_rejects_unsupported_syntax():
    path = Path(
        "tests/fixtures/pathological_board.md"
    )

    tasks = parse_markdown_file(path)

    titles = {
        task.title
        for task in tasks
    }

    assert "Unsupported star marker" not in titles
    assert "Unsupported plus marker" not in titles

def test_pathological_board_ignores_noise():
    path = Path(
        "tests/fixtures/pathological_board.md"
    )

    tasks = parse_markdown_file(path)

    titles = {
        task.title
        for task in tasks
    }

    assert "Bullet without checkbox" not in titles
    assert "Ordered list item" not in titles
    assert "Fake nested task" not in titles
    

def test_pathological_board_parses_unicode():
    path = Path(
        "tests/fixtures/pathological_board.md"
    )

    tasks = parse_markdown_file(path)

    titles = {
        task.title
        for task in tasks
    }

    assert "Русская задача" in titles
    assert "日本語タスク" in titles
    assert "Emoji task 🚀" in titles
    assert "Mixed unicode задача 日本語 🚀" in titles
    
    
def test_pathological_board_final_section():
    path = Path(
        "tests/fixtures/pathological_board.md"
    )

    tasks = parse_markdown_file(path)

    last_task = next(
        task
        for task in tasks
        if task.title == "Last valid task"
    )

    assert last_task.section.raw_title == "Final"
    assert last_task.score == 5