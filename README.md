# Kanban Execution System

Markdown-based personal execution system designed for structured task management, analytics, and AI-assisted planning.

## Features

* Markdown Kanban board parser
* Strong domain model
* Section classification
* Task metadata extraction
* WIP analytics
* Regression-tested parser
* Golden and pathological fixtures

## Project Structure

```text
src/
├── parser/
├── analytics/
└── domain/

tests/
├── fixtures/
├── test_parser.py
├── test_parser_golden.py
└── test_wip.py

docs/
├── domain_contracts.md
├── METADATA_STANDARDS.md
├── SYSTEM_BOUNDARIES.md
└── KANBAN_EXECUTION_SYSTEM.md
```

## Status

Current milestone:

* Domain model stabilized
* Parser stabilized
* Golden test suite completed
* Pathological test suite completed

Next milestone:

* Metadata extraction hardening
* Section metadata parsing
* Analytics reports
* CLI layer
* MCP integration
