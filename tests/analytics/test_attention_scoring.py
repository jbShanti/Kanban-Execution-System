from datetime import datetime, timedelta, date

from src.analytics.attention_scoring import (
    calculate_attention_scores,
)
from src.parser.models import (
    Section,
    SectionType,
    Task,
    TaskStatus,
)


def test_attention_score_ranks_tasks():
    section = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
    )

    now = datetime(2026, 5, 31, 12, 0, 0)

    healthy = Task(
        title="Healthy",
        status=TaskStatus.OPEN,
        section=section,
        updated_at=now - timedelta(days=2),
    )

    stale = Task(
        title="Stale",
        status=TaskStatus.OPEN,
        section=section,
        updated_at=now - timedelta(days=10),
    )

    overdue = Task(
        title="Overdue",
        status=TaskStatus.OPEN,
        section=section,
        due=date(2026, 5, 20),
    )

    results = calculate_attention_scores(
        [healthy, stale, overdue],
        now=now,
    )

    assert len(results) == 2

    assert results[0].task.title == "Overdue"
    assert results[0].final_score == 10

    assert results[1].task.title == "Stale"
    assert results[1].final_score == 1.5

   
def test_attention_score_ignores_non_actionable_tasks():
    section = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
    )

    now = datetime(2026, 5, 31, 12, 0, 0)

    completed = Task(
        title="Completed",
        status=TaskStatus.COMPLETED,
        section=section,
        updated_at=now - timedelta(days=10),
    )

    future = Task(
        title="Future",
        status=TaskStatus.OPEN,
        section=section,
        due=date(2026, 6, 30),
    )

    results = calculate_attention_scores(
        [completed, future],
        now=now,
    )

    assert len(results) == 0