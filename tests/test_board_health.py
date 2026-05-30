from datetime import datetime, timedelta

from src.analytics.board_health import (
    build_board_health_report,
)
from src.analytics.models import (
    AttentionScore,
    PriorityScore,
    StaleTask,
    WipStatus,
)
from src.parser.models import (
    Section,
    SectionType,
    Task,
    TaskStatus,
)


def test_build_board_health_report():
    now = datetime(2026, 5, 31)

    execution_section = Section(
        title="Doing",
        raw_title="Doing",
        type=SectionType.EXECUTION,
        wip_limit=3,
    )

    pipeline_section = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
    )

    important_updated = now - timedelta(days=40)

    important_task = Task(
        title="Important task",
        status=TaskStatus.OPEN,
        section=execution_section,
        updated_at=important_updated,
    )

    pipeline_updated = now - timedelta(days=45)

    pipeline_task = Task(
        title="Pipeline task",
        status=TaskStatus.OPEN,
        section=pipeline_section,
        updated_at=pipeline_updated,
    )

    priority_scores = [
        PriorityScore(
            task=important_task,
            base_score=20,
            section_bonus=10,
            final_score=30,
        )
    ]

    attention_scores = [
        AttentionScore(
            task=important_task,
            stale_score=10,
            due_score=0,
            final_score=5.0,
        )
    ]

    stale_tasks = [
        StaleTask(
            task=important_task,
            age_days=40,
            is_stale=True,
            is_critical=True,
            last_updated=important_updated,
        ),
        StaleTask(
            task=pipeline_task,
            age_days=45,
            is_stale=True,
            is_critical=False,
            last_updated=pipeline_updated,
        ),
    ]

    wip_statuses = [
        WipStatus(
            section_name="Doing",
            active_tasks=5,
            wip_limit=3,
            remaining_capacity=-2,
            utilization=1.67,
            is_near_limit=False,
            is_over_limit=True,
        )
    ]

    report = build_board_health_report(
        priority_scores=priority_scores,
        attention_scores=attention_scores,
        stale_tasks=stale_tasks,
        wip_statuses=wip_statuses,
    )

    assert report.wip_violations == 1
    assert report.stale_task_count == 2

    # 100 -10(WIP) -5(exec critical) -0.5(pipeline stale)
    assert report.board_health_score == 84.5

    assert len(report.top_priority_tasks) == 1
    assert len(report.top_attention_tasks) == 1

    assert len(report.warnings) == 3


def test_health_score_never_goes_below_zero():
    now = datetime(2026, 5, 31)

    section = Section(
        title="Doing",
        raw_title="Doing",
        type=SectionType.EXECUTION,
        wip_limit=1,
    )

    stale_tasks: list[StaleTask] = []

    for i in range(50):
        updated = now - timedelta(days=100)

        task = Task(
            title=f"Task {i}",
            status=TaskStatus.OPEN,
            section=section,
            updated_at=updated,
        )

        stale_tasks.append(
            StaleTask(
                task=task,
                age_days=100,
                is_stale=True,
                is_critical=True,
                last_updated=updated,
            )
        )

    report = build_board_health_report(
        priority_scores=[],
        attention_scores=[],
        stale_tasks=stale_tasks,
        wip_statuses=[],
    )

    assert report.board_health_score == 0.0


def test_health_report_without_problems():
    report = build_board_health_report(
        priority_scores=[],
        attention_scores=[],
        stale_tasks=[],
        wip_statuses=[],
    )

    assert report.board_health_score == 100.0
    assert report.wip_violations == 0
    assert report.stale_task_count == 0
    assert len(report.warnings) == 0