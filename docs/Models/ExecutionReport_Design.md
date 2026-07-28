# Canonical ExecutionReport Design

## 1. Purpose and authority

`ExecutionReport` is the immutable, canonical snapshot at the end of the execution-knowledge pipeline. It is the only contract consumed by user-facing artifacts such as Morning Brief, Daily Review, Weekly Review, Dashboard Snapshot, API responses, and future exports.

This design implements the boundary defined by `docs/Foundations/ARCHITECTURE.md` and `docs/Models/Analytics_Model_v2.md`:

```text
Board
  -> Analytics objects
  -> Findings
  -> ExecutiveSummary
  -> RecommendationCollection
  -> ExecutionReport
  -> Presentation artifacts
```

It does not introduce a new layer or change the direction of data flow. It specifies the currently partial `ExecutionReport` model in `src/analytics/models.py` so it can become the stable presentation contract.

`ExecutionReport` answers one question: **what is the complete execution picture for this analysis cycle?** It does not calculate that picture or decide how a particular screen or document should display it.

## 2. Responsibilities and non-responsibilities

### Responsibilities

`ExecutionReport` must:

- compose the completed executive assessment and recommendation collection into one stable snapshot;
- preserve their content and ordering without modification;
- identify the analysis cycle and contract version needed to interpret the snapshot;
- expose presentation-ready, structured information without exposing mutable internal analytics objects;
- provide the only data input for presentation artifacts and external consumers;
- remain deterministic: identical upstream artifacts and identical supplied report context produce an identical report.

### Non-responsibilities

`ExecutionReport` must not:

- read Markdown, tasks, the board, configuration files, or historical storage;
- calculate metrics, thresholds, confidence, corridor states, or rankings;
- generate findings, an executive interpretation, or recommendations;
- filter, reorder, abbreviate, localize, or render content for a presentation;
- mutate the board, execute a recommendation, record approval, or track user interaction;
- retain a mutable `Board`, `Task`, `AnalyticsSnapshot`, or renderer-specific model.

The report assembler is therefore a composition boundary, not an analytics engine and not a renderer.

## 3. Canonical immutable data model

The wire contract is deliberately small. `summary` and `recommendations` are the two semantic sections required by the analytics model; `metadata` makes the snapshot traceable and safely serializable.

```yaml
ExecutionReport:
  schema_version: "1.0"
  report_id: "..."
  generated_at: "2026-07-28T08:30:00Z"
  provenance:
    source_ref: "..."
    source_digest: "sha256:..."
    analysis_as_of: "2026-07-28T08:30:00Z"
    configuration_ref: "config/scoring.yaml"
    configuration_digest: "sha256:..."
    producer_version: "..."
  summary:
    system_state: "stable"
    primary_conclusion: "..."
    system_health:
      status: "good"
      analytics_confidence: "high"
      explanation: "..."
    strengths: []
    risks: []
    opportunities: []
    context: []
  recommendations:
    availability: "produced"
    operating_mode: {}
    strategic: []
    tactical: []
    tasks: []
  extensions: {}
```

### 3.1 Top-level field ownership

| Field | Required | Owner | Meaning and rules |
| --- | --- | --- | --- |
| `schema_version` | Yes | ExecutionReport contract | Version of this serialized contract, not the producer version. |
| `report_id` | Yes | Report assembler | Deterministic snapshot identifier derived from canonical upstream artifact identities and report context; it is not a random run ID. |
| `generated_at` | Yes | Application/orchestration boundary, copied by assembler | UTC instant at which the analysis cycle is declared complete. It must be supplied, not read implicitly from the system clock. |
| `provenance` | Yes | Application/orchestration boundary, copied by assembler | Immutable identity of the input, configuration, analysis instant, and producer. It contains no analytics conclusion. |
| `summary` | Yes | Executive Summary stage | The ordered executive assessment. The assembler copies it verbatim. |
| `recommendations` | Yes for the full canonical pipeline | Recommendation Engine | The ordered action proposals. The assembler copies it verbatim. |
| `extensions` | No; defaults to an empty mapping | Registered extension producer | Namespaced, versioned optional contract additions. It must not shadow a core field. |

### 3.2 Provenance field ownership

| Field | Owner | Rules |
| --- | --- | --- |
| `source_ref` | Input adapter/application layer | Stable logical identifier for the analyzed board or board set. It may be a repository-relative path or opaque ID; it must not require consumers to read the board. |
| `source_digest` | Input adapter/application layer | Digest of the normalized input snapshot used for this cycle. It enables traceability without embedding raw Markdown. |
| `analysis_as_of` | Application/orchestration boundary | Single injected UTC instant used by all time-sensitive upstream calculations. |
| `configuration_ref` | Configuration layer | Stable logical identifier of the configuration used. |
| `configuration_digest` | Configuration layer | Digest of the validated configuration snapshot used by analytics. |
| `producer_version` | Application release metadata | Identifies the producing KES release; it does not alter analytical meaning. |

### 3.3 Executive summary section

`summary` is owned entirely by the Executive Summary stage. It is a structured interpretation of the completed finding collection, not an `AnalyticsReport` embedded in the report.

| Field | Owner | Meaning |
| --- | --- | --- |
| `system_state` | Executive Summary stage | Canonical high-level state selected from the upstream findings. |
| `primary_conclusion` | Executive Summary stage | One concise statement of what matters most in this cycle. |
| `system_health.status` | Executive Summary stage, sourced from `BoardHealth` | The canonical health classification preserved for presentation; it is not recomputed by the report or renderer. |
| `system_health.analytics_confidence` | Executive Summary stage, derived upstream from `BoardHealth` | `high`, `medium`, `low`, or `none`, using the analytics-model mapping. |
| `system_health.explanation` | Executive Summary stage | Concise reason for the health/confidence state. |
| `strengths` | Executive Summary stage | Ordered, evidence-backed positive conclusions. |
| `risks` | Executive Summary stage | Ordered, evidence-backed conditions requiring attention. |
| `opportunities` | Executive Summary stage | Ordered, evidence-backed improvements available to the user. |
| `context` | Executive Summary stage | Material constraints or qualifications needed to interpret the assessment. |

Each conclusion item is immutable and has this portable shape:

```yaml
Conclusion:
  id: "risk.wip_overload.doing"
  statement: "Doing exceeds its WIP limit."
  severity: "high"
  evidence_refs:
    - "finding.wip_overload.doing"
```

`evidence_refs` are stable identifiers only. They preserve traceability without making a presentation consumer fetch or calculate from a `FindingCollection`. A separate diagnostic/export interface may resolve them upstream; a renderer must not do so.

### 3.4 Recommendation section

`recommendations` is owned by the Recommendation Engine. It is required by the full canonical pipeline defined in the analytics model and contains no board mutations.

| Field | Owner | Meaning |
| --- | --- | --- |
| `availability` | Recommendation Engine | `produced` when recommendations were generated. Before that phase is enabled, it must explicitly be `not_produced`; absence must never be interpreted as “no action needed.” |
| `operating_mode` | Recommendation Engine | Exactly one recommended way to approach the cycle, such as Completion or Recovery mode. |
| `strategic` | Recommendation Engine | Ordered high-level direction recommendations. |
| `tactical` | Recommendation Engine | Ordered recommendations to improve the execution system. |
| `tasks` | Recommendation Engine | Ordered concrete task recommendations, including the proposed next task when one is justified. |

Every recommendation item is immutable and contains only recommendation-owned information:

```yaml
Recommendation:
  id: "task.review_parser_architecture"
  priority: 1
  action: "Review parser architecture"
  rationale: "Highest eligible task after applying configured priority rules."
  evidence_refs:
    - "finding.focus_priority"
  target_ref: "task:..." # optional stable task reference, never a mutable Task object
```

`priority` defines the canonical order. Presentations may group items but must not change this order or invent a higher-priority action.

### 3.5 Immutability rules

- The report and all nested contract objects are immutable value objects after construction.
- Collections are tuples/lists treated as read-only in the wire contract; in an in-memory implementation they must use immutable sequences and read-only mappings.
- Maps must never use mutable default values. `extensions` defaults to an empty immutable mapping.
- The report carries scalar values, immutable nested DTOs, and stable references only. It never holds a live `Task`, `Board`, configuration object, or mutable analytics model.
- The assembler validates required fields and invariants once, then returns a new snapshot. Any correction creates a new report; no in-place patching is permitted.
- `generated_at`, `analysis_as_of`, ordering, and IDs are supplied deterministically. Calls to ambient `datetime.now()` or `date.today()` are forbidden inside report construction.

## 4. Required sections and presentation mapping

The report itself has three required sections: **metadata/provenance**, **summary**, and **recommendations**. These are data sections, not Markdown headings. A presentation owns formatting, selection of allowed detail, language, and layout; it does not own a second analytical interpretation.

| Presentation need | Sole ExecutionReport source | Presentation responsibility |
| --- | --- | --- |
| Executive Situation | `summary.system_state`, `primary_conclusion`, ordered summary conclusions | Compose the concise opening narrative. |
| Operating Mode | `recommendations.operating_mode` | Explain how to approach the day without changing the mode. |
| Today's Priorities | `recommendations.tasks` | Render the already ordered task recommendations and rationale. |
| Recommended Actions | `recommendations.strategic` and `recommendations.tactical` | Render system-improvement actions in canonical priority order. |
| System Health | `summary.system_health` and relevant summary context | Render the health status and qualification without reading `BoardHealth` directly. |
| Daily/Weekly Review | Same report sections | Apply review-specific layout and verbosity only. |
| Dashboard/API | Same serialized report | Select fields or visualize them without recomputing metrics. |

This mapping resolves the existing presentation constraint: a Morning Brief must not access intermediate analytics artifacts, including `BoardHealth`, directly. The Executive Summary stage is responsible for carrying the health assessment needed by presentation; the renderer merely displays it.

### MVP phase rule

The implementation guide excludes the Recommendation Engine from the MVP. That does not allow a renderer to manufacture recommendations. Until the engine is introduced, an emitted report must contain `recommendations.availability: not_produced` and empty recommendation collections, while the presentation states that recommendations are unavailable. A deterministic High Five, if retained as MVP report composition, must first be specified as an upstream deterministic recommendation producer; it cannot be calculated by `ExecutionReport` or the renderer.

## 5. Relation to Analytics

Analytics owns facts and interpretation up to the executive assessment:

```text
Parser/Domain -> Analytics objects -> Findings -> ExecutiveSummary
```

The report assembler consumes the completed `ExecutiveSummary` and `RecommendationCollection` only. It does not accept a `Board`, `AnalyticsSnapshot`, `AnalyticsReport`, `BoardHealth`, `FindingCollection`, or score configuration as a direct input. Existing structures such as `AnalyticsReport`, `BoardHealth`, `ScoreCorridor`, and WIP metrics remain analytics-layer implementation artifacts until their information has been interpreted into the executive summary or recommendation collection.

The existing `ExecutionReport(board_health, executive_summary)` placeholder should therefore evolve toward the contract above rather than becoming a general container for analytics models. In particular, it must not make presentation depend directly on `AnalyticsReport.corridors` or on a live `BoardHealth` object. The executive-summary health projection is the deliberately small, immutable bridge required by System Health presentation.

## 6. Relation to Presentation

Presentation starts after `ExecutionReport` and has no reverse dependency:

```text
ExecutionReport -> Markdown renderer / dashboard adapter / API serializer
```

Allowed presentation work:

- choose a documented view and its section order;
- format text, dates, numbers, headings, links, and localized wording;
- omit optional display detail when the view contract permits;
- render the canonical ordering and state “not produced” where applicable.

Forbidden presentation work:

- read the board or configuration;
- call analytics, score tasks, apply thresholds, calculate health, or select a High Five;
- derive a recommendation from an observation;
- mutate, sort by a new criterion, or alter the report’s conclusions.

Markdown is therefore an output format, not an alternative report model. `src/reporting/` should eventually consume this contract rather than the current parallel `BoardHealthReport` or `AnalyticsReport` paths.

## 7. Serialization strategy

### Canonical format

The canonical serialized form is JSON. JSON provides a portable API and storage boundary; Markdown, YAML, and dashboard payloads are derived representations.

- Field names use `snake_case` and remain stable within a major schema version.
- Timestamps are RFC 3339/ISO 8601 UTC strings with `Z`.
- Dates are ISO 8601 calendar-date strings.
- Enumerations are lower-case strings defined by the contract.
- Stable identifiers are opaque strings; consumers must not parse their internal form.
- Ordered collections are JSON arrays and must preserve report order.
- Optional fields are omitted when absent. Required empty collections serialize as `[]`; required empty mappings serialize as `{}`.
- Numeric metric values, if exposed through a future summary projection, serialize as JSON numbers with a documented unit. Renderers decide display rounding only.

### Deterministic representation

For reproducibility and report IDs, produce a canonical JSON representation: stable field order, lexicographically ordered map keys, UTF-8, no insignificant whitespace, normalized UTC timestamps, and preserved array order. `report_id` is derived from the canonical serialized upstream identities and context, not from a randomly generated UUID.

JSON deserialization must validate `schema_version`, required fields, enum values, timestamps, ID uniqueness, and ordering invariants before producing an in-memory report. Unknown core fields are rejected within a supported major version; unknown namespaced extensions may be retained only when their namespace is recognized by the consumer.

### Derived formats

- **Markdown:** renderer output only; it is not parsed back as an authoritative report.
- **YAML:** optional human-readable export of the same JSON data; it adds no fields or semantics.
- **API:** returns the canonical JSON contract or a documented projection of it. An API projection must identify the source `report_id` and `schema_version`.

## 8. Extension and evolution strategy

The contract must support new reports without forcing changes to the analytics pipeline or existing views.

### New presentation artifacts

To add a new Morning Brief variant, weekly review, dashboard, or API view:

1. consume the existing ExecutionReport fields;
2. define only presentation behavior; and
3. do not change the report schema if the information already exists.

### New execution information

When a future view needs information not present in the report:

1. establish ownership in the existing upstream stage (Analytics, Executive Summary, or Recommendation Engine);
2. add an immutable, presentation-ready field to that stage’s output;
3. add it to `ExecutionReport` only as a copied contract field; and
4. add contract tests for deterministic serialization and view consumption.

Do not bypass the report by giving a renderer direct access to a new analytics model.

### Versioning rules

- Use semantic `schema_version` values.
- A backward-compatible optional field or a new namespaced extension increments the minor version.
- Removing, renaming, changing a field’s meaning, changing an enum incompatibly, or changing ordering semantics requires a major version.
- During a major transition, produce both versions through explicit adapters at the report boundary; do not make presentations infer the version from field presence.
- Preserve old report snapshots as immutable historical artifacts; migrations create new serialized artifacts and retain the original schema version.

### Extensions namespace

`extensions` is reserved for independently versioned, non-core additions:

```yaml
extensions:
  "kes.history/v1":
    trend_window_days: 28
```

An extension key must contain a stable namespace and version. Extensions cannot redefine core fields, alter core ordering, or introduce executable behavior. If an extension becomes necessary to more than one first-party presentation, promote it through the normal core-schema versioning process.

## 9. Contract invariants

- Exactly one immutable report represents one completed analysis cycle.
- `summary` is always present.
- `recommendations` is always structurally present, including when its availability is `not_produced`.
- `summary` and `recommendations` preserve upstream order and wording; the report assembler does not reinterpret them.
- Every conclusion and recommendation ID is unique within its report.
- Every `evidence_ref` references an identifier emitted by the corresponding upstream artifact for the same cycle; it does not require the renderer to retrieve that artifact.
- `analysis_as_of` is not later than `generated_at`.
- No field permits a board mutation, human approval, or autonomous execution.
- All presentation artifacts derive their content exclusively from this contract.

## 10. Implementation alignment note

This is a design contract only. It does not authorize code changes or an architectural rewrite. It gives the existing analytics and reporting modules a clear convergence point: analytics produces the executive assessment, the Recommendation Engine later produces actions, the report assembler composes them immutably, and presentation renders the resulting `ExecutionReport` without recalculation.
