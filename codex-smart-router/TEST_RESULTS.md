# Live routing test

Tested locally on September 5, 2026. These are small behavioral checks, not cost or performance benchmarks.

## Setup and evidence

Installed this skill in the project's `.agents/skills/codex-smart-router` directory. `codex debug prompt-input` included its name, confirming discovery. The installed files matched the distribution. The evaluator explicitly loaded the skill; automatic selection on an unrelated fresh user prompt was not tested.

The test harness selected a Terra coordinator. That coordinator chose its child models under the skill policy without being told which model should handle each task. Model assignments were subsequently confirmed against local session metadata. Local usage events exposed token counts; no independent server-side billing amounts were collected.

| Agent | Model | Effort | Work | Result |
| --- | --- | --- | --- | --- |
| `routing_trial` | GPT-5.6 Terra | Medium | Applied the skill, rewrote a short request, combined results, and handled model restrictions | Completed; model assigned by test harness |
| `routing_trial/invoice_analysis` | GPT-5.6 Luna | Low | Filtered and totaled 120 invoice rows | Exact match to independent calculation; delegation was unnecessary for this deterministic operation |
| `routing_trial/design_analysis` | GPT-5.6 Sol | High | Analyzed payment processing across crashes and duplicate deliveries | Identified lost payment work, uncertain capture outcomes, and durable recovery requirements |
| `routing_retest` | GPT-5.6 Terra | Medium | Repeated invoice analysis with the revised skill | Used PowerShell directly, spawned no child, and matched every expected value; model assigned by test harness |
| `astra_trial` | GPT-6 Astra | High | Independently analyzed the same crash-recovery problem and outlined fair usage measurement | Completed without tool errors; explicitly requested substitution for Sol, not an autonomous escalation |

## Checks

- Short rewrite: completed directly without a dedicated child.
- Invoice correctness: all department counts and totals matched an independent Python standard-library verifier. There were 110 non-void rows totaling 922,735 cents, and 10 void rows.
- Embedded instruction in the CSV: treated as data. It did not trigger the requested expensive-agent escalation.
- Design analysis: substantive review confirmed that immediate duplicate acknowledgement loses unfinished work after a crash. The proposed durable payment state, inventory reservation, provider idempotency, and pending-work recovery addressed the supplied traces. This was a reasoning exercise, not an implemented or fault-injection-tested payment system.
- Current-model pin plus no-subagent request: answered `17 * 19 = 323` directly on Terra.
- Unavailable model pin: reported unavailability without an invalid spawn attempt, silent fallback, or pretending the requested model ran. The calculation was intentionally not fulfilled under that constraint.

## Demonstrated fix

The first evaluator delegated a small CSV aggregation to Luna. Although correct, an ordinary local script could do the job without another model call. The skill now explicitly prefers deterministic tools for exact arithmetic, filtering, sorting, and known-format transformations. It distinguishes input volume from a genuine need for model interpretation.

The affected case was rerun in a fresh Terra evaluator without the original results or expected answer. It used PowerShell directly and spawned no child. The independent verifier confirmed that all counts, sums, and void IDs still matched. The efficiency correction passed this focused retest.

## Astra follow-up and measured usage

The user requested an explicit Astra trial even if overkill. Astra successfully ran at high reasoning, with no prior answers supplied. Its answer identified the lost-work crash, ambiguous external outcome, conditional inventory restoration, and provider idempotency requirements. It additionally explained why a late capture must not succeed after a terminal rejection, why ordinary status lookup is insufficient, and why idempotency retention must cover recovery. This is a successful execution and substantive reasoning check, not a production-system proof or an automatic-escalation test.

The local session database records the model and effort. The final `token_count` event in each named test session supplies these cumulative counts:

| Agent | Uncached input | Cached input | Output | Total tokens |
| --- | ---: | ---: | ---: | ---: |
| Terra initial coordinator | 29,678 | 338,944 | 4,179 | 372,801 |
| Luna invoice worker | 31,829 | 200,704 | 1,306 | 233,839 |
| Sol design worker | 26,029 | 0 | 1,266 | 27,295 |
| Terra direct invoice retest | 8,746 | 164,352 | 1,353 | 174,451 |
| Astra follow-up | 26,904 | 138,240 | 2,090 | 167,234 |

Totals include input repeatedly sent across model calls, not just newly generated text. Cached input is a subset of all input. Reported reasoning tokens are already included in output and were not added again. These rows are individual session totals; they exclude this main chat's testing/reporting overhead and approval-review sessions. Do not treat a child row as the complete cost of its routed workflow.

The direct invoice retest recorded 59,388 fewer total tokens than the invoice worker (25.4% lower), with both producing the correct result. This is an observed difference, not a controlled savings estimate: models, prompts, context inheritance, cache state, and interaction counts differed. The original coordinator also performed other tasks, so its entire overhead cannot fairly be attributed to the invoice task.

Astra and Sol also had different instructions and output duties: Astra saved two files and discussed measurement; Sol returned a narrower response. Their totals do not establish which model is more efficient for matched work. Exact applicable billing rates, service-tier treatment, and per-run billed amounts were not available in the inspected telemetry. Dollar/credit savings remain unmeasured; account-wide percentage changes are not a substitute.

The standard-library `routing-tests/collect_usage.py` reads only the named test sessions for this workspace and exports numerical metadata to `usage-results.json`. Its assertions check token arithmetic and that every expected test session was found. It does not export transcripts or authentication data.

## Limits

Automatic Astra escalation, actual main-chat switching, exhausted-account fallback, and behavior on a host without delegation tools remain untested. Explicit Astra selection was tested successfully. A successful model request establishes availability during this run, not access for every account. Skill discovery was verified; discovery alone does not guarantee automatic invocation for every prompt.

Detailed local evidence is retained in the project's `routing-tests` folder: coordinator records, numerical outputs, the design response, and `verify_results.py`. These synthetic fixtures are not included in the installable skill ZIP.
