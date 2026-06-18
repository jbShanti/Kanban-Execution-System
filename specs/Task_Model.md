---
created: 2026-05-26T22:52
updated: 2026-05-31T15:02
Description: |-
  Canonical task schema for the Kanban Execution System.

  Purpose:
  - define stable machine-readable task structure
  - reduce parsing ambiguity
  - support deterministic analytics
  - preserve human readability
  - enable future automation safely

  This document defines:
  - task object structure
  - task lifecycle
  - metadata semantics
  - parsing invariants
  - archive semantics
  - supported formats
  - forbidden patterns
---
# TASK MODEL



---

# 1. Core Philosophy

Task structure must optimize for:

- clarity
- parsing stability
- maintainability
- human readability
- deterministic processing

NOT:
- visual complexity
- decorative formatting
- excessive nesting
- markdown creativity

---

# 2. Canonical Task Structure

## Base Task Format

```md
- [ ] Task title [[Internal Link]] #Tag @{2026-05-30} [score::15] [time::30m]
```

---

## Canonical Structure Order

Recommended order:

```text
status
→ emoji
→ title
→ links
→ tags
→ deadline metadata
→ score metadata
→ operational metadata
```

Example:

```md
- [ ] 🛠 Review parser architecture [[Parser Architecture]] #AI/Agents @{2026-05-30} [score::15] [time::45m] [finance::free]
```

---

# 3. Supported Task Statuses

## Open Task

```md
- [ ]
```

Meaning:
- active executable task
- counts as active
- included in analytics

---

## In Progress

```md
- [/]
```

Meaning:
- execution started
- still active
- included in active analytics

---

## Completed

```md
- [x]
```

Meaning:
- completed task
- included in completion analytics

---

## Cancelled

```md
- [-]
```

Meaning:
- intentionally cancelled
- excluded from execution metrics
- may remain for historical context

---

## Delegated

```md
- [>]
```

Meaning:
- waiting state
- delegated
- pending future activation
- waiting for task is done by someone

Does NOT represent active execution.

---

## Scheduled / Postponed

```md
- [<]
```

Meaning:
- scheduled on further date
- waiting for start time
- paused
- postponed

Does NOT represent active execution.

---

## Informational / Ignored

```md
- [i]
```

Meaning:
- informational object
- not executable
- ignored by analytics

Used for:
- legends
- reference blocks
- examples

---

# 4. Task Components

## Required Components

Every executable task SHOULD contain:

- status
- emoji
- title

---

## Recommended Components

Strongly recommended:

- score
- due date
- estimated time
- tags

---

## Optional Components

Optional:

- finance metadata
- recurrence metadata
- priority metadata
- category metadata
- tracking metadata
- notes
- links

---

# 5. Task Title Rules

## Title Requirements

Task titles should be:

- action-oriented
- concise
- human-readable
- operationally meaningful

Good:

```md
- [ ] Buy Omega-3
```

Bad:

```md
- [ ] Health
```

---

## Task Language

Preferred:
- English for executable tasks
- Russian allowed for references/context

Mixed language allowed if operationally clearer.

---

## Emojis

Allowed:
- priority signaling
- visual scanning
- semantic hints

Must NOT:
- replace meaning
- break parsing
- contain metadata semantics

---

# 6. Metadata System

## General Metadata Format

Canonical syntax:

```text
[key::value]
```

Whitespace inside metadata is discouraged.

---

## Supported Metadata

### Score

```md
[score::15]
```

Purpose:
- execution priority
- leverage estimation
- importance weighting

Allowed:
- integer values
- recommended range: 0-25

---

### Time Estimate

```md
[time::30m]
```

Supported formats:
- 5m
- 15m
- 1h
- 2h
- 90m
- 1.5h
- 1h30m

---

### Due Date

```md
@{2026-05-30}
```

Canonical deadline format.

Alternative supported:

```md
[due::2026-05-30]
```

---

### Scheduled Date

```md
[scheduled::2026-05-30]
```

Meaning:
- planned execution date
- not hard deadline

---

### Start Date

```md
[start::2026-05-30]
```

Meaning:
- activation date
- recurring baseline

---

### Completion Date

```md
[completion::2026-05-30]
```

Used for:
- analytics
- execution velocity
- historical tracking

---

### Repeat Rules

```md
[repeat::every week]
```

Examples:
- every week
- every month
- every day when done
- every week on Sunday

---

### Priority Metadata

```md
[priority::high]
```

Supported values:
- highest
- high
- medium
- low

---

### Finance Metadata

```md
[finance::planned]
```

Supported examples:
- planned
- free
- income
- regular
- extra
- debts

### Cost Metadata

---
```md
[cost::1500]
```
Is used for price when buying or cost when paying for service

---

### Analytics Metadata

```md
[analytics::ignore]
```

Meaning:
- excluded from analytics
- excluded from recommendations
- excluded from scoring systems

---

### Category Metadata

```md
[Category::Health]
```

Optional semantic classification.

---

## Metadata Types

| Metadata | Type        |
| -------- | ----------- |
| score    | integer     |
| due      | date        |
| time     | duration    |
| repeat   | string/enum |
| analytics| enum        |
| finance  | enum/number |

### Canonical duration formats:  
15m  
30m  
90m  
2h  
1.5h  
1h30m


---
## Explicit Metadata Namespace Rule

Canonical form of metadata: lowercase.  
Parser SHOULD accept legacy mixed-case keys.  
Parser MUST normalize metadata keys to lowercase.

Custom metadata must use:
```md
[x-namespace::value]
```

Example:
```md
[x-health::supplements]
```

---
# 7. Links

## Internal Links

Supported:

```md
[[Document]]
[[Document|Alias]]
```

Must remain unchanged during parsing.

---

## External Links

Supported:

```md
[Title](https://example.com)
```

Must remain preserved.

---

# 8. Tags

## Canonical Tag Format

```md
#Health
#Projects/AI
#Priority/Highest
```

---

## Tag Rules

Allowed:
- nested tags
- hierarchical tags

Avoid:
- inconsistent naming
- duplicate semantics
- excessive fragmentation

---

# 9. Section Model

## Sections Represent Operational Contexts

Examples:
- Inbox
- Critical
- Todo
- Health
- AI and Dev
- Backlog
- Done
- Archive

---

## Section Priority

Optional syntax:

```md
## Health [P::5]
```

Range:
- 1-5

Meaning:
- contextual importance modifier

---

# 10. Archive Semantics

## Canonical Archive Rule

Archived tasks are:

1. tasks inside:

```text
## Archive
```

AFTER:

```text
***
```

OR

2. tasks containing:

```text
||
```

Example:

```md
- [x] Task name [score::10] || 2026-05-20 12:00
```

---

## Archive Behavior

Archived tasks:
- excluded from active analytics
- excluded from overload calculations
- included in historical metrics

---

# 11. Nested Tasks

## Rule

Nested tasks are treated as:

```text
subtasks
```

and ignored by high-level analytics.

---

## Example

```md
- [ ] Main task
    - [ ] Subtask
```

Only:

```text
Main task
```

counts in primary analytics.

---

# 12. Parsing Invariants

## Mandatory Parsing Guarantees

The parser MUST preserve:

- status
- title
- metadata
- tags
- links
- hierarchy
- section placement

---

## Metadata Must Remain Machine-Readable

Avoid:
- malformed brackets
- inconsistent separators
- decorative syntax

---

## Stable Formatting Preferred

Preferred:
- one task per line
- predictable metadata placement
- minimal markdown decoration

---

# 13. Forbidden Patterns

Avoid:

- deeply nested tasks
- decorative markdown
- ambiguous metadata
- inconsistent dates
- metadata inside free text
- parser-breaking formatting
- excessive multiline structures

---

# 14. Canonical Date Format

Required:

```text
YYYY-MM-DD
```

Example:

```text
2026-05-30
```

Avoid:
- localized dates
- ambiguous formats
- textual month names

---

# 15. Score Semantics

## Purpose

Score represents the combined importance of a task.

It is the primary prioritization mechanism used throughout the system.

Score determines:

- execution priority
- analytical grouping
- corridor assignment
- portfolio distribution

---

## Scoring Model

Score is calculated as:

```text
Score = Area Priority × Task Priority
```

Where:

```text
Area Priority ∈ [1..5]

Task Priority ∈ [1..5]
```

Result:

```text
Score ∈ [1..25]
```

---

## Area Priority

Area Priority represents the relative importance of an Area.

Examples:

```text
5 = Mission-Critical Area

4 = Strategic Area

3 = Important Area

2 = Supporting Area

1 = Optional Area
```

Area Priority is defined independently from individual tasks.

---

## Task Priority

Task Priority represents the importance of a task within its Area.

Examples:

```text
5 = Highest Priority

4 = High Priority

3 = Medium Priority

2 = Low Priority

1 = Minimal Priority
```

Task Priority is assigned at the task level.

---

## Examples

Critical task in a critical area:

```text
Area Priority = 5
Task Priority = 5

Score = 25
```

High-priority task in a supporting area:

```text
Area Priority = 2
Task Priority = 5

Score = 10
```

Medium-priority task in an important area:

```text
Area Priority = 3
Task Priority = 3

Score = 9
```

---

## General Interpretation

Higher score indicates greater expected impact from task execution.

Higher score implies:

- higher strategic importance
- higher execution relevance
- higher portfolio value
- higher attention priority

---

## Score Corridors

Score values are grouped into canonical corridors.

### 21-25

Critical Layer

Characteristics:

- mission-critical work
- highest expected impact
- strongest execution priority

Target:

```text
3-5 active tasks
```

---

### 16-20

Strategic Layer

Characteristics:

- high-value work
- significant strategic contribution

Target:

```text
6-10 active tasks
```

---

### 11-15

Core Operational Layer

Characteristics:

- important ongoing work
- primary execution portfolio

Target:

```text
11-20 active tasks
```

---

### 6-10

Supporting Layer

Characteristics:

- useful but non-critical work
- secondary execution priority

Target:

```text
21-30 active tasks
```

---

### 1-5

Optional Layer

Characteristics:

- low-value work
- optional initiatives
- backlog candidates

Target:

```text
≤ 5 active tasks
```

---

### 0

Unprioritized

Characteristics:

- informational items
- reference materials
- uncategorized tasks

---

## 15.1 Score Framework

### Purpose

Score Framework defines the canonical mechanism used to calculate task score.

The framework combines Area importance and Task priority into a single execution score.

Score serves as the primary prioritization signal throughout the system.

---

### Design Principle

A task should receive a high score only when:

```text
Important Area
+
Important Task
```

Both dimensions are required.

A highly important task in an unimportant area should not receive the maximum score.

Likewise, a task in a critical area should not automatically receive the maximum score if the task itself has low priority.

---

### Canonical Formula

```text
Score = Area Priority × Task Priority
```

Where:

```text
Area Priority ∈ [1..5]

Task Priority ∈ [1..5]
```

Result:

```text
Score ∈ [1..25]
```

---

### Area Priority

Area Priority represents the relative importance of an Area within the user's portfolio.

```text
5 = Mission-Critical

4 = Strategic

3 = Important

2 = Supporting

1 = Optional
```

Area Priority is assigned at the Area level.

All tasks within the same Area inherit the same Area Priority.

---

### Task Priority

Task Priority represents the importance of a task within its Area.

```text
5 = Highest Priority

4 = High Priority

3 = Medium Priority

2 = Low Priority

1 = Minimal Priority
```

Task Priority is assigned individually for each task.

---

### Examples

Mission-critical task:

```text
Area Priority = 5
Task Priority = 5

Score = 25
```

---

Strategic task:

```text
Area Priority = 5
Task Priority = 4

Score = 20
```

---

Important operational task:

```text
Area Priority = 3
Task Priority = 4

Score = 12
```

---

Optional task:

```text
Area Priority = 1
Task Priority = 2

Score = 2
```

---

### Interpretation

The score represents expected execution value.

Higher score indicates:

* higher strategic impact
* higher execution relevance
* higher portfolio importance
* higher attention priority

---

### Relationship to Score Corridors

Score is mapped into a ScoreCorridor.

```text
Score
↓
ScoreCorridor
↓
Analytics
```

All corridor-based analytics depend on Score generated by this framework.

---

### Responsibility

Score Framework defines:

* score calculation
* priority composition
* score scale
* score boundaries

It does not define:

* score corridors
* analytics calculations
* recommendations
* report rendering

Those responsibilities belong to other system components.

---

### 15.1.1 Area Priority Source

#### Purpose

Area Priority Source defines how Area Priority is assigned within the scoring framework.

It describes both the current deterministic implementation and the planned semantic classification model.

---

#### Current Implementation

In the current system, Area Priority is derived from the task section.

A section serves two responsibilities:

* defines the Area
* defines the Area Priority

Example:

```text
Health [P:5]
```

Produces:

```text
Area = Health

Area Priority = 5
```

---

Another example:

```text
Learning [P:4]
```

Produces:

```text
Area = Learning

Area Priority = 4
```

---

#### Section-Based Classification

The current classification model is:

```text
Task
↓
Section
↓
Area
↓
Area Priority
```

Tasks within the same section inherit the same Area Priority.

---

#### Generic Sections

Some sections may represent loosely defined areas.

Example:

```text
Other Projects [P:3]
```

In such cases:

```text
Area = Other Projects

Area Priority = 3
```

The system does not require Areas to be highly specific.

Area classification remains valid as long as the section defines a meaningful execution context.

---

#### Inbox Tasks

Inbox tasks do not belong to an Area.

Example:

```text
Inbox
```

Produces:

```text
Area = null

Area Priority = null
```

As a result:

```text
Score = null
```

Inbox tasks are considered unclassified.

They must not participate in score-based analytics until classification is completed.

---

#### Future Semantic Classification

The long-term model replaces section-based classification with semantic classification.

The planned flow is:

```text
Task
↓
SemanticArea
↓
Area Priority
↓
Score
```

SemanticArea may be determined using:

* task title
* task description
* task tags
* historical task patterns

---

#### Area Priority Configuration

Area priorities are not embedded in analytical models.

They are defined through external configuration associated with a Kanban board.

Example:

```yaml
AreaPriorities:

  Health: 5

  Family: 5

  Projects: 4

  Learning: 4

  Administration: 2
```

The configuration serves as the authoritative source of Area Priority values.

---

#### Evolution Path

Current implementation:

```text
Task
↓
Section
↓
Area Priority
↓
Score
```

Target implementation:

```text
Task
↓
SemanticArea
↓
Area Priority Configuration
↓
Score
```

This evolution preserves score semantics while allowing Area classification to become increasingly intelligent and independent from board structure.

---

#### Design Principle

Area Priority must be externally configurable.

Score calculation must remain independent from:

* board layout
* section naming
* analytical models
* report rendering

Only the source of Area determination may evolve over time.

The score calculation model remains unchanged.

---

# 16. Task Lifecycle

```text
Inbox
↓
Clarified
↓
Scored
↓
Scheduled
↓
Execution
↓
Done / Cancelled
↓
Archive
```

---

# 17. Analytics Signals

Analytics signals are deterministic values derived from parsed tasks.

## Task Metrics

- active_tasks
- completed_tasks
- cancelled_tasks
- delegated_tasks
- scheduled_tasks
- archived_tasks

## Time Metrics

- overdue_tasks
- due_today_tasks
- due_next_3_days_tasks

## Score Metrics

- tasks_without_score

## Execution Metrics

- completion_velocity
- completion_rate

## System Metrics

- health_index
- overload_signals

## Analytics Rules

Analytics MUST be deterministic.

Analytics MUST NOT use LLM reasoning.

Analytics signals are derived exclusively from:
- parsed tasks
- task metadata
- section context
- task status

---
# 18. Active Context Rules

The system should maintain:

- 1 primary direction
- 2-3 secondary contexts

Excessive active contexts indicate:
- overload
- fragmentation
- execution instability

---

# 19. Readability Rules

Human readability has priority over:
- compactness
- visual tricks
- markdown creativity

The system is:
- operational infrastructure
- not decorative knowledge management

---

# 20. Deterministic Parsing Principle

If a structure:
- cannot be parsed reliably
- creates ambiguity
- requires interpretation

Then:
- simplify
- normalize
- standardize

Deterministic parsing has priority over formatting flexibility.

---

# 21. Future Compatibility

The task model is designed to support:

- parser layer
- deterministic analytics
- AI recommendations
- automation workflows
- mutation safety systems
- reporting engines
- execution monitoring

Without requiring structural redesign.

---
# 22. Domain Contracts

- Task.section is always Section
- Task.status is always TaskStatus
- Task.metadata values are strings: Raw metadata values are stored as strings. Typed interpretation is performed by parser services.
- Task.updated_at is timezone-aware
- Section is immutable
- Section.type is canonical source of truth
- Stable task identity is not required in Phase 1 parsing architecture.
- Tasks are identified by parser context and document position.
- Persistent task identifiers may be introduced in future automation phases.

---

# 23. Review Result

## 23.1 Review Issue Types  
  
Canonical issue types:  
- metadata_violation  
- parsing_error  
- semantic_issue  
New issue types require Task_Model update.

## 23.2 Review Result Model

Review service MUST return structured output:
```json  
{  
"status": "ok | warning | error",  
"issues": [  
{  
"type": "metadata_violation | parsing_error | semantic_issue",  
"field": "score | time | due | etc",  
"message": "human-readable explanation",  
"severity": "low | medium | high"  
}  
],  
"suggestions": [  
{  
"action": "fix | ignore | rewrite",  
"description": "what should be done"  
}  
]  
}
```

### Rules:

- всегда возвращается массив `issues` (даже если пустой)
- `status = ok` только если issues = []
- review НЕ должен мутировать задачу (только анализ)
- severity влияет только на рекомендации, не на структуру
