from __future__ import annotations

import uuid

from src.analytics.calculators.score_metrics import (
    calculate_score_metrics,
)
from src.analytics.calculators.status_metrics import (
    calculate_status_metrics,
)
from src.analytics.calculators.time_metrics import (
    calculate_time_metrics,
)
from src.analytics.models import (
    ExecutiveSummary,
    ExecutionReport,
    TaskMetrics
)

from src.parser.models import Board, Task

from datetime import date, datetime

from src.analytics.analytics_readiness import (
    build_board_health,
)
from src.analytics.task_snapshot import (
    build_task_snapshot,
)

def generate_execution_report(
    board: Board,
    analysis_date: date | None = None,
) -> ExecutionReport:
    """
    Generate a deterministic ExecutionReport.
    
    This is the canonical pipeline that produces the universal
    execution state. Presentation artifacts consume this report
    and derive their specific views.
    
    Args:
        board: Parsed Kanban board.
        analysis_date: Date for analysis. If None, uses today's date.
                      All internal calculations use this injected date.
    
    Returns:
        ExecutionReport with complete metadata and analytical content.
    """
    # Time resolution at the boundary only
    if analysis_date is None:
        analysis_date = date.today()
    
    # ── Stage 1: Measurements ──────────────────────────────
    task_snapshots = [
        build_task_snapshot(task, analysis_date)
        for task in board.tasks
    ]
    
    # ── Stage 3: Board Health ──────────────────────────────
    board_health = build_board_health(task_snapshots)
    
    # ── Stage 5: Executive Summary (заглушка для MVP) ──────
    executive_summary = ExecutiveSummary(
        summary="TODO: Implement executive summary generation from findings"
    )
    
    # ── Compose ExecutionReport with FULL metadata ─────────
    return ExecutionReport(
        # Metadata and Provenance
        schema_version="1.0",
        report_id=str(uuid.uuid4()),
        analysis_date=analysis_date,
        generated_at=datetime.now(),  # Metadata, не аналитика — допустимо
        board_path=getattr(board, "path", "") or "unknown",
        
        # Analytical content
        board_health=board_health,
        executive_summary=executive_summary,
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