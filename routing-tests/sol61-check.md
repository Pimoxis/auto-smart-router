# Routing answers

The four selectable task/model/effort assignments in the skill are:

| Task | Model | Effort |
| --- | --- | --- |
| Substantial, well-specified extraction, classification, formatting, repetitive edits, or narrow source gathering | `gpt-6-luna` | medium |
| Ordinary multi-step drafting, analysis, implementation, document preparation, or planning | `gpt-6-luna` | high |
| Ambiguous synthesis, difficult diagnosis, conflicting evidence, subtle logic, or consequential design | `gpt-6.1-sol` | high |
| Exceptionally difficult cross-domain reasoning or a hard question still unresolved after an evidence-based attempt | `gpt-6-astra` | high |

Tiny work stays with the current supported GPT-6 parent without a handoff. These are starting preferences, not guaranteed availability or a price ranking.

If only an older Sol is available, report the limitation; do not substitute it. If the parent is older, request a supported GPT-6 selection through the model picker before routed work. The skill cannot switch the parent itself.

Exact CSV sums normally need a short deterministic local script or existing tool, not another model. Use arithmetic appropriate to the data (for example, decimal arithmetic for exact decimal amounts).

# Independent design analysis

**Crash before capture:** the transaction leaves stock allocated and the event ID recorded. Redelivery immediately acknowledges the duplicate, so capture is permanently skipped unless a separate recovery mechanism exists.

**Crash after successful capture:** stock exists, but local completion may be unknown. Duplicate acknowledgement conceals unfinished bookkeeping. Retrying capture without provider protection can double-charge.

**Ambiguous timeout:** the payment may have succeeded or may still succeed. Neither a fresh capture nor releasing stock is safe based on the timeout alone.

**Smallest repair:** turn the existing event row into a durable payment-work record. In the stock transaction, reserve stock and persist pending state plus a stable payment-operation key. After commit, capture with that key, persist confirmed success, then acknowledge. Duplicates inspect state: completed work can acknowledge; pending work resumes or reconciles. A recovery loop scans pending records so queue acknowledgement, lost delivery, or dead-lettering cannot strand them. Concurrent attempts must use the same key and guarded state transitions. Keep stock reserved while payment is unresolved; release it only after definitive failure or cancellation that rules out a later capture.

**Provider guarantees:** repeated and concurrent requests with the same key and identical parameters produce at most one charge; the operation remains identifiable throughout recovery. The provider must replay or expose an authoritative outcome, including late success after timeout, and eventually resolve pending outcomes. A finite idempotency retention window is insufficient if recovery can outlive it without permanent lookup and a safe retry protocol. Eventual provider/database availability and continued recovery retries are also required. Without these guarantees, the database transaction alone cannot ensure both no double charge and eventual recovery.

This model selection is a smoke test, not evidence of automatic escalation. No delegation, browsing, or implementation was performed.
