# KES MVP Gap Analysis

> **Archive notice:** This is an informative, point-in-time assessment from 2026-07-28. It is not normative. The canonical MVP scope is defined in [Product/MVP.md](../Product/MVP.md).

## Purpose and assessment basis

This assessment defines the smallest product scope in which a person can run a deterministic review of an existing Obsidian Markdown Kanban board and receive an immediately useful, trustworthy daily execution report.

It is based on the canonical architecture and implementation guidance in `docs/Foundations/ARCHITECTURE.md` and `docs/Implementation/IMPLEMENTATION_GUIDE.md`, the MVP roadmap, the domain and analytics specifications, and the code and tests under `src/` and `tests/`. It does not recommend an architectural rewrite. The intended one-way pipeline remains the appropriate foundation:

```text
Markdown board -> Parser -> Domain model -> Analytics -> ExecutionReport -> Markdown presentation -> Human review
```

The implementation guide excludes the Recommendation Engine, automation, AI, dashboards, notifications, and external integrations from the MVP. Accordingly, the MVP report should provide deterministic findings and a deterministic High Five; it should not mutate the board or make autonomous decisions.

## 1. Current capabilities

### Board parsing and domain representation

- Parses a single UTF-8 Markdown file into `Board`, `Task`, and `Section` objects.
- Recognizes supported checkbox states, top-level and tab-indented tasks, `##` section headers, section aliases, section WIP limits, and section priority weights.
- Extracts common task data: score, tags, due/scheduled/start/completion dates, time estimate, priority, recurrence, category, finance, cost, currency, analytics flags, links, and leading emoji.
- Handles malformed task input without crashing and has fixture-based parser coverage for normal, nested, complex, malformed, archive-related, and pathological boards.

### Deterministic analytical building blocks

- Calculates board and section task counts, active/actionable/completed/cancelled status counts, scores, and overdue task counts.
- Produces score-corridor distributions and focus/high-value counts.
- Calculates section-level WIP utilization when a WIP limit is present and surfaces near-limit and over-limit signals.
- Calculates priority ordering from task score plus section priority weight.
- Calculates attention signals from overdue dates and, when an update timestamp exists, staleness.
- Provides a metadata-readiness `BoardHealth` model: score coverage, tag coverage, analytical coverage, orphan tasks, and a health classification.

### Existing presentation and callable workflow

- `review_command(board_path)` parses one board and returns a Markdown **Board Health Report** with board metrics, WIP, stale count, top attention, top priority, section summaries, warnings, and overload messages.
- A separate analytics path builds `AnalyticsSnapshot` and `AnalyticsReport`, and can render board-health and score-corridor sections.
- Unit and integration tests cover much of the current parser, metric, WIP, scoring, report-builder, and renderer behavior.

These capabilities are a credible foundation, but they are building blocks rather than the complete daily-review product described in the roadmap.

## 2. Current architecture

The documented architecture is layered and one-way: the parser owns Markdown interpretation; the domain model owns board state; analytics produces deterministic conclusions; `ExecutionReport` is the presentation boundary; renderers consume only that report.

The code generally follows the first three layers, with these current paths:

```text
Single Markdown file
  -> parser.parser.parse_markdown_file
  -> Board / Task / Section
  -> analytics calculations
  -> either AnalyticsSnapshot -> AnalyticsReport -> analytics renderer
     or review_service.run_review -> BoardHealthReport -> Markdown report
```

The last branch is the only end-to-end review entry point, but it renders directly from analytics objects. `ExecutionReport` exists only as a partial model (`board_health` and `executive_summary`) and is not built or consumed by the public report. `config/scoring.yaml` has a loader, but its corridor and target values are not used by analytics; corridor ranges are hard-coded. Thus the repository has the intended layers, but the canonical integration boundary and one public product path are incomplete.

## 3. Missing capabilities required for MVP user value

### A usable, documented product entry point

There is no executable CLI, module entry point, packaging metadata, or documented command for a user to run a review. `src/main.py` defines a callable function only; `src/cli/review_command.py` is effectively empty. A user therefore cannot install KES, point it at a board, choose an output location, or receive clear errors without writing Python.

The MVP needs one supported command and a short getting-started path. It should accept a board path, produce Markdown to stdout and/or an explicitly chosen output file, return meaningful non-zero failures, and document the supported board format and configuration location. A single-board-file workflow is sufficient for MVP; vault-wide discovery is not required unless it becomes the declared input contract.

### Parser validation and trustworthy source interpretation

The implementation guide requires validation, normalization, archive detection, and no silent data loss. The current parser silently ignores unsupported lines and malformed metadata, sets every parsed task's `archived` flag to `False`, and does not populate `updated_at`. It also does not validate documented constraints such as the score range, required metadata syntax, or unsupported statuses. Task depth is parsed but is not used to enforce the documented exclusion of subtasks from high-level analytics.

The MVP needs a structured validation result alongside the parsed board: errors that prevent reliable analysis, warnings that explain exclusions or fallbacks, and source locations/task text sufficient for correction. Archive-section and archive-metadata semantics, plus the high-level-analytics rule for subtasks, must be applied consistently before all metrics. The report must disclose validation and data-quality limitations instead of appearing authoritative when input is incomplete.

### One canonical deterministic review pipeline

The two current report paths calculate overlapping but different concepts. The public review path does not use `AnalyticsReport` or `BoardHealth` metadata readiness; the `AnalyticsReport` path does not drive the public review. This prevents the documented `ExecutionReport` from being the sole presentation contract.

The MVP needs the existing calculations composed into one canonical pipeline that:

1. accepts a parsed and validated board plus an explicit analysis date/time;
2. builds the required analytics and deterministic findings;
3. creates an immutable `ExecutionReport` containing the executive summary and deterministic High Five; and
4. renders the daily report only from that report.

This is a convergence of existing components, not a new parallel architecture. The analysis timestamp must be injected or explicitly recorded so the same board, configuration, and analysis time yield the same report. Current uses of `date.today()` and `datetime.now()` make results depend on ambient time; `AnalyticsReport.generated_at` is also non-deterministic.

### The MVP analytical coverage promised by the roadmap

The MVP roadmap requires Board Health, Focus, Corridor, Flow, Portfolio/Strategic analysis, and a deterministic daily High Five. Current code implements portions of board health, metadata readiness, WIP, score corridors, priority, and attention, but the required product-level analytics are incomplete or disconnected from the report.

The remaining MVP work is:

- **Findings with evidence:** normalized, named findings that state condition, severity, affected scope, and source metrics. This makes every conclusion traceable rather than leaving the user to infer meaning from raw counters.
- **Executive summary:** deterministic synthesis of the most important findings, including reliability caveats when metadata coverage is low.
- **Focus and High Five:** a stable selection of at most five executable tasks, with eligibility rules, deterministic tie-breaking, and a concise rationale. The current top-priority list is useful input but is not yet the specified High Five.
- **Schedule and overdue review:** distinguish overdue, due today, due soon, scheduled, waiting/delegated, and unscheduled actionable work in a user-facing conclusion.
- **Corridor evaluation:** calculate corridor workload against `scoring.yaml` targets and report imbalance, rather than only listing hard-coded score buckets. Configuration must be validated and become the single source for score ranges and targets.
- **Flow/workload analysis:** explain WIP capacity, overload, stale work, and completion/blocked-state pressure as findings. Staleness must operate on data actually available from the parsed board or be reported as unavailable.
- **Portfolio/strategic analysis:** provide the minimum project/section and value-allocation view required by the roadmap, with an explicit finding when the board lacks sufficient classification data.
- **Data-quality and confidence behavior:** include `BoardHealth` and the documented confidence/reliability interpretation in the public report; when coverage is poor or critical, prioritize remediation and suppress or qualify unreliable conclusions.

### A fixed, immediately actionable daily report

The existing renderer is a diagnostic board-health report, not the MVP daily review. It lacks the roadmap's fixed ordering: Inbox, High Five, Schedule Review, Board Health, Focus Analysis, Corridor Analysis, Score Suggestions, Task Analysis, and Strategic Findings. It also lacks an executive summary and the required interpretation that turns metrics into a decision.

The MVP needs a concise Markdown report in this stable order. Each section should be omitted only under documented rules and should explain what to do or why no action is needed. It must render from `ExecutionReport`, preserve the analytical meaning, identify the first task to start, and make data-quality limitations visible. This is not the future Recommendation Engine: all advice remains deterministic and limited to the documented MVP findings and High Five.

### Configuration, distribution, and verification readiness

- `requirements.txt` declares only `pydantic`, although `src/config/scoring_loader.py` imports `yaml`; no supported environment or executable install path is defined.
- The test runner is not declared as a development dependency. In the current environment neither `pytest` nor `python` is available on `PATH`, so the suite could not be executed here. The repository should document a supported Python version and a reproducible test command.
- The real-board snapshot test depends on a personal drive or environment variable and writes `report.md` into the repository. Portable MVP verification requires anonymized fixture coverage and no default test side effects.
- End-to-end tests are missing for the actual user command, validation output, fixed report structure, configuration-driven corridors, deterministic time handling, and the canonical `ExecutionReport` boundary.

## 4. Prioritized roadmap

### Critical

1. Define and document the MVP user contract: one supported board input, one command, output behavior, supported Markdown subset, configuration path, and error behavior.
2. Complete parser validation, archive semantics, and source-aware diagnostics; ensure public analytics consistently exclude/include tasks according to the task model.
3. Converge the current analytics paths into the documented canonical pipeline ending in `ExecutionReport`; make the Markdown renderer consume it exclusively.
4. Implement the deterministic daily-review core: findings, executive summary, reliable High Five, schedule/overdue review, board-health confidence, WIP/flow, corridor target evaluation, and minimum portfolio/strategic findings.
5. Render the fixed, concise MVP daily review and make it runnable through a CLI.
6. Make scoring configuration authoritative and validated; remove the current disconnect between `scoring.yaml` and hard-coded corridor rules.
7. Establish reproducible verification: declared runtime/test dependencies, portable fixtures, and end-to-end deterministic tests.

### Important

1. Improve parser support for all documented task metadata and lifecycle semantics that the MVP analyses consume, including a dependable source for freshness when staleness is reported.
2. Add machine-readable report output (for example JSON serialization of `ExecutionReport`) alongside Markdown, without making it a second source of truth.
3. Add clear report provenance: input path or identifier, analysis time, configuration version/path, validation summary, and analytical-confidence notice.
4. Improve report usability with configurable output path, concise remediation messages, and examples based on the canonical board format.
5. Resolve the small documentation ambiguity between the roadmap's deterministic High Five and the implementation guide's exclusion of the future Recommendation Engine. The MVP should label High Five as deterministic report composition, not as a Recommendation Engine.

### Optional

1. Vault-wide board discovery, multiple-board aggregation, and historical report storage.
2. Daily/weekly review variants, dashboard snapshots, and richer Morning Brief sections once `ExecutionReport` is stable.
3. Task-improvement, inbox-structuring, schedule-planning, and score-optimization suggestions from later roadmap phases.
4. Notifications, Obsidian plugins, APIs, integrations, automation, and AI-assisted interpretation.

## 5. Recommended implementation order

The following milestones are deliberately small and preserve the existing architecture.

### Milestone 1 — Runnable baseline

Add the supported command, installation/runtime documentation, dependency declarations, and a simple fixture-based end-to-end test. The command should analyze one board and return a basic report without modifying that board.

**Exit condition:** a new user can install the declared environment, run one documented command against a fixture or their board, and obtain Markdown output.

### Milestone 2 — Validated board intake

Introduce a parser result/validation contract while retaining the current domain objects. Implement archive handling, metadata/range/status validation, source-aware diagnostics, and report-visible validation/data-quality summaries.

**Exit condition:** malformed or incomplete boards produce actionable diagnostics; analytics never silently treat unsupported data as trustworthy.

### Milestone 3 — Canonical report composition

Choose the existing analytics snapshot/report path as the composition base, complete `ExecutionReport`, and route the public command through it. Inject a single analysis time into all date-sensitive calculations. Retire the duplicate public calculation path only after its useful calculations have been represented in the canonical report.

**Exit condition:** one end-to-end path produces reproducible `ExecutionReport` and Markdown for fixed board, configuration, and clock; presentation accesses no analytical internals.

### Milestone 4 — MVP findings and daily decision support

Add configuration-driven corridor evaluation and deterministic findings for metadata quality, WIP/flow, focus, schedule pressure, and minimum portfolio/strategic allocation. Build the executive summary and deterministic High Five with stable eligibility and tie-breaking rules.

**Exit condition:** every displayed conclusion has evidence, low-confidence conditions are qualified, and the report identifies a defensible first task and the most important board correction.

### Milestone 5 — Fixed daily review and hardening

Render the roadmap's fixed report sections from `ExecutionReport`; add examples and golden end-to-end tests for normal, malformed, overloaded, low-coverage, and empty boards. Make all tests portable and remove test writes to repository-root artifacts.

**Exit condition:** KES reliably gives a user an understandable, deterministic daily review from a supported board, with clear limits when the input cannot support reliable conclusions.

## MVP completion checklist

KES can be considered an MVP when all of the following are true:

- A user can run one documented command on a supported Markdown Kanban board without programming knowledge.
- The command creates a deterministic, human-readable daily review and does not mutate the board.
- The review is composed from a single `ExecutionReport` and honors the documented layer boundaries.
- Input problems, archive treatment, metadata coverage, and analytical confidence are explicit.
- The review provides a traceable executive situation, a deterministic High Five, schedule/WIP/corridor/focus/strategic findings, and next actions appropriate to a deterministic MVP.
- Scoring and corridor targets come from validated configuration rather than duplicated constants.
- The project has a documented, reproducible environment and portable automated tests for the real user workflow.

At that point, KES will deliver the Phase 2 product: a reliable deterministic review that improves daily execution. Recommendation engines, automation, integrations, dashboards, and AI can remain subsequent phases.
