"""Tests for detect_overload."""

from src.analytics.calculators.overload_detector import detect_overload
from src.analytics.models import WipStatus


def _make_wip(section: str, active: int, limit: int) -> WipStatus:
    """Helper to create WipStatus for testing."""
    utilization = active / limit if limit > 0 else 0.0
    return WipStatus(
        section_name=section,
        active_tasks=active,
        wip_limit=limit,
        remaining_capacity=max(limit - active, 0),
        utilization=utilization,
        is_near_limit=utilization >= 0.8,
        is_over_limit=active > limit,
    )


class TestDetectOverload:
    def test_no_overload(self):
        """Normal workload generates no signals."""
        wip = [_make_wip("Dev", 2, 5)]  # 40%
        assert detect_overload(wip) == []

    def test_near_limit_generates_warning(self):
        """Workload >= 80% generates a WARNING signal."""
        wip = [_make_wip("Review", 4, 5)]  # 80%
        signals = detect_overload(wip)
        
        assert len(signals) == 1
        assert signals[0].severity == "WARNING"
        assert "Review" in signals[0].section_name
        assert "nearing WIP limit" in signals[0].message

    def test_over_limit_generates_critical(self):
        """Workload > 100% generates a CRITICAL signal."""
        wip = [_make_wip("Dev", 6, 5)]  # 120%
        signals = detect_overload(wip)
        
        assert len(signals) == 1
        assert signals[0].severity == "CRITICAL"
        assert "OVER WIP limit" in signals[0].message

    def test_sorting_by_severity(self):
        """CRITICAL signals appear before WARNING signals."""
        wip = [
            _make_wip("Review", 4, 5),  # WARNING
            _make_wip("Dev", 6, 5),     # CRITICAL
        ]
        signals = detect_overload(wip)
        
        assert len(signals) == 2
        assert signals[0].severity == "CRITICAL"
        assert signals[1].severity == "WARNING"