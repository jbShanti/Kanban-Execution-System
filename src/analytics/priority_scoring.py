from __future__ import annotations

from src.analytics.models import PriorityScore
from src.parser.models import Task


def calculate_priority_scores(
    tasks: list[Task],
) -> list[PriorityScore]:
    """
    Calculate execution priority scores.

    Rules:
    - only actionable tasks participate
    - task.score is the primary signal
    - section.priority_weight acts as a modifier
    """

    results: list[PriorityScore] = []

    for task in tasks:
        if not task.is_actionable:
            continue

        base_score = task.score or 0
        section_bonus = task.section.priority_weight or 0

        results.append(
            PriorityScore(
                task=task,
                base_score=base_score,
                section_bonus=section_bonus,
                final_score=base_score + section_bonus,
            )
        )

    return sorted(
        results,
        key=lambda item: item.final_score,
        reverse=True,
    )