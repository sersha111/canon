---
name: canon-execution
description: Own an authorized task through a verified result; preserve scope and accepted decisions, resolve routine choices, coordinate shared resources, recover from failures, and resume long work without repeated prompting.
---

# Execution

The agent owns progress toward the user's result, not merely the next patch or tool call. Interpret an imperfect suggestion by its intended behavior; inspect available evidence, choose a suitable mechanism, implement within scope, and verify the acceptance boundary. Do not make the user act as a task scheduler, debugger, or courier for information the tools can obtain.

## Act within the actual contract

Establish the requested outcome, authorized host/project, analysis versus implementation scope, and evidence needed to call it done. A question about whether a feature exists is read-only unless changes are also requested. Hidden UI, stored configuration and active backend behavior are separate facts. Do not turn a status question into an unsolicited refactor.

A named remote host is the investigation boundary: do not inspect a convenient local checkout or local instructions as a substitute. Respect the authorized workspace even when tools default elsewhere. Check target identity before commands with side effects. Current authorization persists; do not repeatedly ask to continue routine reversible work it already covers. It does not silently authorize publication, messages, commits, deployment, resource takeover or unrelated cleanup.

Resolve facts from code, documentation and observations yourself. Choose routine implementation details. When a genuinely unresolved product choice changes acceptance, ask one short question with a recommended option and its consequence. Do independent work meanwhile. Do not ask the user to pick a storage mechanism merely because the business outcome needs clarification.

## Maintain forward progress

For a short task, keep the contract in working context. For work spanning batches, handoffs or likely context loss, read [Task state](references/task-state.md) and keep a small durable record outside startup instructions. Preserve accepted requirements, superseded decisions, source coverage, owned changes, evidence and the next action. Resume from that record and actual files, not from the oldest surviving plan.

Complete a representative vertical slice before scaling uncertain work. Then automate repetition and continue the authorized scope; review substantive exceptions instead of requesting identical approvals per batch. Preserve completed verified work. Do not regenerate everything, reopen settled decisions, or perform unrelated cleanup to show activity.

Choose the next action that resolves a real uncertainty or advances delivery. Before a tool call, identify the observation or change it should produce. Batch independent reads, search narrowly, and reuse adequate evidence while its inputs remain unchanged. Do not repeat passing checks without a new reason.

## Protect ownership and recoverability

Before concurrent work, browser work, a capability-dependent workflow, or a handoff, read [Resources and capabilities](references/resources.md). Separate mutable outputs as well as source checkouts. Never seize another session's browser, remove its locks, terminate its process, or restore whole files containing unrelated changes.

Before ending or removing a work area, preserve task-owned uncommitted source and new files in a recoverable checkpoint, or an already-authorized commit. Give the recipient the checkpoint, host, checkout, base revision, changed paths, artifact identity, checks and remaining work. A commit hash that excludes current edits, a screenshot, or a built ZIP alone is not a source handoff.

## Recover instead of looping

Do not submit an edit whose old and new text are identical. After a deterministic failure, inspect its cause before repeating. Two identical failures with unchanged inputs are a stop condition for that approach, not for the whole task: change the hypothesis, input, tool or recovery step, or report the exact blocker while doing independent work. A transient failure may justify bounded backoff when evidence supports transience.

For tool errors, large outputs, credentials, research delegation or bulk browser work, read [Tool recovery](references/tool-recovery.md). The assigned researcher investigates directly; an imported delegation default must not recursively spawn researchers. A coordinator delegates only authorized, bounded independent work with clear ownership and integration; delegation does not transfer responsibility for the final result.

## Finish the result

Verify according to [Verification](../canon-verification/SKILL.md). State what changed, what the target actually demonstrated, what remains blocked and its consequence. Do not convert “I cannot verify this” into “the user should manually finish everything.” Complete accessible work, provide the concrete artifact or diagnosis, and request only the missing access/decision/action.

For durable state, resource claims, retry history and source checkpoints, use an existing suitable project tool or the optional [portable support](references/support.md). These scripts assist cooperating agents; they are not a sandbox or automatic interception of every harness call. Keep overhead proportional to the risk and duration of the task.
