# tests/test_board_metrics.py

from datetime import date

from src.analytics.board_metrics import calculate_board_metrics
from src.parser.models import (
    Section,
    SectionType,
    Task,
    TaskStatus,
)


def test_calculates_basic_board_metrics():
    section = Section(
        title="Inbox",
        raw_title="Inbox",
        type=SectionType.INBOX,
    )

    tasks = [
        Task(
            title="Open",
            status=TaskStatus.OPEN,
            section=section,
            score=15,
            due=date(2026, 5, 29),
        ),
        Task(
            title="In progress",
            status=TaskStatus.IN_PROGRESS,
            section=section,
            score=22,
        ),
        Task(
            title="Completed",
            status=TaskStatus.COMPLETED,
            section=section,
            score=8,
        ),
        Task(
            title="Cancelled",
            status=TaskStatus.CANCELLED,
            section=section,
            score=None,
        ),
        Task(
            title="Paused",
            status=TaskStatus.PAUSED,
            section=section,
            score=3,
        ),
        Task(
            title="Scheduled",
            status=TaskStatus.SCHEDULED,
            section=section,
            score=12,
        ),
        Task(
            title="Delegated",
            status=TaskStatus.DELEGATED,
            section=section,
            score=5,
        ),
        Task(
            title="Info",
            status=TaskStatus.INFO,
            section=section,
            score=0,
        ),
    ]

    metrics = calculate_board_metrics(
        tasks,
        today=date(2026, 5, 30),
    )

    assert metrics.total_tasks == 8

    assert metrics.active_tasks == 2
    assert metrics.actionable_tasks == 5

    assert metrics.open_tasks == 1
    assert metrics.in_progress_tasks == 1

    assert metrics.completed_tasks == 1
    assert metrics.cancelled_tasks == 1

    assert metrics.paused_tasks == 1
    assert metrics.scheduled_tasks == 1
    assert metrics.delegated_tasks == 1
    assert metrics.info_tasks == 1

    assert metrics.overdue_tasks == 1

    assert metrics.scored_tasks == 7
    assert metrics.unscored_tasks == 1

    assert metrics.total_score == 65

    assert metrics.score_distribution == {
        "21-25": 1,
        "16-20": 0,
        "11-15": 2,
        "6-10": 1,
        "1-5": 2,
        "0": 1,
        "no_score": 1,
    }