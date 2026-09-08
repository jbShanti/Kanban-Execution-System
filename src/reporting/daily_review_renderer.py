"""
DEPRECATED: This module is deprecated and will be removed in a future version.

Use `src.reporting.execution_report_composer.compose_execution_report` instead.

This file is kept temporarily for backward compatibility during migration.
"""

from __future__ import annotations

import warnings

from src.analytics.models import ExecutionReport
from src.reporting.execution_report_composer import compose_execution_report


def render_daily_review(report: ExecutionReport) -> str:
    """
    DEPRECATED: Use compose_execution_report() instead.
    
    This function is kept for backward compatibility only.
    It delegates to the new unified composer.
    """
    warnings.warn(
        "render_daily_review is deprecated. Use compose_execution_report from "
        "src.reporting.execution_report_composer instead.",
        DeprecationWarning,
        stacklevel=2
    )
    return compose_execution_report(report)