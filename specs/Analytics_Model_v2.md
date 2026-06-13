---

created: 2026-06-06
updated: 2026-06-06
Description:
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

---

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

Analytics are organized into four decision domains.
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

# 3. Analytics Architecture

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
ExecutiveSummary
```

Purpose:

Synthesize analytical findings into a concise executive overview.

ExecutiveSummary may interpret measurements generated by previous pipeline stages.

---

## Step 7. Report Assembly

Input:

```text
ExecutiveSummary
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

Analytics components must not depend on ExecutiveSummary.

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

ExecutiveSummary depends on analytical measurements.

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

# 7. Distribution & Corridor Analysis

Distribution & Corridor Analysis provide mechanisms for analyzing the structure of analytical results and interpreting them using predefined evaluation corridors.

Their purpose is to transform analytical measurements into actionable insights by evaluating how values are distributed and how those distributions compare to expected ranges.

## Domain Question

```text
How should analytical results be analyzed and interpreted?
```

## Scope

Distribution & Corridor Analysis operate on analytical results produced by Analytics Objects.

They do not generate analytical measurements themselves.

## Responsibilities

Distribution & Corridor Analysis may:

- analyze metric distributions
- identify concentration patterns
- evaluate distribution balance
- classify results using corridors
- identify deviations from expected ranges
- support summary generation
- support recommendation generation

## Design Principle

Distribution Analysis describes the structure of analytical results.

Corridor Evaluation interprets those results against predefined ranges.

Together they provide the bridge between raw analytical measurements and decision-support outputs.

## Conceptual Flow

```text
Analytics Objects
        ↓
Analytics Results
        ↓
Distribution Analysis
        ↓
Corridor Evaluation
        ↓
Executive Summary
        ↓
Recommendations
```

---

# 8. ExecutiveSummary

---

# 9. Recommendations


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

---

# 10. AnalyticsReport

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

## 9.1 Corridors

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

## 9.2 ExecutiveSummary

### Purpose

ExecutiveSummary provides a concise executive overview of the board state.

It synthesizes findings produced by other analytics components and highlights the most important observations requiring attention.

ExecutiveSummary does not generate new analytics.

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

ExecutiveSummary is an aggregation layer.

Its purpose is to answer:

```text
What matters most right now?
```

---

### Canonical Structure

```yaml
ExecutiveSummary:

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

ExecutiveSummary answers:

* What is the current overall situation?
* What findings are most important?
* What is the primary risk?
* What is the primary opportunity?
* Where should attention be directed next?

ExecutiveSummary does not provide:

* raw metrics
* corridor calculations
* score calculations
* attention calculations

Those responsibilities belong to specialized analytics components.

---

### Design Principle

ExecutiveSummary is designed for rapid report consumption.

A reader should be able to understand the most important conclusions of the report by reading ExecutiveSummary before reviewing detailed analytical sections.


---

## 9.3. CorridorAnalytics

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
