---
created: 2026-06-06
updated: 2026-06-13T16:56
Description: |-
  Canonical analytics output model for the Kanban Execution System.

  This document defines:

  * analytics report structure
  * summary metrics
  * corridor analytics
  * status calculation rules
  * delta calculation rules
  * reporting invariants
---

# ANALYTICS MODEL V2


# 1. Purpose

* define deterministic analytics outputs
* separate analytics data from report presentation
* provide stable contracts for future parsers
* support dashboards, reports and automation
* ensure consistency across implementations


---

# 2. Core Principles

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

## 2.1 Decision-Oriented Analytics
## 2.2 Separation of Concerns
## 2.3 Traceability
## 2.4 Actionability

---

# 3 Analytics Domains

## Purpose

Analytics are organized into five decision domains.
Each domain answers a different class of questions.
Analytics should support decision-making rather than metric collection.

## Domain 1 — Focus Domain

Purpose:
What should be done today and within the next three days?

Questions:
Where is attention currently concentrated?
Which tasks should be moved into focus?
Which tasks may be safely deferred?
Which tasks provide the highest strategic value right now?
How many tasks are overdue, due today or due within the next three days?
What is the total score value of overdue and urgent tasks?

## Domain 2 — Tactical Domain

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

## Domain 3 — Strategic Domain

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

## Domain 4 — Data Quality Domain

Purpose:
Can the analytics be trusted?

Questions:
What percentage of tasks have no score?
What percentage of tasks have no estimate?
How complete is score coverage across total board value?


## Domain 5 — Corridor Domain

Purpose:
To be added

Questions:
To be added


## Design Principle

Analytics domains define:
why analytics exist

AnalyticsReport defines:
what is calculated

Report Renderer defines:
how analytics are presented

---

# 4. Analytics Architecture

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

ExecutiveSummary
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

## ExecutiveSummary

ExecutiveSummary synthesizes analytical findings.

Its purpose is to identify:

* important observations
* primary risks
* primary opportunities
* areas requiring attention

ExecutiveSummary may interpret measurements produced by analytics components.

---

## Recommendation Engine

Recommendation Engine generates actionable guidance.

Its purpose is to answer:

```text
What should be done next?
```

Recommendations may be derived from:

* ExecutiveSummary
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
→ ExecutiveSummary

Recommendation
→ Recommendation Engine
```

Each layer has a single responsibility and must not assume responsibilities belonging to other layers.

---

# 5. Analytics Processing Pipeline

## Purpose

Analytics Processing Pipeline defines the canonical sequence of analytical processing steps.

It describes how raw task data is transformed into an `AnalyticsReport`.

The pipeline ensures that analytics components are executed in a deterministic and reproducible order.

---

## Canonical Pipeline

```text
Tasks
↓
AnalyticsTaskSnapshot Generation
↓
Board Health Analysis
↓
Analytics Confidence Evaluation
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

  board_health_analysis

  analytics_confidence_evaluation

  focus_analysis

  tactical_analysis

  strategic_analysis

  corridor_analysis

  summary_generation

  report_assembly
```

---

## Step 1. Snapshot Generation

### Input

```text
Tasks
```

### Output

```text
AnalyticsTaskSnapshot[]
```

### Purpose

Normalize task data into a canonical analytical representation.

---

## Step 2. Board Health Analysis

### Input

```text
AnalyticsTaskSnapshot[]
```

### Output

```text
BoardHealth
```

### Purpose

Evaluate board metadata quality and analytical readiness.

### Calculated Metrics

* score_coverage
* tag_coverage
* analytics_coverage
* missing_score
* missing_tag
* orphan_tasks
* sample_orphans
* board_health_status

---

## Step 3. Analytics Confidence Evaluation

### Input

```text
BoardHealth
```

### Output

```text
AnalyticsConfidence
```

### Purpose

Derive a standardized analytical confidence level from BoardHealth.

AnalyticsConfidence provides a consistent reliability assessment for all analytical modules.

---

## Step 4. Focus Analysis

### Input

```text
AnalyticsTaskSnapshot[]
```

### Output

```text
FocusAttentionAnalytics
```

### Purpose

Calculate attention distribution, concentration, and alignment metrics.

---

## Step 5. Tactical Analysis

### Input

```text
AnalyticsTaskSnapshot[]
```

### Output

```text
TacticalAnalytics
```

### Purpose

Calculate execution-state and operational metrics.

### Examples

```text
WorkloadHealth
OverduePressure
```

---

## Step 6. Strategic Analysis

### Input

```text
AnalyticsTaskSnapshot[]
```

### Output

```text
StrategicAnalytics
```

### Purpose

Calculate portfolio-level and value-distribution metrics.

### Examples

```text
ValueConcentration
PortfolioBalance
```

---

## Step 7. Corridor Analysis

### Input

```text
AnalyticsTaskSnapshot[]
```

### Output

```text
CorridorAnalytics[]
```

### Purpose

Generate analytics for configured score corridors.

---

## Step 8. Summary Generation

### Input

```text
BoardHealth
AnalyticsConfidence
FocusAttentionAnalytics
TacticalAnalytics
StrategicAnalytics
CorridorAnalytics[]
```

### Output

```text
SummaryAnalytics
```

### Purpose

Synthesize analytical findings into a concise executive overview.

SummaryAnalytics interprets measurements generated by previous pipeline stages.

---

## Step 9. AnalyticsReport Assembly

### Input

```text
BoardHealth
AnalyticsConfidence
SummaryAnalytics
FocusAttentionAnalytics
TacticalAnalytics
StrategicAnalytics
CorridorAnalytics[]
```

### Output

```text
AnalyticsReport
```

### Purpose

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
  → BoardHealth
  → AnalyticsConfidence
  → FocusAttentionAnalytics
  → TacticalAnalytics
  → StrategicAnalytics
  → CorridorAnalytics

Interpretation
  → SummaryAnalytics

Report
  → AnalyticsReport
```

---

## Dependency Rules

Analytics components MUST NOT depend on SummaryAnalytics.

Allowed dependencies:

```text
AnalyticsTaskSnapshot
↓
BoardHealth

BoardHealth
↓
AnalyticsConfidence

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

It does NOT define:

* recommendation generation
* report rendering
* task parsing
* task editing

Those responsibilities belong to other system components.

---

# 6. Analytics Objects

---

## 6.1 Analytics Object Pattern

Analytics Objects are the fundamental analytical building blocks of the Analytics Engine.

Each Analytics Object evaluates a specific aspect of the system and produces a structured analytical result.

Analytics Objects must be:

- Decision-oriented
- Traceable to Task Model data
- Independently interpretable
- Reusable across reports and recommendations

### Canonical Structure

Every Analytics Object should define:

```yaml
AnalyticsObject:

  purpose:

  inputs:

  calculation:

  interpretation:
```

### Fields

#### purpose

Explains why the analytical object exists and what question it answers.

Example:

```yaml
purpose:
  Evaluate workload sustainability.
```

#### inputs

Defines which Task Model fields are used.

Example:

```yaml
inputs:
  - state
  - due_date
  - score
```

#### calculation

Describes the analytical logic used to produce the result.

Calculation may be:

- formula-based
- rule-based
- aggregation-based

Example:

```yaml
calculation:
  active_tasks / target_capacity
```

#### interpretation

Explains how the result should be understood.

Example:

```yaml
interpretation:
  High values indicate workload overload.
```

### Design Principle

Analytics Objects define analytical measurements and interpretations.

They do not generate recommendations.

Recommendations are produced by the Recommendation Engine using Analytics Objects and ExecutiveSummary as inputs.

---

## 6.2 Focus Analytics

Focus Analytics evaluate where attention should be directed.

Their purpose is to identify tasks, projects, and areas that deserve immediate or elevated attention.

Focus Analytics support prioritization decisions and help prevent attention fragmentation.

### Domain Question

```text
What deserves attention right now?
```

### Analytics Objects

Focus Analytics consist of:

- FocusAttentionAnalytics
- FocusUrgencyAnalytics
- FocusPriorityAnalytics

### Responsibilities

Focus Analytics may evaluate:

- concentration of attention
- urgency signals
- priority signals
- attention distribution
- attention fragmentation

### Design Principle

Focus Analytics determine where attention should be directed.

They do not evaluate execution performance, strategic alignment, or data quality.

Those responsibilities belong to Tactical, Strategic, and Data Quality Analytics respectively.

### Scope

Focus Analytics evaluate attention allocation, urgency, and priority.

They do not evaluate execution performance, strategic alignment, data quality, or recommendation generation.

---

### 6.2.1 FocusAttentionAnalytics

FocusAttentionAnalytics evaluates how attention is distributed across the system.

Its purpose is to identify concentration, fragmentation, and allocation of attention.

#### Domain Question

```text
Where is attention currently directed?
```

#### Purpose

Evaluate the current distribution of attention across tasks and projects.

#### Inputs

FocusAttentionAnalytics may use:

- task state
- task score
- project membership
- task priority
- task due date

#### Calculation

FocusAttentionAnalytics evaluates:

- attention concentration
- attention distribution
- attention fragmentation

Specific calculation methods are implementation-dependent.

#### Interpretation

High concentration indicates that attention is focused on a relatively small number of tasks or projects.

High fragmentation indicates that attention is spread across too many competing items.

Balanced distribution indicates sustainable attention allocation.

#### Possible Outputs

Examples:

```yaml
result:

  concentration_score: 0.72

  fragmentation_score: 0.18

  dominant_projects: 3
```

Output structure is implementation-dependent.

---

### 6.2.2 FocusUrgencyAnalytics

FocusUrgencyAnalytics evaluates time-sensitive pressure within the system.

Its purpose is to identify tasks and projects that require attention due to approaching deadlines, overdue status, or other urgency signals.

#### Domain Question

```text
What requires attention soon?
```

#### Purpose

Evaluate urgency pressure across tasks and projects.

#### Inputs

FocusUrgencyAnalytics may use:

- task state
- due date
- task priority
- task score

#### Calculation

FocusUrgencyAnalytics evaluates:

- urgency pressure
- overdue pressure
- deadline proximity
- concentration of urgent work

Specific calculation methods are implementation-dependent.

#### Interpretation

High urgency pressure indicates a growing concentration of time-sensitive work.

High overdue pressure indicates an accumulation of overdue tasks requiring attention.

Low urgency pressure indicates that deadlines and commitments remain manageable.

#### Possible Outputs

Examples:

```yaml
FocusUrgencyAnalytics:

  urgency_pressure_score: 0.81

  overdue_pressure_score: 0.34

  urgent_tasks: 7
```

Output structure is implementation-dependent.

---

### 6.2.3 FocusPriorityAnalytics

FocusPriorityAnalytics evaluates the relative importance of tasks and projects.

Its purpose is to identify where attention should be directed based on value, impact, and priority signals.

#### Domain Question

```text
What deserves attention first?
```

#### Purpose

Evaluate the relative importance of tasks and projects.

#### Inputs

FocusPriorityAnalytics may use:

- task priority
- task score
- project membership
- strategic alignment indicators

#### Calculation

FocusPriorityAnalytics evaluates:

- priority concentration
- priority distribution
- concentration of high-value work
- concentration of low-value work

Specific calculation methods are implementation-dependent.

#### Interpretation

High concentration of high-priority work indicates that a significant portion of the system's value is concentrated in a limited number of tasks or projects.

High concentration of low-priority work may indicate misallocation of attention and execution capacity.

Balanced priority distribution indicates that effort is aligned with expected value.

#### Possible Outputs

Examples:

```yaml
FocusPriorityAnalytics:

  high_priority_ratio: 0.42

  priority_concentration_score: 0.68

  high_value_projects: 4
```

Output structure is implementation-dependent.


---

## 6.3 Tactical Analytics

Tactical Analytics evaluate execution performance and operational health.

Their purpose is to assess how effectively work is progressing through the system and identify operational constraints that may impact execution.

### Domain Question

```text
How is execution progressing?
```

### Scope

Tactical Analytics evaluate execution performance, workload sustainability, operational bottlenecks, and delivery pressure.

They do not evaluate attention allocation, strategic alignment, data quality, or recommendation generation.

### Analytics Objects

Tactical Analytics consist of:

- WorkloadHealthAnalytics
- OverduePressureAnalytics
- ExecutionFlowAnalytics

### Responsibilities

Tactical Analytics may evaluate:

- workload sustainability
- execution capacity
- overdue work
- delivery pressure
- execution flow
- operational bottlenecks
- work accumulation

### Design Principle

Tactical Analytics determine how effectively work is being executed.

They focus on operational performance rather than attention allocation, strategic value, or data quality.

---

### 6.3.1 WorkloadHealthAnalytics

WorkloadHealthAnalytics evaluates the sustainability of the current workload.

Its purpose is to identify whether the volume and distribution of active work remain within healthy operational limits.

#### Domain Question

```text
Is the current workload sustainable?
```

#### Purpose

Evaluate the operational health of the workload and identify conditions that may lead to overload, inefficiency, or execution degradation.

#### Inputs

WorkloadHealthAnalytics may use:

- task state
- task score
- project membership
- active task count
- task estimates

#### Calculation

WorkloadHealthAnalytics evaluates:

- workload volume
- workload distribution
- concentration of active work
- work-in-progress pressure
- workload sustainability

Specific calculation methods are implementation-dependent.

#### Interpretation

Healthy workload conditions indicate that active work remains manageable and execution capacity is not significantly exceeded.

High workload pressure may indicate excessive work-in-progress, reduced focus, and increased execution risk.

Persistent overload may lead to delivery delays and reduced execution quality.

#### Possible Outputs

Examples:

```yaml
WorkloadHealthAnalytics:

  workload_health_score: 0.74

  active_tasks: 18

  work_in_progress_pressure: 0.63
```

Output structure is implementation-dependent.


---

### 6.3.2 OverduePressureAnalytics

OverduePressureAnalytics evaluates the accumulation of overdue work and deadline-related execution pressure.

Its purpose is to identify situations where commitments are being missed or where approaching deadlines create increasing execution risk.

#### Domain Question

```text
Are commitments being missed?
```

#### Purpose

Evaluate deadline pressure and the accumulation of overdue work within the system.

#### Inputs

OverduePressureAnalytics may use:

- task state
- due date
- task score
- project membership

#### Calculation

OverduePressureAnalytics evaluates:

- overdue task accumulation
- overdue work concentration
- deadline pressure
- overdue trend
- commitment pressure

Specific calculation methods are implementation-dependent.

#### Interpretation

Low overdue pressure indicates that commitments are generally being fulfilled within expected timeframes.

Elevated overdue pressure indicates growing execution risk and increasing difficulty in meeting commitments.

Persistent overdue accumulation may indicate structural execution problems requiring attention.

#### Possible Outputs

Examples:

```yaml
OverduePressureAnalytics:

  overdue_pressure_score: 0.58

  overdue_tasks: 12

  overdue_ratio: 0.21
```

Output structure is implementation-dependent.

---

### 6.3.3 ExecutionFlowAnalytics

ExecutionFlowAnalytics evaluates how effectively work progresses through the system.

Its purpose is to identify flow efficiency, execution bottlenecks, and accumulation of work within operational states.

#### Domain Question

```text
Is work moving through the system effectively?
```

#### Purpose

Evaluate the movement of work through the system and identify constraints that may reduce execution effectiveness.

#### Inputs

ExecutionFlowAnalytics may use:

- task state
- task age
- task estimates
- project membership

#### Calculation

ExecutionFlowAnalytics evaluates:

- flow efficiency
- work accumulation
- state distribution
- execution bottlenecks
- flow stability

Specific calculation methods are implementation-dependent.

#### Interpretation

Healthy execution flow indicates that work progresses through operational states without significant accumulation or blockage.

Work accumulation in specific states may indicate execution bottlenecks and reduced delivery effectiveness.

Persistent flow instability may indicate structural process issues requiring attention.

#### Possible Outputs

Examples:

```yaml
ExecutionFlowAnalytics:

  flow_efficiency_score: 0.77

  bottleneck_states: 2

  flow_stability_score: 0.69
```

Output structure is implementation-dependent.

---

## 6.4 Strategic Analytics

Strategic Analytics evaluate the long-term allocation of effort and value creation within the system.

Their purpose is to assess whether work is aligned with strategic objectives and whether resources are being invested in the most valuable areas.

### Domain Question

```text
Are we investing effort in the right things?
```

### Scope

Strategic Analytics evaluate strategic alignment, investment distribution, portfolio composition, and long-term value creation.

They do not evaluate attention allocation, execution performance, data quality, or recommendation generation.

### Analytics Objects

Strategic Analytics consist of:

- StrategicAlignmentAnalytics
- ProjectInvestmentAnalytics
- PortfolioBalanceAnalytics

### Responsibilities

Strategic Analytics may evaluate:

- strategic alignment
- investment distribution
- portfolio composition
- value concentration
- value diversification
- long-term sustainability

### Design Principle

Strategic Analytics determine whether effort and investment are aligned with intended outcomes and long-term objectives.

They focus on value creation and strategic direction rather than operational execution.

---

### 6.4.1 StrategicAlignmentAnalytics

StrategicAlignmentAnalytics evaluates how strongly current work is aligned with defined Goals.

Its purpose is to identify whether effort is being invested in activities that contribute to strategic objectives.

#### Domain Question

```text
Is current work aligned with strategic goals?
```

#### Purpose

Evaluate the degree of alignment between work and the Goals defined within the system.

#### Inputs

StrategicAlignmentAnalytics may use:

- goals
- task descriptions
- project descriptions
- task score
- project membership

#### Calculation

StrategicAlignmentAnalytics evaluates:

- goal alignment
- concentration of aligned work
- concentration of unaligned work
- goal coverage

Alignment assessment may be supported by LLM-based semantic analysis.

Specific calculation methods are implementation-dependent.

#### Interpretation

High alignment indicates that a significant portion of effort contributes to defined Goals.

Low alignment indicates that effort may be dispersed across activities with limited strategic relevance.

Poor goal coverage may indicate that important Goals are insufficiently supported by active work.

#### Possible Outputs

Examples:

```yaml
StrategicAlignmentAnalytics:

  alignment_score: 0.81

  aligned_tasks_ratio: 0.73

  goal_coverage_score: 0.68
```

Output structure is implementation-dependent.


---

### 6.4.2 ProjectInvestmentAnalytics

ProjectInvestmentAnalytics evaluates how effort is distributed across projects and strategic goals.

Its purpose is to identify where the system is investing execution capacity and whether investment distribution reflects intended priorities.

#### Domain Question

```text
Where are we investing effort?
```

#### Purpose

Evaluate the distribution of effort across projects and goals.

#### Inputs

ProjectInvestmentAnalytics may use:

- goals
- project membership
- task score
- task state
- task estimates

#### Calculation

ProjectInvestmentAnalytics evaluates:

- effort distribution
- project investment concentration
- goal investment concentration
- investment imbalance
- concentration of active work

Specific calculation methods are implementation-dependent.

#### Interpretation

Balanced investment indicates that effort is distributed in accordance with intended priorities and strategic objectives.

Excessive concentration may indicate overinvestment in a limited number of projects or goals.

Insufficient investment may indicate that important projects or goals are receiving inadequate execution capacity.

#### Possible Outputs

Examples:

```yaml
ProjectInvestmentAnalytics:

  investment_concentration_score: 0.71

  active_goals: 4

  dominant_goal_ratio: 0.46
```

Output structure is implementation-dependent.

---

### 6.4.3 PortfolioBalanceAnalytics

PortfolioBalanceAnalytics evaluates the overall balance and diversification of the strategic portfolio.

Its purpose is to identify structural imbalances that may reduce long-term sustainability and strategic resilience.

#### Domain Question

```text
Is the strategic portfolio balanced?
```

#### Purpose

Evaluate the balance of effort and investment across the portfolio of goals and projects.

#### Inputs

PortfolioBalanceAnalytics may use:

- goals
- project membership
- task score
- task state

#### Calculation

PortfolioBalanceAnalytics evaluates:

- portfolio balance
- goal diversification
- project diversification
- concentration risk
- portfolio sustainability

Specific calculation methods are implementation-dependent.

#### Interpretation

Balanced portfolios indicate that effort is distributed across strategic objectives in a sustainable manner.

Excessive concentration may indicate strategic dependency on a limited number of goals or projects.

Insufficient diversification may reduce adaptability and increase long-term strategic risk.

#### Possible Outputs

Examples:

```yaml
PortfolioBalanceAnalytics:

  portfolio_balance_score: 0.76

  diversification_score: 0.69

  concentration_risk_score: 0.24
```

Output structure is implementation-dependent.

---

## 6.5 Data Quality Analytics

Data Quality Analytics evaluate the completeness, consistency, and reliability of system data.

Their purpose is to identify data quality issues that may reduce the accuracy of analytics, summaries, recommendations, and decision-making.

### Domain Question

```text
Can the system trust its own data?
```

### Scope

Data Quality Analytics evaluate data completeness, consistency, freshness, and structural integrity.

They do not evaluate attention allocation, execution performance, strategic alignment, or recommendation generation.

### Analytics Objects

Data Quality Analytics consist of:

- DataCompletenessAnalytics
- DataConsistencyAnalytics
- DataFreshnessAnalytics

### Responsibilities

Data Quality Analytics may evaluate:

- metadata completeness
- structural consistency
- data freshness
- missing information
- conflicting information
- analytical reliability

### Design Principle

Data Quality Analytics determine whether system data is sufficiently reliable to support analytics, summaries, recommendations, and decisions.

---

### 6.5.1 DataCompletenessAnalytics

DataCompletenessAnalytics evaluates whether required information is present within the system.

Its purpose is to identify missing data that may reduce analytical reliability and decision quality.

#### Domain Question

```text
Is required information present?
```

#### Purpose

Evaluate the completeness of task, project, and goal data used by the Analytics Engine.

#### Inputs

DataCompletenessAnalytics may use:

- tasks
- projects
- goals
- metadata fields

#### Calculation

DataCompletenessAnalytics evaluates:

- metadata completeness
- missing required fields
- completeness of task data
- completeness of project data
- completeness of goal data

Specific calculation methods are implementation-dependent.

#### Interpretation

High completeness indicates that required information is available for reliable analysis.

Low completeness indicates that missing information may reduce analytical confidence and recommendation quality.

Significant data gaps may limit the ability of the system to generate accurate insights.

#### Possible Outputs

Examples:

```yaml
DataCompletenessAnalytics:

  completeness_score: 0.87

  missing_fields: 12

  incomplete_tasks_ratio: 0.09
```

Output structure is implementation-dependent.

---

### 6.5.2 DataConsistencyAnalytics

DataConsistencyAnalytics evaluates whether information within the system is internally consistent.

Its purpose is to identify contradictions, structural conflicts, and data anomalies that may reduce analytical reliability.

#### Domain Question

```text
Is information internally consistent?
```

#### Purpose

Evaluate the consistency of task, project, goal, and metadata information used by the Analytics Engine.

#### Inputs

DataConsistencyAnalytics may use:

- tasks
- projects
- goals
- metadata fields

#### Calculation

DataConsistencyAnalytics evaluates:

- metadata consistency
- state consistency
- structural consistency
- cross-object consistency
- data anomalies

Specific calculation methods are implementation-dependent.

#### Interpretation

High consistency indicates that system information is coherent and can be reliably interpreted by analytics and recommendation components.

Low consistency indicates the presence of contradictions or structural conflicts that may reduce analytical confidence.

Persistent inconsistencies may indicate process issues, modeling problems, or outdated information.

#### Possible Outputs

Examples:

```yaml
DataConsistencyAnalytics:

  consistency_score: 0.91

  conflicting_items: 4

  anomaly_ratio: 0.03
```

Output structure is implementation-dependent.

---

### 6.5.3 DataFreshnessAnalytics

DataFreshnessAnalytics evaluates whether system information remains sufficiently current for reliable analysis and decision-making.

Its purpose is to identify stale data that may reduce analytical relevance and recommendation quality.

#### Domain Question

```text
Is information current enough to be trusted?
```

#### Purpose

Evaluate the freshness of task, project, goal, and metadata information used by the Analytics Engine.

#### Inputs

DataFreshnessAnalytics may use:

- tasks
- projects
- goals
- metadata fields

#### Assumptions

Task Model, Project Model, Goal Model
should have canonical foeld of changing of the objects.
But they don't have it now.


#### Calculation

DataFreshnessAnalytics evaluates:

- data freshness
- stale information accumulation
- update recency
- freshness distribution
- freshness risk

Specific calculation methods are implementation-dependent.

#### Interpretation

High freshness indicates that system information is regularly maintained and suitable for reliable analysis.

Low freshness indicates that significant portions of the system may no longer accurately reflect current reality.

Persistent freshness issues may reduce confidence in analytics, summaries, recommendations, and decisions.

#### Possible Outputs

Examples:

```yaml
DataFreshnessAnalytics:

  freshness_score: 0.84

  stale_items: 18

  stale_ratio: 0.11
```

Output structure is implementation-dependent.

---

# 7. Distribution Analysis

## Purpose

Distribution Analysis examines how analytical values are distributed across a set of entities.

While Analytics Objects measure individual metrics, Distribution Analysis evaluates the overall shape, concentration, balance, and spread of those metrics.

Its purpose is to answer questions such as:

- Where is work concentrated?
- How evenly is effort distributed?
- Which entities dominate the system?
- Are there significant imbalances?
- Is the portfolio diversified or concentrated?

Distribution Analysis provides structural insight into analytical results before any interpretation is applied.

---

## Responsibilities

Distribution Analysis is responsible for:

- Analyzing distributions of analytical values.
- Identifying concentration and imbalance.
- Detecting dominant entities.
- Comparing relative proportions.
- Producing distribution-level observations.

Distribution Analysis does **not** determine whether a distribution is good or bad.

Interpretation belongs to Corridor Evaluation or other types of distribution evaluation.

---

## Inputs

Distribution Analysis consumes outputs produced by Analytics Objects.

Examples:

- Project scores
- Project workload
- Project priority
- Task age
- Overdue counts
- Strategic alignment scores
- Focus scores

---

## Outputs

Distribution Analysis produces structured distribution results.

Example:

```yaml
distribution:
  metric: project_workload
  entities: 12

  top_share:
    value: 42%
    owner: Project A

  concentration_ratio:
    value: 0.61

  balance:
    value: uneven

  dominant_entity:
    value: Project A
```

Outputs describe the structure of the data but do not provide evaluation.

---

## Common Distribution Patterns

### Balanced Distribution

Work or value is spread relatively evenly across entities.

Example:

```yaml
distribution:
  pattern: balanced
```

---

### Concentrated Distribution

A small number of entities contain most of the value.

Example:

```yaml
distribution:
  pattern: concentrated
```

---

### Dominant Entity

One entity significantly outweighs all others.

Example:

```yaml
distribution:
  pattern: dominant_entity
  owner: Project A
```

---

### Fragmented Distribution

Value is spread across many small entities without clear focus.

Example:

```yaml
distribution:
  pattern: fragmented
```

---

## Distribution Analysis Principles

1. Distribution describes structure, not quality.
2. Distribution is relative rather than absolute.
3. Multiple distributions may be analyzed simultaneously.
4. Distribution results are inputs for Corridor Evaluation and Executive Summary.

---

# 8. Corridor Evaluation

## Purpose

Corridor Evaluation interprets analytical results against predefined reference ranges.

While Analytics Objects calculate values and Distribution Analysis describes their structure, Corridor Evaluation determines what those values mean from a decision-making perspective.

Its purpose is to answer questions such as:

- Is the metric healthy?
- Is attention required?
- Is the value outside acceptable boundaries?
- How severe is the deviation?

Corridor Evaluation transforms measurements into assessments.

---

## Responsibilities

Corridor Evaluation is responsible for:

- Comparing analytical values against predefined corridors.
- Assigning evaluation states.
- Determining severity levels.
- Detecting deviations from desired ranges.
- Producing interpretable assessments.

Corridor Evaluation does not generate recommendations.

Recommendations belong to the Recommendation Engine.

---

## Corridor Concept

A corridor defines an expected operating range for a metric.

Example:

```yaml
corridor:
  metric: overdue_ratio

  healthy:
    min: 0
    max: 10

  warning:
    min: 10
    max: 25

  critical:
    min: 25
```

The metric value is evaluated against the corridor to determine its state.

---

## Evaluation States

### Healthy

The value is within the desired operating range.

Example:

```yaml
evaluation:
  status: healthy
```

---

### Warning

The value is outside the desired range and requires attention.

Example:

```yaml
evaluation:
  status: warning
```

---

### Critical

The value significantly exceeds acceptable limits and requires intervention.

Example:

```yaml
evaluation:
  status: critical
```

---

## Evaluation Output

Example:

```yaml
evaluation:
  metric: overdue_ratio

  value: 18%

  status: warning

  corridor:
    healthy: 0-10%
    warning: 10-25%
    critical: >25%
```

---

## Distribution-Based Evaluation

Corridors may also be applied to distribution results.

Example:

```yaml
evaluation:
  metric: workload_concentration

  value: 62%

  status: warning
```

In this case the evaluated object is not a raw metric but a distribution characteristic.

---

## Corridor Evaluation Principles

1. Corridors provide interpretation, not measurement.
2. Every corridor must be explicitly defined.
3. Evaluation must be deterministic.
4. Identical inputs must always produce identical evaluations.
5. Corridor Evaluation is one of the inputs used by Executive Summary generation.

---

# 9. Executive Summary

## Purpose

Executive Summary converts analytical results into a concise management-level assessment of the system.

While Analytics Objects produce measurements, Distribution Analysis describes structure, and Corridor Evaluation provides assessments, Executive Summary synthesizes these outputs into a coherent narrative that supports decision-making.

Its purpose is to answer questions such as:

- What is happening in the system?
- What deserves attention right now?
- What are the most important strengths?
- What are the most important risks?
- What opportunities exist?
- What additional developments should the decision-maker be aware of?

Executive Summary focuses on interpretation rather than measurement.

---

## Responsibilities

Executive Summary is responsible for:

- Synthesizing results from multiple analytical domains.
- Highlighting the most important strengths.
- Identifying key risks.
- Identifying key opportunities.
- Capturing important contextual findings.
- Describing the current system state.
- Providing management-level situational awareness.

Executive Summary does not generate recommendations.

Recommendations belong to the Recommendation Engine.

---

## Inputs

Executive Summary may consume:

- Focus Analytics
- Tactical Analytics
- Strategic Analytics
- Distribution Analysis results
- Corridor Evaluation results

The summary should integrate information across domains rather than repeating individual metrics.

---

## Outputs

Executive Summary produces a structured assessment of the system.

Example:

```yaml
summary:
  system_state: stable

  strengths:
    - Inbox remains empty.
    - Strategic activity remains healthy.

  risks:
    - Active workload exceeds target corridor.

  opportunities:
    - Archive inactive projects.

  findings:
    - Kanban parser implementation is in progress.
```

The summary describes the system but does not prescribe actions.

---

## Executive Summary Structure

### System State

Provides a high-level characterization of the current state.

Examples:

```yaml
system_state: healthy
```

```yaml
system_state: stable
```

```yaml
system_state: overloaded
```

```yaml
system_state: fragmented
```

---

### Strengths

Strengths identify conditions that positively support execution effectiveness.

Examples:

```yaml
strengths:
  - Inbox remains empty.
  - Strategic activity remains healthy.
  - Focus allocation is balanced.
```

Strengths describe what is working well and should be preserved.

---

### Risks

Risks identify conditions that may negatively impact execution effectiveness.

Examples:

```yaml
risks:
  - Active workload exceeds target corridor.
  - Overdue backlog continues to grow.
  - Project concentration remains excessive.
```

Risks describe potential problems but do not prescribe solutions.

---

### Opportunities

Opportunities identify areas where measurable improvement may be achieved.

Examples:

```yaml
opportunities:
  - Archive inactive projects.
  - Rebalance workload distribution.
  - Increase strategic work allocation.
```

Opportunities describe potential gains but do not prescribe actions.

---

### Findings

Findings capture important contextual observations that do not imply a positive condition, a risk, or a potential improvement.

Examples:

```yaml
findings:
  - Kanban parser implementation is in progress.
  - New project entered active execution.
  - Project portfolio structure changed.
```

Findings provide context and situational awareness.

---

## Summary Generation Principles

### Principle 1 — Synthesis over Enumeration

The summary should combine multiple analytical signals into higher-level observations.

Avoid:

```yaml
summary:
  - focus_score = 73
  - overdue_ratio = 12%
  - active_projects = 14
```

Prefer:

```yaml
summary:
  strengths:
    - Focus remains healthy despite increasing project load.
```

---

### Principle 2 — Prioritize Significance

Only findings with meaningful decision impact should be included.

Minor observations should remain in detailed analytics.

---

### Principle 3 — Cross-Domain Interpretation

Executive Summary should identify relationships across analytical domains.

Example:

```yaml
observation:
  Strategic focus is declining while operational workload is increasing.
```

Such observations often provide more value than isolated metrics.

---

### Principle 4 — Action-Neutral Language

Executive Summary explains what is happening.

It does not explain what should be done.

Action generation belongs to the Recommendation Engine.

---

### Principle 5 — Deterministic Generation

Identical analytical inputs should produce identical summaries.

Summary generation must be rule-based and reproducible.

---

## Position in the Analytics Pipeline

```text
Analytics Objects
        ↓
Distribution Analysis
        ↓
Corridor Evaluation
        ↓
Executive Summary
        ↓
Recommendation Engine
```

Executive Summary acts as the interpretation layer between analytics and recommendations.

---

# 10. Recommendations


## Purpose

RecommendationCollection contains structured actions derived from analytics results.

Its purpose is to:

* improve board health
* maintain score corridor balance
* reduce execution overload
* reduce task debt
* improve execution quality
* support deterministic decision-making

Recommendations are generated from Executive Summary outputs and system configuration.

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

  category:
    string

  action:
    string

  priority:
    high | medium | low

  reason:
    string
```

### Fields

#### category

Domain affected by the recommendation.

Examples:

```text
workload
portfolio
focus
overdue
strategic
```


#### action

Recommended operation.

Examples:

```text
rebalance
archive
cleanup
protect
review
investigate
```

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
category: workload

action: rebalance

priority: high

corridor: "21-25"

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
category: workload

action: rebalance

priority: high

corridor: "21-25"

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

# 11. AnalyticsReport

## Purpose

AnalyticsReport is the canonical output of the analytics system.

It combines executive-level assessment and generated recommendations into a single structured report.

AnalyticsReport serves as the primary interface between analytical components and report rendering components.

---

## Responsibilities

AnalyticsReport is responsible for:

- aggregating analytical outputs
- providing a unified report structure
- exposing ExecutiveSummary
- exposing RecommendationCollection

AnalyticsReport does not perform analysis.

AnalyticsReport does not generate recommendations.

AnalyticsReport does not define rendering, formatting, presentation, or user interface behavior.

These responsibilities belong to other system components.

---

## Structure

Canonical structure:

```yaml
AnalyticsReport:

  generated_at:
    datetime

  summary:
    ExecutiveSummary

  recommendations:
    RecommendationCollection
```

---

## Components

### ExecutiveSummary

Contains the executive-level interpretation of analytical results.

The canonical ExecutiveSummary model is defined in Section 9.

---

### RecommendationCollection

Contains structured recommendations generated from analytical assessments.

The canonical RecommendationCollection model is defined in Section 10.

---

## Position in the Analytics Pipeline

```text
Analytics Objects
        ↓
Distribution Analysis
        ↓
Corridor Evaluation
        ↓
Executive Summary
        ↓
Recommendation Engine
        ↓
RecommendationCollection
        ↓
AnalyticsReport
```

AnalyticsReport represents the final structured output of the analytics system.


---

# 11.1 BoardHealth

## Purpose

`BoardHealth` evaluates the quality and analytical readiness of a Kanban board.

It answers the question:

> How reliable and complete is the board data for analytical processing?

All analytical modules MUST interpret their results in the context of `BoardHealth`.

---

## Output Model

```yaml
board_health:
  total_tasks: integer

  score_coverage: percentage
  tag_coverage: percentage
  analytics_coverage: percentage

  missing_score: integer
  missing_tag: integer

  orphan_tasks: integer

  sample_orphans:
    - task: string
      missing:
        - score
        - tag

  status:
    - excellent
    - good
    - warning
    - poor
    - awful
```

---

## Metrics

### total_tasks

Total number of tasks included in board analysis.

Example:

```yaml
total_tasks: 127
```

---

### score_coverage

Percentage of tasks with a populated `Score`.

Formula:

```text
score_coverage =
(tasks_with_score / total_tasks) × 100
```

Example:

```yaml
score_coverage: 84%
```

---

### tag_coverage

Percentage of tasks assigned at least one analytical tag.

At the current stage of the system, analytical tags are derived from `Tags Area`.

Formula:

```text
tag_coverage =
(tasks_with_tag / total_tasks) × 100
```

Example:

```yaml
tag_coverage: 78%
```

---

### analytics_coverage

Primary indicator of board analytical readiness.

Measures the percentage of tasks that contain both:

* Score
* Analytical Tag

Only these tasks can fully participate in analytical models.

Formula:

```text
analytics_coverage =
(tasks_with_score_and_tag / total_tasks) × 100
```

Example:

```yaml
analytics_coverage: 71%
```

---

### missing_score

Number of tasks without a populated `Score`.

Formula:

```text
missing_score =
count(tasks_without_score)
```

Example:

```yaml
missing_score: 20
```

---

### missing_tag

Number of tasks without an analytical tag.

Formula:

```text
missing_tag =
count(tasks_without_tag)
```

Example:

```yaml
missing_tag: 28
```

---

### orphan_tasks

Number of tasks that cannot fully participate in analytical processing.

A task is considered an orphan if it lacks at least one required analytical attribute:

* Score
* Analytical Tag

Formula:

```text
orphan_tasks =
count(tasks_without_score OR tasks_without_tag)
```

Example:

```yaml
orphan_tasks: 37
```

---

### sample_orphans

Representative sample of orphan tasks.

Contains up to 5 orphan tasks selected from the board.

The purpose of the collection is to help identify the most common metadata quality issues without requiring manual board inspection.

Selection priority:

1. Tasks missing both `Score` and `Tag`
2. Tasks missing `Score`
3. Tasks missing `Tag`

Example:

```yaml
sample_orphans:
  - task: "Refactor Metadata Parser"
    missing:
      - score
      - tag

  - task: "Review Blood Pressure Report"
    missing:
      - tag

  - task: "Telegram Integration Validation"
    missing:
      - score
```

---

## Status Evaluation

Status is determined by `analytics_coverage`.

| Analytics Coverage | Status |
|-------------------|----------|
| ≥ 99% | excellent |
| ≥ 90% | good |
| ≥ 75% | warning |
| ≥ 50% | poor |
| ≥ 25% | awful |
| < 25% | critical |

---

## Interpretation

### excellent

The board demonstrates near-complete analytical readiness.

Analytical conclusions can be considered highly reliable.

### good

The board is analytically healthy.

Minor metadata gaps may exist but are unlikely to significantly affect conclusions.

### warning

A noticeable portion of tasks is excluded from analytical calculations.

Results should be interpreted with caution.

Improving metadata quality is recommended.

### poor

A large portion of the board is excluded from analytical processing.

Analytical conclusions may be materially distorted.

Improving metadata quality should become a priority.

### awful

The board has lost most of its analytical value.

Analytical outputs should be considered unreliable until metadata quality is restored.

### critical

The board is analytically unusable.

Most tasks lack the metadata required for analytical processing.

Analytical conclusions MUST NOT be used for decision-making until board metadata quality is restored.

The primary objective should be metadata remediation rather than analytical interpretation.

---

## Reporting Requirements

`BoardHealth` is a mandatory section of every `AnalyticsReport`.

It MUST be presented before all other analytical modules.

All analytical conclusions MUST be interpreted through the lens of `BoardHealth`.

If:

```yaml
analytics_coverage < 75%
```

the report MUST include a warning indicating reduced analytical reliability.

If:

```yaml
analytics_coverage < 50%
```

the report SHOULD prioritize metadata remediation recommendations over analytical conclusions.


If:

analytics_coverage < 25%

the report MUST clearly state that analytical conclusions are unreliable
and SHOULD prioritize board metadata remediation over analytical findings.


---

## Example

```yaml
board_health:
  total_tasks: 127

  score_coverage: 84%
  tag_coverage: 78%
  analytics_coverage: 71%

  missing_score: 20
  missing_tag: 28

  orphan_tasks: 37

  sample_orphans:
    - task: "Refactor Metadata Parser"
      missing:
        - score
        - tag

    - task: "Telegram Integration Validation"
      missing:
        - score

    - task: "Prepare Strategic Review"
      missing:
        - tag

  status: warning
```

### Interpretation

The board demonstrates partial analytical readiness. Only 71% of tasks participate fully in analytical calculations. Results remain useful but should be interpreted with caution due to the significant number of orphan tasks and incomplete metadata coverage.


---

# 11.2 AnalyticsConfidence

## Purpose

`AnalyticsConfidence` represents the reliability level of analytical conclusions derived from the current board state.

It translates board metadata quality into a confidence level that can be consistently used across all analytical modules.

`AnalyticsConfidence` is derived exclusively from `BoardHealth`.

---

## Output Model

```yaml
analytics_confidence:
  - high
  - medium
  - low
  - none
```

---

## Confidence Mapping

Analytics confidence is determined by `BoardHealth.status`.

| BoardHealth Status | Analytics Confidence |
| ------------------ | -------------------- |
| excellent          | high                 |
| good               | high                 |
| warning            | medium               |
| poor               | low                  |
| awful              | low                  |
| critical           | none                 |

---

## Interpretation

### high

Board metadata quality is sufficient for reliable analytical conclusions.

Findings and recommendations may be used with high confidence.

---

### medium

Board metadata quality contains noticeable gaps.

Analytical conclusions remain useful but should be interpreted with caution.

---

### low

A significant portion of board data is unavailable for analytical processing.

Analytical conclusions may be materially distorted and require careful validation.

---

### none

Board metadata quality is insufficient for meaningful analytical processing.

Analytical conclusions MUST be considered unreliable.

The primary focus should be metadata remediation rather than analytical interpretation.

---

## Usage Rules

All analytical modules MUST expose the current `analytics_confidence` level.

Example:

```yaml
focus_attention:
  analytics_confidence: medium
```

```yaml
strategic:
  analytics_confidence: low
```

---

## Reporting Requirements

Every `AnalyticsReport` MUST include a single top-level `analytics_confidence` value.

Example:

```yaml
analytics_confidence: high
```

This value MUST be derived from `BoardHealth`.

Analytical modules SHOULD reference this value instead of implementing independent confidence calculations.

---

## Future Extensions

Analytical modules may adapt their behavior according to `analytics_confidence`.

Examples:

```text
high
→ Full analytics

medium
→ Full analytics with caution notices

low
→ Analytics with reduced trust and remediation recommendations

none
→ Analytics may be suppressed in favor of metadata remediation guidance
```

The specific adaptation rules are defined by individual analytical modules.



---


## 11.3 Corridors

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