import re
from datetime import date
from typing import Final
from src.parser.models import Priority


METADATA_PATTERN: Final = re.compile(
    r"\[([a-z0-9\-]+)::([^\]]+)\]"
)

TAG_PATTERN: Final = re.compile(
    r"#([\w/\-]+)",
    re.UNICODE,
)

DUE_PATTERN: Final = re.compile(
    r"@\{(\d{4}-\d{2}-\d{2})\}"
)

WHITESPACE_PATTERN: Final = re.compile(r"\s+")

STATUS_PATTERN: Final = re.compile(
    r"^\s*-\s\[([ x/\-<>i])\]"
)

STATUS_MAP: Final[dict[str, str]] = {
    " ": "open",
    "x": "completed",
    "/": "in_progress",
    "-": "cancelled",
    "<": "scheduled",
    ">": "delegated",
    "i": "info",
}

STATUS_CLEAN_PATTERN: Final = re.compile(
    r"^\s*-\s\[[ x/\-<>i]\]\s*"
)

INTERNAL_LINK_PATTERN: Final = re.compile(
    r"\[\[([^\|\]]+)(?:\|([^\]]+))?\]\]"
)

EXTERNAL_LINK_PATTERN: Final = re.compile(
    r"\[([^\]]+)\]\(([^)]+)\)"
)

def extract_metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}

    matches = METADATA_PATTERN.findall(text)

    for key, value in matches:
        if key not in metadata:
            metadata[key] = value.strip()

    return metadata

def extract_tags(text: str) -> list[str]:
    return TAG_PATTERN.findall(text)

def extract_due_date(text: str) -> date | None:
    match = DUE_PATTERN.search(text)

    if not match:
        return None

    try:
        return date.fromisoformat(match.group(1))
    except ValueError:
        return None

def extract_internal_links(text: str) -> list[tuple[str, str]]:
    return INTERNAL_LINK_PATTERN.findall(text)

def extract_external_links(text: str) -> list[tuple[str, str]]:
    return EXTERNAL_LINK_PATTERN.findall(text)

def extract_status(text: str) -> str | None:
    match = STATUS_PATTERN.search(text)

    if not match:
        return None

    raw_status = match.group(1)

    return STATUS_MAP.get(raw_status)

def normalize_whitespace(text: str) -> str:
    return WHITESPACE_PATTERN.sub(" ", text).strip()

def strip_metadata(text: str) -> str:
    text = METADATA_PATTERN.sub("", text)
    text = TAG_PATTERN.sub("", text)
    text = DUE_PATTERN.sub("", text)

    text = INTERNAL_LINK_PATTERN.sub(r"\1", text)
    text = EXTERNAL_LINK_PATTERN.sub(r"\1", text)

    text = STATUS_CLEAN_PATTERN.sub("", text)

    return normalize_whitespace(text)


SCHEDULED_PATTERN = re.compile(
    r"\[scheduled::(\d{4}-\d{2}-\d{2})\]",
    re.IGNORECASE,
)


def extract_scheduled_date(text: str) -> date | None:
    """
    Extracts scheduled date from task metadata.

    Supported format:

        [scheduled::2026-06-20]

    Returns:
        date object if valid date found,
        otherwise None.
    """

    match = SCHEDULED_PATTERN.search(text)

    if not match:
        return None

    try:
        return date.fromisoformat(match.group(1))
    except ValueError:
        return None
    


START_PATTERN = re.compile(
    r"\[start::(\d{4}-\d{2}-\d{2})\]",
    re.IGNORECASE,
)


def extract_start_date(text: str) -> date | None:
    """
    Extracts start date from task metadata.

    Supported format:

        [start::2026-06-20]
    """

    match = START_PATTERN.search(text)

    if not match:
        return None

    try:
        return date.fromisoformat(match.group(1))
    except ValueError:
        return None
    

COMPLETION_PATTERN = re.compile(
    r"\[completion::(\d{4}-\d{2}-\d{2})\]",
    re.IGNORECASE,
)


def extract_completion_date(text: str) -> date | None:
    """
    Extract completion date from metadata.

    Supported format:

        [completion::2026-06-20]
    """

    match = COMPLETION_PATTERN.search(text)

    if not match:
        return None

    try:
        return date.fromisoformat(match.group(1))
    except ValueError:
        return None
    
    
PRIORITY_PATTERN = re.compile(
    r"\[priority::([a-z]+)\]",
    re.IGNORECASE,
)


def extract_priority(text: str) -> Priority | None:
    match = PRIORITY_PATTERN.search(text)

    if not match:
        return None

    try:
        return Priority(match.group(1).lower())
    except ValueError:
        return None
    
    
REPEAT_PATTERN = re.compile(
    r"\[repeat::([^\]]+)\]",
    re.IGNORECASE,
)


def extract_repeat(text: str) -> str | None:
    match = REPEAT_PATTERN.search(text)

    if not match:
        return None

    return match.group(1).strip()


ANALYTICS_PATTERN = re.compile(
    r"\[analytics::([a-z0-9_-]+)\]",
    re.IGNORECASE,
)

def extract_analytics(text: str) -> set[str]:
    return {
        value.lower()
        for value in ANALYTICS_PATTERN.findall(text)
    }
    
    
    
CATEGORY_PATTERN = re.compile(
    r"\[category::([^\]]+)\]",
    re.IGNORECASE,
)


def extract_category(text: str) -> str | None:
    match = CATEGORY_PATTERN.search(text)

    if not match:
        return None

    return match.group(1).strip().lower()


FINANCE_PATTERN = re.compile(
    r"\[finance::([^\]]+)\]",
    re.IGNORECASE,
)


def extract_finance(text: str) -> str | None:
    match = FINANCE_PATTERN.search(text)

    if not match:
        return None

    return match.group(1).strip().lower()



COST_PATTERN = re.compile(
    r"\[cost::(-?\d+(?:\.\d+)?)\]",
    re.IGNORECASE,
)


def extract_cost(text: str) -> int | None:
    match = COST_PATTERN.search(text)

    if not match:
        return None

    try:
        return abs(int(float(match.group(1))))
    except (TypeError, ValueError):
        return None
    
    
CURRENCY_PATTERN = re.compile(
    r"\[currency::([^\]]+)\]",
    re.IGNORECASE,
)


def extract_currency(text: str) -> str | None:
    match = CURRENCY_PATTERN.search(text)

    if not match:
        return None

    value = match.group(1).strip().upper()

    if len(value) < 3:
        return None

    return value[:3]

import unicodedata


def _is_emoji_base(char: str) -> bool:
    return unicodedata.category(char) == "So"


def _parse_emoji_prefix(
    title: str,
) -> tuple[list[str], str]:

    emoji: list[str] = []

    i = 0
    n = len(title)

    while i < n:

        while i < n and title[i].isspace():
            i += 1

        if i >= n:
            break

        char = title[i]

        if not _is_emoji_base(char):
            break

        token = char
        i += 1

        # Variation Selector-16 (⚙️ ❤️ ☀️ ...)
        if i < n and ord(title[i]) == 0xFE0F:
            token += title[i]
            i += 1

        emoji.append(token)

    clean_title = title[i:].strip()

    return emoji, clean_title

def extract_emoji(
    title: str,
) -> list[str]:
    emoji, _ = _parse_emoji_prefix(title)
    return emoji


def strip_emoji(
    title: str,
) -> str:
    _, clean_title = _parse_emoji_prefix(title)
    return clean_title