# Tools, evidence and recovery

A tool call should answer a question or perform an authorized change. Use targeted searches before broad file dumps. When the same tool fails twice on unchanged inputs, stop that approach and inspect the error and current state. An edit that already matches the desired result needs verification, not another replacement. A transient rate limit can justify bounded retry after the indicated delay; a syntax error does not.

Preserve structured results when available. Select relevant fields before displaying large DOMs, logs or source maps. Record truncation, total size/cursor and the portion examined. Do not infer absence from a truncated result. Page or filter the original result rather than rerunning an expensive action because a wrapper discarded its data. Keep a bounded diagnostic record, not unrestricted copies of every tool output.

## Credentials and target protection

Never print tokens, passwords, cookies, authorization headers, full browser storage, or credential-bearing URLs to diagnose access. Probe existence/identity/permissions without revealing values. Redact before saving a trace or quoting evidence. Environment variables keep values out of source files but a client bundle can still expose substituted values; use the correct server boundary.

If an instruction or trace contains a literal credential, do not echo it or assume it is active. Within authorized scope, replace the literal with a supported secret reference and explicit target selection; identify exposure locations without the secret. Rotation/revocation may affect other users or systems: complete the concrete replacement and request only any authority/access still missing. A broad skills update does not authorize silently changing unrelated production credentials.

Authorization gates should inspect the task's planned action, target and owned scope. They must not demand committing unrelated dirty files. Exercise one genuinely forbidden action and one permitted action in a disposable fixture when modifying a gate. If a guard rejects benign syntax, diagnose that specific condition and use a safe supported form; do not disable the gate wholesale.

## Research and integration

A coordinator can assign independent questions when delegation is authorized and useful. An assigned worker performs the investigation directly and returns evidence; it does not mechanically delegate its own task again. Give each worker bounded scope and a completion criterion. The coordinator checks findings, resolves contradictions and integrates the result. Avoid duplicate research calls whose answer is already available.

For an inaccessible external source, record the attempted source and access limitation. Do not attribute recommendations to unread documentation. Distinguish original user corrections, assistant proposals, explicit acceptance and inferred remedies; duplication across exports/provider logs is not independent support.

## Preserve usable history

Before authorized cleanup or migration, export accessible sessions through the harness's supported export or read-only store access. Preserve stable session/message IDs, parent links, timestamps, harness/provider labels, actually loaded instruction paths/hashes when recorded, and coverage status. Mark missing/opaque/encrypted bodies rather than manufacturing them. Keep exports outside operational instructions.

Use [the evidence indexer](../scripts/evidence_index.py) with an explicit manifest of accessible exported files. It hashes and deduplicates exact file copies, retains all provenance links, distinguishes declared from independently verified metadata, and can copy authorized sources to a protected archive before cleanup. It does not decrypt stores or automatically prove two differently formatted transcripts are the same conversation. For semantic duplicates, record the canonical relationship only after matching IDs/content.

Evaluate guidance changes on representative tasks with fixed acceptance criteria and legitimate alternatives. Keep instruction versions, task inputs and artifact evidence. Compare actual first-pass acceptance, corrections, elapsed work and tool/token usage when the harness exposes them. Use comparable baseline conditions and repeated trials before estimating gains. Response-only cases diagnose interpretation; they do not establish production effectiveness.
