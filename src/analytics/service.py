from __future__ import annotations

from src.analytics.board_metrics import build_board_metrics
from src.analytics.board_summary import build_board_summary
from src.analytics.calculators.score_metrics import (
    calculate_score_metrics,
)
from src.analytics.calculators.status_metrics import (
    calculate_status_metrics,
)
from src.analytics.calculators.time_metrics import (
    calculate_time_metrics,
)
from src.analytics.calculators.high_five import calculate_high_five
from src.analytics.focus_analytics import build_focus_attention_analytics
from src.analytics.models import (
    AnalyticsReport,
    AnalyticsSnapshot,
    TaskMetrics
)
from src.analytics.report_builder import (
    build_analytics_report,
)
from src.analytics.section_metrics import (
    build_section_metrics_map,
)
from src.parser.models import Board, Task

from datetime import date, datetime

from src.analytics.analytics_readiness import (
    build_board_health,
)
from src.analytics.task_snapshot import (
    build_task_snapshot,
)


def generate_analytics_report(
    board: Board,
    analysis_date: date,
    generated_at: datetime,
) -> AnalyticsReport:
    snapshot = build_analytics_snapshot(board, analysis_date)

    return build_analytics_report(snapshot, generated_at)


from src.analytics.calculators.wip_metrics import calculate_wip_metrics

def build_analytics_snapshot(
    board: Board,
    analysis_date: date,
) -> AnalyticsSnapshot:
    summary = build_board_summary(board, analysis_date)
    board_metrics = build_board_metrics(summary)
    section_metrics = build_section_metrics_map(board, summary.sections)
    
    task_snapshots = [
        build_task_snapshot(
            task,
            analysis_date,
        )
        for task in board.tasks
    ]
    
    board_health = build_board_health(
        task_snapshots
        )
    
    # Focus Attention Analytics
    focus_attention_analytics = build_focus_attention_analytics(task_snapshots)
    
    # Новый WIP-калькулятор
    wip_statuses = calculate_wip_metrics(board)
    
    # High Five - топ-5 задач на день
    high_five_tasks = calculate_high_five(board.tasks)

    return AnalyticsSnapshot(
        summary=summary,
        board=board_metrics,
        sections=section_metrics,
        board_health=board_health,
        wip_statuses=wip_statuses,
        high_five_tasks=high_five_tasks,
        focus_attention_analytics=focus_attention_analytics,
    )


def calculate_task_metrics(
    tasks: list[Task],
    today: date,
) -> TaskMetrics:
    status_metrics = calculate_status_metrics(
        tasks,
    )

    time_metrics = calculate_time_metrics(
        tasks,
        today,
    )

    score_metrics = calculate_score_metrics(
        tasks,
    )

    return TaskMetrics(
        **status_metrics,
        **time_metrics,
        **score_metrics,
    )
    
    
