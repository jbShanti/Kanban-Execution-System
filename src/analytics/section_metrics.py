from __future__ import annotations

from dataclasses import dataclass

from src.parser.models import Section, Task


@dataclass(slots=True)
class SectionMetrics:
    section: Section

    total_tasks: int = 0

    active_tasks: int = 0
    actionable_tasks: int = 0

    completed_tasks: int = 0
    cancelled_tasks: int = 0

    scored_tasks: int = 0
    total_score: int = 0

    wip_limit: int | None = None

    @property
    def average_score(self) -> float:
        if self.scored_tasks == 0:
            return 0.0

        return self.total_score / self.scored_tasks

    @property
    def wip_usage(self) -> float | None:
        if self.wip_limit is None:
            return None

        if self.wip_limit == 0:
            return 0.0

        return self.active_tasks / self.wip_limit


def calculate_section_metrics(
    tasks: list[Task],
) -> dict[str, SectionMetrics]:
    """
    Calculate metrics grouped by section title.
    """

    metrics_by_section: dict[str, SectionMetrics] = {}

    for task in tasks:
        section_key = task.section.title

        if section_key not in metrics_by_section:
            metrics_by_section[section_key] = SectionMetrics(
                section=task.section,
                wip_limit=task.section.wip_limit,
            )

        metrics = metrics_by_section[section_key]

        metrics.total_tasks += 1

        if task.is_active:
            metrics.active_tasks += 1

        if task.is_actionable:
            metrics.actionable_tasks += 1

        if task.is_completed:
            metrics.completed_tasks += 1

        if task.is_cancelled:
            metrics.cancelled_tasks += 1

        if task.score is not None:
            metrics.scored_tasks += 1
            metrics.total_score += task.score

    return metrics_by_section