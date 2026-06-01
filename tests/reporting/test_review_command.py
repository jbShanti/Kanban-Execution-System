from pathlib import Path

from src.cli.review_command import (
    review_command,
)


def test_review_command_generates_report(
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

    report = review_command(board)

    assert "# Board Health Report" in report
    assert "Total Tasks" in report


def test_review_command_handles_empty_board(
    tmp_path: Path,
):
    board = tmp_path / "empty.md"

    board.write_text(
        "",
        encoding="utf-8",
    )

    report = review_command(board)

    assert "# Board Health Report" in report


def test_review_command_contains_task_names(
    tmp_path: Path,
):
    board = tmp_path / "board.md"

    board.write_text(
        """
# Doing

- [ ] Write architecture
""",
        encoding="utf-8",
    )

    report = review_command(board)

    assert "Write architecture" in report