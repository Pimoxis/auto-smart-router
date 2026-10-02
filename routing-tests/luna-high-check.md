# Luna high check

## Model and effort preferences from `codex-smart-router`

- Substantial, well-specified extraction: `gpt-6-luna` / medium.
- Ordinary multi-step drafting, analysis, implementation, document preparation, or planning: `gpt-6-luna` / high.
- Ambiguous synthesis, difficult diagnosis, conflicting evidence, or consequential design: `gpt-6.1-sol` / high.
- Exceptionally difficult cross-domain reasoning or an unresolved hard question: `gpt-6-astra` / high.

This smoke test was explicitly assigned high effort.

## Tools used

- PowerShell `Import-Csv`, `Where-Object`, and `Measure-Object` to count and sum non-void rows from `routing-tests/invoices.csv`.
- `ConvertTo-Json` for the computed structure.
- No delegation or browsing.
