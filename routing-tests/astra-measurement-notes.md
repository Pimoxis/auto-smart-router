# Fair model token and cost comparisons

Compare matched runs on the same task set, input/context, acceptance criteria, tool access, reasoning effort, output limits, and completion policy. Record the exact model/version and repeat across enough tasks/runs to distinguish normal variation. Score correctness and completion independently: a cheaper incorrect or incomplete answer is not equivalent work.

For every root and delegated call, collect attributable provider or rollout usage: uncached input, cached input, output, and reasoning tokens where exposed. Determine whether reasoning tokens are already included in output before summing. Include routing, delegation, retries, tool-result context, and verification overhead. Record cache conditions, latency, tool usage, failures, and quality alongside token totals. Model tokenizers can differ, so fewer tokens alone does not establish lower cost.

Convert billable usage into money only with verified applicable rates for the exact model, service tier, cache category, and billing arrangement at the time of the run, including separately billed tools. Otherwise report measured token differences with cache usage separated and label dollar savings unavailable. Account-wide percentage changes and unmatched historical runs do not establish per-task costs or causal savings.

For matched successful runs, report absolute usage/cost and savings relative to the baseline, together with variability and quality results. No prices, token counts, or savings are assumed here.
