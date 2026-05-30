from src.analytics.models import (
    SectionMetrics,
    WipStatus,
)


def analyze_wip(
    sections: dict[str, SectionMetrics],
) -> list[WipStatus]:
    results: list[WipStatus] = []

    for metrics in sections.values():
        if metrics.wip_limit is None:
            continue

        active = metrics.active_tasks
        limit = metrics.wip_limit

        utilization = active / limit if limit > 0 else 0.0

        results.append(
            WipStatus(
                section_name=metrics.section.title,
                active_tasks=active,
                wip_limit=limit,
                remaining_capacity=max(limit - active, 0),
                utilization=utilization,
                is_near_limit=utilization >= 0.8,
                is_over_limit=active > limit,
            )
        )

    return results