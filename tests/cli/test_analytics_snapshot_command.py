from pathlib import Path

from src.cli.analytics_snapshot_command import analytics_snapshot_command


def test_analytics_snapshot_command_generates_report(
    tmp_path: Path,
):
    board = tmp_path / "board.md"

    board.write_text(
        """
# Doing

- [ ] Important task [score::20]
- [ ] Another task [score::10]
""",
        encoding="utf-8",
    )

    report = analytics_snapshot_command(board)

    assert "# Analytics Snapshot" in report
    assert "Total Tasks" in report


def test_analytics_snapshot_command_handles_empty_board(
    tmp_path: Path,
):
    board = tmp_path / "empty.md"

    board.write_text(
        "",
        encoding="utf-8",
    )

    report = analytics_snapshot_command(board)

    assert "# Analytics Snapshot" in report
