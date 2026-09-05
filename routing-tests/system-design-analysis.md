# Queue payment design diagnosis

The design does not meet the requirements. After trace A, redelivery sees the inbox duplicate and acknowledges it, so payment is never attempted. Trace B can leave a successful charge unrecorded internally. Trace C forces an unsafe choice: retry and risk a duplicate charge, or stop and violate eventual processing. Allocating inventory before capture does prevent a successful payment without prior allocation, but the allocation and payment state are not recoverable together.

Use these smallest durable transitions:

1. In one transaction, allocate inventory and create `PAYMENT_PENDING`. Record out-of-stock as terminal `FAILED`. Duplicate delivery reads the saved state instead of immediately acknowledging.
2. Capture each pending payment with a stable business-payment idempotency key. Persist `PAID` and the provider reference on success; release inventory and persist `FAILED` on a definitive failure. Do not release inventory after an unknown result.
3. Acknowledge only terminal states. Redelivery or a periodic sweeper resumes pending records, safely retries or queries the provider, and persists the definitive result.

The payment provider needs durable idempotency for the business payment identity and repeatable result lookup, or a retry that is provably safe after a timeout. Unique event IDs are not enough if multiple events can refer to one payment. Without provider idempotency or authoritative outcome lookup, no duplicate charges and eventual completion after an unknown response cannot both be guaranteed.

Rollout:

1. Add payment state, stable idempotency key, provider reference, and business-level uniqueness; backfill existing inbox records.
2. Canary the state-driven handler and reconciliation sweeper, exercise all three crash traces, and monitor duplicate attempts, pending age, and inventory releases.
3. Ramp traffic, reconcile and drain legacy pending records, then remove immediate duplicate acknowledgement and legacy paths.
