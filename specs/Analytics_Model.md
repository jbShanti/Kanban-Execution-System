---

created: 2026-06-06
updated: 2026-06-06
Description: |-
Canonical analytics output model for the Kanban Execution System.

Purpose:

* define deterministic analytics outputs
* separate analytics data from report presentation
* provide stable contracts for future parsers
* support dashboards, reports and automation
* ensure consistency across implementations

This document defines:

* analytics report structure
* summary metrics
* corridor analytics
* status calculation rules
* delta calculation rules
* reporting invariants

---

# ANALYTICS MODEL

---

# 1. Core Philosophy

Analytics must produce:

* deterministic outputs
* reproducible calculations
* presentation-independent structures
* machine-readable results
* stable contracts

Analytics models describe:

```text
Data
```

NOT:

```text
Presentation
```

Examples of presentation:

* Markdown tables
* Dashboards
* Obsidian notes
* HTML reports
* Telegram summaries

All presentations must be generated from the same analytics model.

---

# 2. AnalyticsReport

## Purpose

AnalyticsReport is the canonical output of the Analytics Engine.

Every analytics calculation produces exactly one AnalyticsReport object.

---

## Canonical Structure

```yaml
generated_at: 2026-06-06

summary:
  overdue: 0
  active: 63
  completed: 22
  archived: 80

global_target:
  min: 60
  max: 70

global_status:
  delta: 0
  state: ok

corridors:
  - interval: "21-25"
    overdue: 0
    active: 5
    completed: 3
    archived: 7

    target:
      min: 3
      max: 5

    delta: 0
    state: ok
```

---

# 3. Summary Metrics

## Summary Object

```yaml
summary:
  overdue: 0
  active: 63
  completed: 22
  archived: 80
```

---

## overdue

Number of overdue tasks.

Includes:

* active overdue tasks

Excludes:

* archived tasks
* completed tasks
* cancelled tasks
* paused tasks
* analytics::ignore

---

## active

Number of active tasks.

Includes:

* [ ]
* [/]

Excludes:

* [x]
* [-]
* [<]
* [>]
* archived tasks
* analytics::ignore

---

## completed

Number of completed tasks.

Includes:

* [x]

Excludes:

* archived tasks
* analytics::ignore

---

## archived

Number of archived tasks.

Includes:

* all archived tasks regardless of status

---

# 4. Global Target

## Purpose

Defines the desired total active task range.

Source:

```text
scoring.yaml
```

---

## Structure

```yaml
global_target:
  min: 60
  max: 70
```

---

# 5. Global Status

## Structure

```yaml
global_status:
  delta: 0
  state: ok
```

---

## State Values

Supported values:

```text
ok
underloaded
overloaded
```

---

## Delta Calculation

Inside target:

```text
delta = 0
state = ok
```

Below target:

```text
delta = negative value
state = underloaded
```

Example:

```text
active = 52
target minimum = 60

delta = -8
```

Above target:

```text
delta = positive value
state = overloaded
```

Example:

```text
active = 81
target maximum = 70

delta = +11
```

---

# 6. CorridorReport

## Purpose

Represents analytics for a single score corridor.

---

## Structure

```yaml
interval: "21-25"

overdue: 0
active: 5
completed: 3
archived: 7

total_score: 92
average_score: 23.0
score_share_percentage: 23.4


target:
  min: 3
  max: 5

delta: 0

state: ok
```

---

# 7. Corridor Metrics

## interval

Score range identifier.

Examples:

```text
21-25
16-20
11-15
6-10
1-5
```

---

## overdue

Number of overdue tasks within the corridor.

---

## active

Number of active tasks within the corridor.

---

## total_score

Sum of score values for all tasks within the corridor.

Example:

scores:
21
22
24
25

total_score = 92

---

## average_score

Average score of scored tasks within the corridor.

Formula:

average_score =
total_score / scored_tasks

---

## score_share_percentage

Percentage of total board score represented by the corridor.

Formula:

score_share_percentage =
corridor.total_score
/
board.total_score
× 100

Range:

0.0 .. 100.0

Example:
Board total score = 400

Corridor total score = 92

score_share_percentage =
92 / 400 × 100

= 23.0%

Important: board.total_score =
sum(total_score of all score corridors)

that means

Σ(score_share_percentage)
≈ 100%


---

## completed

Number of completed non-archived tasks within the corridor.

---

## archived

Number of archived tasks within the corridor.

---

# 8. Corridor Target

## Source

Target values must be loaded from:

```text
scoring.yaml
```

Analytics engines must not use hardcoded corridor targets.

---

## Structure

```yaml
target:
  min: 3
  max: 5
```

---

# 9. Corridor Status

## State Values

Supported values:

```text
ok
underloaded
overloaded
```

---

## Delta Rules

Inside target:

```text
delta = 0
state = ok
```

Below target:

```text
delta < 0
state = underloaded
```

Example:

```text
active = 1
target minimum = 3

delta = -2
```

Above target:

```text
delta > 0
state = overloaded
```

Example:

```text
active = 14
target maximum = 10

delta = +4
```

---

# 10. Paused Tasks

Paused tasks:

```text
[<]
```

must not be included in corridor calculations.

They may be reported separately by presentation layers.

Paused tasks do not contribute to:

* active
* overdue
* completed

---

# 11. Analytics Invariants

Analytics engines must guarantee:

* deterministic calculations
* stable outputs
* reproducible results
* scoring targets loaded from configuration
* archived tasks counted only as archived
* analytics::ignore excluded everywhere
* nested tasks excluded from high-level analytics

---

# 12. Presentation Independence

AnalyticsReport must remain independent from:

* Markdown formatting
* tables
* visual indicators
* emojis
* report templates

Examples:

```text
✅ (0)
⚠️ (+4)
⚠️ (-2)
```

are presentation-layer concerns.

The analytics model stores:

```yaml
delta: 4
state: overloaded
```

Presentation layers decide how to display these values.

---

# Domain Contracts

---

## AnalyticsReport

AnalyticsReport is immutable.

AnalyticsReport is the canonical output of the Analytics Engine.

AnalyticsReport is the single source of truth for analytics data.

---

## CorridorReport

Every CorridorReport represents exactly one score corridor.

Corridor interval is a string identifier.

Examples:

```
21-25
16-20
11-15
6-10
1-5
```

Corridor target is always:

```
target:
  min: integer
  max: integer
```

Corridor delta is always:

```
integer
```

Corridor state is always one of:

```
ok
underloaded
overloaded
```

---

## Recommendation

Recommendation is immutable.

Recommendation represents a single recommended action.

Recommendation priority is always one of:

```
high
medium
low
```

Recommendation action is a machine-readable operation.

Recommendation reason is a machine-readable explanation.

---

## RecommendationCollection

RecommendationCollection is an ordered collection of Recommendation objects.

RecommendationCollection must be sorted by priority:

```
high
↓
medium
↓
low
```

Within the same priority:

```
higher impact first
```

---

## Determinism Contract

Identical input MUST produce identical:

* AnalyticsReport
* RecommendationCollection

No component may:

* infer missing analytics values
* recalculate analytics during rendering
* mutate analytics results
* mutate RecommendationCollection

outside its defined responsibility boundary.

---

## Responsibility Contract

Analytics Engine produces:

```
AnalyticsReport
```

Recommendation Engine produces:

```
RecommendationCollection
```

Report Renderer produces:

```
Markdown Report
```

No component may cross responsibility boundaries.


---

# 13. Analytics Lifecycle

```text
Task Board
↓
Parser
↓
Task Objects
↓
Analytics Engine
↓
AnalyticsReport
↓
Recommendation Engine
↓
RecommendationCollection
↓
Report Renderer
↓
Markdown Report
```

AnalyticsReport is the canonical boundary between analytics calculation and report generation.


# Recommendation Model

---

## Purpose

RecommendationCollection are structured actions derived from analytics results.

Their purpose is to:

* improve board health
* maintain score corridor balance
* reduce execution overload
* reduce task debt
* improve execution quality
* support deterministic decision-making

RecommendationCollection are generated from analytics data.

RecommendationCollection are not analytics themselves.

---

## Recommendation Engine Position

```text
Task Board
↓
Parser
↓
Task Objects
↓
Analytics Engine
↓
AnalyticsReport
↓
Recommendation Engine
↓
RecommendationCollection
```

RecommendationCollection must be generated only from AnalyticsReport and system configuration.

---

## RecommendationCollection

Canonical structure:

```yaml
RecommendationCollection:
  - type: rebalance
    priority: high

    corridor: "21-25"

    action: increase

    amount: 2

    reason: underloaded
```

---

## Recommendation

Canonical structure:

```yaml
type: rebalance

priority: high

corridor: "21-25"

action: increase

amount: 2

reason: underloaded
```

---

## Fields

### type

Recommendation category.

Supported values:

```text
rebalance
overdue_cleanup
workload_reduction
focus_protection
```

Future types may be added.

---

### priority

Importance of recommendation.

Supported values:

```text
high
medium
low
```

---

### corridor

Affected score corridor.

Examples:

```text
21-25
16-20
11-15
6-10
1-5
```

Optional for RecommendationCollection that affect the entire board.

---

### action

Recommended operation.

Examples:

```text
increase
decrease
review
cleanup
protect
```

---

### amount

Recommended quantity.

Examples:

```text
2
5
10
```

Represents the number of tasks affected.

---

### reason

Machine-readable explanation.

Examples:

```text
underloaded
overloaded
overdue_tasks
active_overload
```

---

# Rebalance Recommendation

## Purpose

Restore corridor targets defined in scoring.yaml.

---

## Underloaded Corridor

Condition:

```text
active < target.min
```

Generated recommendation:

```yaml
type: rebalance
priority: high

corridor: "21-25"

action: increase

amount: 2

reason: underloaded
```

Meaning:

```text
Promote or create 2 tasks
to reach the target corridor.
```

---

## Overloaded Corridor

Condition:

```text
active > target.max
```

Generated recommendation:

```yaml
type: rebalance
priority: high

corridor: "16-20"

action: decrease

amount: 4

reason: overloaded
```

Meaning:

```text
Move, split, defer or complete
4 tasks to return to target range.
```

---

# Overdue Cleanup Recommendation

## Purpose

Reduce accumulated task debt.

---

## Condition

```text
overdue > 0
```

---

## Structure

```yaml
type: overdue_cleanup

priority: high

action: cleanup

amount: 5

reason: overdue_tasks
```

---

## Amount

Equal to the number of overdue tasks.

---

# Workload Reduction Recommendation

## Purpose

Reduce excessive board size.

---

## Condition

```text
global_status.state = overloaded
```

---

## Structure

```yaml
type: workload_reduction

priority: high

action: decrease

amount: 11

reason: active_overload
```

---

## Amount

Equal to:

```text
active - global_target.max
```

---

# Focus Protection Recommendation

## Purpose

Protect execution focus when high-score corridors are underfilled.

---

## Condition

```text
21-25 corridor below target
```

or

```text
16-20 corridor below target
```

---

## Structure

```yaml
type: focus_protection

priority: high

corridor: "21-25"

action: increase

amount: 1

reason: underloaded
```

---

# Recommendation Priority Rules

## High

Generated when:

* corridor is outside target range
* overdue tasks exist
* board exceeds global target
* critical corridor is underfilled

---

## Medium

Generated when:

* corridor approaches boundary
* moderate task debt exists

---

## Low

Generated when:

* optimization opportunities exist
* no significant imbalance exists

---

# Recommendation Ordering

RecommendationCollection should be sorted by priority.

Order:

```text
high
↓
medium
↓
low
```

Within the same priority:

```text
larger impact first
```

---

# Recommendation Invariants

Recommendation engines must guarantee:

* deterministic generation
* reproducible outputs
* RecommendationCollection derived only from analytics
* no direct dependency on report formatting
* no dependency on LLM interpretation
* identical input produces identical RecommendationCollection

---

# Presentation Independence

RecommendationCollection must remain presentation-independent.

Canonical representation:

```yaml
type: rebalance
priority: high
corridor: "21-25"
action: increase
amount: 2
reason: underloaded
```

Human-readable text such as:

```text
Increase corridor 21-25 by 2 tasks.
```

is generated by the presentation layer and is not part of the recommendation model.

# Analytics Engine

---

## Purpose

The Analytics Engine transforms task data into deterministic analytics outputs.

It is responsible for:

* filtering tasks
* classifying tasks
* assigning tasks to score corridors
* calculating analytics metrics
* calculating corridor status
* generating AnalyticsReport

The Analytics Engine does not generate RecommendationCollection.

The Analytics Engine does not generate report formatting.

Its sole responsibility is producing AnalyticsReport.

---

## Position in System Architecture

```text
Task Board
↓
Parser
↓
Task Objects
↓
Analytics Engine
↓
AnalyticsReport
↓
Recommendation Engine
↓
RecommendationCollection
```

---

# Input

## Input Type

```text
List<Task>
```

Task structure is defined in:

```text
Task_Model.md
```

---

# Processing Pipeline

The Analytics Engine must execute the following stages in order:

```text
1. Filter Tasks
↓
2. Classify Tasks
↓
3. Assign Corridors
↓
4. Aggregate Metrics
↓
5. Calculate Status
↓
6. Build AnalyticsReport
```

---

# 1. Filter Tasks

## Purpose

Remove tasks that must not participate in analytics.

---

## Excluded Tasks

Tasks containing:

```text
analytics::ignore
```

must be excluded from all calculations.

---

## Nested Tasks

Only top-level tasks participate in analytics.

Subtasks must be excluded.

Example:

```text
- [ ] Parent Task
  - [ ] Child Task
```

Analytics includes:

```text
Parent Task
```

Analytics excludes:

```text
Child Task
```

---

# 2. Classify Tasks

## Purpose

Determine analytical state of each task.

---

## Active Task

Statuses:

```text
[ ]
[/]
```

---

## Completed Task

Status:

```text
[x]
```

---

## Cancelled Task

Status:

```text
[-]
```

---

## Paused Task

Status:

```text
[<]
```

---

## Delegated Task

Status:

```text
[>]
```

---

## Archived Task

Determined according to Task_Model rules.

Archived tasks are excluded from active analytics calculations.

Archived tasks contribute only to archive statistics.

---

# 3. Assign Corridors

## Purpose

Assign tasks to score-based workload corridors.

---

## Source

Corridor configuration must be loaded from:

```text
scoring.yaml
```

---

## Corridor Matching

Task score determines corridor assignment.

Examples:

```text
score 23 → corridor 21-25
score 18 → corridor 16-20
score 13 → corridor 11-15
score 8 → corridor 6-10
score 4 → corridor 1-5
```

---

## Paused Tasks

Paused tasks:

```text
[<]
```

must not be assigned to score corridors.

They may be reported separately by presentation layers.

---

# 4. Aggregate Metrics

## Purpose

Calculate corridor and global metrics.

---

## Corridor Metrics

For each corridor calculate:

```text
overdue
active
completed
archived
```

---

## Global Metrics

Calculate:

```text
total_overdue
total_active
total_completed
total_archived
```

---

# Overdue Calculation

## Purpose

Measure accumulated execution debt.

---

## Overdue Condition

A task is overdue when:

```text
task is active
AND
due date < analysis date
```

---

## Included Statuses

```text
[ ]
[/]
```

---

## Excluded Statuses

```text
[x]
[-]
[<]
[>]
```

---

## Archived Tasks

Archived tasks must never be counted as overdue.

---

# Active Calculation

## Included Statuses

```text
[ ]
[/]
```

---

## Excluded Statuses

```text
[x]
[-]
[<]
[>]
```

---

## Important Rule

Overdue tasks remain active tasks.

Therefore:

```text
overdue ⊂ active
```

Every overdue task is also active.

---

# Completed Calculation

## Included Statuses

```text
[x]
```

---

## Excluded

Archived completed tasks.

---

# Archive Calculation

Includes all archived tasks regardless of status.

---

# 5. Calculate Status

## Purpose

Compare actual workload against target workload.

---

## Source

Targets must be loaded from:

```text
scoring.yaml
```

Analytics Engine must never use hardcoded target values.

---

# Corridor Delta Calculation

## Within Target

Condition:

```text
target.min ≤ active ≤ target.max
```

Result:

```text
delta = 0
state = ok
```

---

## Below Target

Condition:

```text
active < target.min
```

Result:

```text
delta = active - target.min
state = underloaded
```

Example:

```text
active = 1
target.min = 3

delta = -2
```

---

## Above Target

Condition:

```text
active > target.max
```

Result:

```text
delta = active - target.max
state = overloaded
```

Example:

```text
active = 14
target.max = 10

delta = +4
```

---

# Global Delta Calculation

## Source

```text
global_active.target
```

from:

```text
scoring.yaml
```

---

## Within Target

```text
delta = 0
state = ok
```

---

## Below Target

```text
delta = active - global_target.min
state = underloaded
```

---

## Above Target

```text
delta = active - global_target.max
state = overloaded
```

---

# 6. Build AnalyticsReport

## Purpose

Generate canonical analytics output.

---

## Output Type

```text
AnalyticsReport
```

Defined in:

```text
Analytics_Model.md
```

---

## Required Components

AnalyticsReport must contain:

```text
summary
global_target
global_status
corridors
```

---

# Determinism Requirements

Analytics Engine must guarantee:

* identical input produces identical output
* no dependence on report formatting
* no dependence on LLM interpretation
* no dependence on recommendation generation
* no hidden calculations
* all targets loaded from configuration

---

# Error Handling

## Missing Score

If task score is missing:

```text
exclude from corridor calculations
record validation warning
```

---

## Invalid Score

If score cannot be mapped to a corridor:

```text
exclude from corridor calculations
record validation warning
```

---

## Missing Configuration

If scoring.yaml cannot be loaded:

```text
analytics execution must fail
```

No fallback values are allowed.

---

# Analytics Engine Boundary

The Analytics Engine is responsible for:

* analytics calculations
* corridor calculations
* workload calculations
* status calculations

The Analytics Engine is not responsible for:

* RecommendationCollection
* task modification
* task prioritization
* report formatting
* dashboard rendering
* user-facing presentation

```
```

---

# Recommendation Engine

---

## Purpose

Recommendation Engine transforms AnalyticsReport into RecommendationCollection.

It is responsible for:

- generating recommendations
- prioritizing recommendations
- ordering recommendations

---

## Position in System Architecture

Task Board
↓
Parser
↓
Task Objects
↓
Analytics Engine
↓
AnalyticsReport
↓
Recommendation Engine
↓
RecommendationCollection

---

## Input

AnalyticsReport

---

## Output

RecommendationCollection

---

## Boundary

Recommendation Engine is responsible for:

- recommendation generation
- recommendation prioritization
- recommendation ordering

Recommendation Engine is not responsible for:

- task modification
- analytics calculations
- report rendering
- board mutation

---


# Report Renderer

---

## Purpose

Report Renderer converts analytics results into human-readable reports.

Report Renderer is the presentation layer of the Kanban Execution System.

Its responsibility is to transform:

```text
AnalyticsReport
+
RecommendationCollection
```

into:

```text
Markdown Report
```

Report Renderer does not perform analytics calculations.

Report Renderer does not generate RecommendationCollection.

Report Renderer does not modify analytics results.

---

## Position in System Architecture

```text
Task Board
↓
Parser
↓
Task Objects
↓
Analytics Engine
↓
AnalyticsReport
↓
Recommendation Engine
↓
RecommendationCollection
↓
Report Renderer
↓
Markdown Report
```

---

# Inputs

## AnalyticsReport

Primary analytics source.

Defined in:

```text
Analytics_Model.md
```

---

## RecommendationCollection

Recommendation source.

Defined in:

```text
Analytics_Model.md
```

---

# Output

## Markdown Report

Canonical human-readable representation of system state.

---

# Rendering Pipeline

The renderer must execute the following stages:

```text
1. Render Executive Summary
↓
2. Render Task Analysis Table
↓
3. Render RecommendationCollection
↓
4. Assemble Report
```

---

# Canonical Markdown Report

## Report Structure

Reports must be rendered in the following order:

```text
Executive Summary
↓
Task Analysis Table
↓
RecommendationCollection
```

---

# Executive Summary

## Purpose

Provide a concise overview of board health.

---

## Data Source

```text
AnalyticsReport.summary
AnalyticsReport.global_status
```

---

## Example

```text
Active Tasks: 63
Overdue Tasks: 0
Completed Tasks: 22
Archived Tasks: 80

Board Status:
✅ Healthy
```

---

# Task Analysis Table

## Purpose

Display workload distribution across score corridors.

---

## Canonical Table

| Interval | Overdue | Active | Target | Status (Δ) | Completed | Archived |
| -------- | ------: | -----: | ------ | ---------- | --------: | -------: |

---

## Row Order

Rows must always appear in the following order:

```text
21-25
16-20
11-15
6-10
1-5
[<] Paused
TOTAL
```

---

## Interval

Source:

```text
corridor.interval
```

---

## Overdue

Source:

```text
corridor.overdue
```

---

## Active

Source:

```text
corridor.active
```

---

## Target

Source:

```text
corridor.target
```

Formatting:

```text
3-5
6-10
11-20
21-30
```

Special case:

```text
0-5
```

must be rendered as:

```text
≤5
```

---

## Status (Δ)

Source:

```text
corridor.state
corridor.delta
```

Rendering rules:

### OK

Input:

```yaml
state: ok
delta: 0
```

Output:

```text
✅ (0)
```

---

### Underloaded

Input:

```yaml
state: underloaded
delta: -2
```

Output:

```text
⚠️ (-2)
```

---

### Overloaded

Input:

```yaml
state: overloaded
delta: 4
```

Output:

```text
⚠️ (+4)
```

---

## Completed

Source:

```text
corridor.completed
```

---

## Archived

Source:

```text
corridor.archived
```

---

# Paused Row

## Purpose

Display paused tasks separately from score corridors.

---

## Source

Tasks with status:

```text
[<]
```

---

## Rules

Paused tasks:

* are not assigned to corridors
* are not included in corridor totals
* are displayed separately

---

## Format

| Interval   | Overdue | Active | Target | Status (Δ) | Completed | Archived |
| ---------- | ------: | -----: | ------ | ---------- | --------: | -------: |
| [<] Paused |       — |      1 | —      | —          |         — |        — |

---

# Total Row

## Purpose

Display overall board statistics.

---

## Source

```text
AnalyticsReport.summary
AnalyticsReport.global_target
AnalyticsReport.global_status
```

---

## Format

| Interval | Overdue | Active | Target | Status (Δ) | Completed | Archived |
| -------- | ------: | -----: | ------ | ---------- | --------: | -------: |
| TOTAL    |       0 |     63 | 60-70  | ✅ (0)      |        22 |       80 |

---

## Total Status Rules

Uses the same rendering rules as corridor rows.

---

# RecommendationCollection

## Purpose

Display actionable RecommendationCollection.

---

## Source

```text
RecommendationCollection
```

---

## Ordering

RecommendationCollection must be rendered by priority:

```text
high
↓
medium
↓
low
```

---

## Example

```text
1. Increase corridor 21-25 by 2 tasks.
2. Reduce corridor 16-20 by 4 tasks.
3. Review 5 overdue tasks.
```

---

# Determinism Requirements

Renderer must guarantee:

* identical input produces identical output
* stable section ordering
* stable row ordering
* stable recommendation ordering
* no hidden calculations
* no analytics recalculation
* no recommendation recalculation

---

# Renderer Boundary

Report Renderer is responsible for:

* formatting
* layout
* ordering
* presentation

Report Renderer is not responsible for:

* parsing
* analytics
* RecommendationCollection
* task management
* prioritization
* business rules

---

# Single Source of Truth

Report Renderer must use:

```text
AnalyticsReport
RecommendationCollection
```

as its only data sources.

No values may be inferred, recalculated, or replaced during rendering.

```
```


