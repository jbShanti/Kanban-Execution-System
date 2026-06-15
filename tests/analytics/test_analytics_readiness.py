
from src.analytics.analytics_readiness import build_board_health
from src.analytics.models import AnalyticsTaskSnapshot, BoardHealthStatus
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
    
    
def test_missing_tag_count() -> None:

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
            score=10,
            tags=(),
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
    assert health.missing_tag == 1
    
    
def test_orphan_tasks_count() -> None:

    snapshots = [
        AnalyticsTaskSnapshot(
            title="Healthy Task",
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
            title="Missing Score",
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
        AnalyticsTaskSnapshot(
            title="Missing Tag",
            section="Doing",
            status=TaskStatus.OPEN,
            score=10,
            tags=(),
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

    assert health.total_tasks == 3
    assert health.orphan_tasks == 2
    
    
def test_score_coverage() -> None:

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

    assert health.score_coverage == 0.5
    
    
def test_tag_coverage() -> None:

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
            score=10,
            tags=(),
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

    assert health.tag_coverage == 0.5
    
    
    
def test_analytics_coverage() -> None:

    snapshots = [
        AnalyticsTaskSnapshot(
            title="Healthy",
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
            title="Missing Score",
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
        AnalyticsTaskSnapshot(
            title="Missing Tag",
            section="Doing",
            status=TaskStatus.OPEN,
            score=10,
            tags=(),
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

    assert health.analytics_coverage == (1 / 3)
    
    
def test_board_health_status_excellent() -> None:

    snapshots = [
        AnalyticsTaskSnapshot(
            title="Healthy Task",
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
    ]

    health = build_board_health(snapshots)

    assert health.analytics_coverage == 1.0
    assert health.status == BoardHealthStatus.EXCELLENT