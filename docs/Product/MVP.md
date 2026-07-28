# KES MVP

## Product Goal

KES MVP turns one existing Obsidian Markdown Kanban board into a concise, deterministic daily execution review. It solves the problem of a board that contains tasks but does not clearly reveal workload pressure, overdue commitments, data-quality gaps, or the most important conditions affecting execution.

The MVP helps one person understand the state of their work quickly enough to make their own next decision with confidence. It improves judgment; it does not make decisions or change the board.

## Target User

The MVP is for a single person who already maintains a Markdown Kanban board in Obsidian and wants a reliable review of that board without adopting another task manager or manually calculating its health.

The user is willing to keep task statuses, sections, scores, dates, and tags in the documented format. They remain responsible for priorities, strategic choices, and board changes.

## User Journey

1. The user provides one supported Markdown Kanban board.
2. KES reads the board and clearly reports any data or formatting problems that limit reliable analysis.
3. KES produces one deterministic daily review for the supplied board and analysis time.
4. The user reads a concise view of board health, active workload, WIP pressure, overdue or stale work, score distribution, and data-quality limitations.
5. The user uses these evidence-based insights to choose what to work on, what to defer, and what to correct on the board.
6. The user updates the board themselves; KES does not modify it.

## Functional Scope

The MVP must provide:

- analysis of one Markdown Kanban board using the documented task and metadata conventions;
- clear validation feedback for unsupported or unreliable input;
- a human-readable daily review generated from the board without modifying it;
- deterministic board-health and data-quality assessment, including an explicit reliability qualification when the board is incomplete;
- active-workload, section/WIP, overdue, stale-work, status, score-corridor, and section-level insights where the board supplies the needed data;
- concise, traceable findings that explain the condition and its evidence rather than only showing raw counts;
- stable output for the same board, configuration, and analysis time;
- an explicit statement when deterministic recommendations have not been produced.

The review must be useful even when the board is imperfect: it should first make limitations visible, then present only conclusions supported by the available information.

## Out of Scope

The MVP intentionally excludes:

- a Recommendation Engine, operating-mode selection, High Five, or system-generated task priorities;
- LLM analysis, conversational assistance, personalization, or adaptive ordering;
- automatic board mutations, task creation, archival, scheduling, or deletion;
- dashboards, notifications, mobile applications, and external integrations;
- multi-user collaboration, permissions, team planning, and project-management features;
- vault-wide aggregation, historical trends, forecasts, and scenario simulation;
- task-improvement, inbox-structuring, score-optimization, and schedule-planning features.

These exclusions protect the MVP from becoming a task manager, an autonomous agent, or a speculative productivity platform.

## Success Criteria

KES MVP is complete when a target user can:

1. provide a supported board without programming against internal APIs;
2. receive a concise daily review without the board being modified;
3. see whether the board is reliable enough for meaningful analysis;
4. identify execution risks such as overload, overdue work, stale work, and incomplete metadata;
5. understand the evidence behind each reported condition;
6. obtain the same review from the same board, configuration, and analysis time; and
7. decide what to inspect, correct, defer, or work on next using their own judgment.

## MVP Principles

1. **Execution insight over task storage.** KES improves an existing board; it does not replace it.
2. **One user, one board, one review.** Solve the smallest complete use case before expanding scope.
3. **Determinism before intelligence.** The same inputs produce the same conclusions.
4. **Evidence before advice.** Every insight must be understandable and traceable to board information.
5. **Honest uncertainty.** Missing or unreliable data is a primary result, not a hidden edge case.
6. **Human authority remains final.** KES informs choices and never makes or applies them in the MVP.
7. **No hidden change.** The MVP is read-only with respect to the user’s board.
8. **Cognitive economy.** The review emphasizes the few conditions that materially affect execution.

## Scope Authority

This document is the single source of truth for KES MVP product scope. Architecture, task models, analytics specifications, implementation guidance, and future roadmaps must align with this MVP boundary; they must not add MVP features implicitly.
