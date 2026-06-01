from pathlib import Path

from src.parser.parser import (
    parse_markdown_file,
)


def test_parse_markdown_file():
    path = Path(
        "tests/fixtures/simple_board.md"
    )

    tasks = parse_markdown_file(path)

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