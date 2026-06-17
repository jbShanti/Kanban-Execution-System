from datetime import date

from src.parser.metadata import (
    extract_metadata,
    extract_priority,
    extract_repeat,
    extract_start_date,
    extract_tags,
    extract_due_date,
    strip_metadata,
    extract_completion_date,
)
from src.parser.models import Priority, SectionType, Section
from src.parser.parser import parse_task_line


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
    




def test_parse_scheduled_date() -> None:
    section = Section(
        title="Doing",
        raw_title="## Doing",
        type=SectionType.EXECUTION,
    )

    task = parse_task_line(
        "- [ ] Prepare report [scheduled::2026-06-20]",
        section,
    )

    assert task is not None
    assert task.scheduled == date(2026, 6, 20)
    assert task.title == "Prepare report"
    
    
def test_parse_invalid_scheduled_date() -> None:
    section = Section(
        title="Doing",
        raw_title="## Doing",
        type=SectionType.EXECUTION,
    )

    task = parse_task_line(
        "- [ ] Prepare report [scheduled::2026-99-99]",
        section,
    )

    assert task is not None
    assert task.scheduled is None
    
def test_extract_start_date() -> None:
    text = "- [ ] Task [start::2026-06-20]"

    result = extract_start_date(text)

    assert result == date(2026, 6, 20)
    
def test_parse_start_date() -> None:
    section = Section(
        title="Doing",
        raw_title="## Doing",
        type=SectionType.EXECUTION,
    )

    task = parse_task_line(
        "- [ ] Prepare report [start::2026-06-20]",
        section,
    )

    assert task is not None
    assert task.start == date(2026, 6, 20)
    assert task.title == "Prepare report"
    
def test_extract_completion_date() -> None:
    text = "- [x] Task [completion::2026-06-20]"

    result = extract_completion_date(text)

    assert result == date(2026, 6, 20)
    
def test_parse_completion_date() -> None:
    section = Section(
        title="Done",
        raw_title="## Done",
        type=SectionType.DONE,
    )

    task = parse_task_line(
        "- [x] Release feature [completion::2026-06-20]",
        section,
    )

    assert task is not None
    assert task.completed_at == date(2026, 6, 20)
    assert task.title == "Release feature"
    
def test_extract_priority() -> None:
    text = "- [ ] Task [priority::high]"

    result = extract_priority(text)

    assert result == Priority.HIGH
    
    
def test_parse_priority() -> None:
    section = Section(
        title="Doing",
        raw_title="## Doing",
        type=SectionType.EXECUTION,
    )

    task = parse_task_line(
        "- [ ] Prepare report [priority::high]",
        section,
    )

    assert task is not None
    assert task.priority == Priority.HIGH
    assert task.title == "Prepare report"
    
    
def test_extract_repeat() -> None:
    text = "- [ ] Weekly review [repeat::every week]"

    result = extract_repeat(text)

    assert result == "every week"

def test_parse_repeat() -> None:
    section = Section(
        title="Doing",
        raw_title="## Doing",
        type=SectionType.EXECUTION,
    )

    task = parse_task_line(
        "- [ ] Weekly review [repeat::every week]",
        section,
    )

    assert task is not None
    assert task.repeat == "every week"
    assert task.title == "Weekly review"