# Architecture

## Purpose

Kanban Execution System (KES) is an execution-intelligence system for Kanban boards stored in Obsidian Markdown. It analyses an existing board and produces deterministic, human-reviewable execution information. It is not a task-management application and it does not hold decision authority.

This document is the single architectural source of truth. Product operating principles, human/AI boundaries, review protocols, and non-architectural safety rules are defined in [CANONICAL.md](CANONICAL.md). Task syntax and lifecycle rules remain in `docs/Models/`; analytics semantics remain in `docs/Models/Analytics_Model_v2.md`.

## Architectural principles

### One-way flow

Information flows only downstream. A higher layer must not read, modify, or bypass a lower-layer contract.

### Single responsibility and source of truth

Each concept has one owner. Parser owns Markdown interpretation; the domain model owns normalized board state; Analytics owns measurements and findings; `ExecutionReport` owns the presentation contract; Presentation owns rendering only.

### Determinism

Given the same normalized input, validated configuration, and injected analysis time, deterministic stages produce the same output. Ambient clocks, mutable shared state, and presentation-side calculation are forbidden in the canonical pipeline.

### Contract isolation

Layers communicate through explicit immutable artifacts. An implementation may add internal helpers, but it must not create a parallel path around a canonical artifact.

### Documentation first

When implementation and the canonical documents conflict, the documentation prevails until deliberately changed.

## Canonical pipeline

```text
Obsidian Markdown Board                 Validated Configuration
          │                                      │
          ▼                                      │
       Parser ──> Domain Model ──────────────────┘
                              │
                              ▼
                          Analytics
                              │
                              ▼
                       FindingCollection
                              │
                              ▼
                       ExecutiveSummary
                              │
                              ▼
                     Recommendation Engine
                              │
                              ▼
                   RecommendationCollection
                              │
                              ▼
                       ExecutionReport
                              │
                              ▼
                         Presentation
                              │
                              ▼
                         Human Review
```

Automation is a future, separate path. It may execute only explicitly approved actions and never alters the analytical or presentation flow.

## Layers and contracts

| Layer | Input | Output | Owns | Must not |
| --- | --- | --- | --- | --- |
| Board | Obsidian Markdown | Markdown source | Human-authored tasks, sections, and metadata | Depend on KES output to remain valid |
| Configuration | Configuration files | Validated configuration | Corridor definitions, target ranges, and other parameters | Contain business logic, calculations, or rendering rules |
| Parser | Markdown source | Domain Model plus validation diagnostics | Syntax recognition, normalization, metadata extraction, archive and hierarchy interpretation | Perform analytics or generate recommendations |
| Domain Model | Parser output | Immutable board/task/section state | Canonical normalized representation of the board | Render or interpret execution quality |
| Analytics | Domain Model + configuration + analysis time | Analytics objects, evaluations, and findings | Metrics, thresholds, data quality, corridor, workload, focus, flow, and strategic conclusions | Read Markdown, render, or generate action proposals |
| Executive Summary | FindingCollection | ExecutiveSummary | Ordered assessment of what matters most, including confidence and material qualifications | Recalculate metrics or decide actions |
| Recommendation Engine | ExecutiveSummary + recommendation configuration | RecommendationCollection | Ordered proposed actions and operating mode | Change analytical truth or mutate the board |
| Execution Report | ExecutiveSummary + RecommendationCollection + report provenance | ExecutionReport | Immutable composition and stable presentation boundary | Perform analytics, generate recommendations, or render output |
| Presentation | ExecutionReport | Markdown, dashboard, API projection, or other view | Formatting, layout, localization, and view-specific verbosity | Access Board, Analytics, Findings, or Recommendation Engine directly; create conclusions or priorities |
| Human Review | Presentation artifact | Human decision or approval | Strategic judgement and acceptance/rejection of proposals | Be replaced by automation |

## Layer rules

### Parser and Domain Model

The Parser is the sole source of Markdown parsing. It creates normalized domain objects according to the Task Model and Metadata Standards, reports validation issues, and preserves documented archive and hierarchy semantics. Analytics receives only domain objects and diagnostics through the parser contract; it never reads Markdown directly.

### Configuration

Configuration is data. `config/scoring.yaml` is the canonical configuration location for score corridors and their targets. It must be validated before Analytics runs. Algorithms, business rules, and rendering rules belong to code and their owning layers, never to configuration.

### Analytics, findings, and Executive Summary

Analytics produces deterministic measurements, evaluations, and findings. It owns factual conclusions such as board health, workload pressure, corridor state, and data-quality confidence. Findings are the only input to the Executive Summary. The Executive Summary selects and communicates what is most important; it does not create new measurements or action proposals.

### Recommendation Engine

The Recommendation Engine is separate from Analytics. It transforms an Executive Summary into a deterministic `RecommendationCollection` containing one operating mode plus ordered strategic, tactical, and task recommendations. It may use configured policies, but it does not recalculate analytics or change finding priority.

AI assistance, if introduced in a future phase, is outside the deterministic analytical core. It may not alter analytical facts, bypass the Recommendation Engine contract, mutate the board without approval, or become a second source of truth.

### ExecutionReport

`ExecutionReport` is the final canonical artifact and the only interface between processing and Presentation. It composes prior immutable outputs without reinterpreting them. Its required semantic sections are:

```text
Report metadata and provenance
ExecutiveSummary
RecommendationCollection
```

It contains no live `Board`, `Task`, `AnalyticsReport`, `AnalyticsSnapshot`, `BoardHealth`, or `FindingCollection` object. Presentation receives the summary and recommendations needed for a view through this contract, not by reaching back into analytics.

The detailed immutable data and serialization contract is defined in [ExecutionReport_Design.md](../Models/ExecutionReport_Design.md).

### Presentation

Presentation artifacts, including Morning Brief, Daily Review, Weekly Review, dashboard views, and API projections, consume only `ExecutionReport`. They may format, group under documented headings, localize, and omit optional display detail. They must preserve canonical ordering and must not calculate metrics, select tasks, infer recommendations, or inspect upstream models.

Markdown is a rendered representation, not another source of truth.

## MVP profile

The MVP preserves the same architecture and does not create a direct `AnalyticsReport -> renderer` path.

The MVP excludes the Recommendation Engine, LLM analysis, automation, dashboards, notifications, and external integrations, as defined by the Implementation Guide. The pipeline still produces an `ExecutionReport`; its recommendation section is structurally present and explicitly states:

```yaml
recommendations:
  availability: not_produced
  operating_mode: null
  strategic: []
  tactical: []
  tasks: []
```

This means recommendations have not been produced; it never means that no action is needed. A presentation must render this state faithfully and must not manufacture task priorities or system actions from `AnalyticsReport`.

When the Recommendation Engine is implemented, it replaces `not_produced` with a produced immutable collection without changing the Presentation boundary.

## Allowed and forbidden dependencies

```text
Allowed:
Board -> Parser -> Domain -> Analytics -> Findings -> Summary
Summary -> Recommendation Engine -> Recommendations -> ExecutionReport -> Presentation

Forbidden:
Presentation -> Analytics, Findings, Parser, Board, or Configuration
ExecutionReport -> Board, Analytics, Findings, or Recommendation logic
Analytics -> Markdown source or Presentation
Parser -> Analytics or Recommendation logic
```

## Change checklist

Before introducing a change, verify:

1. Which layer owns the responsibility?
2. What immutable contract is consumed and produced?
3. Does the change preserve the one-way flow and single source of truth?
4. Does it keep Presentation independent from analytics?
5. Is deterministic behaviour preserved for fixed input, configuration, and analysis time?
6. Can the owning layer be tested without bypassing another layer?

If any answer is negative, redesign the change before implementation.
