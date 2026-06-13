"""Overload detection calculator.

Analyzes WIP statuses to generate actionable overload signals.
Follows the Single Responsibility Principle: it interprets metrics, 
it does not calculate them.
"""

from src.analytics.models import OverloadSignal, WipStatus


def detect_overload(wip_statuses: list[WipStatus]) -> list[OverloadSignal]:
    """Generate overload signals based on WIP utilization.

    Args:
        wip_statuses: List of WIP status objects for board sections.

    Returns:
        A list of OverloadSignal objects, ordered by severity 
        (CRITICAL first, then WARNING).
    """
    signals: list[OverloadSignal] = []

    for wip in wip_statuses:
        if wip.is_over_limit:
            signals.append(OverloadSignal(
                section_name=wip.section_name,
                severity="CRITICAL",
                message=(
                    f"Section '{wip.section_name}' is OVER WIP limit "
                    f"({wip.active_tasks}/{wip.wip_limit} tasks). "
                    "Focus on finishing existing work before pulling new tasks."
                )
            ))
        elif wip.is_near_limit:
            signals.append(OverloadSignal(
                section_name=wip.section_name,
                severity="WARNING",
                message=(
                    f"Section '{wip.section_name}' is nearing WIP limit "
                    f"({wip.active_tasks}/{wip.wip_limit} tasks, {wip.utilization:.0%} utilized). "
                    "Be cautious about adding new work."
                )
            ))

    # Сортируем: сначала CRITICAL, потом WARNING
    severity_order = {"CRITICAL": 0, "WARNING": 1}
    return sorted(signals, key=lambda x: severity_order[x.severity])