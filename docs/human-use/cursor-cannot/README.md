# Cursor cannot

Slices of *Week 1 - Agentic Engineering* that **Cursor does not enforce**. The
agent must not pretend these products exist, and must not build them in this
repo. As of 2026-10-01 the agent **owns** four of these five; the fifth is a human
Steer decision about isolation and reach.

Source: the Week 1 PDF. These pages summarize the practice; they do not copy it.

| PDF section | File | Owner since 2026-10-01 |
| ----------- | ---- | ------------------------ |
| 3.1 Harness Engineering | [harness-engineering.md](harness-engineering.md) | **Agent** (was: human Test) |
| Testing Phase — environment security | [environment-security.md](environment-security.md) | **Human** (Steer) |
| 4. Code Quality Review | [code-quality-review.md](code-quality-review.md) | **Agent** (was: human Test) |
| 5. Optimization Refactor | [optimization-refactor.md](optimization-refactor.md) | **Agent** (was: human Test) |
| Agent-specific Information | [agent-specific.md](agent-specific.md) | **Agent** (was: human Steer) |

**Do not conflate the two meanings of "environment."**
[environment-security.md](environment-security.md) is the **dev** environment —
isolation, web reach, permission posture. It is not art environment design. The
first stays human; the second is human taste. Mixing them up once would have
stripped your verify-command gate on the strength of a word.

What we *do* implement lives in [OWNERSHIP.md](../OWNERSHIP.md), the cycle gates,
and the six core skills. Do not add a seventh skill or an always-on rule for these
gaps.

The owner column changed on 2026-10-01: these practices used to be handed to you,
and are now the agent's job. The **descriptions stay** — the agent still must not
pretend a product exists. Harness engineering, code quality review, optimization
and context management are now things the agent does itself, without the tooling
the PDF assumed.

Repo tools that also cannot reach something: [automation-gaps.md](../../operational/automation-gaps.md).
