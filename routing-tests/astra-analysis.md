# Queue, inventory, and payment recovery

The proposed design does not meet all requirements. Its inbox records that inventory was allocated, but duplicate delivery is treated as proof that payment processing finished.

- **A — commit, then crash before capture:** redelivery finds the inbox entry and immediately acknowledges it. Inventory remains allocated, but payment is never attempted. Eventual processing fails.
- **B — successful capture, then crash before acknowledgement:** immediate acknowledgement on redelivery avoids another capture in this execution. However, the database has no durable payment outcome; this cannot safely distinguish B from A.
- **C — capture times out:** the provider may have charged the customer. Blind retry can charge twice; abandoning the attempt can leave an uncaptured order unfinished. Releasing inventory while the result is unknown can leave a paid order without allocated inventory.

## Smallest coherent repair

Use the existing inbox row as the durable payment work record. Three states suffice: `PENDING_CAPTURE`, `PAID`, and `REJECTED`. `PENDING_CAPTURE` means inventory is allocated and must remain allocated, including while the external result is unknown.

1. **Receive:** in one database transaction, insert the unique event and conditionally decrement inventory. If allocation succeeds, persist `PENDING_CAPTURE` with a stable payment operation key and immutable capture arguments. If inventory is insufficient, persist `REJECTED` without allocating inventory. Commit before any capture call. A duplicate event must use its existing state and allocation; it must not allocate again. The key must identify the logical charge, not a delivery attempt; use an order/payment-operation key if multiple event IDs can represent the same charge.
2. **Recover and capture:** a worker scans committed `PENDING_CAPTURE` rows and invokes or reconciles capture using that same key. A timeout or recoverable failure leaves the row pending. Do not free inventory or create a new payment key. A separate persistent `UNKNOWN` state is unnecessary because pending already requires reconciliation.
3. **Complete:** confirmed capture success changes `PENDING_CAPTURE` to `PAID` in a database transaction. An authoritative, terminal no-charge outcome changes it to `REJECTED` and restores inventory in that same transaction. Restore inventory only when this conditional state transition succeeds, so competing workers cannot restore it twice. A transient failure or an ordinary “not found” response is not a terminal no-charge outcome if an earlier request can still succeed.
4. **Acknowledge:** with a reliable scanner responsible for all pending rows, acknowledge the queue message after the initial durable transaction. Duplicate messages can then be acknowledged because the database owns recovery. Without a scanner, retain/redeliver pending messages until terminal completion and resume processing on duplicates rather than immediately acknowledging them.

No lock spanning the network call or separate outbox table is required: the pending inbox row supplies durable work, provider idempotency protects concurrent capture attempts, and conditional database transitions protect local completion. Workers must derive requests from committed state.

This recovers A by finding pending work; B by replaying or reconciling the original successful capture and recording `PAID`; and C by resolving the same operation without another charge. Inventory stays allocated throughout uncertainty. Eventual completion assumes fair retries, eventual recovery of the database/provider, and a provider that eventually exposes a terminal result; permanent business rejection is a completed rejection.

## External capability and impossibility boundary

The payment API must support a stable, caller-supplied operation key with **atomic deduplication of concurrent and repeated captures**, immutable request semantics, and a way to recover the original outcome through replay or authoritative lookup. A terminal no-charge result must also prevent delayed or repeated requests for that operation from charging after inventory is restored. Its deduplication retention must cover the full recovery interval; an expiring key cannot support arbitrary delayed recovery unless another durable reconciliation mechanism safely closes the gap. A provider-enforced unique merchant transaction reference with equivalent reconciliation guarantees also works.

Without such a capability or an equivalent atomic external protocol, all requirements cannot be guaranteed. After an ambiguous timeout, “no charge occurred” and “charge occurred but the response was lost” are indistinguishable locally. Retrying risks a duplicate charge; never retrying risks an order that never gets captured. A database lock, inbox uniqueness, or a local `SENT` flag does not resolve that uncertainty. Status lookup alone also fails if it can report no charge while an earlier capture is still in flight and able to succeed.
