from pathlib import Path

from src.parser.models import Board
from src.parser.parser import parse_markdown_file


def load_test_board(
    filename: str | Path,
) -> Board:
    path = Path(filename)

    if not path.is_absolute():
        path = (
            Path("tests/fixtures")
            / path
        )

    return parse_markdown_file(path)