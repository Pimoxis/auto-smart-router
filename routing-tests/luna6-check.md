# Luna 6 extraction check

- Input read: `routing-tests/invoices.csv` only. Notes were treated as data and not interpreted.
- Tool: PowerShell `Import-Csv`, `Group-Object`, and integer (`Int64`) accumulation; JSON written with `ConvertTo-Json`.
- Method: excluded `status=void` rows from departments and grand total; collected void IDs in source order; counted non-void `status=paid` rows.

## Separate policy cases

- Exact CSV totals with shell: appropriate for deterministic aggregation; used this path.
- User says “no subagents”: honor it; do not delegate.
- All GPT-6 models unavailable, GPT-5.6 Terra available: route to GPT-5.6 Terra if a model selection is needed and tool permits it.
- Parent is GPT-5.6 and no parent-switch tool exists: continue on the parent; report that a parent model switch is unavailable rather than claiming a switch.
