from src.parser.models import Section

from src.analytics.service import (
    build_analytics_snapshot,
)

from src.reporting.report_adapter import (
    render_snapshot,
)

from tests.helper import (
    load_test_board,
)


def load_real_board():
    return load_test_board(
        "Doing (KB).md"
    )


def test_real_board_snapshot_builds():
    board = load_real_board()

    snapshot = build_analytics_snapshot(board)

    report = render_snapshot(snapshot)

    print(report)

    report_path = "report.md"

    with open(
        report_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(report)

    print(snapshot.summary)
    print(snapshot.board)

    assert snapshot.summary.total_tasks > 0
    assert len(snapshot.sections) > 0


def test_real_board_snapshot_builds_tmp():
    board = load_real_board()

    snapshot = build_analytics_snapshot(board)

    print()

    print(
        "TOTAL:",
        snapshot.summary.total_tasks,
    )

    print(
        "ACTIVE:",
        snapshot.summary.active_tasks,
    )

    print(
        "COMPLETED:",
        snapshot.summary.completed_tasks,
    )

    print(
        "SECTIONS:",
        len(snapshot.sections),
    )

    for (
        name,
        section_summary,
    ) in snapshot.summary.sections.items():
        print(
            name,
            section_summary.total_tasks,
            section_summary.active_tasks,
        )

    assert snapshot.summary.total_tasks > 0


def test_real_board_sections():
    board = load_real_board()

    sections: list[Section] = board.sections

    for section in sections:
        print(
            section.title,
            section.type,
            section.wip_limit,
        )

    assert len(sections) > 0