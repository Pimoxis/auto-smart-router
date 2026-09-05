# Codex Smart Router

A general-purpose Codex skill for cost-conscious task routing across writing, research, planning, documents, data, coding, and automation.

It keeps small tasks in the main chat, uses deterministic tools for exact calculations, and delegates worthwhile subtasks to suitable available models.

## Install

Download [codex-smart-router.zip](codex-smart-router.zip), extract it, and copy the `codex-smart-router` folder into the skills directory your Codex installation uses. For a single project, use `.agents/skills/` inside that project.

See [setup instructions](codex-smart-router/SETUP.md) for personal installation, activation, and compatibility details.

Then select the skill or ask:

```text
Use $codex-smart-router for this task: [your task].
```

## Default routing

| Work | Preferred model / reasoning |
| --- | --- |
| Small tasks and exact operations handled by tools | Current main-chat model |
| Bounded work requiring simple model interpretation | GPT-5.6 Luna / Low |
| Ordinary multi-step work | Current parent; Terra / Medium for suitable independent work |
| Hard diagnosis, ambiguous synthesis, or consequential design | GPT-5.6 Sol / High |
| Exceptionally difficult reasoning | GPT-6 Astra / High |

These are preferences, subject to available tools, model access, and explicit user choices. The skill can select supported child models; it does not automatically switch the main chat's model. It preserves existing service-tier settings.

## Validation

Live tests exercised Terra, Luna, Sol, and explicitly selected Astra. Tests covered extraction correctness, model restrictions, and treating embedded source instructions as data. A demonstrated efficiency fix made exact CSV aggregation run directly through local tools.

Read the [test report](codex-smart-router/TEST_RESULTS.md) for measured token counts and limitations. Dollar savings have not been established; the recorded runs are not a controlled benchmark.

With Python 3.9 or newer, run from this repository:

```sh
python check_package.py
python routing-tests/verify_results.py
python routing-tests/verify_results.py extraction-retest.json
```

`routing-tests/collect_usage.py` is specific to the original local test sessions and is not a portable benchmark. The committed `usage-results.json` preserves the measured counts without session transcripts.

The ZIP contains the same skill files as `codex-smart-router/`. Local installation does not change your global settings.
