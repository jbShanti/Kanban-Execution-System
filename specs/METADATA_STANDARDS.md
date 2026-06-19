---
created: 2026-05-26
updated: 2026-05-26T23:42
description: Canonical metadata specification for the Kanban Execution System. Defines deterministic metadata syntax, validation rules, typing, parsing guarantees, and automation-compatible standards.
---
Canonical metadata specification for the Kanban Execution System.

Purpose:
- standardize metadata syntax
- ensure deterministic parsing
- reduce ambiguity
- support analytics and automation
- preserve human readability

This document defines:
- canonical metadata syntax
- supported metadata fields
- metadata typing
- validation rules
- parsing guarantees
- edge case handling
- namespace conventions

---

# 1. Core Principles

Metadata must be:

- machine-readable
- deterministic
- compact
- human-readable
- parser-safe

Metadata must NOT:

- require interpretation
- contain decorative syntax
- depend on formatting creativity
- contain unstable semantics

---

# 2. Canonical Metadata Syntax

## Standard Format

```text
[key::value]
```

Examples:

```md
[score::15]
[time::30m]
[priority::high]
```

---

## Syntax Rules

### Metadata MUST:

- start with `[`
- end with `]`
- contain exactly one `::`
- use lowercase keys
- avoid surrounding whitespace

---

## Valid Example

```md
[score::15]
```

---

## Invalid Examples

```md
[score : 15]
[Score::15]
[score=15]
[score::15::extra]
```

---

# 3. Metadata Placement Rules

## Recommended Placement

Metadata SHOULD appear:

```text
at the end of the task
```

Example:

```md
- [ ] Review architecture @{2026-05-30} [score::15] [time::45m]
```

---

## Metadata Ordering

Recommended order:

```text
deadlines
→ score
→ time
→ priority
→ tracking
→ finance
→ analytics
→ custom metadata
→ recurrence
```

---

# 4. Metadata Types

## Primitive Types

Supported types:

| Type | Example |
|---|---|
| integer | `15` |
| float | `1.5` |
| string | `high` |
| enum | `planned` |
| boolean | `true` |
| date | `2026-05-30` |
| duration | `30m` |

---

# 5. Canonical Metadata Registry

## score

### Syntax

```md
[score::15]
```

### Type

```text
integer
```

### Purpose

Execution importance and leverage weighting.

### Validation Rules

- minimum: 0
- maximum: 25
- integers only

---

## time

### Syntax

```md
[time::30m]
```

### Type

```text
duration
```

### Supported Formats

```text
5m
15m
30m
1h
2h
90m
```

### Invalid Formats

```text
30 minutes
1 hour
~30m
```

---

## due

### Canonical Syntax

```md
@{2026-05-30}
```

### Alternative Syntax

```md
[due::2026-05-30]
```

### Type

```text
date
```

### Validation Rules

Must follow:

```text
YYYY-MM-DD
```

---

## scheduled

### Syntax

```md
[scheduled::2026-05-30]
```

### Type

```text
date
```

### Meaning

Planned execution date.

NOT a hard deadline.

---

## start

### Syntax

```md
[start::2026-05-30]
```

### Type

```text
date
```

### Meaning

Activation date or recurrence baseline.

---

## completion

### Syntax

```md
[completion::2026-05-30]
```

### Type

```text
date
```

### Meaning

Historical completion tracking.

---

## repeat

### Syntax

```md
[repeat::every week]
```

### Type

```text
string
```

### Supported Examples

```text
every day
every week
every month
every year
every week on Sunday
every day when done
```

---

## priority

### Syntax

```md
[priority::high]
```

### Type

```text
enum
```

### Supported Values

```text
highest
high
medium
low
```

---

## analytics

### Syntax

```md
[analytics::ignore]
```

### Type

```text
enum flags
```

### Supported Values

```text
ignore
external
```

---

## finance

### Syntax

```md
[finance::planned]
```

### Type

```text
enum
```

### Supported Values

```text
planned
free
income
regular
extra
debts
skipped
```

---

## cost

### Syntax

```md
[cost::1500]
```

### Type

```text
integer
```

### Meaning

Numeric financial amount.

---

## currency

### Syntax

```md
[currency::RUB]
```

### Type

```text
string
```

### Supported Examples

```text
RUB
USD
EUR
CHF
```

---

## category

### Syntax

```md
[category::health]
```

### Type

```text
string
```

### Purpose

Semantic grouping.

---

# 6. Boolean Metadata

## Canonical Values

Supported:

```text
true
false
```

---

## Valid Example

```md
[blocked::true]
```

---

## Invalid Examples

```text
yes
no
1
0
TRUE
False
```

---

# 7. Date Standards

## Canonical Format

```text
YYYY-MM-DD
```

Example:

```text
2026-05-30
```

---

## Invalid Formats

```text
30.05.2026
05/30/2026
May 30
30 May
```

---

# 8. Duration Standards

## Canonical Units

| Unit | Meaning |
|---|---|
| m | minutes |
| h | hours |

---

## Valid Examples

```text
5m
30m
1h
2h
90m
```

---

## Invalid Examples

```text
30 minutes
1 hour
~1h
```

---

# 9. Metadata Namespace Rules

## Canonical Rule

All metadata keys MUST:

- be lowercase
- use ASCII characters
- avoid spaces

---

## Reserved Namespaces

Reserved keys:

```text
score
time
due
scheduled
start
completion
repeat
priority
analytics
finance
cost
currency
category
```

---

## Custom Metadata

Custom metadata SHOULD use:

```text
[x-namespace::value]
```

Example:

```md
[x-health::supplements]
[x-energy::low]
```

Purpose:
- avoid collisions
- preserve parser stability
- support future extensibility

---

# 10. Duplicate Metadata Rules

## Forbidden

Multiple identical metadata keys inside one task.

Invalid:

```md
[score::10] [score::15]
```

---

## Parser Behavior

If duplicates exist:

```text
first value wins
```

Later duplicates:
- ignored
- logged as parser warning

---

# 11. Unknown Metadata Rules

Unknown metadata is:

- preserved
- parsed as custom metadata
- ignored by deterministic analytics

Unless explicitly registered later.

---

# 12. Metadata Extraction Rules

Parser MUST extract:

- all metadata blocks
- all valid dates
- all canonical tags
- all links

Without modifying source text.

---

# 13. Metadata Stability Rules

Metadata semantics MUST remain:

- stable
- backward compatible
- deterministic

Avoid:
- changing meanings
- overloaded semantics
- implicit interpretation

---

# 14. Parser Safety Rules

Metadata parsing MUST NOT depend on:

- emojis
- indentation
- markdown decoration
- visual formatting
- line wrapping

Only:
- canonical syntax
- structural delimiters
- explicit metadata markers

---

# 15. Edge Cases

## Metadata Inside Text

Avoid:

```md
This is [score::15] inside normal text
```

unless intended as actual metadata.

---

## Broken Metadata

Broken metadata MUST:

- remain untouched
- generate parser warning
- not crash parser

Example:

```md
[score:15]
```

---

## Escaped Characters

Escaped brackets are treated as plain text.

Example:

```text
\[score::15\]
```

NOT metadata.

---

# 16. Analytics Compatibility

Metadata is designed to support:

- task scoring
- execution velocity
- overload analysis
- recurrence handling
- trend analysis
- reporting
- recommendation systems

Without requiring LLM interpretation.

---

# 17. Automation Compatibility

Metadata structure is optimized for:

- deterministic automation
- safe mutations
- recurring task generation
- archive handling
- parser resilience
- future workflow engines

---

# 18. Human Readability Rule

Metadata exists to support:

```text
human execution
+
machine processing
```

The system prioritizes:

```text
clarity
>
compact cleverness
```

---

# 19. Deterministic Parsing Rule

If metadata:
- creates ambiguity
- requires interpretation
- cannot be parsed reliably

Then:
- simplify
- normalize
- standardize

Parser reliability has priority over flexibility.

---

# 20. Future Compatibility

This metadata model is designed to support:

- parser layer
- analytics engine
- AI-assisted recommendations
- mutation systems
- reporting systems
- workflow orchestration
- automation runtime

Without requiring structural redesign.