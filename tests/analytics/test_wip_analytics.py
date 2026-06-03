from src.analytics.board_summary import build_board_summary
from src.parser.models import Board, Section, SectionType, Task, TaskStatus
from src.analytics.section_metrics import build_section_metrics_map
from src.analytics.wip_analytics import analyze_wip


def test_detects_wip_pressure():
    focus = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
        wip_limit=3,
    )

    tasks = [
        Task(
            title=f"Task {i}",
            status=TaskStatus.OPEN,
            section=focus,
        )
        for i in range(3)
    ]

    summary = build_board_summary(Board(tasks=tasks))

    section_metrics = build_section_metrics_map(
        Board(tasks=tasks),
        summary.sections,
    )

    result = analyze_wip(section_metrics)

    assert len(result) == 1

    wip = result[0]

    assert wip.active_tasks == 3
    assert wip.wip_limit == 3

    assert wip.remaining_capacity == 0

    assert wip.utilization == 1.0

    assert wip.is_near_limit is True
    assert wip.is_over_limit is False
    
def test_detects_wip_violation():
    focus = Section(
        title="Focus",
        raw_title="Focus",
        type=SectionType.FOCUS,
        wip_limit=2,
    )

    tasks = [
        Task(
            title=f"Task {i}",
            status=TaskStatus.OPEN,
            section=focus,
        )
        for i in range(3)
    ]

    summary = build_board_summary(Board(tasks=tasks))

    metrics = build_section_metrics_map(
        Board(tasks=tasks),
        summary.sections,
    )

    result = analyze_wip(metrics)

    wip = result[0]

    assert wip.active_tasks == 3
    assert wip.wip_limit == 2

    assert wip.is_over_limit is True