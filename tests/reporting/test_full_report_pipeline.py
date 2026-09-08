"""Integration test for the full report generation pipeline."""

from src.analytics.service import generate_execution_report
from src.parser.parser import parse_markdown_lines
from src.parser.models import Board
from src.reporting.execution_report_composer import compose_execution_report
from datetime import date
import tempfile
import os


def test_full_report_pipeline_with_simple_board():
    """Test the full pipeline with a simple board fixture."""
    # Load the simple board fixture
    fixture_path = "tests/fixtures/simple_board.md"
    
    with open(fixture_path, 'r', encoding='utf-8') as f:
        board_content = f.read()
    
    # Parse the board
    board = Board(parse_markdown_lines(board_content.splitlines()))
    
    # Generate execution report
    analysis_date = date(2026, 1, 15)
    report = generate_execution_report(board, analysis_date)
    
    # Compose markdown report
    markdown = compose_execution_report(report)
    
    # Verify all 9 sections are present in correct order
    assert "# Daily Execution Report" in markdown
    assert "## Inbox" in markdown
    assert "## High Five" in markdown
    assert "## Schedule Review" in markdown
    assert "## Board Health" in markdown
    assert "## Focus Analysis" in markdown
    assert "## Corridor Analysis" in markdown
    assert "## Score Suggestions" in markdown
    assert "## Task Analysis" in markdown
    assert "## Strategic Findings" in markdown
    
    # Verify section order
    inbox_idx = markdown.index("## Inbox")
    high_five_idx = markdown.index("## High Five")
    schedule_idx = markdown.index("## Schedule Review")
    health_idx = markdown.index("## Board Health")
    focus_idx = markdown.index("## Focus Analysis")
    corridor_idx = markdown.index("## Corridor Analysis")
    score_idx = markdown.index("## Score Suggestions")
    task_idx = markdown.index("## Task Analysis")
    strategic_idx = markdown.index("## Strategic Findings")
    
    assert inbox_idx < high_five_idx
    assert high_five_idx < schedule_idx
    assert schedule_idx < health_idx
    assert health_idx < focus_idx
    assert focus_idx < corridor_idx
    assert corridor_idx < score_idx
    assert score_idx < task_idx
    assert task_idx < strategic_idx
    
    # Verify report metadata
    assert "**Analysis Date:** 2026-01-15" in markdown
    assert "**Report ID:**" in markdown
    assert "**Schema Version:** 1.0" in markdown
    assert "Generated at" in markdown


def test_full_report_pipeline_with_complex_board():
    """Test the full pipeline with a complex board fixture."""
    fixture_path = "tests/fixtures/complex_board.md"
    
    with open(fixture_path, 'r', encoding='utf-8') as f:
        board_content = f.read()
    
    board = Board(parse_markdown_lines(list(board_content.splitlines())))
    analysis_date = date(2026, 1, 15)
    report = generate_execution_report(board, analysis_date)
    markdown = compose_execution_report(report)
    
    # Verify all sections present
    assert "## Inbox" in markdown
    assert "## High Five" in markdown
    assert "## Schedule Review" in markdown
    assert "## Board Health" in markdown
    assert "## Focus Analysis" in markdown
    assert "## Corridor Analysis" in markdown
    assert "## Score Suggestions" in markdown
    assert "## Task Analysis" in markdown
    assert "## Strategic Findings" in markdown
    
    # Verify section order
    sections = [
        "## Inbox",
        "## High Five",
        "## Schedule Review",
        "## Board Health",
        "## Focus Analysis",
        "## Corridor Analysis",
        "## Score Suggestions",
        "## Task Analysis",
        "## Strategic Findings",
    ]
    
    prev_idx = -1
    for section in sections:
        idx = markdown.index(section)
        assert idx > prev_idx, f"Section {section} appears out of order"
        prev_idx = idx


def test_full_report_pipeline_deterministic():
    """Test that the full pipeline produces deterministic output."""
    fixture_path = "tests/fixtures/simple_board.md"
    
    with open(fixture_path, 'r', encoding='utf-8') as f:
        board_content = f.read()
    
    board = Board(parse_markdown_lines(board_content.splitlines()))
    analysis_date = date(2026, 1, 15)
    
    # Generate report twice
    report1 = generate_execution_report(board, analysis_date)
    markdown1 = compose_execution_report(report1)
    
    report2 = generate_execution_report(board, analysis_date)
    markdown2 = compose_execution_report(report2)
    
    # Reports should be identical (except for report_id and generated_at)
    # We'll compare the structure by removing dynamic fields
    def normalize(md: str) -> str:
        lines = md.split('\n')
        normalized = []
        for line in lines:
            if line.startswith("**Report ID:**") or line.startswith("*Generated at"):
                continue
            normalized.append(line)
        return '\n'.join(normalized)
    
    assert normalize(markdown1) == normalize(markdown2)


def test_full_report_pipeline_empty_board():
    """Test the full pipeline with an empty board."""
    board_content = """# Kanban Board

## Backlog

## Doing

## Done
"""
    
    board = Board(parse_markdown_lines(board_content.splitlines()))
    analysis_date = date(2026, 1, 15)
    report = generate_execution_report(board, analysis_date)
    markdown = compose_execution_report(report)
    
    # Should still generate all sections
    assert "## Inbox" in markdown
    assert "## High Five" in markdown
    assert "## Schedule Review" in markdown
    assert "## Board Health" in markdown
    assert "## Focus Analysis" in markdown
    assert "## Corridor Analysis" in markdown
    assert "## Score Suggestions" in markdown
    assert "## Task Analysis" in markdown
    assert "## Strategic Findings" in markdown
    
    # Should indicate empty state appropriately
    assert "Inbox is clear" in markdown or "No tasks" in markdown


def test_full_report_pipeline_with_nested_tasks():
    """Test the full pipeline with nested tasks."""
    fixture_path = "tests/fixtures/nested_tasks.md"
    
    with open(fixture_path, 'r', encoding='utf-8') as f:
        board_content = f.read()
    
    board = Board(parse_markdown_lines(list(board_content.splitlines())))
    analysis_date = date(2026, 1, 15)
    report = generate_execution_report(board, analysis_date)
    markdown = compose_execution_report(report)
    
    # Verify all sections present
    assert "## Inbox" in markdown
    assert "## High Five" in markdown
    assert "## Schedule Review" in markdown
    assert "## Board Health" in markdown
    assert "## Focus Analysis" in markdown
    assert "## Corridor Analysis" in markdown
    assert "## Score Suggestions" in markdown
    assert "## Task Analysis" in markdown
    assert "## Strategic Findings" in markdown


def test_compose_execution_report_structure():
    """Test that compose_execution_report produces well-formed markdown."""
    fixture_path = "tests/fixtures/simple_board.md"
    
    with open(fixture_path, 'r', encoding='utf-8') as f:
        board_content = f.read()
    
    board = Board(parse_markdown_lines(list(board_content.splitlines())))
    analysis_date = date(2026, 1, 15)
    report = generate_execution_report(board, analysis_date)
    markdown = compose_execution_report(report)
    
    # Check basic markdown structure
    lines = markdown.split('\n')
    
    # First line should be the title
    assert lines[0] == "# Daily Execution Report"
    
    # Should have metadata
    metadata_lines = [l for l in lines if l.startswith("**Analysis Date:**") or 
                      l.startswith("**Report ID:**") or 
                      l.startswith("**Schema Version:**")]
    assert len(metadata_lines) == 3
    
    # Each section should be separated by blank lines
    # Count section headers
    section_headers = [l for l in lines if l.startswith("## ")]
    assert len(section_headers) == 9  # 9 sections
    
    # Should end with footer
    assert "---" in markdown
    assert "Generated at" in markdown


def test_full_report_composition_without_placeholders():
    """
    Integration test: Proof of MVP.
    
    Verifies that the composed report:
    - Does NOT contain placeholder text "_⚠️ Will be implemented_"
    - Contains real section headers: ## High Five, ## Focus Analysis, ## Board Health
    - Contains generation timestamp in format YYYY-MM-DD HH:MM:SS
    """
    import re
    
    fixture_path = "tests/fixtures/simple_board.md"
    
    with open(fixture_path, 'r', encoding='utf-8') as f:
        board_content = f.read()
    
    board = Board(parse_markdown_lines(board_content.splitlines()))
    analysis_date = date(2026, 1, 15)
    report = generate_execution_report(board, analysis_date)
    markdown = compose_execution_report(report)
    
    # 1. Assert NO placeholder text remains
    assert "_⚠️ Will be implemented_" not in markdown, \
        "Report still contains placeholder text '_⚠️ Will be implemented_'"
    
    # 2. Assert real section headers are present
    assert "## High Five" in markdown, "Missing '## High Five' section"
    assert "## Focus Analysis" in markdown, "Missing '## Focus Analysis' section"
    assert "## Board Health" in markdown, "Missing '## Board Health' section"
    assert "## Inbox" in markdown, "Missing '## Inbox' section"
    assert "## Schedule Review" in markdown, "Missing '## Schedule Review' section"
    assert "## Corridor Analysis" in markdown, "Missing '## Corridor Analysis' section"
    assert "## Score Suggestions" in markdown, "Missing '## Score Suggestions' section"
    assert "## Task Analysis" in markdown, "Missing '## Task Analysis' section"
    assert "## Strategic Findings" in markdown, "Missing '## Strategic Findings' section"
    
    # 3. Assert generation timestamp format: YYYY-MM-DD HH:MM:SS
    timestamp_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    assert re.search(timestamp_pattern, markdown), \
        f"Report missing timestamp in format YYYY-MM-DD HH:MM:SS. Found: {markdown[-200:]}"
    
    # Additional: verify the timestamp is in the footer area (after ---)
    footer_section = markdown.split("---")[-1] if "---" in markdown else markdown
    assert re.search(timestamp_pattern, footer_section), \
        "Timestamp not found in footer section"


if __name__ == "__main__":
    test_full_report_pipeline_with_simple_board()
    test_full_report_pipeline_with_complex_board()
    test_full_report_pipeline_deterministic()
    test_full_report_pipeline_empty_board()
    test_full_report_pipeline_with_nested_tasks()
    test_compose_execution_report_structure()
    test_full_report_composition_without_placeholders()
    print("All integration tests passed!")