---
name: canon-expression
description: Name code and explain behavior with accurate domain meaning, contextual comments, readable flow, and audience-appropriate detail during implementation and review.
---

# Expression

Preserve meaning before shortening or polishing. Read the surrounding code or explanation: a locally true sentence can still hide the responsibility, scope, sequence, or exception the reader needs. Do not replace precise constraints with slogans such as “clean architecture” or “explain why.”

## Names

Name the domain role and distinguish values with different meanings: requested versus effective permission, template versus instance, recorded event versus requested action. Use singular/plural to reflect the actual value and update all consumers when renaming. Do not label a new, never-used feature “legacy” to justify invented compatibility.

A contextual name can be short when the surrounding owner supplies the meaning. A detached public name must supply enough context to identify its contract. Avoid both repeated owner prefixes in every local variable and generic names such as `data` when several different facts compete. Do not invent business concepts to make code look abstract.

## Comments carry the flow

Use a comment when the reader needs the responsibility of a block, its relationship to adjacent phases, a constraint, a non-obvious decision, or an exception. A comment may explain what a phase accomplishes when that connects the flow; “only explain why” is too narrow. Do not narrate every assignment or force a comment on every branch.

Bad:
```text
// Process data.
rows = rows.filter(isVisible)
render(rows)
```
Better when the ordering is a real requirement:
```text
// Remove inaccessible records before building the summary;
// hidden records must not contribute names or totals.
visible = records.filter(canView)
renderSummary(visible)
```
This is useful even though it says what happens: it identifies the boundary and the consequence. It would be wrong if only the display were filtered while totals still used all records. Check the code against the comment.

Bad: `// Increment counter` above `count += 1`.
Allowed: `// Reserve this sequence number before enqueueing: retries reuse it.` when that invariant is real. A direct, familiar loop needs neither an extracted helper nor a paragraph just to acquire a label.

Preserve semantic emphasis, paragraph/line grouping, and placement when they carry scope or sequence. Put a constraint next to the operation it governs; separate distinct phases with readable spacing. Do not mechanically collapse a two-phase explanation into one vague sentence. Follow evidenced project formatting rather than inventing a universal decorative comment style. For a required lint suppression, place the specific reason at the suppressed operation and keep its scope narrow; do not generalize one suppression request into a rule to suppress all warnings.

When consolidating instructions or refactoring comments, compare meaning before and after: owner, order, condition, reason, exception, emphasis, and example. Keep unique valid examples or replace them with examples preserving the same distinction. Preserve a stated contrast when it explains the surprising failure: direct access being denied does not imply summaries hide inaccessible names. A shorter comment must retain that distinction, not only say "prevent leaks." For example: "Filter before summarizing: direct-access denial alone still leaves hidden names and amounts exposed." Do not claim a preservation audit of inaccessible guidance.

## Audience determines vocabulary

For ordinary product users, use visible translated labels and actual navigation paths. Quote a UI label when that distinguishes it from prose. Explain permissions as user capabilities and roles. Do not expose flags, translation keys, component names, technical group IDs, libraries, or database records merely because those are convenient for the implementer.

Bad user guide: “Set isManager=true; columns come from ColumnSetting records.”
Better, if those labels exist: “Managers can edit the directory. Open ‘Settings’ > ‘Directory’ > ‘Columns’ to choose which details appear.”
Verify the labels against the interface/translation source; do not invent a navigation path.

For an engineer diagnosing authorization, the exact flag, query, and component may be essential. Preserve technical specificity for that audience. Hiding implementation details is not a prohibition on technical documentation.

In reports, lead with the actual outcome. Distinguish implemented, locally tested, packaged, installed, and observed in the target environment. State important uncertainty directly. Keep explanations connected and concise; do not replace evidence with celebratory summaries or lists of test counts.
