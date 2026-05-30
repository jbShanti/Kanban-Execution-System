from __future__ import annotations

from pathlib import Path

from src.application.review_service import (
    run_review,
)
from src.parser.parser import (
    parse_markdown_file,
)


def review_command(
    board_path: str | Path,
) -> str:
    board_path = Path(board_path)

    tasks = parse_markdown_file(
        board_path
    )

    return run_review(tasks)