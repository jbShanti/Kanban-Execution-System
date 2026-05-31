from src.analytics.models import TaskMetrics
from src.analytics.service import calculate_task_metrics

from src.parser.models import (
    Section,
    SectionType,
    Task,
    TaskStatus,
)
    
from datetime import date, timedelta

def test_calculate_basic_task_metrics() -> None:
    section = Section(
        title="Inbox",
        raw_title="Inbox",
        type=SectionType.INBOX,
    )

    tasks = [
        Task(
            title="Open 1",
            status=TaskStatus.OPEN,
            section=section,
            score=10,
        ),
        Task(
            title="Open 2",
            status=TaskStatus.OPEN,
            section=section,
            score=10,
        ),
        Task(
            title="In Progress",
            status=TaskStatus.IN_PROGRESS,
            section=section,
            score=10,
        ),
        Task(
            title="Completed",
            status=TaskStatus.COMPLETED,
            section=section,
            score=10,
        ),
        Task(
            title="Cancelled",
            status=TaskStatus.CANCELLED,
            section=section,
            score=10,
        ),
        Task(
            title="Delegated",
            status=TaskStatus.DELEGATED,
            section=section,
            score=10,
        ),
        Task(
            title="Scheduled",
            status=TaskStatus.SCHEDULED,
            section=section,
            score=10,
        ),
    ]

    metrics = calculate_task_metrics(tasks)

    assert metrics == TaskMetrics(
        active_tasks=3,
        completed_tasks=1,
        cancelled_tasks=1,
        delegated_tasks=1,
        scheduled_tasks=1,
        archived_tasks=0,
        
        tasks_without_score=0,
        total_score=70,
        active_score=30,
    )
    
def test_calculate_metrics_with_archived_tasks() -> None:
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
            score=10,
        ),
        Task(
            title="Completed",
            status=TaskStatus.COMPLETED,
            section=section,
            score=10,
        ),
        Task(
            title="Archived Open",
            status=TaskStatus.OPEN,
            section=section,
            archived=True,
            score=10,
        ),
        Task(
            title="Archived Completed",
            status=TaskStatus.COMPLETED,
            section=section,
            archived=True,
            score=10,
        ),
    ]

    metrics = calculate_task_metrics(tasks)

    assert metrics == TaskMetrics(
        active_tasks=1,
        completed_tasks=1,
        cancelled_tasks=0,
        delegated_tasks=0,
        scheduled_tasks=0,
        archived_tasks=2,
        
        tasks_without_score=0,
        total_score=20,
        active_score=10,
    )
    
def test_archived_tasks_are_counted_separately() -> None:
    section = Section(
        title="Archive",
        raw_title="Archive",
        type=SectionType.ARCHIVE,
    )

    tasks = [
        Task(
            title="Archived completed",
            status=TaskStatus.COMPLETED,
            section=section,
            archived=True,
        ),
        Task(
            title="Archived open",
            status=TaskStatus.OPEN,
            section=section,
            archived=True,
        ),
    ]

    metrics = calculate_task_metrics(tasks)

    assert metrics.archived_tasks == 2
    

def test_calculate_time_metrics() -> None:
    today = date.today()

    section = Section(
        title="Inbox",
        raw_title="Inbox",
        type=SectionType.INBOX,
    )

    tasks = [
        Task(
            title="Overdue",
            status=TaskStatus.OPEN,
            section=section,
            due=today - timedelta(days=1),
        ),
        Task(
            title="Due today",
            status=TaskStatus.OPEN,
            section=section,
            due=today,
        ),
        Task(
            title="Due in 2 days",
            status=TaskStatus.OPEN,
            section=section,
            due=today + timedelta(days=2),
        ),
        Task(
            title="Due in 10 days",
            status=TaskStatus.OPEN,
            section=section,
            due=today + timedelta(days=10),
        ),
    ]

    metrics = calculate_task_metrics(tasks)

    assert metrics.overdue_tasks == 1
    assert metrics.due_today_tasks == 1
    assert metrics.due_next_3_days_tasks == 2
    
def test_calculate_score_metrics() -> None:
    section = Section(
        title="Inbox",
        raw_title="Inbox",
        type=SectionType.INBOX,
    )

    tasks = [
        Task(
            title="Open 10",
            status=TaskStatus.OPEN,
            section=section,
            score=10,
        ),
        Task(
            title="In Progress 20",
            status=TaskStatus.IN_PROGRESS,
            section=section,
            score=20,
        ),
        Task(
            title="Completed 30",
            status=TaskStatus.COMPLETED,
            section=section,
            score=30,
        ),
        Task(
            title="No Score",
            status=TaskStatus.OPEN,
            section=section,
        ),
    ]

    metrics = calculate_task_metrics(tasks)

    assert metrics.tasks_without_score == 1
    assert metrics.total_score == 60
    assert metrics.active_score == 30