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

from src.analytics.board_summary import build_board_summary

def generate_execution_report(
    board: Board,
    analysis_date: date | None = None,
) -> ExecutionReport:
    """Generate a deterministic ExecutionReport."""
    if analysis_date is None:
        analysis_date = date.today()
    
    # ── Stage 1: Task Snapshots ──────────────────────────────
    task_snapshots = [
        build_task_snapshot(task, analysis_date)
        for task in board.tasks
    ]
    
    # ── Stage 2: Board Health ────────────────────────────────
    board_health = build_board_health(task_snapshots)
    
    # ── Stage 3: Board Summary ───────────────────────────────
    board_summary = build_board_summary(board, analysis_date)  # ← ДОБАВИТЬ
    
    # ── Stage 4: Executive Summary ───────────────────────────
    executive_summary = ExecutiveSummary(
        summary="TODO: Implement executive summary generation from findings"
    )
    
    # ── Compose ExecutionReport ──────────────────────────────
    return ExecutionReport(
        schema_version="1.0",
        report_id=str(uuid.uuid4()),
        analysis_date=analysis_date,
        generated_at=datetime.now(),
        board_path=getattr(board, "path", "") or "unknown",
        board_health=board_health,
        board_summary=board_summary,  # ← ДОБАВИТЬ
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