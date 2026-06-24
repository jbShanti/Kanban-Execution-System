# IMPLEMENTATION_GUIDE.md

# Purpose

This document defines the implementation strategy for Kanban Execution System.

Its purpose is to ensure that all contributors, human or AI, implement the system consistently and according to the canonical architecture.

This document complements:

* README.md
* KANBAN_EXECUTION_SYSTEM.md
* SYSTEM_BOUNDARIES.md
* TASK_MODEL.md
* METADATA_STANDARDS.md
* ANALYTICS_MODEL_V2.md

If implementation conflicts with canonical documents, canonical documents take precedence.

---

# Development Philosophy

The system must be built from the inside out.

Implementation order is mandatory.

```text
Foundation
↓
Parser
↓
Analytics
↓
Recommendations
↓
Automation
```

Skipping phases is prohibited.

Introducing future-phase functionality into earlier phases is prohibited.

---

# MVP Definition

The MVP boundary is fixed.

## MVP Includes

```text
Markdown Vault
↓
Parser Layer
↓
Task Objects
↓
Analytics Engine
↓
Analytics Report
```

### Components

* Parser Layer
* Task Model
* Metadata Processing
* Analytics Engine
* Markdown Report Generation

---

## MVP Excludes

* Recommendation Engine
* LLM Analysis
* Automation Layer
* Dashboards
* Notifications
* External Integrations

These belong to future phases.

---

# Canonical Data Flow

The following pipeline defines the official processing sequence.

```text
Obsidian Vault
↓
Markdown Files
↓
Parser Layer
↓
Task Objects
↓
Analytics Engine
↓
Analytics Report
↓
Human Review
```

Future phases may extend this pipeline but may not bypass it.

---

# Repository Structure

Recommended project structure:

```text
src/

├── parser/
│   ├── markdown_parser.py
│   ├── metadata_parser.py
│   ├── validators.py
│   └── normalizers.py
│
├── models/
│   ├── task.py
│   ├── analytics.py
│   └── report.py
│
├── analytics/
│   ├── workload.py
│   ├── focus.py
│   ├── corridor.py
│   ├── quality.py
│   └── executive_summary.py
│
├── reporting/
│   ├── markdown_renderer.py
│   └── templates/
│
├── recommendations/
│
├── automation/
│
└── tests/
```

The recommendations and automation folders may exist before implementation but must remain inactive until their respective roadmap phases.

---

# Parser Layer

## Goal

Transform Markdown into deterministic Task Objects.

Parser behavior must be deterministic.

Parser must not use LLMs.

---

## Responsibilities

### Task Extraction

Extract all task entities from source Markdown.

---

### Metadata Extraction

Extract metadata according to METADATA_STANDARDS.md.

---

### Section Detection

Detect:

* project sections
* operational sections
* hierarchy
* grouping structures

---

### Archive Detection

Implement archive semantics defined by TASK_MODEL.md.

---

### Validation

Detect:

* malformed metadata
* unsupported statuses
* structural violations

Validation must never silently discard data.

---

### Normalization

Produce canonical Task Objects.

All downstream systems must consume normalized objects only.

---

# Parser Output Contract

The Parser Layer produces a collection of Task Objects.

Conceptually:

```text
Markdown
↓
TaskObject[]
```

Every task must conform to the canonical Task Model.

No analytics logic may exist inside the parser.

No recommendations may exist inside the parser.

---

# Definition of Done — Parser

Parser is considered complete when:

* tasks are extracted correctly
* metadata is extracted correctly
* archives are detected correctly
* validation is implemented
* normalization is implemented
* deterministic behavior is verified
* test coverage exists for supported syntax

The parser must successfully process a real vault.

---

# Analytics Layer

## Goal

Transform Task Objects into Analytics Reports.

Analytics must be deterministic.

Analytics must not use LLMs.

---

# Analytics Responsibilities

## Focus Analytics

Measure:

* attention concentration
* active priorities
* urgency distribution

---

## Workload Analytics

Measure:

* active workload
* overdue pressure
* execution capacity

---

## Strategic Analytics

Measure:

* project distribution
* value allocation
* portfolio balance

---

## Data Quality Analytics

Measure:

* metadata completeness
* consistency
* structural quality

---

## Corridor Analytics

Implement the corridor methodology defined in ANALYTICS_MODEL_V2.md.

---

## Executive Summary

Generate deterministic conclusions based on metrics.

No AI interpretation.

Only rule-based synthesis.

---

# Analytics Output Contract

Conceptually:

```text
TaskObject[]
↓
Analytics Engine
↓
AnalyticsReport
```

AnalyticsReport becomes the canonical output of Phase 2.

No recommendations are generated here.

---

# Definition of Done — Analytics

Analytics is complete when:

* all analytical domains are implemented
* all required metrics are calculated
* corridor analysis works
* executive summary is generated
* markdown report rendering works
* deterministic behavior is verified

---

# Report Generation

## Goal

Generate human-readable analytical reports.

Reports must contain:

* Executive Summary
* Focus Analysis
* Workload Analysis
* Strategic Analysis
* Corridor Analysis
* Data Quality Analysis

Reports should be understandable without access to raw data.

---

# Testing Strategy

Every layer requires tests.

---

## Parser Tests

Must validate:

* task extraction
* metadata extraction
* archive handling
* malformed input handling

---

## Analytics Tests

Must validate:

* metric calculations
* score calculations
* corridor calculations
* report generation

---

## Integration Tests

Must validate:

```text
Vault
↓
Parser
↓
Analytics
↓
Report
```

end-to-end execution.

---

# Recommendation Engine (Future Phase)

This phase begins only after MVP completion.

Input:

```text
AnalyticsReport
```

Output:

```text
RecommendationCollection
```

Responsibilities:

* prioritization recommendations
* overload interpretation
* focus recommendations
* simplification proposals

Recommendations must not modify source data.

Recommendations are advisory only.

---

# Automation Layer (Future Phase)

This phase begins only after Recommendation Engine completion.

Automation may execute approved actions only.

Every action must be:

* deterministic
* reversible
* auditable

Human approval remains mandatory.

---

# Acceptance Criteria For MVP

The MVP is considered complete when:

1. A real Obsidian vault can be processed.
2. Markdown is transformed into Task Objects.
3. Task Objects are transformed into Analytics Reports.
4. Reports are rendered successfully.
5. No LLM dependency exists in Parser or Analytics.
6. Processing is deterministic and repeatable.

Official MVP pipeline:

```text
Markdown Vault
↓
Parser Layer
↓
Task Objects
↓
Analytics Engine
↓
Analytics Report
```

Any functionality beyond this boundary is not required for MVP completion.
