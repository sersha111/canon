# Durable task state

Use this for long tasks, repeated content/browser jobs, migrations, handoffs and context recovery. Do not create a ledger for a one-line edit.

Record the current outcome and acceptance criteria; authorized host/root/mode and external actions; accepted decisions with their evidence and superseded alternatives; required sources; item status; owned files and preexisting changes; capability/resource blockers; checks actually performed; and next action. Keep it outside AGENTS/CLAUDE startup text. The portable session script can maintain the machine-readable portion; a short adjacent note can hold reasoning.

An accepted decision is not simply the latest sentence. Recover its scope, sequence and acceptance. Example: a single panel needs fullscreen but the application supports three modes; do not turn the panel constraint into a product-wide mode restriction. Mark an earlier choose-one proposal superseded when all three were accepted.

For each batch item, record required source references with specific supporting locations, output identity, substantive validation and status. “File exists” or “sources listed” is not completion. If existing material lacks required source support, audit and repair that material; retain correct portions. Verify sources actually inform the output, not just that their names appear. Generated tests can check structure but cannot certify pedagogical or business meaning.

Select a representative end-to-end pilot, including saving, reopening, verification and any required human handoff. Once the pattern is accepted, continue all authorized items without batch approvals. Queue only incomplete or invalidated items. Record partial successes before a failure so a retry neither duplicates writes nor repurchases completed work. Preserve idempotency keys and result identities where the service supports them; ambiguous writes require readback before retry.

For a bulk browser job, inventory item IDs before opening tabs. Test one complete supported path, including authentication and downloads. Persist each item's result and resume from it. If the supported workflow requires a user action, explain that exact step and complete other items that do not depend on it. Do not open hundreds of tabs before discovering a mandatory handoff.

Source-language fidelity is distinct from the operator's communication language. Preserve existing quotations exactly where required and provide the requested explanation/translation alongside them. Assemble reversible internal drafts and unchanged bilingual quotations under existing authorization. Ask when ambiguity changes business meaning or external publication requires approval, not for every unchanged quotation. Do not silently impose the operator's preferred language on a customer's interface.

On resumption, compare output fingerprints, required-source versions and the current accepted contract. Reopen an item when its output or source changed, or when the recorded check no longer covers it. Do not trust a green status from an obsolete contract. Record loaded instruction paths and hashes for consequential or long work so future diagnosis can distinguish guidance actually used from merely installed files.
