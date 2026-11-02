# Acceptance in the actual environment

Use for UI implementation/review, recurring defects, state/representation migrations, concurrency and release work.

## Reproduce the discriminating trigger

Recover the exact preceding actions, persisted data and host environment. Example: reload → change approver → save is different from ordinary save. Trace source → mapper → state → all writers → persisted response → displayed result. Include old records that were not re-saved; do not build fixtures in states the real application cannot produce.

For a recurring failure, reproduce it before claiming the fix. If reproduction is impossible, state what was tested instead and keep the claim bounded. A negative control should fail on the known-bad behavior and pass on the correction; a green test that never triggered the defect is not evidence of repair. Capture the relevant DOM, network and state using available tooling instead of asking the user to act as a diagnostic instrument. Avoid secrets and excessive dumps.

For shared UI, choose the affected dimensions from RTL/LTR, light/dark, keyboard/pointer, viewport and supported input methods. Test the changed interaction and neighboring accepted behavior, not a blind full Cartesian matrix. Style work must not remove keyboard activation, alter selected state or change layout semantics.

## Domain contracts

Turn the user's distinguishing example into an independent expected result. Replacing a row preserves table length; inserting grows it. An approver change preserves the intended approval stage and refreshes the version from every writer. Tenant configuration must match the actual target, not a convenient default. Do not accept a source-string assertion in place of these behaviors; retain structural checks where the contract really is structural.

For coordinate/unit migrations, record a version/unit and reference frame, and define explicit conversion boundaries. Never guess pixels versus fractions from numeric magnitude: valid pixel positions can be below one. Include origin, dimensions, zoom/rotation and scaling ownership where relevant. Read legacy records through a known version/provenance rule; ambiguous untagged records require recovered metadata or explicit resolution, not a new heuristic. Verify drag → save → reopen → actual rendered/exported placement, old and new records, and that scale is applied exactly once.

For concurrent writes, test at the server boundary with overlapping requests using the same version. One wins; the other returns the defined conflict without losing unsaved work. A disabled button prevents some local duplicates but does not replace conditional writes. Test retries/idempotency separately when relevant.

## Release is more than a successful command

Use or establish a small project-owned verification command for the relevant checks; inspect what it actually executes and whether it collects real tests. Keep routine checks nonmutating. A command that deploys or repairs data belongs to an explicit, authorized release path.

Before an authorized release, verify host/cwd/revision, target account/environment, packaged production configuration, required migrations/indexes/data, and expected artifact identity. Stop conflicting watchers or shared-output writers through coordination, not takeover. Verify the served version and live critical behavior after release; the CLI exit status is only one observation.

Required authentication must deny access or fail startup when its secret/configuration is missing. Test missing configuration, unauthenticated, wrong-credential and authorized paths, including relevant direct routes/APIs. Never print the secret. If production access is unavailable, deliver the verified package and concrete remaining release checks without calling the release complete.

Keep a release record linking source checkpoint, build, deployed/served identity, data prerequisites and observed acceptance results. Preserve rollback information where release risk warrants it; do not roll back or redeploy without existing authorization.
