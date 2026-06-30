from src.parser.models import SectionType
from src.parser.section_parser import (
    build_section,
    clean_section_title,
    extract_priority_weight,
    extract_wip_limit,
)
from src.parser.metadata import extract_emoji
from src.parser.sections import resolve_section_type


def test_build_simple_section():
    raw_title = "Health"
    clean_title = clean_section_title(raw_title)

    section = build_section(
        raw_title=raw_title,
        clean_title=clean_title,
        section_type=resolve_section_type(clean_title),
    )

    assert section.raw_title == "Health"
    assert section.title == "Health"
    assert section.emoji == []
    assert section.priority_weight is None
    assert section.wip_limit is None


def test_extract_section_priority():
    assert extract_priority_weight("Health [P::5]") == 5
    assert extract_priority_weight("Inbox") is None


def test_extract_section_wip_limit():
    assert extract_wip_limit("Todo (3)") == 3
    assert extract_wip_limit("Done") is None


def test_extract_section_emoji():
    assert extract_emoji("❤️ Health") == ["❤️"]
    assert extract_emoji("📥 Inbox") == ["📥"]
    assert extract_emoji("Health") == []


def test_clean_section_title():
    assert clean_section_title("❤️ Health [P::5] (3)") == "Health"
    assert clean_section_title("📥 Inbox") == "Inbox"
    assert clean_section_title("Done") == "Done"


def test_section_type_after_emoji_removal():
    raw_title = "📥 Inbox"
    clean_title = clean_section_title(raw_title)

    assert clean_title == "Inbox"
    assert resolve_section_type(clean_title) == SectionType.INBOX


def test_build_section_with_emoji_and_priority():
    raw_title = "❤️ Health [P::5]"
    clean_title = clean_section_title(raw_title)

    section = build_section(
        raw_title=raw_title,
        clean_title=clean_title,
        section_type=resolve_section_type(clean_title),
    )

    assert section.raw_title == "❤️ Health [P::5]"
    assert section.title == "Health"
    assert section.emoji == ["❤️"]
    assert section.priority_weight == 5


def test_build_section_with_multiple_emoji():
    raw_title = "❤️🔥 Health"
    clean_title = clean_section_title(raw_title)

    section = build_section(
        raw_title=raw_title,
        clean_title=clean_title,
        section_type=resolve_section_type(clean_title),
    )

    assert section.title == "Health"
    assert section.emoji == ["❤️", "🔥"]