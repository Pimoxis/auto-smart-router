# GPT-6 Sol bounded check

The proposed flow does not meet the requirements. After the DB commit, a crash before capture leaves stock allocated; redelivery sees the duplicate ID and acknowledges it, so payment never happens. A crash after successful capture but before acknowledgement has the same duplicate path, so the DB may never record the payment. A capture timeout is ambiguous: retrying with a fresh request can charge twice, while acknowledging or releasing stock can abandon an actual charge.

Minimal repair: keep the unique event ID and transactional stock reservation, but persist a payment state (`pending`, then `paid` or definitively `failed`). Every delivery, including a duplicate, resumes a `pending` payment using the same stable provider idempotency key derived from that event/order ID and the same capture parameters. Record the confirmed provider result in the DB, then acknowledge. A confirmed decline can mark `failed`, release stock, and acknowledge. Never release reserved stock or treat a timeout as failure while capture may have succeeded. On redelivery after a successful capture, the same key must return the original result; then the worker records `paid` and acknowledges. A periodic scan of `pending` rows is a small recovery backstop if queue delivery or acknowledgement behavior fails.

The provider must guarantee one capture per idempotency key across concurrent calls and retries, return or expose a stable result for that key, and retain the key/result for the entire retry and reconciliation window. If its idempotency window is shorter, the system needs a reliable lookup/reconciliation by merchant reference before another capture. Without either guarantee, an unknown timeout cannot be resolved while assuring both no duplicate charge and eventual recovery. The DB must retain the stock reservation until payment is definitively failed or reversed, so a paid order always has stock.

Routing mini-cases:

1. Exact CSV sum with a local shell: use a short local script or existing tool; no model worker.
2. Tiny rewrite with “no subagents”: do it directly in the parent thread; no delegation.
3. User pins `gpt-6-terra`, but exposed tools do not list it: do not claim a switch or silently substitute. State that the pinned model is unavailable through current tools, recommend the model picker if it offers it, and continue only work that does not require that specific model.

This was a reasoning check; no payment system was run or verified.
