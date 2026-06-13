from __future__ import annotations

from datetime import datetime

from src.analytics.calculators.wip_metrics import calculate_wip_metrics

from src.analytics.attention_scoring import (
    calculate_attention_scores,
)
from src.analytics.board_health import (
    build_board_health_report,
)
from src.analytics.board_metrics import (
    calculate_board_metrics,
)
from src.analytics.board_summary import build_board_summary
from src.analytics.priority_scoring import (
    calculate_priority_scores,
)
from src.analytics.section_metrics import (
    build_section_metrics_map,
    )
from src.analytics.stale_analytics import (
    calculate_stale_tasks,
)

from src.reporting.markdown_report import (
    render_markdown_report,
)
from src.parser.models import Task, Board


def run_review(
    tasks: list[Task],
    now: datetime | None = None,
) -> str:
    now = now or datetime.now()

    board=Board(tasks=tasks)
    
    board_metrics = calculate_board_metrics(
        board,
        today=now.date(),
    )

    summary = build_board_summary(board)

    section_metrics = build_section_metrics_map(
        board,
        summary.sections,
    )

    wip_statuses = calculate_wip_metrics(board)

    stale_tasks = calculate_stale_tasks(
        tasks,
        now=now,
    )

    priority_scores = calculate_priority_scores(
        tasks,
    )

    attention_scores = calculate_attention_scores(
        tasks,
        now=now,
    )

    board_health = build_board_health_report(
        priority_scores=priority_scores,
        attention_scores=attention_scores,
        stale_tasks=stale_tasks,
        wip_statuses=wip_statuses,
    )

    return render_markdown_report(
        board_metrics=board_metrics,
        section_metrics=list(
            section_metrics.values()
        ),
        board_health=board_health,
    )
    
    