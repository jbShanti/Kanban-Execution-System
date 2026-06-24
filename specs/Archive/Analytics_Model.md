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

# 2. AnalyticsReport

AnalyticsReport is the canonical output artifact produced by the Analytics Engine.

It aggregates all calculated analytics, synthesized conclusions, and generated recommendations into a single structured report.

AnalyticsReport serves as the primary interface between the Analytics Engine and downstream consumers such as review protocols, dashboards, agents, and decision-support workflows.

## Structure

```yaml
AnalyticsReport:

  generated_at:
    datetime

  summary:
    ExecutiveSummary

  focus:

    attention:
      FocusAttentionAnalytics

    urgency:
      FocusUrgencyAnalytics

    priority:
      FocusPriorityAnalytics

  tactical:
    TacticalAnalytics

  strategic:
    StrategicAnalytics

  data_quality:
    DataQualityAnalytics

  corridors:
    CorridorsAnalytics

  recommendations:
    Recommendations
```

## Design Principles

### Single Source of Truth

AnalyticsReport is the only canonical representation of analytical results.

All downstream consumers should operate on AnalyticsReport rather than recalculating metrics independently.

### Separation of Concerns

AnalyticsReport stores analytical outputs only.

Raw task data remains within the Kanban system and is not duplicated inside the report.

### Hierarchical Organization

Analytics are grouped by decision horizon:

- Focus — immediate attention allocation decisions.
- Tactical — execution management decisions.
- Strategic — long-term system evolution decisions.
- Data Quality — assessment of model reliability.
- Corridors — acceptable operating ranges and deviations.

### Extensibility

New analytics objects may be added within existing sections without breaking the top-level report contract.

New sections should be introduced only when they represent a fundamentally distinct decision domain.

### Recommendation Integration

Recommendations are derived from analytics and stored separately from analytical observations.

Analytics describe the system state.

Recommendations describe proposed actions.

---

# 2.1 Analytics Design Principles

## Measurement First

Analytics components produce measurements.

Their responsibility is to describe the current state of the system using objective and reproducible metrics.

Analytics components must answer:

```text
What is happening?
```

They must not answer:

```text
Why is it happening?

What should be done?
```

---

## Separation of Responsibilities

```text
Analytics Engine
↓
Measurements

SummaryAnalytics
↓
Synthesis

Recommendation Engine
↓
Actions
```

---

## Analytics Engine

Analytics Engine produces measurements.

Examples:

```yaml
WorkloadHealth:

  active_tasks: 17

  target:

    min: 15

    max: 20

  delta: 0

  state: ok
```

```yaml
OverduePressure:

  overdue_tasks: 4

  overdue_percentage: 23.5

  overdue_score: 68

  state: elevated
```

Analytics components may calculate derived metrics.

They must not generate interpretations, recommendations, or action plans.

---

## SummaryAnalytics

SummaryAnalytics synthesizes analytical findings.

Its purpose is to identify:

* important observations
* primary risks
* primary opportunities
* recommended focus areas

SummaryAnalytics may interpret measurements produced by analytics components.

---

## Recommendation Engine

Recommendation Engine generates actionable guidance.

Its purpose is to answer:

```text
What should be done next?
```

Recommendations may be derived from:

* SummaryAnalytics
* TacticalAnalytics
* StrategicAnalytics
* FocusAttentionAnalytics

---

## Design Principle

The analytics architecture follows a layered model:

```text
Measurements
↓
Interpretation
↓
Recommendation
```

Where:

```text
Measurements
→ Analytics Engine

Interpretation
→ SummaryAnalytics

Recommendation
→ Recommendation Engine
```

Each layer has a single responsibility and must not assume responsibilities belonging to other layers.
---

# 2.2 Analytics Processing Pipeline

## Purpose

Analytics Processing Pipeline defines the canonical sequence of analytical processing steps.

It describes how raw task data is transformed into an AnalyticsReport.

The pipeline ensures that analytics components are executed in a deterministic and reproducible order.

---

## Canonical Pipeline

```text
Tasks
↓
AnalyticsTaskSnapshot Generation
↓
Focus Analysis
↓
Tactical Analysis
↓
Strategic Analysis
↓
Corridor Analysis
↓
Summary Generation
↓
AnalyticsReport Assembly
```

---

## Canonical Structure

```yaml
AnalyticsPipeline:

  snapshot_generation

  focus_analysis

  tactical_analysis

  strategic_analysis

  corridor_analysis

  summary_generation

  report_assembly
```

---

## Step 1. Snapshot Generation

Input:

```text
Tasks
```

Output:

```text
AnalyticsTaskSnapshot[]
```

Purpose:

Normalize task data into a canonical analytical representation.

---

## Step 2. Focus Analysis

Input:

```text
AnalyticsTaskSnapshot[]
```

Output:

```text
FocusAttentionAnalytics
```

Purpose:

Calculate attention distribution, concentration, and alignment.

---

## Step 3. Tactical Analysis

Input:

```text
AnalyticsTaskSnapshot[]
```

Output:

```text
TacticalAnalytics
```

Purpose:

Calculate execution-state metrics.

Examples:

```text
WorkloadHealth
OverduePressure
```

---

## Step 4. Strategic Analysis

Input:

```text
AnalyticsTaskSnapshot[]
```

Output:

```text
StrategicAnalytics
```

Purpose:

Calculate value-distribution and portfolio metrics.

Examples:

```text
ValueConcentration
PortfolioBalance
```

---

## Step 5. Corridor Analysis

Input:

```text
AnalyticsTaskSnapshot[]
```

Output:

```text
CorridorAnalytics[]
```

Purpose:

Generate analytics for configured score corridors.

---

## Step 6. Summary Generation

Input:

```text
FocusAttentionAnalytics
TacticalAnalytics
StrategicAnalytics
CorridorAnalytics[]
```

Output:

```text
SummaryAnalytics
```

Purpose:

Synthesize analytical findings into a concise executive overview.

SummaryAnalytics may interpret measurements generated by previous pipeline stages.

---

## Step 7. Report Assembly

Input:

```text
SummaryAnalytics
FocusAttentionAnalytics
TacticalAnalytics
StrategicAnalytics
CorridorAnalytics[]
```

Output:

```text
AnalyticsReport
```

Purpose:

Assemble all analytical artifacts into the canonical report structure.

---

## Design Principle

The pipeline follows the architecture defined in Analytics Design Principles:

```text
Measurements
↓
Interpretation
↓
Report
```

Where:

```text
Measurements
→ Focus
→ Tactical
→ Strategic
→ Corridors

Interpretation
→ Summary

Report
→ AnalyticsReport
```

---

## Dependency Rules

Analytics components must not depend on SummaryAnalytics.

Allowed dependencies:

```text
AnalyticsTaskSnapshot
↓
FocusAttentionAnalytics

AnalyticsTaskSnapshot
↓
TacticalAnalytics

AnalyticsTaskSnapshot
↓
StrategicAnalytics

AnalyticsTaskSnapshot
↓
CorridorAnalytics
```

SummaryAnalytics depends on analytical measurements.

AnalyticsReport depends on all analytical components.

---

## Responsibility

Analytics Processing Pipeline defines:

* processing order
* data flow
* dependency rules
* report assembly sequence

It does not define:

* recommendation generation
* report rendering
* task parsing
* task editing

Those responsibilities belong to other system components.

---

# 2.3 Analytics Engine

## Purpose

Analytics Engine is the application service responsible for generating AnalyticsReport objects from task data.

It serves as the single entry point for analytical processing.

Analytics Engine orchestrates the execution of the Analytics Processing Pipeline and assembles the resulting AnalyticsReport.

---

## Canonical Interface

```yaml
AnalyticsEngine:

  generate_report(
    tasks
  ) -> AnalyticsReport
```

---

## Input

Input:

```text
Task[]
```

Analytics Engine consumes task data as the source of analytical information.

Tasks must not be modified during processing.

---

## Output

Output:

```text
AnalyticsReport
```

AnalyticsReport is the canonical analytical artifact produced by the system.

All analytical consumers must depend on AnalyticsReport rather than individual analytics components.

---

## Processing Flow

Analytics Engine executes the Analytics Processing Pipeline.

```text
Tasks
↓
AnalyticsTaskSnapshot Generation
↓
Focus Analysis
↓
Tactical Analysis
↓
Strategic Analysis
↓
Corridor Analysis
↓
Summary Generation
↓
AnalyticsReport Assembly
```

Pipeline stages must be executed in the order defined by Analytics Processing Pipeline.

---

## Single Entry Point

Analytics Engine is the single entry point for analytical report generation.

Consumers should not invoke analytical components directly.

```text
Consumer
↓
Analytics Engine
↓
AnalyticsReport
```

---

## Deterministic Processing

Analytics Engine must be deterministic.

Identical input must produce identical output.

```text
Same Tasks
↓
Analytics Engine
↓
Same AnalyticsReport
```

Analytics calculations must not depend on random or non-deterministic behavior.

---

## Read-Only Processing

Analytics Engine performs analytical computation only.

It must never:

* modify tasks
* change task metadata
* update board state
* generate recommendations

Analytics Engine is a read-only component.

---

## Responsibility

Analytics Engine is responsible for:

* snapshot generation
* analytical orchestration
* pipeline execution
* report assembly

Analytics Engine is not responsible for:

* task parsing
* recommendation generation
* report rendering
* task modification

Those responsibilities belong to other system components.

---

## Design Principle

Analytics Engine orchestrates analytical computation.

Analytics components perform measurements.

SummaryAnalytics performs interpretation.

Analytics Engine assembles the final report.

```text
Measurements
↓
Interpretation
↓
AnalyticsReport
```

Analytics Engine is responsible for coordinating this process, not for introducing additional analytical logic.

---

## Dependency Rules

Analytics Engine may depend on:

```text
AnalyticsTaskSnapshot
FocusAttentionAnalytics
TacticalAnalytics
StrategicAnalytics
CorridorAnalytics
SummaryAnalytics
AnalyticsReport
```

Analytical components must not depend on Analytics Engine.

Dependency direction must always be:

```text
Analytics Engine
↓
Analytics Components
```


---

# 3. Domain Contracts

## Purpose

Domain Contracts define canonical analytical value objects shared across the analytics model.

They provide a common vocabulary for analytical processing and ensure consistent interpretation of task metadata.

Domain Contracts are immutable value objects.

They may be referenced by multiple analytics components.

---

# 3.1 TagsArea

## Purpose

TagsArea represents a deterministic area classification derived from task tags.

TagsArea provides a stable and reproducible area assignment without requiring semantic analysis.

---

## Canonical Structure

```yaml
TagsArea:

  value:
```

---

## Example

```yaml
TagsArea:

  value:
    Projects/AI
```

---

## Generation Rules

TagsArea is derived from the first two levels of the task tag hierarchy.

Examples:

```text
#Projects/AI/Agent
↓
Projects/AI
```

```text
#Health/Sleep/HRV
↓
Health/Sleep
```

---

## Design Principle

TagsArea is:

```text
Deterministic
Config-Free
Reproducible
```

Given the same tags, TagsArea must always produce the same result.

---

## Responsibility

TagsArea answers:

```text
Which tag-based area does this task belong to?
```

---

# 3.2 SemanticArea

## Purpose

SemanticArea represents an LLM-derived area classification.

It provides a semantic interpretation of task purpose using task content and available metadata.

---

## Canonical Structure

```yaml
SemanticArea:

  value:
```

---

## Example

```yaml
SemanticArea:

  value:
    Health
```

---

## Inputs

SemanticArea may use:

* task title
* task description
* task tags

---

## Design Principle

SemanticArea is:

```text
Semantic
Context-Aware
LLM-Based
```

Unlike TagsArea, SemanticArea is not derived from deterministic tag rules.

---

## Responsibility

SemanticArea answers:

```text
What is the actual area of this task?
```

---

## Relationship to TagsArea

Priority order:

```text
SemanticArea
↓
TagsArea
```

When SemanticArea is unavailable, TagsArea should be used as the fallback classification.

---

# 3.3 ScoreCorridor

## Purpose

ScoreCorridor represents a canonical score interval used for analytical aggregation.

It serves as the primary grouping mechanism for corridor-based analytics.

---

## Canonical Structure

```yaml
ScoreCorridor:

  min_score:

  max_score:

  label:
```

---

## Example

```yaml
ScoreCorridor:

  min_score:
    21

  max_score:
    25

  label:
    21-25
```

---

## Generation Rules

ScoreCorridor is determined from task score.

Examples:

```text
score = 23
↓
21-25
```

```text
score = 8
↓
6-10
```

---

## Design Principle

ScoreCorridor is:

```text
Deterministic
Score-Based
Immutable
```

The same score must always map to the same corridor.

---

## Responsibility

ScoreCorridor answers:

```text
Which score corridor does this task belong to?
```

---

## Consumers

ScoreCorridor may be used by:

* AnalyticsTaskSnapshot
* CorridorAnalytics
* ValueConcentration
* OverduePressure
* SummaryAnalytics
* AnalyticsReport.Corridors

---

## Design Principle

ScoreCorridor is the canonical value-grouping mechanism of the analytics system.

All corridor-based analytics must use ScoreCorridor rather than custom score grouping logic.


---

### 3.4 AreaPriorityConfiguration

#### Purpose

AreaPriorityConfiguration defines the priority assigned to each Area.

It serves as the authoritative source of Area Priority used in score calculation.

---

#### Design Principle

Area priorities are configured externally to the board.

They are not derived from task metadata.

They represent strategic importance rather than operational activity.

---

#### Canonical Structure

```yaml
AreaPriorityConfiguration:

  Health: 5

  Projects: 5

  Learning: 4

  Family: 4

  Administration: 3

  Other Projects: 3

  Someday: 1
```

---

#### Responsibility

AreaPriorityConfiguration defines:

- Area Priority values
- score calculation inputs
- expected attention distribution

It does not define:

- task priorities
- task scores
- corridor assignments


---

# 4. Board Metrics

## Summary Object

```yaml
BoardMetrics:
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

# 5. Focus Analytics

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

# 5.1 FocusUrgencyAnalytics

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

# 5.1.1 AnalyticsTaskSnapshot

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

  tags_area: TagsArea

  semantic_area: SemanticArea

  corridor: ScoreCorridor
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

Used by:

* Urgency Analytics

---

### tags_area

Deterministic analytical grouping derived from task tags.

Tags Area is the canonical grouping dimension used by deterministic analytics.

Examples:

```text
#Health
→ Health

#Finance/Investments
→ Finance/Investments

#Projects/AI
→ Projects/AI

#Projects/AI/Agents
→ Projects/AI
```

---

#### Resolution Rule

Tags Area is derived from the first two levels of the tag hierarchy.

Canonical rule:

```text
tags_area = first_two_tag_levels
```

Examples:

```text
#Projects/AI/Agents
→ Projects/AI

#Projects/AI
→ Projects/AI

#Health
→ Health
```

---

#### Multiple Tags

When multiple analytical tags exist:

```text
#Projects/AI
#Business
```

the first analytical tag becomes the source of Tags Area.

Current implementations must produce exactly one Tags Area value.

Future versions may support multi-area analytics.

---

#### Design Principle

Tags Area is:

* deterministic
* reproducible
* machine-derived
* independent from AI interpretation

Used by:

* FocusAttentionAnalytics
* Distribution Analytics
* Concentration Analytics
* Alignment Analytics

---

### semantic_area

AI-generated analytical grouping.

Semantic Area provides higher-level semantic classification beyond the tag hierarchy.

Semantic Area may be derived from:

* task title
* task description
* tags
* metadata
* section context

using AI classification.

---

#### Examples

```text
Task:
Configure Docker for Job Agent

Tags:
#Projects/AI

Semantic Area:
AI Infrastructure
```

---

```text
Task:
Design Analytics Engine

Tags:
#Projects/AI

Semantic Area:
Kanban System Development
```

---

```text
Task:
Buy Omega-3

Tags:
#Health

Semantic Area:
Health Optimization
```

---

#### Availability

Semantic Area is optional.

Analytics systems may operate without Semantic Area.

---

#### Design Principle

Semantic Area is:

* AI-derived
* non-deterministic
* semantically meaningful
* higher-level

Semantic Area must never replace Tags Area in deterministic analytics.

---

## Design Principle

AnalyticsTaskSnapshot should contain only fields required by analytics.

Analytics models must not depend on the full Task object.

AnalyticsTaskSnapshot serves as the canonical analytical representation of a task and provides a stable contract between the Analytics Engine and downstream consumers.


---

# 5.2 FocusAttentionAnalytics

## Purpose

FocusAttentionAnalytics describes how attention is currently distributed across the system.

It helps identify:

* where attention is concentrated
* how attention is distributed across areas
* whether attention allocation is balanced
* whether current attention aligns with strategic priorities

Attention is measured using score rather than task count.

---

## Canonical Structure

```yaml
attention:

  distribution:
    ...

  concentration:
    ...

  alignment:
    ...
```

---

# 5.2.1 Distribution

## Purpose

Describe how active score is distributed across analytical areas.

Distribution answers:

* Where is attention currently allocated?
* Which areas receive the largest share of attention?
* Which areas receive little or no attention?

---

## Structure

```yaml
distribution:

  total_active_score:
    0

  areas:

    - area:
        Infrastructure

      active_score:
        85

      score_share_percentage:
        34.0

    - area:
        Health

      active_score:
        60

      score_share_percentage:
        24.0
```

---

## total_active_score

Sum of scores of all active tasks.

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

---

## active_score

Sum of active task scores within the area.

---

## score_share_percentage

Formula:

```text
area.active_score
/
distribution.total_active_score
× 100
```

Range:

```text
0.0 .. 100.0
```

---

## Design Principle

Distribution measures:

```text
allocation
```

not:

```text
performance
```

---

# 5.2.2 Concentration

## Purpose

Measure how strongly attention is concentrated.

Concentration answers:

* Is attention spread across many areas?
* Is attention focused on a small number of areas?
* Is attention fragmented?

---

## Structure

```yaml
concentration:

  largest_area:
    Infrastructure

  largest_area_share:
    34.0

  top_3_share:
    72.0

  status:
    balanced
```

---

## largest_area

Area with the highest active score.

---

## largest_area_share

Percentage of total active score represented by the largest area.

---

## top_3_share

Combined percentage of active score represented by the three largest areas.

Formula:

```text
sum(top_3_area_scores)
/
total_active_score
× 100
```

---

## status

Supported values:

```text
fragmented
balanced
concentrated
```

---

## Purpose of Status

Provide a simplified attention signal.

Examples:

```text
fragmented
```

Attention spread across many unrelated areas.

```text
balanced
```

Attention focused without excessive concentration.

```text
concentrated
```

Most attention allocated to a small number of areas.

---

# 5.2.3 Alignment

## Purpose

Measure whether actual attention allocation aligns with strategic importance.

Alignment answers:

* Is attention concentrated where the most value exists?
* Are high-value areas receiving enough attention?
* Is attention being wasted on low-value areas?

---

## Structure

```yaml
alignment:

  high_value_share:
    58.0

  attention_share:
    61.0

  delta:
    3.0

  status:
    aligned
```

---

## high_value_share

Percentage of total board score represented by high-value work.

Example:

```text
21-25
+
16-20
```

score corridors.

---

## attention_share

Percentage of active score currently allocated to high-value work.

---

## delta

Formula:

```text
attention_share
-
high_value_share
```

---

## status

Supported values:

```text
aligned
underfocused
overfocused
```

---

## Design Principle

Alignment measures:

```text
attention
vs
importance
```

This is not a productivity metric.

It is an allocation metric.

---

## Responsibility

FocusAttentionAnalytics answers:

* Where attention is currently allocated.
* How concentrated attention is.
* Whether attention allocation matches strategic importance.

It does not measure:

* effort spent
* execution velocity
* completion rates
* productivity

Those concerns belong to Tactical Analytics and Strategic Analytics.

---

# 6. AnalyticsReport

## Purpose

AnalyticsReport is the canonical output of the Analytics Engine.

It contains all analytical results generated from a collection of AnalyticsTaskSnapshot objects.

AnalyticsReport serves as the primary contract between:

* Analytics Engine
* Recommendation Engine
* Report Renderer

AnalyticsReport is immutable.

---

## Canonical Structure

```yaml
AnalyticsReport:

  generated_at:

  summary:

  focus_attention:

  tactical:

  strategic:

  corridors:
```

---

## Fields

### generated_at

Timestamp indicating when the report was generated.

Example:

```text
2026-06-10T09:30:00Z
```

---

### summary

High-level analytical overview of the board.

Purpose:

Provide a concise executive summary before detailed analytics.

Typical contents may include:

* total tasks
* total score
* active workload
* overdue workload
* major observations

---

### focus_attention

FocusAttentionAnalytics object.

Purpose:

Describe how attention is distributed across analytical areas.

Answers:

* Where attention is concentrated.
* Whether attention is fragmented.
* Whether attention aligns with strategic value.

---

### tactical

TacticalAnalytics object.

Purpose:

Describe execution-level conditions requiring attention.

Examples:

* overdue pressure
* workload imbalance
* execution bottlenecks
* corridor health issues

---

### strategic

StrategicAnalytics object.

Purpose:

Describe long-term portfolio composition and value allocation.

Examples:

* score distribution
* value concentration
* portfolio balance
* strategic focus

---

### corridors

Collection of CorridorAnalytics objects.

Purpose:

Provide the canonical score-corridor analytical table.

Each corridor represents one score range.

Examples:

```text
21-25
16-20
11-15
6-10
1-5
```

---

## Generation Flow

```text
Tasks
↓
AnalyticsTaskSnapshot
↓
Analytics Engine
↓
AnalyticsReport
↓
Recommendation Engine
↓
Report Renderer
```

---

## Design Principle

AnalyticsReport is the single source of truth for analytical output.

Consumers must depend on AnalyticsReport rather than individual analytics engines.

This ensures a stable contract between analytics generation and report rendering.

---

## Responsibility

AnalyticsReport answers:

* What is happening on the board?
* Where attention is allocated?
* What requires intervention?
* How value is distributed?
* What strategic patterns are present?

AnalyticsReport does not contain:

* raw task objects
* task editing logic
* board parsing logic
* recommendation generation logic

Those responsibilities belong to other system components.


---

## 6.1 AnalyticsReport.Corridors

### Purpose

Corridors contains analytics for all configured score corridors.

It provides the primary analytical table used for workload, value and attention analysis across score ranges.

Each corridor is represented by a CorridorAnalytics object.

---

### Canonical Structure

```yaml
corridors:

  - CorridorAnalytics

  - CorridorAnalytics

  - CorridorAnalytics

  - CorridorAnalytics

  - CorridorAnalytics
```

---

### Ordering

Corridors must be sorted by descending score range.

Example:

```text
21-25
16-20
11-15
6-10
1-5
```

The ordering must match the configured score corridor definitions.

---

### Completeness

Every configured score corridor must appear in the report.

Empty corridors must not be omitted.

Example:

```yaml
interval:
  21-25

workload:

  active:
    0

  overdue:
    0

  completed:
    0

  archived:
    0
```

---

### Corridor Source

Corridors are generated from AnalyticsTaskSnapshot objects.

Generation flow:

```text
AnalyticsTaskSnapshot
↓
Corridor Assignment
↓
CorridorAnalytics
↓
AnalyticsReport.Corridors
```

---

### Design Principle

Corridors represent the canonical analytical table of the system.

Each CorridorAnalytics object corresponds to a single analytical row.

```text
CorridorAnalytics
↓
Analytical Row
↓
Analytics Table
```

The Report Renderer should render corridors directly from this collection without additional aggregation.

---

### Responsibility

AnalyticsReport.Corridors answers:

* How workload is distributed across score ranges.
* How value is distributed across score ranges.
* How attention is distributed across score ranges.
* Which score corridors require intervention.

AnalyticsReport.Corridors does not provide:

* task-level analytics
* focus distribution by area
* strategic recommendations
* prioritization decisions

Those concerns belong to other analytics components.
---

## 6.2 SummaryAnalytics

### Purpose

SummaryAnalytics provides a concise executive overview of the board state.

It synthesizes findings produced by other analytics components and highlights the most important observations requiring attention.

SummaryAnalytics does not generate new analytics.

Instead, it aggregates and prioritizes insights generated by:

* FocusAttentionAnalytics
* TacticalAnalytics
* StrategicAnalytics
* DataQualityAnalytics

---

### Design Principle

```text
Focus
+
Tactical
+
Strategic
+
Data Quality
↓
Summary
```

SummaryAnalytics is an aggregation layer.

Its purpose is to answer:

```text
What matters most right now?
```

---

### Canonical Structure

```yaml
SummaryAnalytics:

  overall_assessment:

  key_findings:

  primary_risk:

  primary_opportunity:

  recommended_focus:
```

---

### overall_assessment

A concise high-level assessment of the current board state.

Typically expressed as a single sentence.

Example:

```text
Attention is concentrated on high-value work and corridor health is within target ranges.
```

---

### key_findings

List of the most important observations identified by the analytics system.

Recommended range:

```text
2-5 findings
```

Examples:

```text
- 63% of active attention is concentrated in Projects/AI.
- Corridor 21-25 is operating within target range.
- Health-related work receives only 8% of active attention.
```

---

### primary_risk

The single most important risk currently affecting execution or value delivery.

Examples:

```text
High-value overdue score is accumulating in corridor 16-20.
```

```text
Attention is heavily concentrated in one area, creating portfolio imbalance.
```

---

### primary_opportunity

The highest-value opportunity currently available.

Examples:

```text
Completing two tasks in corridor 21-25 would unlock 46 score points.
```

```text
Resolving a small overdue backlog would restore corridor health.
```

---

### recommended_focus

The primary recommendation generated from the report.

Recommended Focus should describe where attention should be directed next.

Examples:

```text
Maintain focus on Projects/AI and reduce overdue workload in corridor 16-20.
```

```text
Increase attention allocation to Health-related work during the next planning cycle.
```

---

### Responsibility

SummaryAnalytics answers:

* What is the current overall situation?
* What findings are most important?
* What is the primary risk?
* What is the primary opportunity?
* Where should attention be directed next?

SummaryAnalytics does not provide:

* raw metrics
* corridor calculations
* score calculations
* attention calculations

Those responsibilities belong to specialized analytics components.

---

### Design Principle

SummaryAnalytics is designed for rapid report consumption.

A reader should be able to understand the most important conclusions of the report by reading SummaryAnalytics before reviewing detailed analytical sections.


---

## 6.3. CorridorAnalytics

### Purpose

CorridorAnalytics represents analytics for a single score corridor.

Its purpose is to provide a complete analytical view of:

* workload
* value concentration
* attention allocation
* corridor health

CorridorAnalytics is the canonical analytics structure used by Corridor Analytics.

Each CorridorAnalytics object represents exactly one score corridor.

Examples:

```text
21-25
16-20
11-15
6-10
1-5
```

---

### Canonical Structure

```yaml
CorridorAnalytics:

  interval:

  workload:
    ...

  value:
    ...

  attention:
    ...

  health:
    ...
```

---

### 6.3.1 Interval

#### Purpose

Identifies the score corridor.

Examples:

```text
21-25
16-20
11-15
6-10
1-5
```

---

### 6.3.2 Workload

#### Purpose

Describes task counts within the corridor.

Answers:

* How many active tasks exist?
* How many overdue tasks exist?
* How many tasks have been completed?
* How many tasks have been archived?

---

#### Structure

```yaml
workload:

  active:
    5

  overdue:
    1

  completed:
    3

  archived:
    7
```

---

#### active

Number of active tasks within the corridor.

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

---

#### overdue

Number of overdue active tasks within the corridor.

---

#### completed

Number of completed non-archived tasks within the corridor.

---

#### archived

Number of archived tasks within the corridor.

---

### 6.3.3 Value

#### Purpose

Describes score value contained within the corridor.

Answers:

* How much score value exists?
* What percentage of board value does the corridor represent?
* What is the average score of tasks in the corridor?

---

#### Structure

```yaml
value:

  total_score:
    92

  average_score:
    23.0

  score_share_percentage:
    23.0
```

---

#### total_score

Sum of scores for all tasks within the corridor.

---

#### average_score

Average score of scored tasks within the corridor.

Formula:

```text
average_score =
total_score / scored_tasks
```

---

#### score_share_percentage

Percentage of total board score represented by the corridor.

Formula:

```text
corridor.total_score
/
board.total_score
× 100
```

Range:

```text
0.0 .. 100.0
```

---

### 6.3.4 Attention

#### Purpose

Describes how much corridor value is currently receiving attention.

Answers:

* How much score is active?
* How much score is overdue?
* How much value is currently at risk?

---

#### Structure

```yaml
attention:

  active_score:
    71

  overdue_score:
    24
```

---

#### active_score

Sum of scores of active tasks within the corridor.

Includes:

```text
[ ]
[/]
```

---

#### overdue_score

Sum of scores of overdue active tasks within the corridor.

---

### 6.3.5 Health

#### Purpose

Measures corridor status relative to configured targets.

Answers:

* Is the corridor underloaded?
* Is the corridor overloaded?
* Does the corridor satisfy target levels?

---

#### Structure

```yaml
health:

  target:

    min:
      3

    max:
      5

  delta:
    0

  state:
    ok
```

---

#### target

Target workload range loaded from:

```text
scoring.yaml
```

---

#### delta

Difference between actual workload and target workload.

Rules:

Within target:

```text
delta = 0
```

Below target:

```text
delta = active - target.min
```

Above target:

```text
delta = active - target.max
```

---

#### state

Supported values:

```text
ok
underloaded
overloaded
```

---

#### Design Principle

Health represents the relationship between:

```text
actual workload
vs
target workload
```

Health does not measure:

* value
* priority
* urgency
* execution quality

---

# 7. Recommendation Model

---

## Purpose

RecommendationCollection contains structured actions derived from analytics results.

Its purpose is to:

* improve board health
* maintain score corridor balance
* reduce execution overload
* reduce task debt
* improve execution quality
* support deterministic decision-making

Recommendations are generated from analytics results.

Recommendations are not analytics themselves.

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

RecommendationCollection must be generated only from:

* AnalyticsReport
* system configuration

The Recommendation Engine must not directly inspect raw task data.

---

## RecommendationCollection

Canonical structure:

```yaml
RecommendationCollection:
  - Recommendation
```

A RecommendationCollection may contain zero or more recommendations.

---

## Recommendation

Canonical structure:

```yaml
Recommendation:

  type:
    string

  priority:
    high | medium | low

  reason:
    string
```

### Fields

#### type

Recommendation category.

Examples:

```text
rebalance
overdue_cleanup
workload_reduction
focus_protection
```

Additional recommendation types may be added in future versions.

#### priority

Importance of recommendation.

Supported values:

```text
high
medium
low
```

#### reason

Machine-readable explanation for recommendation generation.

Examples:

```text
underloaded
overloaded
overdue_tasks
active_overload
```

---

## Rebalance Recommendation

### Purpose

Restore corridor targets defined in scoring.yaml.

### Structure

```yaml
type: rebalance

priority: high

corridor: "21-25"

action: increase

amount: 2

reason: underloaded
```

### Additional Fields

#### corridor

Affected score corridor.

Examples:

```text
21-25
16-20
11-15
6-10
1-5
```

#### action

Recommended operation.

Examples:

```text
increase
decrease
review
cleanup
protect
```

#### amount

Recommended quantity.

Represents the number of tasks affected.

Examples:

```text
2
5
10
```

---

### Underloaded Corridor

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

### Overloaded Corridor

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

## Model Boundary

The Recommendation Model defines recommendation structures only.

The following concerns are outside its scope:

* analytics calculations
* recommendation generation algorithms
* report formatting
* report rendering
* user interface behaviour

These responsibilities belong to other system components.




---


# 8. TacticalAnalytics

## Purpose

TacticalAnalytics evaluates execution conditions and identifies operational risks requiring intervention.

It focuses on execution health rather than value distribution, strategic alignment, or attention allocation.

TacticalAnalytics answers:

* Is the current workload sustainable?
* Does execution require intervention?
* Are there operational risks affecting delivery?
* Is the system operating within configured limits?

---

## Canonical Structure

```yaml
TacticalAnalytics:

  workload_health:
```

---

## Design Principle

TacticalAnalytics evaluates the operational condition of the execution system.

It focuses on:

```text
Execution State
vs
Target State
```

Unlike StrategicAnalytics, TacticalAnalytics does not evaluate long-term value allocation.

Unlike FocusAttentionAnalytics, TacticalAnalytics does not evaluate attention distribution.

Its responsibility is operational execution health.

---

## Responsibility

TacticalAnalytics answers:

* Is workload within target limits?
* Is the system overloaded?
* Is the system underloaded?
* Does execution require corrective action?

TacticalAnalytics does not provide:

* strategic portfolio analysis
* attention analysis
* corridor value analysis
* recommendation generation

Those concerns belong to other analytics components.

---

# 8.1 WorkloadHealth

## Purpose

WorkloadHealth evaluates whether the current active workload is within the configured operational limits.

It provides a board-level health assessment based on the number of active tasks.

---

## Canonical Structure

```yaml
WorkloadHealth:

  active_tasks:

  target:

    min:

    max:

  delta:

  state:
```

---

## Example

```yaml
WorkloadHealth:

  active_tasks:
    17

  target:

    min:
      15

    max:
      20

  delta:
    0

  state:
    ok
```

---

## active_tasks

Number of active tasks currently present on the board.

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

---

## target

Target active workload range.

Structure:

```yaml
target:

  min:

  max:
```

Target values must be loaded from system configuration.

Analytics engines must never use hardcoded target values.

---

## delta

Difference between actual workload and target workload.

Within target:

```text
delta = 0
```

Below target:

```text
delta = active_tasks - target.min
```

Above target:

```text
delta = active_tasks - target.max
```

---

## state

Supported values:

```text
ok
underloaded
overloaded
```

---

## Design Principle

WorkloadHealth measures:

```text
actual active workload
vs
target active workload
```

It does not measure:

* score value
* strategic importance
* attention allocation
* corridor health

Those concerns belong to other analytics components.

---

## Relationship to Corridor Health

WorkloadHealth operates at board level.

CorridorAnalytics.Health operates at corridor level.

Together they provide a hierarchical health model:

```text
Board
↓
WorkloadHealth

Corridor
↓
Health
```

Both components use the same principle:

```text
Actual State
vs
Target State
↓
Health Assessment
```
---

# 8.2 OverduePressure

## Purpose

OverduePressure evaluates the operational impact of overdue work.

It measures how much active workload is overdue and how much score value is currently at risk.

OverduePressure is a tactical execution metric.

---

## Canonical Structure

```yaml
OverduePressure:

  overdue_tasks:

  overdue_percentage:

  overdue_score:

  state:
```

---

## Example

```yaml id="5n1b5v"
OverduePressure:

  overdue_tasks:
    4

  overdue_percentage:
    23.5

  overdue_score:
    68

  state:
    elevated
```

---

## overdue_tasks

Number of overdue active tasks.

Includes only active tasks whose due date has passed.

Formula:

```text id="v9fzkj"
due < today
```

---

## overdue_percentage

Percentage of active tasks that are overdue.

Formula:

```text id="rt8d7s"
overdue_tasks
/
active_tasks
× 100
```

Range:

```text id="hv1kxu"
0.0 .. 100.0
```

---

## overdue_score

Sum of scores of overdue active tasks.

Purpose:

Measure the amount of value currently affected by overdue execution.

Formula:

```text id="9a9ckq"
Σ score
for all overdue active tasks
```

---

## state

Operational pressure level.

Supported values:

```text id="e7mbv4"
none
low
elevated
critical
```

---

## State Evaluation

No overdue work:

```text id="lh9q2n"
none
```

Minor overdue pressure:

```text id="g22ibz"
low
```

Significant overdue pressure:

```text id="b1s3xg"
elevated
```

Immediate intervention required:

```text id="m0mjlwm"
critical
```

Exact threshold values are implementation-specific and may be configured separately.

---

## Design Principle

OverduePressure measures:

```text id="jtwx1y"
overdue workload
+
overdue value
↓
execution pressure
```

It does not measure:

* workload capacity
* strategic value allocation
* attention distribution
* corridor health

Those concerns belong to other analytics components.

---

## Relationship to WorkloadHealth

WorkloadHealth evaluates:

```text id="6v93r4"
How much work exists.
```

OverduePressure evaluates:

```text id="i5hzyx"
How much of that work is overdue.
```

Together they provide a tactical view of execution health:

```text id="0obc4g"
WorkloadHealth
+
OverduePressure
↓
Execution Health
```

---

## Responsibility

OverduePressure answers:

* How many active tasks are overdue?
* What percentage of active work is overdue?
* How much score value is affected?
* Does execution require intervention?

OverduePressure does not answer:

* where attention is allocated
* which areas receive focus
* strategic portfolio balance
* corridor distribution

Those responsibilities belong to other analytics components.

---

# 9. StrategicAnalytics

## Purpose

StrategicAnalytics evaluates long-term value allocation and portfolio composition.

It focuses on how value is distributed across the system rather than how work is currently executed.

StrategicAnalytics answers:

* Where is value concentrated?
* How balanced is the portfolio?
* Are strategic areas receiving proportional investment?
* Is value excessively concentrated in a small number of areas?

---

## Canonical Structure

```yaml
StrategicAnalytics:

  value_concentration:

  portfolio_balance:
```

---

## Design Principle

StrategicAnalytics evaluates:

```text
Value Distribution
↓
Portfolio Structure
↓
Strategic Balance
```

Unlike TacticalAnalytics, StrategicAnalytics does not evaluate execution conditions.

Unlike FocusAttentionAnalytics, StrategicAnalytics does not evaluate current attention allocation.

Its responsibility is strategic portfolio analysis.

---

## Responsibility

StrategicAnalytics answers:

* Where value is concentrated.
* How value is distributed.
* Whether the portfolio is balanced.
* Whether strategic concentration risks exist.

StrategicAnalytics does not provide:

* execution health
* overdue analysis
* attention analysis
* recommendations

Those concerns belong to other analytics components.

# 9.1 ValueConcentration

## Purpose

ValueConcentration measures how score value is distributed across score corridors.

Its purpose is to identify whether value is concentrated in a small number of corridors or distributed across the portfolio.

---

## Canonical Structure

```yaml
ValueConcentration:

  dominant_corridor:

  dominant_share_percentage:

  top_corridors_share_percentage:
```

---

## Example

```yaml
ValueConcentration:

  dominant_corridor:
    21-25

  dominant_share_percentage:
    42.7

  top_corridors_share_percentage:
    71.3
```

---

## dominant_corridor

Corridor containing the largest share of total board score.

Example:

```text
21-25
```

---

## dominant_share_percentage

Percentage of total board score contained within the dominant corridor.

Formula:

```text
dominant_corridor.total_score
/
board.total_score
× 100
```

Range:

```text
0.0 .. 100.0
```

---

## top_corridors_share_percentage

Combined percentage of total board score contained within the top two highest-value corridors.

Formula:

```text
(top_corridor.total_score
+
second_corridor.total_score)
/
board.total_score
× 100
```

Range:

```text
0.0 .. 100.0
```

---

## Design Principle

ValueConcentration measures:

```text
Score Value
↓
Corridor Distribution
↓
Concentration
```

It does not measure:

* execution health
* overdue pressure
* attention allocation
* area distribution

---

## Responsibility

ValueConcentration answers:

* Which corridor contains the most value?
* How concentrated is value across corridors?
* Is value concentrated in a small number of score ranges?

# 9.2 PortfolioBalance

## Purpose

PortfolioBalance evaluates how score value is distributed across Areas.

Its purpose is to identify strategic concentration and portfolio imbalance.

---

## Canonical Structure

```yaml
PortfolioBalance:

  dominant_area:

  dominant_area_share_percentage:

  active_areas:

  balance_state:
```

---

## Example

```yaml
PortfolioBalance:

  dominant_area:
    Projects/AI

  dominant_area_share_percentage:
    58.2

  active_areas:
    5

  balance_state:
    concentrated
```

---

## dominant_area

Area containing the largest share of total board score.

Area determination should use:

```text
semantic_area
```

When semantic classification is unavailable:

```text
tags_area
```

may be used as a fallback.

---

## dominant_area_share_percentage

Percentage of total board score contained within the dominant area.

Formula:

```text
dominant_area.total_score
/
board.total_score
× 100
```

Range:

```text
0.0 .. 100.0
```

---

## active_areas

Number of areas containing at least one scored task.

Formula:

```text
count(area.total_score > 0)
```

---

## balance_state

Portfolio balance classification.

Supported values:

```text
balanced
concentrated
highly_concentrated
```

Thresholds are implementation-specific and may be configured separately.

---

## Design Principle

PortfolioBalance measures:

```text
Score Value
↓
Area Distribution
↓
Portfolio Balance
```

It does not measure:

* workload
* execution health
* overdue pressure
* current attention allocation

---

## Responsibility

PortfolioBalance answers:

* Which area contains the most value?
* How concentrated is value across areas?
* How many areas contain meaningful value?
* Is the portfolio balanced?


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

# 13. CorridorAnalytics


CorridorAnalytics is immutable.

Each CorridorAnalytics object represents exactly one score corridor.

CorridorAnalytics is the canonical output structure for corridor-level analytics.

---

## Canonical Structure

```yaml
CorridorAnalytics:

  interval:

  workload:
    ...

  value:
    ...

  attention:
    ...

  health:
    ...
```

---

## interval

Corridor identifier.

Examples:

```text
21-25
16-20
11-15
6-10
1-5
```

---

## workload

Workload metrics for the corridor.

Structure:

```yaml
workload:

  active:
    integer

  overdue:
    integer

  completed:
    integer

  archived:
    integer
```

---

## value

Value metrics for the corridor.

Structure:

```yaml
value:

  total_score:
    integer

  average_score:
    float

  score_share_percentage:
    float
```

---

## attention

Attention metrics for the corridor.

Structure:

```yaml
attention:

  active_score:
    integer

  overdue_score:
    integer
```

---

## health

Health metrics for the corridor.

Structure:

```yaml
health:

  target:

    min:
      integer

    max:
      integer

  delta:
    integer

  state:
    string
```

---

## Health State

Supported values:

```text
ok
underloaded
overloaded
```

---

## Health Target

Target values must be loaded from:

```text
scoring.yaml
```

Analytics engines must never use hardcoded target values.

---

## Health Delta

Within target:

```text
delta = 0
```

Below target:

```text
delta = active - target.min
```

Above target:

```text
delta = active - target.max
```

---

## Design Principle

CorridorAnalytics combines four analytical perspectives:

```text
workload
↓
value
↓
attention
↓
health
```

Each perspective answers a different management question.

Together they provide a complete analytical representation of a score corridor.

---

# 14. Analytics Lifecycle

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

---

# 15. Report Renderer

## Purpose

Report Renderer is responsible for transforming an AnalyticsReport into a human-readable report.

It serves as the presentation layer of the analytics system.

Report Renderer consumes analytical artifacts and produces structured output suitable for human review.

---

## Canonical Structure

```yaml
ReportRenderer:

  render(
    AnalyticsReport
  ) -> Report
```

---

## Input

Input:

```text
AnalyticsReport
```

Report Renderer consumes analytical results only.

It must not access tasks directly.

```text
Task[]
↓
Analytics Engine
↓
AnalyticsReport
↓
Report Renderer
```

---

## Output

Output:

```text
Report
```

Examples:

* Markdown Report
* Daily Review Report
* Weekly Review Report
* Executive Summary
* Dashboard View

The output format is implementation-specific.

---

## Rendering Pipeline

```text
AnalyticsReport
↓
Section Rendering
↓
Report Composition
↓
Final Report
```

---

## Section Renderers

Report Renderer may contain specialized section renderers.

Examples:

```yaml
FocusRenderer

TacticalRenderer

StrategicRenderer

CorridorRenderer

SummaryRenderer
```

Each renderer is responsible for presenting a specific analytical component.

---

## Rendering Rules

Report Renderer must preserve analytical meaning.

It may:

* reorder presentation elements
* format tables
* generate headings
* generate summaries
* apply templates

It must not:

* modify analytical measurements
* alter calculated values
* generate new analytics
* recalculate metrics

---

## Presentation Independence

AnalyticsReport must remain independent from presentation concerns.

Analytics components must not contain:

* markdown formatting
* HTML formatting
* visual templates
* report-specific structures

Presentation concerns belong exclusively to Report Renderer.

---

## Design Principle

Analytics and presentation are separate concerns.

```text
Analytics Engine
↓
AnalyticsReport
↓
Report Renderer
↓
Human-Readable Report
```

Analytics Engine produces facts.

Report Renderer presents facts.

---

## Multiple Presentation Formats

A single AnalyticsReport may be rendered in multiple formats.

Example:

```text
AnalyticsReport
├── Markdown Report
├── Daily Review
├── Weekly Review
├── Dashboard View
└── Executive Summary
```

The analytical result remains identical regardless of presentation format.

---

## Deterministic Rendering

Report rendering should be deterministic.

The same AnalyticsReport should produce the same report output when rendered using the same template.

```text
Same AnalyticsReport
+
Same Template
↓
Same Report
```

---

## Responsibility

Report Renderer is responsible for:

* report composition
* section rendering
* presentation formatting
* template application
* output generation

Report Renderer is not responsible for:

* analytics calculation
* task processing
* recommendation generation
* task modification

Those responsibilities belong to other system components.

---

## Dependency Rules

Allowed dependency direction:

```text
AnalyticsReport
↓
Report Renderer
↓
Report
```

Analytics components must not depend on Report Renderer.

Report Renderer depends on AnalyticsReport but AnalyticsReport must remain presentation-independent.

---

## Position in System Architecture

```text
Task[]
↓
Analytics Engine
↓
AnalyticsReport
↓
Report Renderer
↓
Report
```

Report Renderer is the canonical presentation layer of the analytics subsystem.



---

# 16. Canonical Report Template

## Purpose

Canonical Report Template defines the standard structure of the report produced by Analytics Engine and rendered for Morning Review.

The template is designed to support daily decision-making rather than expose internal analytical models.

---

## Design Principle

The report should answer three fundamental questions:

```text
What is happening?

What requires attention?

What should be done next?
```

The report progresses from observation to decision.

```text
Board State
↓
Analysis
↓
Focus
↓
Actions
↓
Readiness
```

---

## Canonical Structure

```yaml
AnalyticsReport:

  generated_at:

  executive_summary:

  board_snapshot:

  attention_analysis:

  tactical_analysis:

  strategic_analysis:

  daily_focus:

  maintenance_actions:

  prepared_board:
```

---

## 16.1 Executive Summary

### Purpose

Provides a concise overview of the most important findings.

This section should allow the user to understand the current situation within seconds.

---

### Questions Answered

```text
What is important right now?

What requires immediate attention?
```

---

### Typical Content

* major attention shifts
* critical findings
* workload warnings
* strategic concerns
* notable improvements

---

## 16.2 Board Snapshot

### Purpose

Provides an objective view of the current board state.

This section focuses on measurable system indicators.

---

### Questions Answered

```text
What does the board currently look like?
```

---

### Typical Content

* task counts
* area distribution
* corridor distribution
* active workload
* due task statistics
* health indicators

---

## 16.3 Attention Analysis

### Purpose

Evaluates how attention is currently distributed across Areas.

---

### Questions Answered

```text
Where is attention concentrated?

Which Areas receive insufficient attention?

Does attention align with priorities?
```

---

### Source Analytics

* Attention Snapshot
* Alignment Assessment
* Concentration Assessment

---

## 16.4 Tactical Analysis

### Purpose

Evaluates operational execution risks.

---

### Questions Answered

```text
What operational problems require attention?

Are there signs of overload?

Are important tasks stalled?
```

---

### Source Analytics

* Workload Assessment
* Stagnation Assessment
* Priority Assessment

---

## 16.5 Strategic Analysis

### Purpose

Evaluates long-term portfolio health and strategic balance.

---

### Questions Answered

```text
Are strategic priorities reflected in execution?

Is value concentrated appropriately?

Is the portfolio balanced?
```

---

### Source Analytics

* Value Concentration
* Portfolio Balance

---

## 16.6 Daily Focus

### Purpose

Defines the primary object of attention for the current day.

---

### Questions Answered

```text
What is the most important focus today?
```

---

### Source Analytics

* Daily Focus

---

### Output

```yaml
DailyFocus:

  focus_type:

  target:

  rationale:
```

---

## 16.7 Maintenance Actions

### Purpose

Defines corrective actions required before or during execution.

---

### Questions Answered

```text
What should be fixed?

What maintenance work is required?
```

---

### Source Analytics

* Maintenance Actions

---

### Typical Actions

* Classify Tasks
* Process Inbox
* Reschedule Tasks
* Reduce Workload
* Balance Corridors

---

## 16.8 Prepared Board Status

### Purpose

Determines whether the board is ready for execution.

---

### Questions Answered

```text
Is the system ready for execution?

Can work begin immediately?
```

---

### Source Analytics

* Prepared Board

---

### Output

```yaml
PreparedBoard:

  readiness_status:

  readiness_checks:

  daily_focus:
```

---

## Report Flow

```text
Executive Summary
↓
Board Snapshot
↓
Attention Analysis
↓
Tactical Analysis
↓
Strategic Analysis
↓
Daily Focus
↓
Maintenance Actions
↓
Prepared Board Status
```

---

## Design Principle

The report should guide decisions rather than present raw analytics.

Each section should contribute to a transition from observation to action.

```text
Observe
↓
Understand
↓
Focus
↓
Act
```


---

# 17. Morning Review

### Purpose

Morning Review is the primary daily management ritual of the Kanban Execution System.

It transforms analytical information into execution awareness and helps establish intentional focus for the day.

Morning Review consumes AnalyticsReport and presents the most relevant information required for daily decision-making.

---

### Objectives

Morning Review should help answer:

- What deserves attention today?
- Where is execution risk increasing?
- Which areas require intervention?
- Is current attention aligned with priorities?
- What should be actively advanced today?

---

### Position in System Architecture

```text
Kanban Board
↓
Analytics Engine
↓
AnalyticsReport
↓
Morning Review
↓
Daily Execution
```

Morning Review serves as the bridge between analytics and execution.

---

### Canonical Structure

```yaml
MorningReview:

  summary:

  focus:

  execution:

  strategic:

  observations:
```

---

## 17.1 Inputs

### Purpose

Defines the information sources used during Morning Review.

---

### Canonical Structure

```yaml
MorningReviewInputs:

  analytics_report:

  board_metrics:

  generated_at:
```

---

### Design Principle

Morning Review should consume analytical outputs rather than raw task data.

```text
Tasks
↓
Analytics Engine
↓
AnalyticsReport
↓
Morning Review
```

---
## 17.2 Review Questions

### Purpose

Review Questions define the canonical questions that Morning Review must answer.

Morning Review exists to transform analytical data into execution awareness.

All analytical components should contribute to answering one or more review questions.

---

### Focus Questions

#### Q1. Where is my attention currently concentrated?

```text
На каких областях сейчас сосредоточено моё внимание?
```

Purpose:

Determine the current distribution of attention across Areas.

Primary Source:

```text
FocusAttentionAnalytics.Distribution
```

---

#### Q2. Is my attention aligned with my priorities?

```text
Соответствует ли текущее распределение внимания моим приоритетам?
```

Purpose:

Evaluate whether actual attention allocation matches intended priorities.

Primary Source:

```text
FocusAttentionAnalytics.Alignment
```

---

#### Q3. Is my attention fragmented across too many areas?

```text
Не распылено ли моё внимание между слишком большим количеством направлений?
```

Purpose:

Evaluate focus concentration and context-switching risk.

Primary Source:

```text
FocusAttentionAnalytics.Concentration
```

---

### Execution Questions

#### Q4. Are there signs of execution overload?

```text
Есть ли признаки перегруза в текущем объёме работы?
```

Purpose:

Evaluate workload sustainability and execution health.

Primary Source:

```text
TacticalAnalytics.WorkloadHealth
```

---

#### Q5. Are any critical tasks stagnating?

```text
Есть ли критически важные задачи без движения?
```

Purpose:

Detect high-value tasks that are not progressing.

Primary Source:

```text
TacticalAnalytics.OverduePressure
```

---

### Priority Questions

#### Q6. Am I spending too much effort on low-priority work?

```text
Не трачу ли я слишком много ресурсов на низкоприоритетные задачи?
```

Purpose:

Evaluate the quality of attention allocation across score corridors.

Primary Source:

```text
CorridorAnalytics
```

---

### Daily Focus Question

#### Q7. What should be the primary object of attention today?

```text
Что является главным объектом внимания сегодня?
```

Purpose:

Identify the most important area, corridor, or execution focus for the current day.

Primary Source:

```text
AnalyticsReport
```

This question represents the final outcome of Morning Review.

---

### Design Principle

Questions should be answered in the following order:

```text
Attention
↓
Alignment
↓
Concentration
↓
Workload
↓
Stagnation
↓
Priority Quality
↓
Today's Focus
```

The sequence moves from awareness toward execution focus.

---

### Responsibility

Review Questions define:

* what Morning Review must answer
* why analytics are generated
* how analytical outputs are interpreted

They do not define:

* recommendations
* execution decisions
* task selection

Those responsibilities belong to future system components.

---

## 17.3 Review Structure

### Purpose

Review Structure defines the canonical sequence of Morning Review.

The structure guides the user from situational awareness toward daily execution focus.

---

### Design Principle

Morning Review should answer questions in a progressively narrowing sequence.

```text
Awareness
↓
Alignment
↓
Execution Health
↓
Priority Quality
↓
Today's Focus
```

The review begins with understanding the current state and ends with identifying the primary focus of the day.

---

### Canonical Structure

```text
1. Attention Review

2. Alignment Review

3. Concentration Review

4. Execution Health Review

5. Stagnation Review

6. Priority Review

7. Daily Focus
```

---

### Phase 1. Attention Review

Question:

```text
Where is my attention currently concentrated?
```

Purpose:

Establish awareness of current attention allocation across Areas.

Primary Source:

```text
FocusAttentionAnalytics.Distribution
```

---

### Phase 2. Alignment Review

Question:

```text
Is my attention aligned with my priorities?
```

Purpose:

Determine whether actual effort matches intended priorities.

Primary Source:

```text
FocusAttentionAnalytics.Alignment
```

---

### Phase 3. Concentration Review

Question:

```text
Is my attention fragmented across too many areas?
```

Purpose:

Evaluate focus concentration and context-switching risk.

Primary Source:

```text
FocusAttentionAnalytics.Concentration
```

---

### Phase 4. Execution Health Review

Question:

```text
Are there signs of execution overload?
```

Purpose:

Evaluate sustainability of the current workload.

Primary Source:

```text
TacticalAnalytics.WorkloadHealth
```

---

### Phase 5. Stagnation Review

Question:

```text
Are any critical tasks stagnating?
```

Purpose:

Identify important tasks that are not progressing.

Primary Source:

```text
TacticalAnalytics.OverduePressure
```

---

### Phase 6. Priority Review

Question:

```text
Am I spending too much effort on low-priority work?
```

Purpose:

Evaluate the quality of attention allocation across score corridors.

Primary Source:

```text
CorridorAnalytics
```

---

### Phase 7. Daily Focus

Question:

```text
What should be the primary object of attention today?
```

Purpose:

Identify the most important focus for the current day.

Primary Source:

```text
AnalyticsReport
```

This phase represents the final outcome of Morning Review.

---

### Review Outcome

The expected outcome of Morning Review is:

```text
Awareness
+
Alignment
+
Execution Context
+
Daily Focus
```

The review should conclude with a clear understanding of where attention should be directed during the day.

---

### Deterministic Structure

The same AnalyticsReport should produce the same Morning Review structure.

The sequence of review phases must remain stable regardless of report content.


---

## 17.4 Review Outputs

### Purpose

Review Outputs define the canonical outputs produced by Morning Review.

Each output corresponds to a specific review phase and answers a specific review question.

Together they form the MorningReviewOutput contract.

---

### Canonical Structure

```yaml
MorningReviewOutput:

  attention_snapshot:

  alignment_assessment:

  concentration_assessment:

  workload_assessment:

  stagnation_assessment:

  priority_assessment:

  daily_focus:
```

---

#### Attention Snapshot

##### Purpose

Provides a summary of current attention allocation across Areas.

Answers:

```text
Where is my attention currently concentrated?
```

##### Primary Sources

```text
FocusAttentionAnalytics.Distribution
```

##### Output Format

```yaml
AttentionSnapshot:

  top_areas:

  attention_distribution:

  dominant_area:
```

---

#### Alignment Assessment

##### Purpose

Evaluates whether actual attention allocation matches intended priorities.

Answers:

```text
Is my attention aligned with my priorities?
```

##### Primary Sources

```text
FocusAttentionAnalytics.Alignment
```

##### Output Format

```yaml
AlignmentAssessment:

  alignment_score:

  status:

  observations:
```

---

#### Concentration Assessment

#### Purpose

Evaluates focus concentration and context-switching pressure.

Answers:

```text
Is my attention fragmented across too many areas?
```

##### Primary Sources

```text
FocusAttentionAnalytics.Concentration
```

##### Output Format

```yaml
ConcentrationAssessment:

  active_areas:

  concentration_score:

  status:
```

---

#### Workload Assessment

##### Purpose

Evaluates current workload sustainability.

Answers:

```text
Are there signs of execution overload?
```

##### Primary Sources

```text
TacticalAnalytics.WorkloadHealth
```

##### Output Format

```yaml
WorkloadAssessment:

  active_tasks:

  workload_status:

  workload_score:
```

---

#### Stagnation Assessment

##### Purpose

Identifies critical tasks that are not progressing.

Answers:

```text
Are any critical tasks stagnating?
```

##### Primary Sources

```text
TacticalAnalytics.OverduePressure
```

##### Output Format

```yaml
StagnationAssessment:

  affected_tasks:

  pressure_score:

  status:
```

---

#### Priority Assessment

##### Purpose

Evaluates whether attention is concentrated in the appropriate score corridors.

Answers:

```text
Am I spending too much effort on low-priority work?
```

##### Primary Sources

```text
CorridorAnalytics
```

##### Output Format

```yaml
PriorityAssessment:

  high_value_share:

  low_value_share:

  status:
```

---

#### Daily Focus

##### Purpose

Identifies the primary object of attention for the current day.

Answers:

```text
What should be the primary object of attention today?
```

##### Primary Sources

```text
AttentionSnapshot

AlignmentAssessment

ConcentrationAssessment

WorkloadAssessment

StagnationAssessment

PriorityAssessment
```

##### Output Format

```yaml
DailyFocus:

  area:

  rationale:

  supporting_observations:
```

---

### Design Principle

Each review phase produces a single assessment.

The final Daily Focus is derived from the combined interpretation of all preceding assessments.

```text
Attention Snapshot
↓
Alignment Assessment
↓
Concentration Assessment
↓
Workload Assessment
↓
Stagnation Assessment
↓
Priority Assessment
↓
Daily Focus
```

---

### Responsibility

MorningReviewOutput defines:

* review results
* assessment outputs
* daily focus determination

It does not define:

* recommendations
* task selection
* execution planning

Those responsibilities belong to future system components.

---

## 17.4.1 Daily Focus

### Purpose

Daily Focus represents the primary object of attention for the current day.

It is the final outcome of Morning Review and serves as the bridge between analysis and execution.

All preceding review phases contribute to determining Daily Focus.

---

### Canonical Structure

```yaml
DailyFocus:

  focus_type:

  target:

  rationale:

  supporting_signals:
```

---

### Design Principle

Morning Review should reduce uncertainty and produce a clear focus for the day.

```text
Analytics
↓
Assessment
↓
Daily Focus
↓
Execution
```

---

### Responsibility

Daily Focus defines:

- what deserves attention today
- where execution effort should be concentrated
- why this focus was selected

It does not define:

- specific recommendations
- execution plans
- maintenance actions

---

### 17.4.1.1 Focus Types

#### Purpose

Defines the canonical types of Daily Focus.

Different situations may require attention at different levels of the system.

---

#### Area Focus

```yaml
focus_type: AREA
```

Examples:

```text
Health

Learning

Projects

Family
```

Use when a specific Area requires concentrated attention.

---

#### Corridor Focus

```yaml
focus_type: CORRIDOR
```

Examples:

```text
21-25

16-20
```

Use when attention should be directed toward a specific score corridor.

---

#### Task Focus

```yaml
focus_type: TASK
```

Example:

```text
Complete Quarterly Planning
```

Use when a single task dominates execution importance.

---

#### Maintenance Focus

```yaml
focus_type: MAINTENANCE
```

Examples:

```text
Inbox Processing

Workload Reduction

Board Cleanup
```

Use when board maintenance should take precedence over task execution.

---

#### Portfolio Focus

```yaml
focus_type: PORTFOLIO
```

Examples:

```text
Restore Balance

Reduce Fragmentation

Increase Strategic Focus
```

Use when attention should be directed toward portfolio-level improvements.

---
### 17.4.1.2 Focus Determination

#### Purpose

Defines how Daily Focus is determined.

---

#### Inputs

Daily Focus may use signals from:

```text
Attention Snapshot

Alignment Assessment

Concentration Assessment

Workload Assessment

Stagnation Assessment

Priority Assessment
```

---

#### Determination Process

```text
Assessment Results
↓
Signal Aggregation
↓
Daily Focus
```

---

#### Design Principle

Daily Focus should be derived from analytical observations.

The determination process should remain deterministic.

The same analytical inputs should produce the same Daily Focus.

---

#### Future Evolution

Future versions may incorporate:

- Recommendation Engine
- LLM-based reasoning
- historical execution patterns

Such enhancements may improve focus selection without changing the Daily Focus contract.

---

### 17.4.1.3 Focus Rationale

#### Purpose

Explains why Daily Focus was selected.

---

#### Design Principle

Every Daily Focus should be explainable.

The user should be able to understand which observations contributed to the selected focus.

---

#### Canonical Structure

```yaml
FocusRationale:

  summary:

  supporting_signals:
```

---

#### Example

```yaml
DailyFocus:

  focus_type: AREA

  target: Projects

  rationale:
    High concentration of score 21-25 tasks.

  supporting_signals:

    - Alignment Gap

    - Critical Task Stagnation

    - Strategic Underinvestment
```

---

#### Responsibility

Focus Rationale defines:

- why focus was selected
- which signals influenced the decision
- how analytical results are connected to execution focus

It does not define:

- recommendations
- execution strategy
- task sequencing

---

## 17.5 Design Principles

### Purpose

Defines the governing principles of Morning Review.

---

### Principles

#### Action Orientation

Morning Review exists to improve execution.

---

#### Focus First

Focus-related information should be presented before operational details.

---

#### Strategic Awareness

Daily execution should remain connected to long-term priorities.

---

#### Progressive Disclosure

Present:

```text
Conclusions
↓
Observations
↓
Details
```

---

#### Deterministic Review

The same AnalyticsReport should produce the same Morning Review structure.

---

#### Analytics Before Recommendations

Morning Review is based on analytical observations.

Recommendations may be added by future system components but are not required for the review itself.

---

## 17.6 Review Lifecycle

### Purpose

Review Lifecycle defines the canonical execution flow of Morning Review.

Morning Review is not limited to analytical assessment.

It also includes board maintenance activities required to prepare the system for effective daily execution.

---

### Design Principle

Morning Review consists of two sequential phases.

```text
Assessment
↓
Maintenance
↓
Daily Execution
```

The board should first be understood and only then modified.

---

### Canonical Lifecycle

```text
1. Assessment

2. Maintenance

3. Daily Execution
```

---

#### Phase 1. Assessment

##### Purpose

Assessment establishes situational awareness.

The goal is to understand the current state of execution before making any changes.

---

##### Inputs

```text
AnalyticsReport
```

---

##### Activities

```text
Attention Review

Alignment Review

Concentration Review

Execution Health Review

Stagnation Review

Priority Review

Daily Focus Identification
```

---

##### Outputs

```text
MorningReviewOutput
```

Including:

```text
Attention Snapshot

Alignment Assessment

Concentration Assessment

Workload Assessment

Stagnation Assessment

Priority Assessment

Daily Focus
```

---

##### Design Principle

Assessment should answer questions.

Assessment should not modify the board.

---

#### Phase 2. Maintenance

##### Purpose

Maintenance prepares the board for effective execution.

The goal is to reduce ambiguity, restore structure, and ensure that work is correctly organized before the day begins.

---

##### Typical Activities

###### Inbox Processing

Classify new tasks.

```text
Inbox
↓
Area Assignment
↓
Priority Assignment
↓
Score Assignment
```

---

###### Task Classification

Ensure tasks belong to appropriate Areas.

Examples:

```text
Missing Tags

Incorrect Area

Unclassified Tasks
```

---

###### Task Rescheduling

Move tasks that are no longer relevant for the current day.

Examples:

```text
Overloaded Day

Expired Schedule

Changed Priorities
```

---

###### Corridor Balancing

Review score corridor distribution.

Examples:

```text
Too many low-value tasks

Insufficient high-value tasks

Excessive corridor concentration
```

---

###### Workload Adjustment

Reduce excessive active work.

Examples:

```text
Pause Tasks

Defer Tasks

Reschedule Tasks
```

---

###### Board Cleanup

Remove structural inconsistencies.

Examples:

```text
Duplicate Tasks

Stale Tasks

Incomplete Metadata
```

---

##### Outputs

```text
Prepared Board
```

The board should be ready for focused daily execution.

---

#### Phase 3. Daily Execution

##### Purpose

Execute work using the understanding established during Assessment and the structure restored during Maintenance.

---

##### Inputs

```text
Prepared Board

Daily Focus
```

---

##### Outputs

```text
Task Progress

Task Completion

Board State Changes
```

---

### Lifecycle Summary

```text
Kanban Board
↓
Analytics Engine
↓
AnalyticsReport
↓

Assessment
↓
MorningReviewOutput
↓

Maintenance
↓
Prepared Board
↓

Daily Execution
```

---

### Future Evolution

Future versions may introduce automated assistance during the Maintenance phase.

Examples:

```text
Suggested Classification

Suggested Rescheduling

Suggested Corridor Balancing

Suggested Workload Reduction
```

Such capabilities remain optional and do not alter the canonical Morning Review lifecycle.

---

### Responsibility

Review Lifecycle defines:

* review phases
* review sequence
* maintenance responsibilities
* execution handoff

It does not define:

* recommendation generation
* task execution
* analytical calculations

Those responsibilities belong to other system components.

---

## 17.7 Maintenance Actions

### Purpose

Maintenance Actions represent the canonical actions produced during the Maintenance phase of Morning Review.

They provide a standardized mechanism for describing board modifications independently of how such modifications were identified.

Maintenance Actions may originate from:

- manual review
- deterministic analytics
- future recommendation engines
- future LLM-based assistants

---

### Design Principle

Maintenance Actions describe proposed changes to board state.

They do not perform modifications directly.

```text
Observation
↓
Maintenance Action
↓
Board Modification
```

---

### Canonical Structure

```yaml
MaintenanceAction:

  type:

  target:

  rationale:
```

---

### Fields

#### type

Defines the category of maintenance activity.

Example:

```text
CLASSIFY_TASK

RESCHEDULE_TASK

MOVE_TASK

UPDATE_PRIORITY
```

---

#### target

Identifies the object affected by the action.

Examples:

```text
Task

Area

Section

Score Corridor
```

---

#### rationale

Provides the reason for the action.

The rationale should be traceable to observations produced during Morning Review.

---

### Responsibility

MaintenanceAction defines:

- what should be changed
- where the change should occur
- why the change is required

It does not define:

- how the change is executed
- who executes the change
- whether the change is accepted

---

### 17.7.1 Maintenance Action Types

#### Purpose

Defines the canonical categories of maintenance activities supported by the system.

---

#### Task Classification

```text
CLASSIFY_TASK
```

Assign a task to an Area or Section.

Examples:

```text
Inbox
↓
Projects

Inbox
↓
Health
```

---

#### Task Relocation

```text
MOVE_TASK
```

Move a task between sections.

Examples:

```text
Backlog
↓
Doing

Doing
↓
Waiting
```

---

#### Task Rescheduling

```text
RESCHEDULE_TASK
```

Adjust planned execution date.

Examples:

```text
Today
↓
Tomorrow

This Week
↓
Next Week
```

---

#### Priority Adjustment

```text
UPDATE_PRIORITY
```

Modify task priority.

Examples:

```text
Priority 3
↓
Priority 5
```

---

#### Corridor Balancing

```text
BALANCE_CORRIDOR
```

Adjust portfolio composition across score corridors.

Examples:

```text
Reduce low-value tasks

Increase high-value tasks
```

---

#### Workload Reduction

```text
REDUCE_WORKLOAD
```

Decrease active work volume.

Examples:

```text
Pause Task

Defer Task

Archive Task
```

---

#### Board Cleanup

```text
CLEANUP_BOARD
```

Remove structural inconsistencies.

Examples:

```text
Duplicate Tasks

Incomplete Metadata

Obsolete Tasks
```

---

### 17.7.2 Maintenance Action Collection

#### Purpose

Defines the collection of maintenance actions produced during Morning Review.

---

#### Canonical Structure

```yaml
MaintenanceActionCollection:

  actions:
```

---

#### Design Principle

Multiple observations may generate multiple maintenance actions.

```text
Morning Review
↓
Observations
↓
Maintenance Actions
↓
Prepared Board
```

---

#### Example

```yaml
MaintenanceActionCollection:

  actions:

    - type: CLASSIFY_TASK
      target: "Implement API caching"
      rationale: "Task remains in Inbox"

    - type: RESCHEDULE_TASK
      target: "Prepare presentation"
      rationale: "Current day is overloaded"

    - type: REDUCE_WORKLOAD
      target: "Research alternatives"
      rationale: "Active task count exceeds target range"
```

---

#### Future Evolution

Future system components may automatically generate Maintenance Actions.

Examples:

```text
Recommendation Engine

LLM Assistant

Workflow Automation
```

All such components should produce actions using the same canonical contract.

---

#### Responsibility

MaintenanceActionCollection defines:

- maintenance outputs
- action aggregation
- action transport between system components

It does not define:

- action execution
- action prioritization
- action approval workflows

---

## 17.8 Prepared Board

### Purpose

Prepared Board represents the target board state produced by Morning Review.

It serves as the readiness contract between Morning Review and Daily Execution.

A board is considered prepared when the required readiness checks have been completed and the board is suitable for focused execution.

---

### Canonical Structure

```yaml
PreparedBoard:

  readiness_status:

  readiness_checks:

  daily_focus:
```

---

### Design Principle

Morning Review should not end with analysis.

Morning Review should end with a board that is ready for execution.

```text
Analytics
↓
Assessment
↓
Maintenance
↓
Prepared Board
↓
Daily Execution
```

---

### Responsibility

Prepared Board defines:

* execution readiness
* board quality
* maintenance completion

It does not define:

* task execution
* recommendations
* execution outcomes

### 17.8.1 Readiness Checks

#### Purpose

Readiness Checks define the validations used to determine whether a board is ready for daily execution.

Each check evaluates a specific aspect of board quality.

---

#### Canonical Structure

```yaml
ReadinessChecks:

  inbox:

  classification:

  workload:

  corridors:

  focus:
```

---

#### Inbox Check

Validates that incoming tasks have been reviewed.

Examples:

```text
Inbox Empty

Inbox Reviewed

Inbox Within Acceptable Range
```

---

#### Classification Check

Validates that tasks are assigned to appropriate Areas.

Examples:

```text
No Unclassified Tasks

Tags Present

Area Assigned
```

---

#### Workload Check

Validates that active workload remains within acceptable limits.

Examples:

```text
Active Tasks Within Target Range

No Excessive Overload
```

---

#### Corridor Check

Validates that score corridor distribution remains healthy.

Examples:

```text
Sufficient High-Value Tasks

No Excessive Low-Value Concentration
```

---

#### Focus Check

Validates that Daily Focus has been identified.

Examples:

```text
Daily Focus Defined

Focus Supported By Analytics
```

---

#### Design Principle

Readiness Checks evaluate board state.

They do not prescribe corrective actions.

### 17.8.2 Readiness Status

#### Purpose

Readiness Status represents the outcome of all readiness checks.

It determines whether the board is ready for execution.

---

#### Canonical Structure

```yaml
ReadinessStatus:

  overall_status:

  check_results:
```

---

#### Overall Status

Possible values:

```text
READY

WARNING

NOT_READY
```

---

#### READY

All critical readiness checks pass.

The board is suitable for daily execution.

---

#### WARNING

Execution may proceed, but one or more non-critical issues require attention.

Examples:

```text
Minor Inbox Backlog

Slight Workload Excess

Moderate Corridor Imbalance
```

---

#### NOT_READY

Critical readiness issues remain unresolved.

Examples:

```text
Large Inbox

Missing Classification

Severe Workload Overload

No Daily Focus
```

---

#### Design Principle

Readiness Status should provide a simple execution signal.

```text
READY
↓
Execute

WARNING
↓
Execute Carefully

NOT_READY
↓
Complete Maintenance First
```

### 17.8.3 Readiness Criteria

#### Purpose

Readiness Criteria define the rules used to evaluate each readiness check.

Thresholds may evolve over time without changing the Prepared Board model.

---

#### Inbox Criteria

```text
READY
Inbox Empty

WARNING
1-5 Tasks

NOT_READY
More Than 5 Tasks
```

---

#### Classification Criteria

```text
READY
All Tasks Classified

WARNING
Small Number Of Unclassified Tasks

NOT_READY
Significant Number Of Unclassified Tasks
```

---

#### Workload Criteria

```text
READY
Within Target Workload Range

WARNING
Moderate Overload

NOT_READY
Severe Overload
```

---

#### Corridor Criteria

```text
READY
Corridor Distribution Within Expected Ranges

WARNING
Moderate Corridor Imbalance

NOT_READY
Severe Corridor Imbalance
```

---

#### Focus Criteria

```text
READY
Daily Focus Identified

NOT_READY
Daily Focus Missing
```

---

#### Future Evolution

Future versions may introduce:

* configurable thresholds
* user-specific readiness profiles
* adaptive workload limits
* semantic readiness evaluation

Such enhancements should not alter the Prepared Board contract.

---

#### Design Principle

Criteria may evolve.

The meaning of Prepared Board should remain stable.


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


