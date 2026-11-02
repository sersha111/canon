# Canon

Personal engineering principles for coding agents. Covers autonomous execution, architecture, implementation, explanations, performance, verification, and commits across projects and languages.

Canon treats code design as part of correctness and makes agents responsible for carrying authorized work through to a verified result. It asks agents to keep behavior with its owner, justify abstractions through actual needs, preserve meaning in names and comments, and verify both behavior and structure. Its rules include concrete examples and exceptions so they apply to the responsibility at hand.

## Install

```sh
vpx skills add sersha111/canon
```

## Use

Type `$canon` in your conversation with the agent. [SKILL.md](SKILL.md) routes the current task to the relevant skills. Every substantive task loads Execution; implementation and review also load Construction, Expression, and Verification. Architecture, Performance, and Commits load when the task needs them.

## Skills

| Skill | Purpose |
|---|---|
| [canon-execution](canon-execution/SKILL.md) | Complete authorized work, preserve scope and accepted decisions, coordinate resources, and recover from failures. |
| [canon-construction](canon-construction/SKILL.md) | Implement with meaningful ownership and justified function extraction. |
| [canon-architecture](canon-architecture/SKILL.md) | Choose responsibility boundaries, interfaces, representations, and execution order. |
| [canon-expression](canon-expression/SKILL.md) | Preserve terminology, conditions, and intended meaning in names, comments, and explanations. |
| [canon-performance](canon-performance/SKILL.md) | Compare implementations with reproducible measurements and control metered resource use. |
| [canon-verification](canon-verification/SKILL.md) | Check behavior, structural constraints, affected consumers, and delivered artifacts; report verification gaps. |
| [canon-commits](canon-commits/SKILL.md) | Group changes by purpose, write precise subjects, and perform authorized commit operations. |

## Project context

Canon reads the target project's architecture documentation for the affected area. This connects the principles to the project's actual owners, contracts, and constraints.

If missing, Canon reconstructs the decision needed for the current task from interfaces, constraints, and explicitly accepted choices. Consequential accepted choices stay in the target project's own architecture documentation, not in the personal skills.

The skills work without private conversation histories or audit records. Their examples teach distinctions that apply through the target language's own constructs. Optional Python support tools travel with the relevant skills; use existing project tools when they satisfy the same contracts.
