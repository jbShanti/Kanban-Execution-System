from __future__ import annotations

from src.analytics.models import FocusAttentionAnalytics


def render_focus_analysis_section(
    analytics: FocusAttentionAnalytics,
) -> str:
    """Render the Focus Analysis section showing attention distribution by tags."""

    lines: list[str] = []

    lines.append("## Focus Analysis")
    lines.append("")

    lines.append(f"- Active Tasks: {analytics.active_tasks}")
    lines.append(f"- Overdue Tasks: {analytics.overdue_tasks}")
    lines.append(f"- High Score Tasks: {analytics.high_score_tasks}")
    lines.append(f"- Total Attention Score: {analytics.total_attention_score}")
    lines.append("")

    if not analytics.top_attention_tags:
        lines.append("No attention data available.")
        lines.append("")
        return "\n".join(lines)

    lines.append("### Attention by Tag")
    lines.append("")

    for tag, score, share in analytics.top_attention_tags:
        percentage = share * 100
        bar_length = int(percentage / 5)  # 20 chars = 100%
        bar = "█" * bar_length + "░" * (20 - bar_length)
        lines.append(f"- **{tag}**: {score} ({percentage:.1f}%) `{bar}`")

    lines.append("")

    # Check for overload/concentration
    if analytics.top_attention_tags:
        top_tag, _, top_share = analytics.top_attention_tags[0]
        if top_share > 0.6:  # More than 60% in one tag
            lines.append(
                f"⚠️ **Overload Alert**: "
                f"'{top_tag}' consumes {top_share:.0%} of attention. "
                f"Consider redistributing workload."
            )
            lines.append("")

    return "\n".join(lines)