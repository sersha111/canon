---
name: canon-construction
description: Implement, refactor, and review code while preserving meaningful owners and interfaces, avoiding needless function fragmentation, and reusing actual shared operations.
---

# Construction

Before adding behavior, find its established owner, callers, state, and relevant existing operations. Search the affected responsibility, not just the proposed function name. Preserve the owner's public contract unless changing it is part of the authorized task.

## Keep behavior with its owner

Place an operation where its invariant, lifecycle, and state are already maintained. Call the established interface instead of reaching into its internals. Do not move fragments into free functions, a new utility module, or an invented manager merely to make an existing class/component look smaller or satisfy a function-count rule. A new owner needs a distinct responsibility, a coherent contract, and a real lifecycle or dependency boundary.

This is not a mandate for classes. A module, component, service, actor, or pure function can own a responsibility. A stateless transformation with a useful input/output contract can legitimately be a free function; an operation that coordinates account state belongs to that account's established owner. Framework callbacks can remain callbacks. Preserve these distinctions across languages.

## Justify every extraction

Keep a short, single-use sequence inline when extraction only labels a branch, wraps a language construct, renames one field access, or forces the reader to jump elsewhere to recover the same flow. A nice name, a short body, line-count limits, or a hypothetical future caller is insufficient justification.

Extract when there is a meaningful domain operation with its own contract, substantial shared behavior with the same semantics, or a necessary boundary such as a framework callback or independently variable external dependency. Size alone neither requires nor forbids extraction. Small domain operations can protect important invariants; large functions may still need separation when they contain independent responsibilities. Explain the contract or reuse, not a slogan about cleanliness.

Bad: move three statements that update an order's state into a free `completeOrderFields(order)`, then expose internal fields to let it run. Better: retain the transition in the existing order operation and keep its validation and mutation together. Allowed: the order already exposes `complete()` as the transition contract, even if its body is short.

Bad: introduce `hasItems(xs)` solely for `xs.length > 0` in one branch. Better: use the direct condition. Allowed: `isEligibleForRenewal(policy, today)` encodes a named business rule shared by quoting and renewal, including dates and exceptions; it is not just a cosmetic predicate.

## Reuse semantics, not similar shapes

Before creating parallel handlers, check for an existing parameterized operation. Use one table-row deletion operation when the tables share deletion semantics, allowed keys, and minimum-row rules. Do not generate one wrapper per table merely to give it a specific name.

Do not force unrelated operations together because their bodies look alike. A draft table may allow its last row to disappear while a submitted table requires an audited replacement. Preserve that difference, either through an explicit supported policy or separate operations; avoid a generic boolean soup.

Shared document layout used by several generators may belong in a focused reusable module. Keep document-specific selection and workflow in their owners. Do not delete an internal-report generator simply because a public-report generator uses similar rendering code. Check callers and outputs first.

## State, composition, and scope

Keep one authoritative representation of a fact. If multiple consumers need the same expensive derivation, compute at the owner with an explicit invalidation rule and pass the result. Do not create a second writable copy merely to avoid a calculation. A cheap derivation can remain computed locally.

Use the actual runtime namespace and lifecycle when sharing constants or behavior. Two files loaded as classic scripts may share one global scope; duplicating a top-level constant can fail even though each file looks valid alone. Module isolation must be real.

Do not invent compatibility for an unreleased feature without existing consumers or stored data. Preserve compatibility when actual deployed consumers require it. Verify lifecycle hooks and ordering: style decisions that affect layout must happen before measurement, not after drawing.

When changing a name or contract, update affected readers, writers, serializers, and consumers. Preserve unrelated work. A narrow rollback must restore the intended fields without broad exclusions that leave unwanted writes behind.

Before finishing implementation or review, inspect added/moved functions and owners. For each questionable fragment, identify its contract, reuse, or required boundary. Inline unjustified fragments, restore misplaced behavior, and verify legitimate alternatives remain possible. This check is part of normal work, not an optional cleanup pass.
