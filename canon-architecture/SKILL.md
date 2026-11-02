---
name: canon-architecture
description: Choose or change architectural owners, interfaces, state representations, storage, composition, and execution order using the affected domain's constraints.
---

# Architecture

Start with the behavior and constraints the boundary must preserve: who owns the state, who changes it, its lifetime, consistency requirements, access paths, and external effects. Recover accepted choices from explicit decisions and their actual outcomes. Current code can be wrong; a generated architecture document can merely describe that mistake.

For the affected decision, state:
- Applicability: which responsibility and circumstances this pattern covers.
- Owner and contract: inputs, outputs, state, errors, and permitted callers.
- Composition and ordering: which layer calls which, and which effects must happen together or before others.
- Constraints and alternatives: why this choice fits, what other choice would fit different conditions.
- Failure checks: observable violations and the test or inspection that exposes them.

Keep this record concise in the project's architecture documentation. Do not turn every local decision into a personal rule. Use different patterns in different areas when their constraints differ.

## Distinguish entities by meaning

A command requests an action; an event records what happened; a notification communicates it; a work item tracks responsibility and completion. Do not create a new entity or owner because a UI label sounds like one. An activity timeline can present events without becoming an executable action. Add a persistent work item only when assignment, independent lifecycle, or completion tracking is actually needed. Notifications alone may suffice for reminders. If the user is asking whether tasks are useful, investigate that need rather than treating an assistant's earlier task model as accepted.

## Choose storage from required behavior

Embedded records fit data owned and changed atomically with one parent. Independent records fit independent lifecycles, cross-parent querying, separate permissions, and separate update rates. Compare update consistency, indexing, concurrency, and migration cost. Neither JSON documents nor normalized tables are universally preferred.

Example: approval steps that live and die with a request can remain embedded while reminders with independent ownership use separate records. If an embedded design causes expensive searches, first examine available indexing/filtering; a full migration is not the automatic fix. Conversely, do not keep embedding when independently queried records and conflicting updates make it unsuitable.

An argument only counts if implemented. Choosing a store for optimistic concurrency requires conditional writes and conflict handling; merely using that store provides no protection. Do not discard unsaved edits on a conflict without an explicit product decision.

## Keep boundaries useful

Prefer a coherent interface that hides substantial implementation decisions. Do not extract an adapter, repository, service, or strategy solely because a pattern catalog recommends it. A stable external integration, independent substitution need, or real policy variation can justify one. Use direct language/framework facilities when they express the required contract adequately.

When selecting a replacement framework or integration, prototype the uncertain seam on a representative bounded slice. Measure actual compatibility and identify excluded capabilities. One successful screen does not establish whole-application migration feasibility.

Preserve established meaningful owners; Construction defines the extraction checks. Review public entry points, data/effect boundaries, and order-sensitive hooks against this decision. If a proposed design moves responsibility outside its accepted interface, either justify and document an authorized boundary change or keep the original owner.
