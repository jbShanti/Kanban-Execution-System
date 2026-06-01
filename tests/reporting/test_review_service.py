from datetime import datetime, timedelta

from src.application.review_service import (
    run_review,
)
from src.parser.models import (
    Section,
    SectionType,
    Task,
    TaskStatus,
)


def test_run_review_generates_report():
    section = Section(
        title="Doing",
        raw_title="Doing",
        type=SectionType.EXECUTION,
        wip_limit=3,
        priority_weight=10,
    )

    now = datetime(
        2026,
        5,
        31,
        12,
        0,
        0,
    )

    tasks = [
        Task(
            title="Task A",
            status=TaskStatus.OPEN,
            section=section,
            score=20,
            updated_at=now - timedelta(days=40),
        ),
        Task(
            title="Task B",
            status=TaskStatus.IN_PROGRESS,
            section=section,
            score=15,
            updated_at=now - timedelta(days=2),
        ),
        Task(
            title="Task C",
            status=TaskStatus.OPEN,
            section=section,
            score=10,
            updated_at=now - timedelta(days=1),
        ),
        Task(
            title="Task D",
            status=TaskStatus.OPEN,
            section=section,
            score=5,
            updated_at=now - timedelta(days=1),
        ),
    ]

    report = run_review(
        tasks,
        now=now,
    )

    assert "# Board Health Report" in report

    assert "Health Score:" in report

    assert "Task A" in report

    assert "WIP Violations" in report

    assert "Top Priority" in report

    assert "Top Attention" in report


def test_run_review_empty_board():
    report = run_review([])

    assert "# Board Health Report" in report

    assert "Health Score: 100.0/100" in report

    assert "No warnings" in report


def test_run_review_without_wip_limits():
    section = Section(
        title="Inbox",
        raw_title="Inbox",
        type=SectionType.INBOX,
    )

    task = Task(
        title="Inbox Task",
        status=TaskStatus.OPEN,
        section=section,
    )

    report = run_review([task])

    assert "# Board Health Report" in report

    assert "Inbox Task" in report