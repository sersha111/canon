# Resources and capabilities

Before a workflow depends on external access, use the least intrusive probe for the actual harness and target: authenticated identity and tenant/account, browser availability and target tab, relevant GitHub/M365 permission, installed runtime/dependencies, deployment mode and target, or requested model availability. Check only capabilities the task needs. Report access denied as a capability failure, not proof that a resource or product behavior does not exist.

Use one documented recovery path that fits the failure, and test it on a small operation. Do not reinstall tools, switch providers, create another checkout or rotate credentials at random. Respect requested provider/model settings. If unavailable, report the exact dependency and continue unaffected work; do not silently substitute a model.

## Concurrent work

Give each implementation worker a distinct writable scope. Use a supported isolated checkout when changes overlap or independent builds require it; disjoint read-only work does not require worktrees. Record the host, absolute checkout, base revision, owner and expected deliverable. Provision dependencies/configuration before treating a failed test as a code defect.

Source isolation alone is insufficient: check build outputs, caches, watchers, servers, databases and deployment targets for shared writes. Isolate mutable outputs or serialize them under an agreed owner. Record server cwd, port and served revision. Do not kill an existing process simply because it occupies the preferred port.

Before handoff or cleanup, save an owned patch or explicit selected-file checkpoint including untracked source files, with base revision and hashes. Preserve preexisting user changes too, but distinguish them from task-owned edits. Never commit without authorization. Check the recovery copy can reconstruct the intended files; do not delete the only worktree until the recipient has the source checkpoint and can locate it. An artifact hash proves artifact identity, not source recovery.

Mutation tests, destructive experiments and negative controls that modify code/data run in disposable copies with explicitly scoped test data. Never restore an entire live working file from Git to undo a mutation. Compare before/after and reverse only owned changes.

## Authenticated browsers

Treat a logged-in browser profile as a shared resource with an owner. Identify the intended account, tenant, tab/URL and application revision before testing. A profile-in-use error calls for coordination, serialized use, or an independently authenticated isolated profile. Do not delete locks, kill the current owner's browser, copy an active profile, or assume a new empty profile has equivalent access.

Continue independent work while waiting. If UI behavior requires a browser and access stays unavailable, HTTP checks may provide additional evidence but do not replace the missing interaction test. Record that boundary accurately.

The portable claim command provides exclusive ownership only among cooperating callers using the same registry path and resource name. Release only your own claim; do not automatically steal an old claim based on a timeout. Confirm an abandoned owner's state through the environment's supported coordination mechanism before recovery. Claims do not replace the harness's own isolation tools.
