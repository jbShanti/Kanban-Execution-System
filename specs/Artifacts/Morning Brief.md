# MORNING BRIEF

## 1. Vision

The MorningBrief is the primary user-facing artifact of the Kanban Execution System.

It is the first interaction between the user and the system each day.

Its purpose is not to present analytics, but to help the user make better execution decisions.

The MorningBrief should allow the user to understand the current state of the system and determine today's priorities in less than one minute.

---

## 2. Purpose

The MorningBrief transforms an `ExecutionReport` into a concise, actionable daily briefing.

It answers five questions:

1. What is the current situation?
2. What deserves my attention today?
3. What should I do first?
4. What should I avoid today?
5. Is the system healthy?

---

## 3. Reading Flow

The Morning Brief is organized into two consecutive phases.

### Phase 1 — Execute Today's Work

The first phase helps the user begin productive work as quickly as possible.

It answers three essential questions:

1. **What is happening?** — Executive Situation
2. **How should I work today?** — Operating Mode
3. **What should I work on first?** — Today's Priorities

After completing this phase, the user should have everything necessary to start executing work immediately.

---

### Phase 2 — Improve the Execution System

The second phase helps the user improve the effectiveness of the Kanban execution system itself.

It answers three additional questions:

1. **What should I improve?** — Recommended Actions
2. **How healthy is the system?** — System Health


This phase is intended to improve long-term execution quality without delaying the start of productive work.


---

## 4. Design Principles

The MorningBrief must:

* prioritize execution over analysis;
* minimize cognitive load;
* communicate only information relevant to today's execution;
* remain stable in structure between days;
* transform analytical results into clear decisions.

Every section must conclude with a clear conclusion, recommendation, or suggested action.

---

## 5. Input Contract

The MorningBrief accepts exactly one input:

```text
ExecutionReport
```

The `ExecutionReport` is the only source of truth.

The MorningBrief must not access the Board or intermediate analytical artifacts directly.

## 6. ExecutionReport Mapping

| MorningBrief Section | Source in `ExecutionReport`                                                     |
| -------------------- | ------------------------------------------------------------------------------- |
| Executive Situation  | `ExecutiveSummary`                                                              |
| Operating Mode       | `RecommendationCollection.OperatingMode`                                        |
| Today's Priorities   | `RecommendationCollection.TaskRecommendations`                                  |
| Recommended Actions  | `RecommendationCollection.StrategicRecommendations` + `TacticalRecommendations` |
| System Health        | `BoardHealth`                                                                   |



### Completeness Rule

Every required MorningBrief section MUST have exactly one corresponding source within the `ExecutionReport`.

A section may consume multiple objects from the `ExecutionReport`, but it must not access analytical artifacts outside of the `ExecutionReport`.

Every object in the `ExecutionReport` should have at least one consumer within the MorningBrief or another presentation artifact.

---

## 7. Output Contract

Target reading time:

**30–60 seconds**

Maximum reading time:

**2 minutes**

Given the same `ExecutionReport`, the MorningBrief must communicate the same conclusions and recommended actions.

An LLM may improve wording, readability, and style, but it must not introduce analytical conclusions that are not supported by the `ExecutionReport`.

---


## 8. Generation Pipeline

```text
Board
        ↓
Analytics Engine
        ↓
ExecutionReport
        ↓
MorningBrief Generator
        ↓
MorningBrief
```

The MorningBrief performs no analytical calculations.

Its sole responsibility is to transform an `ExecutionReport` into a human-readable daily briefing.

---

## 9. Canonical Structure

Every MorningBrief must contain the following sections:

1. Executive Situation
2. Operating Mode
3. Today's Priorities
4. Recommended Actions
5. System Health

Optional sections may be included when supported by the `ExecutionReport`, but they must never replace the required sections.

---

## 10. Section Specifications

This section defines the contract for every MorningBrief section.

Each section specification should describe:

* purpose;
* source data from the `ExecutionReport`;
* required content;
* optional content;
* rendering constraints;
* required conclusion or recommendation.

---

### Executive Situation

#### Purpose

The **Executive Situation** provides the user with an immediate understanding of the current execution state.

It serves as the entry point to the MorningBrief and establishes the context for all subsequent sections.

The user should understand the overall situation within a few seconds, without reading the remainder of the briefing.

---

#### Source Data

Derived exclusively from the `ExecutionReport`.

Primary sources include:

* `ExecutiveSummary`
* High-priority findings
* Overall execution assessment

The section must not access analytical models directly.

---

#### Required Content

The section must communicate:

* the overall execution state;
* the most significant characteristic of the current day;
* the primary factor influencing execution.

The information should be presented as a concise narrative rather than a list of metrics.

---

#### Optional Content

When supported by the `ExecutionReport`, the section may additionally include:

* significant change since the previous execution cycle;
* exceptional conditions requiring immediate attention;
* positive achievements worth highlighting.

Optional information must improve situational awareness without increasing cognitive load.

---

#### Rendering Constraints

The section should contain no more than **2–3 short paragraphs**.

Raw analytical data, detailed metrics, and implementation details should be avoided unless they are essential for understanding the situation.

Priority should always be given to interpretation over observation.

---

#### Actionability Requirement

The section must conclude with a clear conclusion describing the current execution state.

If immediate action is required, the conclusion must explicitly state the highest-priority recommendation.

The user should never need to infer what the overall situation means.

---

#### Example Outcome

The reader should finish this section with a clear understanding of:

* where the system currently stands;
* what defines today's execution context;
* whether immediate corrective action is required.

---

### Operating Mode

#### Purpose

The Operating Mode communicates the execution mode that best matches the current state of the system.

It establishes the behavioral context for all work performed during the day.

All subsequent recommendations and priorities should be interpreted within the context of the selected Operating Mode.

Unlike **Today's Priorities**, this section focuses on *how to work*, not *what to work on*.

---

#### Source Data

Derived exclusively from the `ExecutionReport`.

Primary sources include:

* `ExecutiveSummary`
* `RecommendationCollection`
* Cross-cutting analytical conclusions

The section must not access analytical models directly.

---

#### Required Content

The section must communicate:

* the primary execution strategy for the day;
* the key behavioral principle that should guide decision-making;
* any global execution constraints that apply today.

The strategy should remain valid regardless of the individual tasks selected for execution.

---

#### Optional Content

When supported by the `ExecutionReport`, the section may additionally include:

* workload balancing guidance;
* context-switching recommendations;
* focus management advice;
* execution pacing recommendations;
* portfolio-level strategic guidance.

Optional content must reinforce a single coherent execution strategy rather than introduce competing ideas.

---

#### Rendering Constraints

The section should contain:

* one primary strategy;
* no more than three supporting principles.

Each principle should be expressed as a short, actionable statement.

---

#### Actionability Requirement

The section must conclude with a clear execution recommendation describing how the user should approach today's work.

The user should finish this section with a clear understanding of the execution strategy that should guide every decision throughout the day.

---

#### Example Outcome

The reader should finish this section with a clear understanding of:

* how today's work should be approached;
* which execution principles take precedence;
* which behaviors should be encouraged or avoided throughout the day.

---
### Today's Priorities

#### Purpose

The **Today's Priorities** section identifies the highest-priority tasks recommended for execution during the current day.

Its purpose is to translate analytical recommendations into a clear, actionable list of tasks that should receive the user's primary attention.

Unlike **Operating Mode**, which defines *how to work*, this section defines *what to work on*.

---

#### Source Data

Derived exclusively from:

* `RecommendationCollection.TaskRecommendations`

The section must not access analytical models directly.

---

#### Required Content

The section must include:

* the recommended tasks for today;
* the priority order of those tasks;
* the recommendation rationale for each task.

Each task should clearly communicate why it has been selected.

---

#### Optional Content

When available, the section may additionally include:

* estimated effort;
* expected impact;
* dependencies;
* blocking conditions.

Optional information should improve decision-making without increasing cognitive load.

---

#### Current Implementation

In the current implementation, the unit of prioritization is an individual Task.

Future versions may support higher-level work items such as Projects or Initiatives.

---

#### Rendering Constraints

The section should present a concise list of recommended tasks.

The number of displayed tasks should remain limited to maintain focus and support effective execution.

Tasks should be ordered by recommendation priority.

Each task should include a brief explanation that can be understood within a few seconds. 


---

#### Actionability Requirement

The section must conclude with a clear recommendation indicating which task should be started first.

The user should finish this section with an unambiguous understanding of what to work on next.

---

### Recommended Actions

#### Purpose

The **Recommended Actions** section identifies improvements that should be made to the execution system in order to increase its effectiveness.

Its purpose is to translate analytical recommendations into concrete actions that improve the quality, stability, and sustainability of the user's Kanban system.

Unlike **Today's Priorities**, which focuses on executing work, this section focuses on improving the system used to execute that work.

---

#### Source Data

Derived exclusively from:

* `RecommendationCollection.StrategicRecommendations`
* `RecommendationCollection.TacticalRecommendations`

The section must not access analytical models directly.

---

#### Required Content

The section must include:

* the recommended system improvements;
* the recommendation rationale for each action;
* the expected benefit of implementing each recommendation.

Each recommendation should clearly communicate why it has been generated and what improvement it is intended to achieve.

---

#### Optional Content

When available, the section may additionally include:

* implementation priority;
* estimated effort;
* expected impact;
* dependencies;
* supporting analytical evidence.

Optional information should help the user evaluate recommendations without increasing cognitive load.

---

#### Current Implementation

In the current implementation, recommended actions focus exclusively on improvements to the Kanban execution system.

Future versions may additionally include recommendations related to long-term planning, workflow optimization, and personal productivity.

---

#### Rendering Constraints

The section should present a concise list of recommended actions.

Actions should be ordered by recommendation priority.

Each action should include:

* a short actionable statement;
* a brief recommendation rationale;
* the expected benefit of implementing the recommendation.

Recommended Actions should recommend changes to the execution system rather than the execution of individual tasks.

Recommendations that instruct the user to perform specific tasks belong to **Today's Priorities**, not to this section.

---

#### Actionability Requirement

The section must conclude with a clear recommendation identifying the most valuable system improvement to perform today.

The user should finish this section with a clear understanding of how the execution system itself can be improved.

---

### System Health

#### Purpose

The **System Health** section provides a concise assessment of the current operational health of the Kanban execution system.

Its purpose is to communicate the overall reliability of the board and highlight any conditions that may reduce the accuracy or usefulness of analytical conclusions.

Unlike **BoardHealth**, which represents a complete analytical model, this section presents only the information necessary to support informed decision-making.

---

#### Source Data

Derived exclusively from:

* `BoardHealth`

The section must not access analytical models directly.

---

#### Required Content

The section must include:

* the current Board Health status;
* a concise explanation of the current health assessment;
* the primary factor affecting the current health status.

The section should enable the user to understand whether the analytical conclusions can be considered reliable.

---

#### Optional Content

When available, the section may additionally include:

* current analytical coverage;
* the number of orphan tasks;
* the most significant metadata issue;
* a brief trend indication compared to the previous report.

Optional information should improve situational awareness without increasing cognitive load.

---

#### Current Implementation

In the current implementation, the section is derived exclusively from `BoardHealth`.

Future versions may additionally include execution quality indicators, workflow health metrics, and historical trends.

---

#### Rendering Constraints

The section should present a concise health summary that can be understood within a few seconds.

The health status should be expressed using its canonical classification:

* Excellent
* Good
* Warning
* Poor
* Awful
* Critical

The explanation should focus on the single most important factor influencing the current health status.

Detailed analytical metrics should remain within `BoardHealth` and should not be duplicated unless they improve understanding.

---

#### Actionability Requirement

The section must conclude with a clear recommendation describing the single most important improvement that would increase the overall health of the execution system.



---

## 11. Rendering Rules

Rendering rules define how information is presented to the user.

They include:

* ordering of sections;
* formatting conventions;
* verbosity limits;
* emphasis rules;
* language and tone;
* Markdown formatting.

These rules affect presentation only and must not change analytical meaning.

---

## 12. Future Extensions

Future versions of the MorningBrief may introduce additional presentation features, including:

* adaptive verbosity;
* audience-specific rendering;
* personalized recommendations;
* multimodal presentation;
* localization.

Any extension must preserve compatibility with the canonical `ExecutionReport` and must not alter the analytical pipeline.
