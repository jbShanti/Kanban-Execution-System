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

# 1.2 Analytics Domains

## Purpose

AnalyticsReport exists to support management decisions.
Analytics are organized into four decision domains.
Each domain answers a different class of questions.
Analytics should support decision-making rather than metric collection.

## Domain 1 — Focus Decisions

Purpose:
What should be done today and within the next three days?

Questions:
Where is attention currently concentrated?
Which tasks should be moved into focus?
Which tasks may be safely deferred?
Which tasks provide the highest strategic value right now?
How many tasks are overdue, due today or due within the next three days?
What is the total score value of overdue and urgent tasks?

## Domain 2 — Tactical Decisions

Purpose:
How should the current workload be managed?

Questions:
Is the system overloaded?
Is there a mismatch between importance and actual attention?
How healthy is the score distribution?
What is the current work-in-progress level?
How many tasks are blocked, delegated or waiting?
What is the current execution velocity?
What is the ratio of completed, cancelled and archived tasks?

## Domain 3 — Strategic Decisions

Purpose:
Is the current board structure leading toward meaningful results?

Questions:
Where is the largest concentration of potential value?
How is the board structure changing over time?
What is the total score value of active work and what percentage of total score does it represent?
What is the overall board health status?
Is value excessively concentrated in a small number of tasks?
Is execution momentum increasing or decreasing?
What strategic execution debt is accumulating?

## Domain 4 — Data Quality

Purpose:
Can the analytics be trusted?

Questions:
What percentage of tasks have no score?
What percentage of tasks have no estimate?
How complete is score coverage across total board value?

## Design Principle

Analytics domains define:
why analytics exist

AnalyticsReport defines:
what is calculated

Report Renderer defines:
how analytics are presented

---

# 1.3 Analytics Sections

## Purpose

AnalyticsReport is organized into analytical sections.

Each section supports one decision domain.

Sections define where analytics results are stored.

Sections do not define calculations.

Calculations are defined by the Analytics Engine.

Presentation is defined by the Report Renderer.

---

## Canonical Structure

```yaml
AnalyticsReport:

  focus:
    ...

  tactical:
    ...

  strategic:
    ...

  data_quality:
    ...

  corridors:
    ...
```

---

## Focus Analytics

### Purpose

Support daily and short-term execution decisions.

### Questions

* What should be done today?
* What should be done within the next three days?
* Which tasks should be prioritized?
* Which tasks may be safely deferred?
* What urgent risks require attention?

---

## Tactical Analytics

### Purpose

Support workload and execution flow management.

### Questions

* Is the system overloaded?
* Is attention aligned with importance?
* Is workload balanced?
* Are there blocked tasks?
* What is the current execution velocity?

---

## Strategic Analytics

### Purpose

Support long-term execution and value allocation decisions.

### Questions

* Where is value concentrated?
* How is the board evolving?
* Is execution momentum improving?
* Is strategic debt accumulating?
* Does the current structure support meaningful results?

---

## Data Quality Analytics

### Purpose

Measure analytics reliability.

### Questions

* How complete is scoring coverage?
* How complete are task estimates?
* Can analytics results be trusted?

---

## Corridor Analytics

### Purpose

Support score-based workload balancing.

### Contains

* corridor statistics
* corridor targets
* corridor status
* corridor deltas
* score distribution metrics

Corridor Analytics are configuration-driven through:

```text
scoring.yaml
```

---

## Design Principle

Domains define:

```text
Why analytics exist.
```

Sections define:

```text
Where analytics are stored.
```

Analytics Engine defines:

```text
How analytics are calculated.
```

Report Renderer defines:

```text
How analytics are presented.
```


---

# 2. AnalyticsReport

## Purpose

AnalyticsReport is the canonical output of the Analytics Engine.

Every analytics calculation produces exactly one AnalyticsReport object.

AnalyticsReport stores analytical results.

AnalyticsReport does not contain:

* recommendation logic
* rendering rules
* report formatting
* business logic

AnalyticsReport is presentation-independent.

---

## Canonical Structure

```yaml
AnalyticsReport:

  generated_at: 2026-06-06

  focus:
    ...

  tactical:
    ...

  strategic:
    ...

  data_quality:
    ...

  corridors:
    ...

  summary:
    ...
```

---

## Sections

### focus

Contains analytics supporting daily and short-term execution decisions.

Examples:

* attention allocation
* focus candidates
* urgent tasks
* overdue risk
* near-term priorities

---

### tactical

Contains analytics supporting workload and execution flow management.

Examples:

* overload detection
* WIP analysis
* blocked work
* delegated work
* execution velocity
* workload balance

---
#### Tactical Workload Status

##### Purpose

Represents current workload status relative to configured workload targets.

Used to detect:

* overload
* underload
* workload balance

Supports Tactical Analytics decisions.

---

##### Structure

```yaml
tactical:

  workload:
    active: 63

  target:
    min: 60
    max: 70

  status:
    delta: 0
    state: ok
```

---

##### workload

###### active

Number of active tasks.

Includes:

```text
[ ]
[/]
```

Excludes:

```text
[x]
[-]
[<]
[>]
```

Archived tasks are excluded.

---

##### target

###### Purpose

Defines the desired active workload range.

Source:

```text
scoring.yaml
```

---

###### Structure

```yaml
target:
  min: 60
  max: 70
```

---

##### status

###### Purpose

Represents workload health relative to the configured target range.

---

###### Structure

```yaml
status:
  delta: 0
  state: ok
```

---

###### State Values

Supported values:

```text
ok
underloaded
overloaded
```

---

###### Delta Calculation

Within target:

```text
delta = 0
state = ok
```

---

Below target:

```text
delta = active - target.min
state = underloaded
```

Example:

```text
active = 52
target.min = 60

delta = -8
```

---

Above target:

```text
delta = active - target.max
state = overloaded
```

Example:

```text
active = 81
target.max = 70

delta = +11
```

---

##### Design Principle

Workload targets are configuration-driven.

Targets must be loaded from:

```text
scoring.yaml
```

Analytics engines must never use hardcoded workload targets.

```
```



---

### strategic

Contains analytics supporting long-term execution and value allocation decisions.

Examples:

* value concentration
* board evolution
* active value share
* execution momentum
* execution debt
* board health

---

### data_quality

Contains analytics describing data completeness and reliability.

Examples:

* score coverage
* estimate coverage
* metadata completeness
* analytics confidence indicators

---

### corridors

Contains score corridor analytics.

Defined by:

```text
scoring.yaml
```

Contains:

* corridor statistics
* corridor targets
* corridor status
* corridor deltas
* score distribution metrics

---

### summary

Contains a concise executive overview of the current board state.

Purpose:

Provide a human-readable summary of the most important analytical findings.

The summary is intended for rapid review and should allow a user to understand the current situation without inspecting individual analytics sections.

The summary may aggregate signals from:

* focus analytics
* tactical analytics
* strategic analytics
* data quality analytics
* corridor analytics

---

#### Design Principles

The summary is:

* concise
* human-oriented
* decision-oriented

The summary is not:

* a complete analytics report
* a source of truth
* a replacement for detailed analytics sections

Detailed analytics must remain within their respective sections.

---

#### Example

```yaml
summary:

  board_health: yellow

  primary_signal:
    WIP overload detected

  secondary_signal:
    3 high-score overdue tasks

  focus_recommendation:
    Reduce active workload before starting new work
```

---

#### Responsibility

Analytics Engine:

```text
Produces summary signals.
```

Report Renderer:

```text
Determines how summary information is presented.
```

Recommendation Engine:

```text
May use summary signals as recommendation inputs.
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

# 4. Focus Analytics

## Purpose

Focus Analytics supports daily and short-term execution decisions.

Its purpose is to determine where attention should be directed today and within the next three days.

Focus Analytics is action-oriented.

Unlike Tactical Analytics and Strategic Analytics, Focus Analytics is concerned with immediate execution priorities.

---

## Supported Questions

Focus Analytics should help answer the following questions:

1. Where is attention currently concentrated?

2. Which tasks should be moved into focus?

3. Which tasks may be safely deferred?

4. Which tasks provide the highest strategic value right now?

5. Which tasks are overdue, due today or due within the next three days?

6. What is the total score value of overdue and urgent tasks?

7. Which tasks provide the highest value per unit of time?

8. Which tasks have the highest score efficiency?

Definition:
score_efficiency = score / estimate
Score efficiency represents expected value produced per unit of estimated effort.


---

## Canonical Structure

```yaml
focus:

  urgency:
    ...

  attention:
    ...

  priority:
    ...
```

---

### urgency

Purpose:

Identify work requiring immediate attention.

Focuses on time-sensitive execution risks.

---

### attention

Purpose:

Describe current attention allocation.

Focuses on where effort is currently invested.

---

### priority

Purpose:

Identify where attention should be directed.

Focuses on value and execution impact.

Supports:

- focus selection
- task ranking
- strategic value analysis
- score efficiency analysis

---

### Score Efficiency

Definition:

```text
score_efficiency = score / estimate
```
Purpose:

Identify tasks that provide the highest value per unit of estimated effort.

Used for:
- daily planning
- constrained time windows
- focus selection
- recommendation generation


---

# 4.1 FocusUrgencyAnalytics

## Purpose

FocusUrgencyAnalytics identifies tasks requiring immediate attention.

It measures execution risk associated with approaching or missed deadlines.

FocusUrgencyAnalytics is time-oriented.

Unlike Priority Analytics, which evaluates value, Urgency Analytics evaluates temporal risk.

---

## Supported Questions

FocusUrgencyAnalytics should help answer the following questions:

1. Which tasks are overdue?

2. Which tasks are due today?

3. Which tasks are due within the next three days?

4. What is the total score value associated with urgent work?

5. What level of execution risk currently exists?

---

## Canonical Structure

```yaml
urgency:

  overdue:
    ...

  due_today:
    ...

  due_next_3_days:
    ...

  risk:
    ...
```

---

## Components

### overdue

Purpose:

Identify tasks whose due date has already passed.

Structure:

```yaml
overdue:

  task_count:
    0

  score_value:
    0

  tasks:
    - AnalyticsTaskSnapshot
    - AnalyticsTaskSnapshot
```

Answers:

* Which tasks are overdue?
* What score value is currently overdue?

---

### due_today

Purpose:

Identify tasks that should be completed today.

Structure:

```yaml
due_today:

  task_count:
    0

  score_value:
    0

  tasks:
    - AnalyticsTaskSnapshot
    - AnalyticsTaskSnapshot
```

Answers:

* Which tasks are due today?
* What score value is due today?

---

### due_next_3_days

Purpose:

Identify tasks that should be completed within the next three days.

Structure:

```yaml
due_next_3_days:

  task_count:
    0

  score_value:
    0

  tasks:
    - AnalyticsTaskSnapshot
    - AnalyticsTaskSnapshot
```

Answers:

* Which tasks are due within the next three days?
* What score value is due soon?

---

### risk

Purpose:

Provide an aggregated urgency signal.

Structure:

```yaml
risk:

  score_value:
    0

  status:
    normal
```

---

### Supported Status Values

```text
normal
warning
critical
```

Answers:

* What is the current urgency level?
* How much score value is at risk?

---

## Design Principle

FocusUrgencyAnalytics should detect execution risk as early as possible.

Urgency is determined by time constraints.

Urgency Analytics does not determine task priority.

Priority decisions belong to FocusPriorityAnalytics.

---

# 4.1.1 AnalyticsTaskSnapshot

## Purpose

AnalyticsTaskSnapshot is a lightweight task representation used by analytics models.

It contains only fields required for analytics, recommendations and report rendering.

AnalyticsTaskSnapshot is derived from Task.

It is not a replacement for Task.

---

## Canonical Structure

```yaml
AnalyticsTaskSnapshot:

  title:

  score:

  estimate:

  status:

  due:

  area:
```

---

## Fields

### title

Human-readable task name.

---

### score

Task value score.

Used by:

* Focus Analytics
* Tactical Analytics
* Strategic Analytics
* Corridor Analytics

---

### estimate

Estimated effort required to complete the task.

Used by:

* Focus Analytics
* Recommendation Engine
* Daily Planning
* Score Efficiency Analytics

---

### status

Current task status.

Examples:

```text
active
scheduled
delegated
blocked
```

---

### due

Task due date.

Used by Urgency Analytics.

---

### area

Logical task grouping used for analytics.

Source:
Derived from Task categorization metadata.

Examples:

```text
Health
Infrastructure
Product
Business
```

---

## Design Principle

AnalyticsTaskSnapshot should contain only fields required by analytics.

Analytics models must not depend on the full Task object.

---

# 4.2 FocusAttentionAnalytics

## Purpose

FocusAttentionAnalytics describes how attention is currently distributed across the system.

It helps identify where attention is concentrated and whether current attention allocation is aligned with intended priorities.

---

## Attention Definition

Attention represents the distribution of active score across analytical areas.

Attention is measured using score rather than task count.

Score is treated as a unit of intended attention allocation.

Higher score indicates a greater share of attention that should be directed toward a task.

Task count may be used as a supplementary metric but is not the primary measure of attention.

---

## Design Principle

FocusAttentionAnalytics does not measure effort spent.

FocusAttentionAnalytics measures intended attention allocation as represented by score.

The purpose of Attention Analytics is to answer:

* Where is attention currently concentrated?
* How is attention distributed across areas?
* Is attention aligned with priorities?


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
tactical.status.state = overloaded
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
active - tactical.target.max
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
delta = active - tactical.target.min
state = underloaded
```

---

## Above Target

```text
delta = active - tactical.target.max
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
  generated_at:
  focus:
  tactical:
  strategic:
  data_quality:
  corridors:
  summary:
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
AnalyticsReport.tactical.status
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
AnalyticsReport.tactical.target
AnalyticsReport.tactical.status
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


