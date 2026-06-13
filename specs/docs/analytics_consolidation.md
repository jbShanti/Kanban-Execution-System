## WIP Metrics Migration

| Old Module | New Calculator | Status |
|---|---|---|
| `wip_analytics.py::analyze_wip()` | `calculators/wip_metrics.py::calculate_wip_metrics()` | ✅ Migrated |

### Design Decision
`calculate_wip_metrics` takes `Board` (not `list[Task]`) because WIP is a 
section-level metric. It returns `list[WipStatus]` instead of `dict[str, int]` 
because WIP status includes multiple fields (utilization, capacity, flags).

This is a deliberate deviation from the task-level calculator pattern, justified 
by the different abstraction level.


## Completed Migrations

### WIP Analytics (2026-01-XX)
- **Old**: `src/analytics/wip_analytics.py::analyze_wip()`
- **New**: `src/analytics/calculators/wip_metrics.py::calculate_wip_metrics()`
- **Status**: ✅ Migrated and old file deleted
- **Notes**: 
  - New calculator works directly with `Board` (not `SectionMetrics`)
  - Returns `list[WipStatus]` instead of complex nested structures
  - All tests passing, no usages of old code found