# Portable execution support

These Python 3.9+ standard-library tools run on the authorized host. They never grant authority or intercept every harness call. Prefer an existing project tool when it meets the same contract. State writes and archives are private by default; do not put credentials in arguments, source references or error summaries.

## Task state

Run from a suitable working directory with explicit paths:
```sh
python3 session.py init /private/task/state.json --root /work/project --mode implementation --intent "Deliver all approved items" --source handbook-v2 --item item-1 --instruction /work/project/AGENTS.md
python3 session.py decision /private/task/state.json --key modes --value "all three" --evidence "current accepted product decision"
python3 session.py item /private/task/state.json item-1 --status done --output output/item-1.md --source "handbook-v2=chapter 3, paragraphs 2-4" --check "Reviewed source support and independently checked the result"
python3 session.py status /private/task/state.json
```

The script's location is [scripts/session.py](../scripts/session.py); replace session.py in the example with that path. Use stable versioned source IDs. The item inventory is explicit; a done item requires every required source reference, a check description and an existing output. Status detects changed/missing outputs and accepted-decision or required-source changes. Update source versions using sources STATE --source NEW_ID --evidence ACCEPTED_CHANGE; previous source requirements remain recorded. This does not prove the references were consulted or the check was sound; the agent must examine substantive support. Changed content behind an unchanged external source ID still requires the agent to detect the change and update its recorded version; the script does not fetch external sources.

The state records the actual execution hostname/root and fingerprints instructions the caller declares read. It does not prove automatic harness discovery. The decision command keeps superseded values rather than erasing them. An analysis-mode task refuses a write guard; the guard also rejects paths escaping the root. Passing that guard does not authorize external actions or permit overwriting others' edits.

## Recovery and handoff

```sh
python3 session.py checkpoint /private/task/state.json --base BASE_REVISION --file src/changed.py --file src/new.py
```

The result gives a protected source checkpoint and manifest with root, host, base, hashes and original permission modes. Copies remain private (0600); restore the recorded mode when recovering an executable. Symlinks or symlink-containing source paths are refused instead of silently losing their identity; use link-aware project recovery tooling for them. It includes selected untracked files and readbacks the copied bytes. Select the complete set of source changes needed to resume, using --deleted path for each absent task-owned file as well. Complete file snapshots may include preexisting edits: distinguish them in the handoff and restore selectively after comparing current work. The tool does not restore, commit or remove files.

Known private-key/credential-URL patterns and common secret filenames are refused. This is not comprehensive secret scanning; review selected files and use the project's protected recovery mechanism for sensitive sources.

Record a failed tool attempt with a concise nonsecret error category:
```sh
python3 session.py attempt /private/task/state.json --operation edit-rule --input SOURCE_HASH --error identical-replacement
```
The second consecutive identical failure returns exit 3 and stop_unchanged_approach=true. Recording a recovery explanation alone does not reset the counter; the actual input/operation/error must change. Call this from a cooperating orchestration loop after failures, and honor its result before repeating. It is not an installed universal harness hook.

## Shared resources

```sh
python3 session.py claim /shared/canon-claims --resource authenticated-browser-profile --owner task-unique-id
python3 session.py release /shared/canon-claims --resource authenticated-browser-profile --owner task-unique-id
```

All participants must use the same registry/resource key. Claims serialize through a file lock. A second claimant is rejected, including the same owner accidentally claiming twice. Only the recorded owner releases it. No timeout steals ownership; coordinate abandoned claims explicitly.

## Export/index

Use [scripts/evidence_index.py](../scripts/evidence_index.py) on an explicit JSON list:
```json
[{"harness":"example-harness","session_id":"session-1","parent_id":null,"path":"/private/export/session.jsonl","coverage":"narrative reviewed; attachments unreviewed","instruction_versions":[]}]
```
```sh
python3 evidence_index.py manifest.json /private/new-index --copy
```
Without --copy this creates a provenance/fingerprint index. With --copy it preserves deduplicated exact private source bytes and verifies their hashes. Use only authorized exports; raw copies may contain secrets and must not be published. Existing destinations are refused. Source metadata remains explicitly caller-declared. Export live SQLite stores through supported read-only/consistent-snapshot APIs first; copying a database file while WAL writes are active is not a consistent transcript export.

## Project verification gate

[Verification runner](../../canon-verification/scripts/verify.py) runs a reviewed argument-array manifest with an explicit root and report path. Example:
```json
{"checks":[{"name":"public-behavior-tests","argv":["python3","-m","unittest","discover","-s","tests"],"effects":"temporary-only","timeout_seconds":120}]}
```
```sh
python3 verify.py verify.json --root /work/project --report /private/task/verification.json
```
Choose actual project checks and confirm they collect tests; this example is not proof that any particular repository has them. The runner refuses zero checks, invalid/out-of-root working directories, unreviewed effects and deployment-labelled checks. It records exits, time and observed output hashes without retaining/printing raw outputs. Output above max_output_bytes (default 8 MiB) fails the check and is marked incomplete; a prefix hash is not a full-output hash. Timeout/output-limit cleanup kills the command process group, including ordinary children. Do not use the gate for persistent services. Deliberately detached sessions remain outside this cleanup; the runner is not a process sandbox. Commands still need review: declared effects are not a sandbox. Diagnose a failure by targeted redacted inspection, not an automatic dump of secrets or huge logs.

For release work, put target revision/data/auth checks in the project's own authorized release procedure as described in the acceptance reference. Do not smuggle deployment into a nominal check.
