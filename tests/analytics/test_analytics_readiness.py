
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
            effective_score=10,
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
            effective_score=0,
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
            effective_score=10,
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
            effective_score=10,
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
            effective_score=10,
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
            effective_score=0,
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
            effective_score=10,
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
            effective_score=10,
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
            effective_score=0,
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
            effective_score=10,
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
            effective_score=10,
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
            effective_score=10,
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
            effective_score=0,
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
            effective_score=10,
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
                effective_score=10,
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
        
    
    
    
import pytest

from src.analytics.analytics_readiness import (
    evaluate_board_health_status,
)


@pytest.mark.parametrize(
    ("coverage", "expected"),
    [
        (1.00, BoardHealthStatus.EXCELLENT),
        (0.99, BoardHealthStatus.EXCELLENT),

        (0.91, BoardHealthStatus.GOOD),

        (0.76, BoardHealthStatus.WARNING),

        (0.51, BoardHealthStatus.POOR),

        (0.26, BoardHealthStatus.AWFUL),

        (0.25, BoardHealthStatus.CRITICAL),
        (0.00, BoardHealthStatus.CRITICAL),
    ],
)
def test_evaluate_board_health_status(
    coverage: float,
    expected: BoardHealthStatus,
) -> None:

    assert (
        evaluate_board_health_status(coverage)
        == expected
    )
    
@pytest.mark.parametrize(
    ("coverage", "expected"),
    [
        (0.99, BoardHealthStatus.EXCELLENT),

        (0.90, BoardHealthStatus.WARNING),

        (0.75, BoardHealthStatus.POOR),

        (0.50, BoardHealthStatus.AWFUL),

        (0.25, BoardHealthStatus.CRITICAL),
    ],
)
def test_board_health_status_boundaries(
    coverage: float,
    expected: BoardHealthStatus,
) -> None:

    assert (
        evaluate_board_health_status(coverage)
        == expected
    )
    
    
def test_sample_orphans_prioritization() -> None:

    snapshots = [
        AnalyticsTaskSnapshot(
            title="Missing Score",
            section="Doing",
            status=TaskStatus.OPEN,
            score=None,
            effective_score=0,
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
            effective_score=10,
            tags=(),
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        AnalyticsTaskSnapshot(
            title="Missing Score And Tag",
            section="Doing",
            status=TaskStatus.OPEN,
            score=None,
            effective_score=0,
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

    assert len(health.sample_orphans) == 3

    assert (
        health.sample_orphans[0].title
        == "Missing Score And Tag"
    )

    assert (
        health.sample_orphans[1].title
        == "Missing Tag"
    )

    assert (
        health.sample_orphans[2].title
        == "Missing Score"
    )
    

  
def test_sample_orphans_is_limited_to_top_five() -> None:

    snapshots = [
        AnalyticsTaskSnapshot(
            title=f"Orphan {index}",
            section="Doing",
            status=TaskStatus.OPEN,
            score=None,
            effective_score=0,
            tags=(),
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        )
        for index in range(1, 7)
    ]

    health = build_board_health(snapshots)

    assert len(health.sample_orphans) == 5

    assert tuple(
        orphan.title
        for orphan in health.sample_orphans
    ) == (
        "Orphan 1",
        "Orphan 2",
        "Orphan 3",
        "Orphan 4",
        "Orphan 5",
    )
    
    
def test_ignored_tasks_are_excluded_from_orphans() -> None:

    snapshots = [
        AnalyticsTaskSnapshot(
            title="Ignored Orphan",
            section="Doing",
            status=TaskStatus.OPEN,
            score=None,
            effective_score=0,
            tags=(),
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
            analytics_ignore=True,
        ),
        AnalyticsTaskSnapshot(
            title="Real Orphan",
            section="Doing",
            status=TaskStatus.OPEN,
            score=None,
            effective_score=0,
            tags=(),
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
            analytics_ignore=False,
        ),
    ]

    health = build_board_health(snapshots)

    assert health.total_tasks == 1

    assert health.orphan_tasks == 1

    assert len(health.sample_orphans) == 1

    assert (
        health.sample_orphans[0].title
        == "Real Orphan"
    )
    
def test_inactive_orphans_are_excluded() -> None:
    """Inactive tasks must NOT appear in sample_orphans, even if they lack metadata."""
    snapshots = [
        # Неактивная сирота (нет тега) — должна быть ИСКЛЮЧЕНА
        AnalyticsTaskSnapshot(
            title="Inactive Missing Tag",
            section="Doing",
            status=TaskStatus.OPEN,
            score=10,
            effective_score=10,
            tags=(),
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            is_active=False,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        # Активная сирота (нет тега) — должна быть ВКЛЮЧЕНА
        AnalyticsTaskSnapshot(
            title="Active Missing Tag",
            section="Doing",
            status=TaskStatus.OPEN,
            score=10,
            effective_score=10,
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

    # Только активная сирота должна быть в списке
    assert len(health.sample_orphans) == 1
    assert health.sample_orphans[0].title == "Active Missing Tag"
    assert health.sample_orphans[0].is_active is True


def test_active_orphans_are_prioritized_by_title() -> None:
    """When multiple active orphans exist, they are sorted deterministically."""
    snapshots = [
        AnalyticsTaskSnapshot(
            title="Zebra task",
            section="Doing",
            status=TaskStatus.OPEN,
            score=10,
            effective_score=10,
            tags=(),
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        AnalyticsTaskSnapshot(
            title="Alpha task",
            section="Doing",
            status=TaskStatus.OPEN,
            score=10,
            effective_score=10,
            tags=(),
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        AnalyticsTaskSnapshot(
            title="Middle task",
            section="Doing",
            status=TaskStatus.OPEN,
            score=10,
            effective_score=10,
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

    # Все 3 активные сироты должны быть в списке
    assert len(health.sample_orphans) == 3
    
    # Порядок должен быть детерминированным
    titles = [orphan.title for orphan in health.sample_orphans]
    assert titles == sorted(titles), "Orphans must be sorted deterministically"


def test_completed_orphans_are_excluded() -> None:
    """Completed tasks must NOT appear in orphans, even if they lack metadata."""
    snapshots = [
        # Завершённая сирота (нет тега) — должна быть ИСКЛЮЧЕНА
        AnalyticsTaskSnapshot(
            title="Completed Missing Tag",
            section="Done",
            status=TaskStatus.COMPLETED,
            score=10,
            effective_score=10,
            tags=(),
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            is_active=True,
            is_completed=True,
            is_archived=False,
            is_overdue=False,
        ),
        # Активная сирота (нет тега) — должна быть ВКЛЮЧЕНА
        AnalyticsTaskSnapshot(
            title="Active Missing Tag",
            section="Doing",
            status=TaskStatus.OPEN,
            score=10,
            effective_score=10,
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

    # Только активная сирота должна быть в списке
    assert health.orphan_tasks == 1
    assert len(health.sample_orphans) == 1
    assert health.sample_orphans[0].title == "Active Missing Tag"


def test_archived_orphans_are_excluded() -> None:
    """Archived tasks must NOT appear in orphans, even if they lack metadata."""
    snapshots = [
        # Архивная сирота (нет score) — должна быть ИСКЛЮЧЕНА
        AnalyticsTaskSnapshot(
            title="Archived Missing Score",
            section="Archive",
            status=TaskStatus.OPEN,
            score=None,
            effective_score=0,
            tags=("work",),
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            is_active=True,
            is_completed=False,
            is_archived=True,
            is_overdue=False,
        ),
        # Активная сирота (нет score) — должна быть ВКЛЮЧЕНА
        AnalyticsTaskSnapshot(
            title="Active Missing Score",
            section="Doing",
            status=TaskStatus.OPEN,
            score=None,
            effective_score=0,
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

    # Только активная сирота должна быть в списке
    assert health.orphan_tasks == 1
    assert len(health.sample_orphans) == 1
    assert health.sample_orphans[0].title == "Active Missing Score"


def test_archive_section_without_date_excluded_from_orphans() -> None:
    """Tasks in Archive section without || date must NOT appear in orphans."""
    snapshots = [
        # Задача в секции Archive БЕЗ даты || (is_archived=False, но section_type="archive")
        # должна быть ИСКЛЮЧЕНА из сирот
        AnalyticsTaskSnapshot(
            title="Archive Without Date",
            section="Archive",
            section_type="archive",
            status=TaskStatus.OPEN,
            score=None,
            effective_score=0,
            tags=("work",),
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            is_active=True,
            is_completed=False,
            is_archived=False,  # нет даты ||, поэтому archived=False
            is_overdue=False,
        ),
        # Активная сирота (нет score) — должна быть ВКЛЮЧЕНА
        AnalyticsTaskSnapshot(
            title="Active Missing Score",
            section="Doing",
            section_type="tactical",
            status=TaskStatus.OPEN,
            score=None,
            effective_score=0,
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

    # Только активная сирота должна быть в списке
    assert health.orphan_tasks == 1
    assert len(health.sample_orphans) == 1
    assert health.sample_orphans[0].title == "Active Missing Score"


def test_archive_section_with_date_still_excluded() -> None:
    """Tasks in Archive section WITH || date must still be excluded (regression test)."""
    snapshots = [
        # Задача в секции Archive С датой || (is_archived=True, section_type="archive")
        # должна быть ИСКЛЮЧЕНА из сирот
        AnalyticsTaskSnapshot(
            title="Archive With Date",
            section="Archive",
            section_type="archive",
            status=TaskStatus.OPEN,
            score=None,
            effective_score=0,
            tags=("work",),
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            is_active=True,
            is_completed=False,
            is_archived=True,  # есть дата ||, поэтому archived=True
            is_overdue=False,
        ),
        # Активная сирота (нет score) — должна быть ВКЛЮЧЕНА
        AnalyticsTaskSnapshot(
            title="Active Missing Score",
            section="Doing",
            section_type="tactical",
            status=TaskStatus.OPEN,
            score=None,
            effective_score=0,
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

    # Только активная сирота должна быть в списке
    assert health.orphan_tasks == 1
    assert len(health.sample_orphans) == 1
    assert health.sample_orphans[0].title == "Active Missing Score"


def test_non_archive_section_without_score_still_orphan() -> None:
    """Tasks outside Archive with score=None must still appear in orphans (regression test)."""
    snapshots = [
        # Задача НЕ в Archive, без score — должна быть ВКЛЮЧЕНА в сирот
        AnalyticsTaskSnapshot(
            title="Non-Archive Missing Score",
            section="Doing",
            section_type="tactical",
            status=TaskStatus.OPEN,
            score=None,
            effective_score=0,
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

    assert health.orphan_tasks == 1
    assert len(health.sample_orphans) == 1
    assert health.sample_orphans[0].title == "Non-Archive Missing Score"