---
name: canon-verification
description: Verify changes and reviews against intended behavior, structural constraints, affected consumers, the actual delivery artifact, and explicit limits of evidence.
---

# Verification

Identify what would fail if the user's requirement were missed. Choose checks that distinguish that failure from legitimate alternatives. Verify the normal behavior and the important boundary, including structural constraints such as ownership and ordering that output-only tests can miss. Read Construction and Expression during ordinary implementation/review.

Use an independent expected result. A test that repeats the implementation's calculation, accepts constant answers, or only matches keywords may validate the same mistake twice. Evaluate the meaning of generated content where required; formatting, counts, and literal-word filters do not establish semantic correctness.

Trace affected readers and writers. A rename, rollback, permission change, saved preference, or navigation change can pass an isolated test while another consumer breaks. Include the affected path, not every unrelated test. Preserve useful integration and public-interface tests; do not require user confirmation for routine reversible verification already authorized by the task.

For UI implementation or review (including shared-component styling), recurring defects, state/representation migrations, concurrent writes, or release work, read [Acceptance in the actual environment](references/acceptance.md) before selecting checks. It defines exact-trigger reproduction, negative controls, domain fixtures, UI dimensions, versioned conversions, server concurrency, and release/authentication preflight.

## Verify the boundary being claimed

Distinguish:
- implementation inspection;
- unit/simulator checks;
- integration with the real runtime;
- packaging and artifact inspection;
- installation/deployment;
- observed target behavior.

A simulator may accept syntax the native runtime rejects. Hundreds of green tests do not override a target failure. Exercise the relevant native interface when available. If unavailable, report the exact untested boundary, continue independent checks, and avoid claims such as “site-tested.”

When delivering a file, verify that the named output path contains the newly built artifact. For packaged applications, inspect the shipped configuration and, where material, compare the embedded/installed bytes with the verified build. A successful temporary build does not update an older ZIP elsewhere. Local development mode and production packaging are different checks.

After changing permissions, check every relevant exposure surface: direct access, search results, cached names, and metadata as applicable. Direct denial alone may leave a confidentiality defect.

For projects lacking a usable check gate, the optional [manifest runner](../canon-execution/references/support.md) provides bounded commands and structured evidence. Configure it with actual project checks; a generic runner is not evidence that application behavior passed.

## Keep checks safe and interpretable

Inspect unfamiliar check commands before running them: a target named “check” can deploy or modify tracked data. Record a baseline of relevant working changes before a potentially mutating operation and compare afterward. Never attribute all differences from HEAD to your command when changes already existed. Preserve unrelated work; do not use broad resets to clean up.

For isolated checkouts, establish required dependencies and configuration before interpreting failures. Distinguish missing setup from product regressions. If a guard blocks a harmless command, investigate its actual match and use an authorized safe form; do not weaken protections broadly.

Compare like-for-like test populations. A reduction from 70 to 9 reported tests may be deduplication or a changed collector, not 61 regressions. Record exclusions and the check's scope. During review, cover relevant uncommitted changes as well as committed ranges; distinguish requirement violations from preferences invented by the reviewer.

Once appropriate checks pass, stop repeating them unless new changes, failures, or unresolved concerns justify it. For low-impact reversible edits, inspection or an existing check can suffice; do not create tests that merely restate the edit.

Finish with what changed, what actually passed, what failed or was deferred, and the consequence. Never invent timings, requests, target observations, or acceptance. If one part is blocked, complete the independent authorized work and name the precise remaining dependency.
