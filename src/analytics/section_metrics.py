from __future__ import annotations

from src.analytics.models import (
    SectionMetrics,
    SectionSummary,
)
from src.parser.models import (
    Board,
    Section,
)


def build_section_metrics(
    section: Section,
    summary: SectionSummary,
) -> SectionMetrics:
    return SectionMetrics(
        section=section,
        summary=summary,
        wip_limit=section.wip_limit,
    )


def build_section_metrics_map(
    board: Board,
    summaries: dict[str, SectionSummary],
) -> dict[str, SectionMetrics]:
    metrics_by_section: dict[str, SectionMetrics] = {}

    for task in board.tasks:
        section = task.section
        section_name = section.title

        if section_name in metrics_by_section:
            continue

        metrics_by_section[section_name] = (
            build_section_metrics(
                section=section,
                summary=summaries[section_name],
            )
        )

    return metrics_by_section


