from pathlib import Path

from src.parser.models import Board, Section, SectionType
from src.parser.parser import parse_markdown_file
from src.parser.section_parser import build_section, clean_section_title


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

def create_section(
    *,
    title: str = "Inbox",
    section_type: SectionType = SectionType.INBOX,
    emoji: list[str] | None = None,
    priority_weight: int | None = None,
    wip_limit: int | None = None,
) -> Section:
    if emoji is None:
        emoji = []

    raw_title = title

    if emoji:
        raw_title = f"{''.join(emoji)} {raw_title}"

    if priority_weight is not None:
        raw_title += f" [P::{priority_weight}]"

    if wip_limit is not None:
        raw_title += f" ({wip_limit})"

    clean_title = clean_section_title(raw_title)

    return build_section(
        raw_title=raw_title,
        clean_title=clean_title,
        emoji=emoji,
        priority_weight=priority_weight,
        wip_limit=wip_limit,
        section_type=section_type,
    )