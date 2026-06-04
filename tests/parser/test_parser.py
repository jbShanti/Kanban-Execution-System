from pathlib import Path

from src.parser.parser import (
    parse_markdown_file,
    is_section_header
)

from src.parser.models import (
    Board,
    Section,
    SectionType,
    Task,
    TaskStatus,
)


def test_parse_markdown_file():
    path = Path(
        "tests/fixtures/simple_board.md"
    )

    tasks = parse_markdown_file(path).tasks

    assert len(tasks) == 4

    assert tasks[0].title == "Review parser"
    assert tasks[0].section.raw_title == "Inbox"
    assert tasks[0].score == 15

    assert tasks[1].status.value == "completed"

    assert tasks[2].due is not None

    assert tasks[3].section.raw_title == "Waiting"
    assert tasks[3].status.value == "delegated"
    
from datetime import timedelta

import pytest

from src.parser.parser import parse_duration


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("15m", timedelta(minutes=15)),
        ("90m", timedelta(minutes=90)),
        ("2h", timedelta(hours=2)),
        ("1.5h", timedelta(minutes=90)),
        ("1h30m", timedelta(minutes=90)),
    ],
)
def test_parse_duration(
    value: str,
    expected: timedelta,
) -> None:
    assert parse_duration(value) == expected
    

from datetime import timedelta
from src.parser.parser import parse_duration

def test_parse_duration_min_suffix():
    assert parse_duration("10min") == timedelta(minutes=10)
    
def test_parse_duration_plain_minutes():
    assert parse_duration("120") == timedelta(minutes=120)
    
def test_parse_duration_continuous():
    assert parse_duration("continuous") is None
    
def test_parse_duration_arbitrary_text_returns_none():
    assert parse_duration("foobar") is None
    
    

def test_board_sections_returns_unique_sections():
    inbox = Section(
        title="Inbox",
        raw_title="Inbox",
        type=SectionType.INBOX,
    )

    focus = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
    )

    board = Board(
        tasks=[
            Task(
                title="Task 1",
                status=TaskStatus.OPEN,
                section=inbox,
            ),
            Task(
                title="Task 2",
                status=TaskStatus.OPEN,
                section=inbox,
            ),
            Task(
                title="Task 3",
                status=TaskStatus.OPEN,
                section=focus,
            ),
        ]
    )

    sections = board.sections

    assert len(sections) == 2
    assert {s.title for s in sections} == {
        "Inbox",
        "Focus",
    }
    
    
def test_detect_section_header():
    assert is_section_header(
        "## Inbox"
    )


def test_single_hash_is_not_section():
    assert not is_section_header(
        "# Inbox"
    )


def test_triple_hash_is_not_section():
    assert not is_section_header(
        "### Inbox"
    )


def test_hashtag_is_not_section():
    assert not is_section_header(
        "#Health/Physical"
    )


def test_indented_hashtag_is_not_section():
    assert not is_section_header(
        "    #Health/Physical"
    )