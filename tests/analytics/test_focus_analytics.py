from datetime import date

from src.analytics.focus_analytics import (
    build_focus_attention_analytics,
)
from src.analytics.models import AnalyticsTaskSnapshot
from src.parser.models import TaskStatus


def test_build_focus_attention_analytics():
    snapshots = [
        AnalyticsTaskSnapshot(
            title="Task A",
            section="Doing",
            status=TaskStatus.OPEN,
            score=9,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=('Health',),
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        AnalyticsTaskSnapshot(
            title="Task B",
            section="Doing",
            status=TaskStatus.IN_PROGRESS,
            score=5,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=(),
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        AnalyticsTaskSnapshot(
            title="Task C",
            section="Doing",
            status=TaskStatus.OPEN,
            score=17,
            due_date=date(2026, 6, 10),
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=('AI',),
            is_active=False,
            is_completed=False,
            is_archived=False,
            is_overdue=True,
        ),
        AnalyticsTaskSnapshot(
            title="Task D",
            section="Done",
            status=TaskStatus.COMPLETED,
            score=3,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=(),
            is_active=False,
            is_completed=True,
            is_archived=False,
            is_overdue=False,
        ),
    ]

    analytics = build_focus_attention_analytics(
        snapshots=snapshots,
    )

    assert analytics.active_tasks == 2
    assert analytics.overdue_tasks == 1
    assert analytics.high_score_tasks == 1