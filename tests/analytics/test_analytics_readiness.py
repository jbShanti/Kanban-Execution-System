
from src.analytics.analytics_readiness import build_board_health
from src.analytics.models import AnalyticsTaskSnapshot
from src.parser.models import TaskStatus


def test_missing_score_count() -> None:

    snapshots = [
        AnalyticsTaskSnapshot(
            title="Task A",
            section="Doing",
            status=TaskStatus.OPEN,
            score=10,
            tags=("work",),
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        AnalyticsTaskSnapshot(
            title="Task B",
            section="Doing",
            status=TaskStatus.OPEN,
            score=None,
            tags=("work",),
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
    ]

    health = build_board_health(snapshots)

    assert health.total_tasks == 2
    assert health.missing_score == 1