# Execution Report Architecture Specification

## 1. Purpose and Context

This document defines the canonical architecture for the **Execution Report module** in the Kanban Execution System (KES).

It establishes:

- The single authoritative data model for execution state (`ExecutionReport`)
- The deterministic generation pipeline aligned with `Analytics_Model_v2`
- Contracts between architectural layers
- Criteria for reproducibility and testability
- Technical debt elimination plan

This specification implements the canonical pipeline defined in `docs/Models/Analytics_Model_v2.md` Section 5 (Execution Artifact Pipeline) and aligns with `docs/Foundations/ARCHITECTURE.md`.

### Scope

This document covers the **entire Execution Report module**, not a single presentation artifact.

`ExecutionReport` is the universal canonical snapshot consumed by **all** presentation artifacts:

- Morning Brief
- Daily Review
- Weekly Review
- Dashboard Snapshot
- API responses
- Future exports

The 9-section structure defined in `docs/Product/Roadmap.md` Phase 2 is the structure of the **Daily Review renderer**, not the structure of `ExecutionReport` itself.

---

## 2. Architectural Principles

### 2.1 Single Source of Truth

There is exactly **one canonical report model**: `ExecutionReport`.

All presentation artifacts consume only `ExecutionReport`. No alternative report models may exist in the codebase.

### 2.2 ExecutionReport Is Not a Report Template

`ExecutionReport` represents the **universal state of the execution system**, not the layout of any specific report.

It must not contain fields that exist solely for one presentation artifact. Fields like `inbox_tasks`, `high_five_tasks`, or `due_today_tasks` are **presentation concerns** and belong to renderers, not to the canonical model.

### 2.3 Presentation Derives from ExecutionReport

The data flow is strictly one-directional:

```text
ExecutionReport -> Presentation Artifact
```

Never the reverse. Presentation artifacts select, filter, and format data from `ExecutionReport`. They never inject structure back into it.

### 2.4 Deterministic Pipeline

The generation pipeline must be fully deterministic:

- Identical board input + identical injected analysis date produces identical `ExecutionReport`
- No internal use of `datetime.now()`, `date.today()`, or ambient clocks
- All time-dependent calculations receive time as an explicit parameter
- All functions are pure where possible (same input produces same output)

### 2.5 Composition over Computation

`ExecutionReport` is a **composition boundary**, not an analytical engine:

- It aggregates pre-computed analytics artifacts
- It does not perform calculations, generate findings, or render content
- It preserves upstream artifacts without modification

### 2.6 Strict Layering

The pipeline follows the canonical artifact sequence from `Analytics_Model_v2`:

```text
Board
  -> Measurements
  -> DistributionProfile
  -> CorridorEvaluation
  -> FindingCollection
  -> ExecutiveSummary
  -> RecommendationCollection
  -> ExecutionReport
  -> Presentation Artifacts
```

Each layer communicates through explicit immutable contracts. No layer may bypass an intermediate contract or reach back into upstream layers.

---

## 3. Canonical Data Model

### 3.1 ExecutionReport Structure

`ExecutionReport` is organized around the four canonical semantic sections defined in `Analytics_Model_v2` and `ExecutionReport_Design.md`:

1. **Metadata and Provenance** — traceability
2. **Executive Summary** — what matters most
3. **Recommendation Collection** — what should be done
4. **Analytics** — what was measured (for transparency and debugging)
5. **Findings** — analytical conclusions

```python
from dataclasses import dataclass, field
from datetime import datetime, date
from src.analytics.models import (
    BoardHealth,
    FocusAttentionAnalytics,
    ScoreCorridor,
    AnalyticsTaskSnapshot,
    BoardSummary,
    SectionMetrics,
    WipStatus,
)

@dataclass(frozen=True)
class ExecutionReport:
    """
    Canonical immutable snapshot of the execution system state.
    
    ExecutionReport is the final output of the analytics pipeline and
    the sole contract consumed by all presentation artifacts.
    
    It represents the UNIVERSAL state of the system, not the layout
    of any specific report. Presentation artifacts derive their
    structure from this model.
    """
    
    # ============================================================
    # 1. METADATA AND PROVENANCE
    # ============================================================
    
    schema_version: str
        # Semantic version of the report contract (e.g., "1.0")
    
    report_id: str
        # Unique identifier for this report instance (UUID)
    
    analysis_date: date
        # The date for which this report was generated (injected, not ambient)
    
    generated_at: datetime
        # Timestamp of report creation (injected, not datetime.now())
    
    board_path: str
        # Source board identifier for provenance
    
    board_digest: str
        # SHA-256 digest of the source board for reproducibility
    
    configuration_digest: str
        # SHA-256 digest of the configuration used
    
    # ============================================================
    # 2. EXECUTIVE SUMMARY
    # ============================================================
    
    executive_summary: ExecutiveSummary
        # Synthesized assessment of what matters most.
        # Aggregated from FindingCollection.
        # Contains: system_state, strengths, risks, opportunities, context
    
    # ============================================================
    # 3. RECOMMENDATION COLLECTION
    # ============================================================
    
    recommendations: RecommendationCollection
        # Structured actionable recommendations.
        # In MVP: availability = "not_produced"
        # In Phase 3+: operating_mode, strategic, tactical, task recommendations
    
    # ============================================================
    # 4. ANALYTICS (Measurements and Evaluations)
    # ============================================================
    
    analytics: AnalyticsBundle
        # Complete analytical measurements for transparency.
        # Presentation artifacts may render subsets of this data.
    
    # ============================================================
    # 5. FINDINGS
    # ============================================================
    
    findings: tuple[Finding, ...]
        # Analytical conclusions supported by evidence.
        # Ordered by severity and decision significance.
    
    # ============================================================
    # 6. BOARD HEALTH (cross-cutting concern)
    # ============================================================
    
    board_health: BoardHealth
        # Analytics readiness and metadata quality assessment.
        # Every presentation artifact must interpret findings
        # through the lens of board_health.
```

### 3.2 AnalyticsBundle

`AnalyticsBundle` contains all raw measurements and evaluations. Presentation artifacts select what they need.

```python
@dataclass(frozen=True)
class AnalyticsBundle:
    """
    Complete analytical measurements produced by the Analytics Engine.
    
    This is a transparency layer: presentation artifacts may render
    any subset of this data, but must not modify it.
    """
    
    # Board-level summary
    board_summary: BoardSummary
        # Total tasks, active tasks, scored tasks, score corridors, etc.
    
    # Section-level metrics
    section_metrics: tuple[SectionMetrics, ...]
        # Per-section breakdown: tasks, scores, WIP
    
    # WIP analysis
    wip_statuses: tuple[WipStatus, ...]
        # WIP limits, utilization, over-limit signals
    
    # Focus analysis
    focus_analytics: FocusAttentionAnalytics
        # Attention distribution by tags, overload alerts
    
    # Corridor analysis
    corridor_analysis: tuple[ScoreCorridor, ...]
        # Score distribution across corridors (21-25, 16-20, etc.)
    
    # Complete task snapshots
    task_snapshots: tuple[AnalyticsTaskSnapshot, ...]
        # Analytical view of every task (for Task Analysis section)
    
    # Data quality
    analytics_confidence: str
        # high | medium | low | none (derived from BoardHealth)
```

### 3.3 ExecutiveSummary

```python
@dataclass(frozen=True)
class ExecutiveSummary:
    """
    Synthesized assessment of the current system state.
    
    Aggregated from FindingCollection. Does not perform analysis.
    """
    
    system_state: str
        # stable | warning | critical | degraded
    
    primary_conclusion: str
        # One-sentence assessment of the system
    
    strengths: tuple[str, ...]
        # What is working well
    
    risks: tuple[str, ...]
        # What requires attention
    
    opportunities: tuple[str, ...]
        # What could be improved
    
    context: tuple[str, ...]
        # Background information
```

### 3.4 RecommendationCollection

```python
@dataclass(frozen=True)
class RecommendationCollection:
    """
    Structured actionable recommendations.
    
    In MVP: availability = "not_produced"
    In Phase 3+: populated by Recommendation Engine
    """
    
    availability: str
        # "not_produced" (MVP) | "produced" (Phase 3+)
    
    operating_mode: str | None
        # Completion Mode, Recovery Mode, Deep Focus Mode, etc.
        # None in MVP
    
    strategic: tuple[Recommendation, ...]
        # High-level direction recommendations
    
    tactical: tuple[Recommendation, ...]
        # System-level change recommendations
    
    task_recommendations: tuple[TaskRecommendation, ...]
        # Specific task-level recommendations
        # THIS is where High Five, Inbox priorities, Schedule live


@dataclass(frozen=True)
class Recommendation:
    """A single actionable recommendation."""
    id: str
    priority: str  # high | medium | low
    action: str
    rationale: str
    source_finding_ids: tuple[str, ...]


@dataclass(frozen=True)
class TaskRecommendation:
    """A recommendation tied to a specific task."""
    task_id: str
    task_title: str
    recommendation_type: str  # do_today | schedule | delegate | archive | score_adjust
    priority: int
    rationale: str
    suggested_date: date | None
    suggested_score: int | None
```

### 3.5 Finding

```python
@dataclass(frozen=True)
class Finding:
    """
    Analytical conclusion supported by evidence.
    Follows Finding Catalogue specification from Analytics_Model_v2.
    """
    id: str
    title: str
    type: str  # Observation, Strength, Risk, Opportunity
    statement: str
    severity: str  # Info, Success, Warning, Critical
    confidence: str  # High, Medium, Low
    evidence: tuple[EvidenceFact, ...]
    analytics_sources: tuple[str, ...]


@dataclass(frozen=True)
class EvidenceFact:
    """Objective fact supporting a Finding."""
    fact_type: str  # metric, entity, comparison
    key: str
    value: str | int | float
```

---

## 4. Generation Pipeline

### 4.1 Canonical Pipeline (aligned with Analytics_Model_v2)

```text
+------------------------------------------------------------------+
|                        INPUT LAYER                                |
+------------------------------------------------------------------+
|  Obsidian Markdown Board  |  config/scoring.yaml  |  as_of_date  |
+--------------+------------+-----------+-----------+------+-------+
               |                        |                  |
               v                        v                  |
+------------------------------------------------------------------+
|                      PARSER LAYER                                 |
+------------------------------------------------------------------+
|  parse_markdown_file(path) -> Board (domain model)                |
+-------------------------------+----------------------------------+
                                |
                                v
+------------------------------------------------------------------+
|                    ANALYTICS LAYER                                |
+------------------------------------------------------------------+
|                                                                   |
|  Stage 1: Measurements                                            |
|  +- build_task_snapshots(board, as_of_date)                      |
|  |    -> list[AnalyticsTaskSnapshot]                              |
|  +- build_board_summary(board)                                    |
|  |    -> BoardSummary                                             |
|  +- build_section_metrics(board)                                  |
|  |    -> list[SectionMetrics]                                     |
|  +- calculate_wip_metrics(board)                                  |
|       -> list[WipStatus]                                          |
|                                                                   |
|  Stage 2: Distribution and Corridor Evaluation                    |
|  +- calculate_corridors(task_snapshots)                           |
|  |    -> list[ScoreCorridor]                                      |
|  +- build_focus_analytics(task_snapshots)                         |
|       -> FocusAttentionAnalytics                                  |
|                                                                   |
|  Stage 3: Board Health                                            |
|  +- build_board_health(task_snapshots)                            |
|       -> BoardHealth                                              |
|                                                                   |
|  Stage 4: Findings                                                |
|  +- generate_findings(                                            |
|  |      board_summary, corridor_analysis,                         |
|  |      focus_analytics, board_health, wip_statuses               |
|  |  )                                                             |
|       -> list[Finding]                                            |
|                                                                   |
+-------------------------------+----------------------------------+
                                |
                                v
+------------------------------------------------------------------+
|                  SYNTHESIS LAYER                                  |
+------------------------------------------------------------------+
|                                                                   |
|  Stage 5: Executive Summary                                       |
|  +- build_executive_summary(findings)                             |
|       -> ExecutiveSummary                                         |
|                                                                   |
|  Stage 6: Recommendations                                         |
|  +- build_recommendation_collection(executive_summary)            |
|       -> RecommendationCollection                                 |
|       (MVP: availability="not_produced")                          |
|                                                                   |
+-------------------------------+----------------------------------+
                                |
                                v
+------------------------------------------------------------------+
|                  COMPOSITION LAYER                                |
+------------------------------------------------------------------+
|                                                                   |
|  assemble_execution_report(                                       |
|      metadata=...,                                                |
|      executive_summary=executive_summary,                         |
|      recommendations=recommendations,                             |
|      analytics=analytics_bundle,                                  |
|      findings=findings,                                           |
|      board_health=board_health,                                   |
|  )                                                                |
|  -> ExecutionReport                                               |
|                                                                   |
+-------------------------------+----------------------------------+
                                |
                                v
+------------------------------------------------------------------+
|                  PRESENTATION LAYER                               |
+------------------------------------------------------------------+
|                                                                   |
|  Each artifact derives its structure from ExecutionReport:        |
|                                                                   |
|  DailyReviewRenderer                                              |
|  +- Section 1: Inbox        <- recommendations.task_recommendations|
|  +- Section 2: High Five    <- recommendations.task_recommendations|
|  +- Section 3: Schedule     <- recommendations.task_recommendations|
|  +- Section 4: Board Health <- board_health                       |
|  +- Section 5: Focus        <- analytics.focus_analytics          |
|  +- Section 6: Corridors    <- analytics.corridor_analysis        |
|  +- Section 7: Scores       <- recommendations.task_recommendations|
|  +- Section 8: Tasks        <- analytics.task_snapshots           |
|  +- Section 9: Findings     <- findings                           |
|                                                                   |
|  MorningBriefRenderer                                             |
|  +- Operating Mode    <- recommendations.operating_mode           |
|  +- Top Priorities    <- recommendations.task_recommendations     |
|  +- Schedule          <- recommendations.task_recommendations     |
|  +- System State      <- executive_summary.system_state           |
|                                                                   |
|  DashboardRenderer                                                |
|  +- Metrics           <- analytics.board_summary                  |
|  +- Corridors         <- analytics.corridor_analysis              |
|  +- Health            <- board_health                             |
|                                                                   |
+------------------------------------------------------------------+
```

### 4.2 Implementation: Service Layer

```python
# src/analytics/service.py

from datetime import date, datetime
import uuid
import hashlib

def generate_execution_report(
    board: Board,
    as_of_date: date | None = None,
) -> ExecutionReport:
    """
    Generate a deterministic ExecutionReport.
    
    This is the canonical pipeline that produces the universal
    execution state. Presentation artifacts consume this report
    and derive their specific views.
    """
    # Inject analysis date explicitly
    analysis_date = as_of_date if as_of_date is not None else date.today()
    
    # ── Stage 1: Measurements ──────────────────────────────
    task_snapshots = tuple(
        build_task_snapshot(task, analysis_date)
        for task in board.tasks
    )
    
    board_summary = build_board_summary(board)
    section_metrics = tuple(build_section_metrics_map(board, board_summary.sections).values())
    wip_statuses = tuple(calculate_wip_metrics(board))
    
    # ── Stage 2: Distribution and Corridor Evaluation ──────
    corridor_analysis = tuple(calculate_corridors(task_snapshots))
    focus_analytics = build_focus_attention_analytics(task_snapshots)
    
    # ── Stage 3: Board Health ──────────────────────────────
    board_health = build_board_health(task_snapshots)
    analytics_confidence = derive_analytics_confidence(board_health)
    
    # ── Stage 4: Findings ──────────────────────────────────
    findings = tuple(generate_findings(
        board_summary=board_summary,
        corridor_analysis=corridor_analysis,
        focus_analytics=focus_analytics,
        board_health=board_health,
        wip_statuses=wip_statuses,
    ))
    
    # ── Stage 5: Executive Summary ─────────────────────────
    executive_summary = build_executive_summary(findings)
    
    # ── Stage 6: Recommendations ───────────────────────────
    recommendations = build_recommendation_collection(executive_summary)
    # MVP: returns RecommendationCollection(availability="not_produced", ...)
    
    # ── Compose AnalyticsBundle ────────────────────────────
    analytics_bundle = AnalyticsBundle(
        board_summary=board_summary,
        section_metrics=section_metrics,
        wip_statuses=wip_statuses,
        focus_analytics=focus_analytics,
        corridor_analysis=corridor_analysis,
        task_snapshots=task_snapshots,
        analytics_confidence=analytics_confidence,
    )
    
    # ── Compose ExecutionReport ────────────────────────────
    return ExecutionReport(
        schema_version="1.0",
        report_id=str(uuid.uuid4()),
        analysis_date=analysis_date,
        generated_at=datetime.now(),
        board_path=board.path or "unknown",
        board_digest=compute_board_digest(board),
        configuration_digest=compute_config_digest(),
        executive_summary=executive_summary,
        recommendations=recommendations,
        analytics=analytics_bundle,
        findings=findings,
        board_health=board_health,
    )
```

---

## 5. Presentation Layer Architecture

### 5.1 Key Principle

Presentation artifacts **derive** their structure from `ExecutionReport`. They do not define the structure of `ExecutionReport`.

The 9 sections from `Roadmap.md` are the structure of `DailyReviewRenderer`, not the structure of `ExecutionReport`.

### 5.2 Daily Review Renderer (MVP)

```python
# src/reporting/daily_review_renderer.py

def render_daily_review(report: ExecutionReport) -> str:
    """
    Render the Daily Review presentation artifact.
    
    This implements the 9-section structure from Roadmap.md Phase 2.
    All data is derived from ExecutionReport.
    """
    
    sections = [
        "# Daily Review",
        f"\n**Analysis Date:** {report.analysis_date.isoformat()}\n",
        
        # Section 1: Inbox
        _render_inbox_section(report.recommendations),
        
        # Section 2: High Five
        _render_high_five_section(report.recommendations),
        
        # Section 3: Schedule Review
        _render_schedule_review_section(report.recommendations),
        
        # Section 4: Board Health
        _render_board_health_section(report.board_health),
        
        # Section 5: Focus Analysis
        _render_focus_analysis_section(report.analytics.focus_analytics),
        
        # Section 6: Corridor Analysis
        _render_corridor_section(report.analytics.corridor_analysis),
        
        # Section 7: Score Suggestions
        _render_score_suggestions_section(report.recommendations),
        
        # Section 8: Task Analysis
        _render_task_analysis_section(report.analytics.task_snapshots),
        
        # Section 9: Strategic Findings
        _render_strategic_findings_section(report.findings),
    ]
    
    return "\n".join(section for section in sections if section)


def _render_inbox_section(recommendations: RecommendationCollection) -> str:
    """Derive Inbox from task recommendations with type='process_inbox'."""
    inbox_recs = [
        rec for rec in recommendations.task_recommendations
        if rec.recommendation_type == "process_inbox"
    ]
    # ... render markdown


def _render_high_five_section(recommendations: RecommendationCollection) -> str:
    """Derive High Five from task recommendations with type='do_today'."""
    top_five = [
        rec for rec in recommendations.task_recommendations
        if rec.recommendation_type == "do_today"
    ][:5]
    # ... render markdown


def _render_schedule_review_section(recommendations: RecommendationCollection) -> str:
    """Derive Schedule from task recommendations with type='schedule'."""
    scheduled = [
        rec for rec in recommendations.task_recommendations
        if rec.recommendation_type == "schedule"
    ]
    # ... render markdown
```

### 5.3 Morning Brief Renderer (Future)

```python
# src/reporting/morning_brief_renderer.py

def render_morning_brief(report: ExecutionReport) -> str:
    """
    Render the Morning Brief presentation artifact.
    
    Different structure from Daily Review, same data source.
    """
    
    sections = [
        "# Morning Brief",
        f"\n**{report.analysis_date.isoformat()}**\n",
        
        # Operating Mode
        _render_operating_mode(report.recommendations.operating_mode),
        
        # System State
        _render_system_state(report.executive_summary),
        
        # Top Priorities (from recommendations)
        _render_top_priorities(report.recommendations.task_recommendations),
        
        # Today's Schedule
        _render_schedule(report.recommendations.task_recommendations),
        
        # Key Risks
        _render_risks(report.executive_summary.risks),
    ]
    
    return "\n".join(section for section in sections if section)
```

### 5.4 Section Renderer Contract

Each renderer function:

- Receives only the data it needs from `ExecutionReport` (minimal surface)
- Returns a Markdown string (or empty string if no content)
- Is a pure function (no side effects)
- Does not access `Board`, `Analytics`, or `Findings` directly
- Does not perform analytics calculations
- Does not generate new recommendations

---

## 6. Layer Contracts

### 6.1 Parser to Analytics Contract

**Input:** `Board` (immutable domain model)

**Invariants:**
- Board contains only normalized, validated tasks
- All metadata is extracted and validated
- No Markdown syntax remains in domain objects

### 6.2 Analytics to Findings Contract

**Input:** Measurements (BoardSummary, ScoreCorridor[], FocusAttentionAnalytics, BoardHealth, WipStatus[])

**Invariants:**
- Every Finding is traceable to specific measurements
- Findings are deterministic: same measurements produce same findings
- Findings do not perform new calculations

### 6.3 Findings to ExecutiveSummary Contract

**Input:** `FindingCollection`

**Invariants:**
- ExecutiveSummary aggregates Findings exclusively
- It never consumes measurements directly
- It does not create new Findings
- It does not generate recommendations

### 6.4 ExecutiveSummary to RecommendationCollection Contract

**Input:** `ExecutiveSummary` + `RecommendationConfiguration`

**Invariants:**
- Recommendations are derived from ExecutiveSummary
- Recommendation Engine does not recalculate analytics
- In MVP: `availability = "not_produced"`

### 6.5 ExecutionReport to Presentation Contract

**Input:** Immutable `ExecutionReport`

**Invariants:**
- Presentation never accesses Parser, Analytics, or Board directly
- Presentation never performs calculations or generates findings
- Presentation only formats, groups, and localizes data
- Each presentation artifact selects a subset of ExecutionReport fields

**Presentation must not:**
- Read Markdown files
- Access `AnalyticsReport` or `AnalyticsSnapshot`
- Calculate metrics, thresholds, or rankings
- Infer recommendations or priorities not present in `RecommendationCollection`
- Filter or reorder data beyond presentation preferences

---

## 7. Determinism Requirements

### 7.1 Time Injection Rule

**Forbidden:**

```python
# Uses ambient clock - NOT ALLOWED
today = date.today()
now = datetime.now()
```

**Required:**

```python
# Injected explicitly - CORRECT
def calculate_overdue(task: Task, as_of_date: date) -> bool:
    return task.due_date < as_of_date if task.due_date else False
```

### 7.2 Pure Functions

All analytics calculations must be pure functions:

```python
# Pure: same input produces same output
def calculate_corridor_score(tasks: list[Task], corridor_name: str) -> int:
    return sum(task.score for task in tasks if task.corridor == corridor_name)

# Impure: depends on external state - NOT ALLOWED
def get_current_corridor_score(corridor_name: str) -> int:
    return cache.get(corridor_name)  # Mutable shared state
```

### 7.3 Reproducibility Test

Every analytics function must have a reproducibility test:

```python
def test_corridor_calculation_is_deterministic():
    tasks = create_sample_tasks()
    
    result1 = calculate_corridor_score(tasks, "21-25")
    result2 = calculate_corridor_score(tasks, "21-25")
    
    assert result1 == result2  # Must always pass
```

### 7.4 Report Identity

The `report_id` (UUID) and `generated_at` timestamp are **metadata**, not analytics. They are acceptable to use ambient time because they identify the report instance, not affect its content.

However, `analysis_date` must be injected to ensure analytics are reproducible for any given date.

---

## 8. MVP Profile

### 8.1 What MVP Includes

Per `docs/Foundations/ARCHITECTURE.md` and `docs/Product/Roadmap.md` Phase 2:

- Complete `ExecutionReport` model with all canonical sections
- Deterministic analytics pipeline (Stages 1-4)
- Executive Summary generation (Stage 5)
- `RecommendationCollection` with `availability = "not_produced"` (Stage 6)
- Daily Review renderer with 9 sections
- Complete test suite

### 8.2 What MVP Excludes

- Recommendation Engine (populated in Phase 3)
- LLM analysis
- Morning Brief renderer (future)
- Weekly Review renderer (future)
- Dashboard (future)
- Automation layer

### 8.3 MVP RecommendationCollection

In MVP, the RecommendationCollection is structurally present but explicitly empty:

```python
RecommendationCollection(
    availability="not_produced",
    operating_mode=None,
    strategic=(),
    tactical=(),
    task_recommendations=(),
)
```

This means recommendations have **not been produced**. It never means that no action is needed.

### 8.4 MVP Presentation Artifacts

In MVP, only the **Daily Review renderer** is implemented. It derives the 9 sections from `ExecutionReport`:

| Section | Data Source |
|---------|-------------|
| 1. Inbox | `recommendations.task_recommendations` (type=process_inbox) |
| 2. High Five | `recommendations.task_recommendations` (type=do_today, top 5) |
| 3. Schedule Review | `recommendations.task_recommendations` (type=schedule) |
| 4. Board Health | `board_health` |
| 5. Focus Analysis | `analytics.focus_analytics` |
| 6. Corridor Analysis | `analytics.corridor_analysis` |
| 7. Score Suggestions | `recommendations.task_recommendations` (type=score_adjust) |
| 8. Task Analysis | `analytics.task_snapshots` |
| 9. Strategic Findings | `findings` |

**Note:** In MVP, since `RecommendationCollection.availability = "not_produced"`, sections 1, 2, 3, and 7 will render fallback content derived from `analytics.task_snapshots` (e.g., tasks without score for Inbox, top-scored tasks for High Five). When the Recommendation Engine is implemented in Phase 3, these sections will automatically use the real recommendations without changing the renderer structure.

---

## 9. Deprecated Code Elimination Plan

### 9.1 Models to Remove

The following models are **deprecated** and must be removed:

| Model | File | Reason | Replacement |
|-------|------|--------|-------------|
| `AnalyticsReport` | `src/analytics/models.py` | Legacy report model, contains `datetime.now()` | `ExecutionReport` |
| `BoardHealthReport` | `src/analytics/models.py` | Duplicates `BoardHealth`, used by legacy renderer | `BoardHealth` |
| `AnalyticsSnapshot` | `src/analytics/models.py` | Intermediate artifact, not canonical | `ExecutionReport` |

### 9.2 Renderers to Remove

The following renderers are **deprecated** and must be removed:

| Renderer | File | Reason | Replacement |
|----------|------|--------|-------------|
| `render_markdown_report` | `src/reporting/markdown_report.py` | Uses deprecated `BoardHealthReport` | `render_daily_review` |
| `render_analytics_report` | `src/reporting/analytics_report_renderer.py` | Uses deprecated `AnalyticsReport` | `render_daily_review` |
| `render_analytics_report_with_snapshot` | `src/reporting/analytics_report_renderer.py` | Incomplete, uses deprecated models | `render_daily_review` |
| `render_snapshot` | `src/reporting/report_adapter.py` | Uses deprecated `AnalyticsSnapshot` | `render_daily_review` |

### 9.3 Functions to Remove

| Function | File | Reason |
|----------|------|--------|
| `build_analytics_report` | `src/analytics/report_builder.py` | Builds deprecated `AnalyticsReport` |
| `generate_analytics_report` | `src/analytics/service.py` | Returns deprecated `AnalyticsReport` |
| `render_overload_section` | `src/reporting/markdown_report.py` | Tied to legacy renderer |

### 9.4 Tests to Update

| Test File | Action | Reason |
|-----------|--------|--------|
| `tests/analytics/test_report_builder.py` | Remove | Tests deprecated `build_analytics_report` |
| `tests/reporting/test_markdown_report.py` | Remove | Tests deprecated `render_markdown_report` |
| `tests/cli/test_analytics_snapshot_command.py` | Update | Must use new `ExecutionReport` flow |

### 9.5 Migration Steps

**Phase 1: Implement Canonical Model**

1. Define `ExecutionReport`, `AnalyticsBundle`, `ExecutiveSummary`, `RecommendationCollection`, `Finding` in `src/analytics/models.py`
2. Implement `generate_execution_report` in `src/analytics/service.py`
3. Implement Finding generation
4. Implement Executive Summary generation

**Phase 2: Implement Presentation Layer**

1. Create `src/reporting/daily_review_renderer.py`
2. Implement section renderers in `src/reporting/sections/`
3. Wire CLI to use new pipeline

**Phase 3: Deprecate Legacy Code**

1. Mark deprecated models with `@deprecated` decorator
2. Add warnings in deprecated renderers
3. Update all imports

**Phase 4: Clean Up**

1. Delete deprecated models
2. Delete deprecated renderers
3. Delete deprecated functions
4. Remove/update legacy tests

---

## 10. Success Criteria

### 10.1 Determinism

- [ ] Identical board + identical `as_of_date` produces identical `ExecutionReport` (byte-for-byte)
- [ ] No analytics function uses `datetime.now()` or `date.today()` internally
- [ ] All calculations are pure functions

### 10.2 Architectural Compliance

- [ ] `ExecutionReport` contains NO presentation-specific fields (no `inbox_tasks`, `high_five_tasks`, `due_today_tasks`)
- [ ] `ExecutionReport` follows the canonical pipeline: Measurements -> Findings -> ExecutiveSummary -> Recommendations -> ExecutionReport
- [ ] Presentation artifacts derive ALL data from `ExecutionReport`
- [ ] No renderer accesses `AnalyticsReport` or `AnalyticsSnapshot`
- [ ] No renderer performs analytics calculations

### 10.3 Completeness

- [ ] `ExecutionReport` contains all canonical sections: metadata, executive_summary, recommendations, analytics, findings, board_health
- [ ] Daily Review renderer implements all 9 sections from Roadmap.md
- [ ] Report can be generated for any valid board

### 10.4 Testability

- [ ] Every analytics function has unit tests
- [ ] Every section renderer has snapshot tests
- [ ] Integration test: board -> ExecutionReport -> Daily Review Markdown
- [ ] Reproducibility test: same board + same date -> same output

---

## 11. Appendix: Presentation Artifact Registry

| Artifact | Status | Renderer | Key Data Sources |
|----------|--------|----------|------------------|
| Daily Review | MVP | `daily_review_renderer.py` | All ExecutionReport sections |
| Morning Brief | Phase 3 | `morning_brief_renderer.py` | recommendations, executive_summary |
| Weekly Review | Phase 4 | `weekly_review_renderer.py` | findings, analytics (trends) |
| Dashboard | Phase 4 | `dashboard_renderer.py` | analytics, board_health |
| API Response | Phase 4 | `api_serializer.py` | Full ExecutionReport (JSON) |

---

## 12. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-08-05 | Initial specification for Execution Report MVP |
| 2.0 | 2026-08-05 | Major revision: separated ExecutionReport (universal state) from DailyReviewRenderer (presentation). Removed presentation-specific fields from ExecutionReport. Aligned with Analytics_Model_v2 canonical pipeline. |

---

## 13. References

- `docs/Product/Roadmap.md` - Phase 2 MVP requirements (9-section Daily Review structure)
- `docs/Foundations/ARCHITECTURE.md` - System architecture principles
- `docs/Models/Analytics_Model_v2.md` - Analytics model specification, canonical pipeline
- `docs/Models/ExecutionReport_Design.md` - ExecutionReport design contract
- `docs/Implementation/IMPLEMENTATION_GUIDE.md` - Implementation strategy