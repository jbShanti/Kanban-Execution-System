from datetime import datetime, timedelta

from src.reporting.sections.high_five_section import (
    render_high_five_section,
)
from src.parser.models import (
    Section,
    SectionType,
    Task,
    TaskStatus,
)


def test_render_high_five_section():
    section = Section(
        title="Doing",
        raw_title="Doing",
        type=SectionType.EXECUTION,
    )

    now = datetime(2026, 5, 31, 12, 0, 0)

    tasks = [
        Task(
            title="High Priority Task",
            status=TaskStatus.OPEN,
            section=section,
            score=25,
            due=now.date(),
        ),
        Task(
            title="Medium Task",
            status=TaskStatus.IN_PROGRESS,
            section=section,
            score=15,
        ),
        Task(
            title="Low Task",
            status=TaskStatus.OPEN,
            section=section,
            score=5,
        ),
    ]

    report = render_high_five_section(tasks)

    assert "High Five" in report
    assert "High Priority Task" in report
    assert "Medium Task" in report
    assert "Low Task" in report
    assert "score: 25" in report
    assert "score: 15" in report
    assert "score: 5" in report


def test_render_high_five_section_empty():
    report = render_high_five_section([])

    assert "High Five" in report
    assert "No tasks available" in report


def test_render_high_five_section_with_due_date():
    section = Section(
        title="Doing",
        raw_title="Doing",
        type=SectionType.EXECUTION,
    )

    now = datetime(2026, 5, 31, 12, 0, 0)

    tasks = [
        Task(
            title="Due Today",
            status=TaskStatus.OPEN,
            section=section,
            score=10,
            due=now.date(),
        ),
        Task(
            title="No Due Date",
            status=TaskStatus.OPEN,
            section=section,
            score=10,
        ),
    ]

    report = render_high_five_section(tasks)

    assert "due: 2026-05-31" in report
    assert "No Due Date" in report