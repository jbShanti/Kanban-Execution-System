"""WIP (Work In Progress) metrics calculator.

Calculates WIP utilization per section, detecting overload and
near-limit situations. This calculator works at the section level,
unlike task-level calculators (status, time, score).
"""

from src.analytics.models import WipStatus
from src.parser.models import Board, TaskStatus


def calculate_wip_metrics(
    board: Board,
) -> list[WipStatus]:
    """Calculate WIP status for each section with a defined WIP limit.

    Only sections that have a ``wip_limit`` configured are included
    in the results. Active tasks are those with status OPEN or
    IN_PROGRESS and are not archived.

    Args:
        board: The board containing tasks and sections.

    Returns:
        A list of WipStatus objects, one per section with a WIP limit.
    """
    # Step 1: Count active tasks per section
    active_by_section: dict[str, int] = {}

    for task in board.tasks:
        if task.archived:
            continue

        if task.status in {TaskStatus.OPEN, TaskStatus.IN_PROGRESS}:
            section_name = task.section.title
            active_by_section[section_name] = (
                active_by_section.get(section_name, 0) + 1
            )

    # Step 2: Build WIP status for each section with a limit
    results: list[WipStatus] = []

    for section in board.sections:
        if section.wip_limit is None:
            continue

        active = active_by_section.get(section.title, 0)
        limit = section.wip_limit
        utilization = active / limit if limit > 0 else 0.0

        results.append(
            WipStatus(
                section_name=section.title,
                active_tasks=active,
                wip_limit=limit,
                remaining_capacity=max(limit - active, 0),
                utilization=utilization,
                is_near_limit=utilization >= 0.8,
                is_over_limit=active > limit,
            )
        )

    return results