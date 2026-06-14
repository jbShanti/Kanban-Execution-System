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
    
    
    


def test_attention_by_tag_aggregates_scores():
    snapshots = [
        AnalyticsTaskSnapshot(
            title="Task A",
            section="Doing",
            status=TaskStatus.OPEN,
            score=10,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=("health",),
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        AnalyticsTaskSnapshot(
            title="Task B",
            section="Doing",
            status=TaskStatus.OPEN,
            score=15,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=("health",),
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        AnalyticsTaskSnapshot(
            title="Task C",
            section="Doing",
            status=TaskStatus.OPEN,
            score=20,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=("ai",),
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
    ]

    analytics = build_focus_attention_analytics(
        snapshots=snapshots,
    )

    assert analytics.attention_by_tag == {
        "health": 25,
        "ai": 20,
    }
    
    

def test_attention_by_tag_counts_score_for_each_tag():
    snapshots = [
        AnalyticsTaskSnapshot(
            title="Task A",
            section="Doing",
            status=TaskStatus.OPEN,
            score=20,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=("health", "ai"),
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
    ]

    analytics = build_focus_attention_analytics(
        snapshots=snapshots,
    )

    assert analytics.attention_by_tag == {
        "health": 20,
        "ai": 20,
    }
    
    
def test_total_attention_score():
    snapshots = [
        AnalyticsTaskSnapshot(
            title="Task A",
            section="Doing",
            status=TaskStatus.OPEN,
            score=10,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=("health",),
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        AnalyticsTaskSnapshot(
            title="Task B",
            section="Doing",
            status=TaskStatus.OPEN,
            score=15,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=("health",),
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        AnalyticsTaskSnapshot(
            title="Task C",
            section="Doing",
            status=TaskStatus.OPEN,
            score=20,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=("ai",),
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
    ]

    analytics = build_focus_attention_analytics(
        snapshots=snapshots,
    )

    assert analytics.attention_by_tag == {
        "health": 25,
        "ai": 20,
    }

    assert analytics.total_attention_score == 45
    
    
def test_total_attention_score_not_duplicated_by_multiple_tags():
        
    snapshots = [
    AnalyticsTaskSnapshot(
        title="Task A",
        section="Doing",
        status=TaskStatus.OPEN,
        score=20,
        due_date=None,
        scheduled_date=None,
        time_estimate_minutes=None,
        tags=("health", "ai"),
        is_active=True,
        is_completed=False,
        is_archived=False,
        is_overdue=False,
    ),
]

    analytics = build_focus_attention_analytics(
        snapshots=snapshots,
    )

    assert analytics.total_attention_score == 20

    assert analytics.attention_by_tag == {
        "health": 20,
        "ai": 20,
    }
    
    
from src.analytics.focus_analytics import (
    build_focus_attention_analytics,
)
from src.analytics.models import AnalyticsTaskSnapshot
from src.parser.models import TaskStatus


def test_top_attention_tags_include_share():
    snapshots = [
        AnalyticsTaskSnapshot(
            title="Task A",
            section="Doing",
            status=TaskStatus.OPEN,
            score=25,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=("health",),
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        AnalyticsTaskSnapshot(
            title="Task B",
            section="Doing",
            status=TaskStatus.OPEN,
            score=40,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=("ai",),
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        AnalyticsTaskSnapshot(
            title="Task C",
            section="Doing",
            status=TaskStatus.OPEN,
            score=10,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=("career",),
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
        AnalyticsTaskSnapshot(
            title="Task D",
            section="Doing",
            status=TaskStatus.OPEN,
            score=30,
            due_date=None,
            scheduled_date=None,
            time_estimate_minutes=None,
            tags=("finance",),
            is_active=True,
            is_completed=False,
            is_archived=False,
            is_overdue=False,
        ),
    ]

    analytics = build_focus_attention_analytics(
        snapshots=snapshots,
    )

    assert analytics.top_attention_tags == (
        ("ai", 40, 40 / 105),
        ("finance", 30, 30 / 105),
        ("health", 25, 25 / 105),
        ("career", 10, 10 / 105),
    )