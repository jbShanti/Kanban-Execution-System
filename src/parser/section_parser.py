import re
from typing import Optional

from src.parser.models import Section, SectionType

from src.parser.metadata import (
    strip_emoji,
)


PRIORITY_PATTERN = re.compile(
    r"\[P::(?P<priority>[0-5])\]",
)

WIP_PATTERN = re.compile(
    r"\((?P<wip>\d+)\)",
)


def extract_priority_weight(
    raw_title: str,
) -> Optional[int]:
    match = PRIORITY_PATTERN.search(raw_title)

    if match is None:
        return None

    return int(match.group("priority"))


def extract_wip_limit(
    raw_title: str,
) -> Optional[int]:
    match = WIP_PATTERN.search(raw_title)

    if match is None:
        return None

    return int(match.group("wip"))


def clean_section_title(
    raw_title: str,
) -> str:
    title = PRIORITY_PATTERN.sub("", raw_title)
    title = WIP_PATTERN.sub("", title)
    title = strip_emoji(title)

    return title.strip()


def build_section(
    *,
    raw_title: str,
    clean_title: str,
    emoji: list[str],
    priority_weight: int | None,
    wip_limit: int | None,
    section_type: SectionType,
) -> Section:
    return Section(
        title=clean_title,
        raw_title=raw_title,
        emoji=emoji,
        type=section_type,
        wip_limit=wip_limit,
        priority_weight=priority_weight,
    )