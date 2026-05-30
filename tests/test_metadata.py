from datetime import date

from src.parser.metadata import (
    extract_metadata,
    extract_tags,
    extract_due_date,
    strip_metadata,
)


def test_extract_metadata():
    text = "- [ ] Task [score::15] [time::30m]"

    result = extract_metadata(text)

    assert result["score"] == "15"
    assert result["time"] == "30m"


def test_extract_tags():
    text = "#Health #Projects/AI"

    result = extract_tags(text)

    assert "Health" in result
    assert "Projects/AI" in result


def test_extract_due_date():
    text = "- [ ] Task @{2026-05-30}"

    result = extract_due_date(text)

    assert result == date(2026, 5, 30)


def test_strip_metadata():
    text = "- [ ] Review [[Parser]] #AI @{2026-05-30} [score::15]"

    result = strip_metadata(text)

    assert result == "Review Parser"