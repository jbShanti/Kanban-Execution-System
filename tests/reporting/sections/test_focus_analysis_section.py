from src.analytics.models import FocusAttentionAnalytics
from src.reporting.sections.focus_analysis_section import (
    render_focus_analysis_section,
)


def test_render_focus_analysis_section():
    """Test rendering focus analysis section with data."""
    analytics = FocusAttentionAnalytics(
        active_tasks=10,
        overdue_tasks=2,
        high_score_tasks=3,
        attention_by_tag={
            "health": 50,
            "ai": 30,
            "career": 20,
        },
        total_attention_score=100,
        top_attention_tags=(
            ("health", 50, 0.5),
            ("ai", 30, 0.3),
            ("career", 20, 0.2),
        ),
    )

    report = render_focus_analysis_section(analytics)

    assert "Focus Analysis" in report
    assert "Active Tasks: 10" in report
    assert "Overdue Tasks: 2" in report
    assert "High Score Tasks: 3" in report
    assert "Total Attention Score: 100" in report
    assert "health" in report
    assert "ai" in report
    assert "career" in report
    assert "50.0%" in report  # health share
    assert "30.0%" in report  # ai share
    assert "20.0%" in report  # career share


def test_render_focus_analysis_section_empty():
    """Test rendering focus analysis section with no data."""
    analytics = FocusAttentionAnalytics(
        active_tasks=0,
        overdue_tasks=0,
        high_score_tasks=0,
        attention_by_tag={},
        total_attention_score=0,
        top_attention_tags=(),
    )

    report = render_focus_analysis_section(analytics)

    assert "Focus Analysis" in report
    assert "Active Tasks: 0" in report
    assert "Overdue Tasks: 0" in report
    assert "High Score Tasks: 0" in report
    assert "Total Attention Score: 0" in report
    assert "No attention data available" in report


def test_render_focus_analysis_section_with_many_tags():
    """Test rendering focus analysis section with many tags (top 7)."""
    analytics = FocusAttentionAnalytics(
        active_tasks=20,
        overdue_tasks=1,
        high_score_tasks=5,
        attention_by_tag={
            "tag1": 100,
            "tag2": 90,
            "tag3": 80,
            "tag4": 70,
            "tag5": 60,
            "tag6": 50,
            "tag7": 40,
            "tag8": 30,  # Should not appear in top 7
        },
        total_attention_score=520,
        top_attention_tags=(
            ("tag1", 100, 100/520),
            ("tag2", 90, 90/520),
            ("tag3", 80, 80/520),
            ("tag4", 70, 70/520),
            ("tag5", 60, 60/520),
            ("tag6", 50, 50/520),
            ("tag7", 40, 40/520),
        ),
    )

    report = render_focus_analysis_section(analytics)

    assert "tag1" in report
    assert "tag7" in report
    assert "tag8" not in report  # Only top 7 should be shown
    assert "19.2%" in report  # tag1 share (100/520 ≈ 19.2%)


def test_render_focus_analysis_section_overload_indicators():
    """Test that overload indicators are shown when attention is concentrated."""
    analytics = FocusAttentionAnalytics(
        active_tasks=10,
        overdue_tasks=0,
        high_score_tasks=2,
        attention_by_tag={
            "health": 80,
            "ai": 10,
            "career": 10,
        },
        total_attention_score=100,
        top_attention_tags=(
            ("health", 80, 0.8),
            ("ai", 10, 0.1),
            ("career", 10, 0.1),
        ),
    )

    report = render_focus_analysis_section(analytics)

    assert "Focus Analysis" in report
    assert "health" in report
    assert "80.0%" in report
    # Should indicate concentration/overload
    assert "⚠️" in report or "overload" in report.lower() or "concentrated" in report.lower()