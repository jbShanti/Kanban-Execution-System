from __future__ import annotations

from datetime import datetime, date

from src.analytics.models import AttentionScore
from src.parser.models import Task


def _calculate_stale_score(
    task: Task,
    now: datetime,
) -> int:
    if task.updated_at is None:
        return 0

    age_days = (now - task.updated_at).days

    if age_days >= 30:
        return 7

    if age_days >= 7:
        return 3

    return 0


def _calculate_due_score(
    task: Task,
    today: date,
) -> int:
    if task.due is None:
        return 0

    overdue_days = (today - task.due).days

    if overdue_days <= 0:
        return 0

    if overdue_days > 30:
        return 15

    if overdue_days > 7:
        return 10

    return 5


def calculate_attention_scores(
    tasks: list[Task],
    now: datetime | None = None,
) -> list[AttentionScore]:
    now = now or datetime.now()

    results: list[AttentionScore] = []

    for task in tasks:
        if not task.is_actionable:
            continue

        stale_score = _calculate_stale_score(
            task,
            now,
        )

        due_score = _calculate_due_score(
            task,
            now.date(),
        )
        
        final_score = due_score + (stale_score * 0.5)
        if final_score <= 0:
            continue
        
        results.append(
            AttentionScore(
                task=task,
                stale_score=stale_score,
                due_score=due_score,
                final_score=final_score,
            )
        )

    return sorted(
        results,
        key=lambda item: item.final_score,
        reverse=True,
    )