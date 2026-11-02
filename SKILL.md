---
name: canon
description: Apply the maintainer's engineering principles during implementation, refactoring, review, design, explanation, measurement, verification, and commit preparation. Route ordinary work through construction, expression, and verification.
---

# Canon

Apply the engineering principles below to achieve the user's intended result. Interpret corrections in their surrounding decision and preserve legitimate alternatives; do not mechanically export a local choice to every project. Execution owns the common autonomy and scope rules.

For every substantive task, first read [Execution](canon-execution/SKILL.md). It governs autonomous progress, scope, durable state, shared resources and recovery. For implementation, refactoring, or code review, also read these three skills before editing or judging:
- [Construction](canon-construction/SKILL.md): ownership, functions, reuse, state and interfaces.
- [Expression](canon-expression/SKILL.md): naming, contextual comments, explanations and audience.
- [Verification](canon-verification/SKILL.md): intended behavior, affected consumers, artifacts and truthful completion.

Also read:
- [Architecture](canon-architecture/SKILL.md) when choosing or changing owners, boundaries, storage, composition, execution order, or public interfaces.
- [Performance](canon-performance/SKILL.md) when claiming speed/memory gains, changing a hot path, batching, caching, or consuming metered resources.
- [Commits](canon-commits/SKILL.md) when drafting subjects, grouping changes, or executing an authorized commit.

For explanation-only tasks read Expression; include Architecture for design explanations. For test-only work read Verification and Construction; read Expression for changed test names/comments. For performance work read Performance and Verification. For commit-only work read Commits and Verification. Do not load every specialty for an unrelated task.

Read the target project's architecture documentation for the affected area. If absent, reconstruct only the decision needed now from its interfaces, constraints, and explicit accepted choices; do not invent an entire architecture. Record new consequential accepted choices in the project's own architecture document, not in personal skills.

Do not treat existing code, imported skills, test counts, or agent-written plans as proof of intended behavior. Preserve useful established patterns while correcting demonstrated defects. A correction applies to its actual scope: different parts of the same system may use different valid designs.

Common rules belong in the linked skills. Audit reports and private conversations are not required to use this set. Do not load them during ordinary work.
