# Docs/17b — HS-B Swarm Ops Tighten

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead Luke Thompson, **`APPROVE HS-B`**, 2026-09-17 ET |
| **Date** | 2026-09-17 (ET) |
| **Author** | Conductor executor (HomeWorld) — `gh` Contents API only |
| **Parent plan** | [17_HS_AUDIT_STRATEGY.md](17_HS_AUDIT_STRATEGY.md) — Lead **`APPROVE HS STRATEGY`**, 2026-09-17 ET |
| **Prior gate** | [17a_HS_INVENTORY.md](17a_HS_INVENTORY.md) — Lead **`APPROVE HS-A`**, 2026-09-17 ET (stamp PR **#88**) |
| **Baseline main** | tip at authoring (post-#88); strategy baseline `d59a0b2` (PL CLOSED) |
| **Scope** | Encode post-PL swarm contracts for debt **#2, #4, #6, #8** — DESKTOP parent-only, Contents API fallback, batch digests, resume-from-handoff |
| **Hard rules honored** | Docs/07 CLOSED; FALLBACK glide only; no combat; Content KEEP-LOCAL (allowlist [20_UASSET_AI_POLICY.md](20_UASSET_AI_POLICY.md)); exactly 10 masters; no invented product phases |

**Gate:** Lead **`APPROVE HS-B`** — **APPROVED** (Luke Thompson, 2026-09-17 ET). **HS-C UNLOCKED**.

---

## Why

After Docs/16 PL **CLOSED**, Conductor still carried ops rules as tribal knowledge: DESKTOP Shell only works on the Conductor **parent**, cloud agents flake to Contents API, stamp PRs spam Lead, and chat refresh loses continuity. HS-B writes those contracts into `swarm/` + pointers so the next session does not re-discover them.

**Out of scope (this WAVE):** HS-C branch protection · HS-D evidence scripts · HS-E Mannequins · new product phases · GUI automation revival · new agent runners.

---

## Debt closed by this WAVE (from Docs/17a)

| # | Debt | Disposition after HS-B | Where encoded |
|---|------|------------------------|---------------|
| 2 | DESKTOP Shell = Conductor parent only | **ACCEPT** as law (ceiling documented) | [PHASE_BOARD.md](../swarm/PHASE_BOARD.md) · [CLOUD_AGENT_PACKET.md](../swarm/CLOUD_AGENT_PACKET.md) · [HANDOFF_TEMPLATE.md](../swarm/HANDOFF_TEMPLATE.md) · [SWARM_OPS.md](../swarm/SWARM_OPS.md) · [WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) |
| 4 | Cloud ResourceExhausted / unreliable | **FIX** — Contents API fallback **sanctioned** | Packet + handoff template + SWARM_OPS |
| 6 | Stamp / phase PR volume | **FIX** — prefer **phase-end digests** with PR links | Packet + SWARM_OPS |
| 8 | Session transcript lag | **FIX** — **resume from handoff** + SESSION_SUMMARY policy | SWARM_OPS + [AGENTS.md](../AGENTS.md) pointer |

---

## Checklist — what changed

| # | Deliverable | Status | Paths |
|---|-------------|--------|-------|
| 1 | HS-B handoff (this file) | Done | [Docs/17b_HS_SWARM_OPS.md](17b_HS_SWARM_OPS.md) |
| 2 | PHASE_BOARD post-PL / HS section; DESKTOP parent-only explicit; **HS-B IN PROGRESS** kept | Done | [swarm/PHASE_BOARD.md](../swarm/PHASE_BOARD.md) |
| 3 | Cloud packet + handoff template (Contents API fallback, no-DESKTOP-for-executors, batch digests) | Done | [swarm/CLOUD_AGENT_PACKET.md](../swarm/CLOUD_AGENT_PACKET.md), [swarm/HANDOFF_TEMPLATE.md](../swarm/HANDOFF_TEMPLATE.md) |
| 4 | SWARM_OPS / WINDOWS_BRIDGE cross-links (DESKTOP parent-only happy path) | Done | [swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md), [docs/Setup/WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) |
| 5 | Resume-from-handoff + SESSION_SUMMARY pointer | Done | [swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md) §13 · [AGENTS.md](../AGENTS.md) |

**Not in scope:** Branch protection (HS-C), evidence scripts (HS-D), Mannequins policy (HS-E), product phases, claiming **`APPROVE HS-B`**.

---

## Contracts encoded (summary)

### DESKTOP = Conductor parent only

- **YES:** Conductor **parent** session → `ListMachines` → `machineId=929b6d1e-df75-4a84-b73c-a171c6eb877c` → Shell on **DESKTOP-21CT3H0**.
- **NO:** Cursor **Task** executor subagents · cloud Linux VMs claiming DESKTOP Shell / MCP / PIE.
- Happy path: [WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) · proof: [handoffs/HR3_A_WINDOWS_EXEC.md](handoffs/HR3_A_WINDOWS_EXEC.md).

### ResourceExhausted → sanctioned `gh` Contents API

When a cloud/clone path returns **ResourceExhausted** (or equivalent clone/checkout failure), workers **may** complete docs-only work via GitHub **Contents API** (`gh api repos/.../contents/...`) — **no local clone required**. Prefer Contents API over inventing a second checkout strategy. Still KEEP-LOCAL Content (allowlist per Docs/20); still no DESKTOP claims from cloud.

### Batch digest preference

Prefer **one phase-end digest** (status + PR URLs + merge SHAs) over per-CI / per-stamp chat spam. Stamp-only PRs remain valid for Lead gates; Conductor batches Lead-facing updates.

### Session resume

On chat refresh or new Conductor session: read latest `Docs/handoffs/SESSION_HANDOFF_*.md` + [docs/SESSION_SUMMARY.md](../docs/SESSION_SUMMARY.md) + [swarm/PHASE_BOARD.md](../swarm/PHASE_BOARD.md). **Do not rewrite all history** — append SESSION_SUMMARY; durable continuity lives in handoffs.

---

## Verification

- [ ] `validate` + `python-lint` green on HS-B PR
- [ ] PHASE_BOARD current phase remains **HS-B IN PROGRESS** (no false APPROVE)
- [ ] Packet / template / SWARM_OPS name Contents API fallback + DESKTOP parent-only + digests
- [ ] Lead reviews → types **`APPROVE HS-B`** (not claimed here)

---

## Next (after Lead `APPROVE HS-B`)

**HS-C** — CI as law: apply branch protection on `main` **or** Lead **`ACCEPT HS-C DEFER`**. Deliverable: [17c_HS_CI_LAW.md](17c_HS_CI_LAW.md) (not started).

---

*PENDING — Docs/17b HS-B Swarm Ops. Awaiting Lead **`APPROVE HS-B`**. Do not unlock HS-C until stamped.*

## Lead APPROVE HS-B

Lead **`APPROVE HS-B`** (Luke Thompson, 2026-09-17 ET) — swarm ops tighten **APPROVED / CLOSED**. **HS-C** (CI as law) **UNLOCKED**.

---

*HS-B **APPROVED / CLOSED** — Lead **`APPROVE HS-B`**, 2026-09-17 ET.*
