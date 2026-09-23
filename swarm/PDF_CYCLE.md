# PDF development cycle

**Companion to [SWARM_OPS.md](SWARM_OPS.md)** — do not duplicate full swarm law here.

**PDF** = **P**lan/design → **D**evelop/implement → **F**ix (after test), i.e. **Design → Implement → Test → Fix → re-Test → Lead gate**. Not a document format.

## Purpose and when to use

Use the PDF loop when Conductor assigns a **bounded product or engineering slice** that needs explicit stage owners and file handoffs:

| Mode | Use PDF cycle? |
|------|----------------|
| **SWARM** | Yes — default for post-audit tracks, kit work, multi-file features with gates |
| **HYBRID** | Yes — design/test/fix in sidebar agents; implement may stay NON-SWARM if packet says so |
| **NON-SWARM** | No — single-owner typo, CI, one-file fix; Conductor does not fan out PDF agents |

**Parent:** **Conductor** (HomeWorld Grok Bot) assigns packets, refuses bad handoffs, and owns **DESKTOP** Shell/MCP/PIE ([SWARM_OPS.md](SWARM_OPS.md) §16). Sidebar agents are **Task** chats — not DESKTOP executors.

**Living owners:** Lead-approved teammates **HomeWorld Design**, **HomeWorld Implement**, **HomeWorld Test**, and **HomeWorld Fix** hold the stages below; Conductor routes packets and does not replace them on their write paths.

---

## Stage table

| Stage | Owner (sidebar) | May write | Forbids | Handoff out |
|-------|-----------------|-----------|---------|-------------|
| **Design** | HomeWorld Design | `Docs/**` (spec/plan only), `Docs/handoffs/PDF_DESIGN_{slug}.md`, read-only elsewhere | Code, `.blend`, UE maps, marking work complete, inventing `APPROVE *` | Packet + paths → **Implement** |
| **Implement** | HomeWorld Implement | Paths on packet only (`Source/`, `Content/Python/`, `Lib/`, lowercase `docs/` if scoped) | QA pass, DESKTOP PIE, editing another owner’s paths, self-closing gates | `Docs/handoffs/PDF_IMPL_{slug}.md` → **Test** |
| **Test** | HomeWorld Test | Test plans, checklists, defect lists, `Docs/handoffs/PDF_TEST_{slug}.md`; score **returned** evidence (logs, PNG, CI) | Fixing product code, kit edits, claiming Lead approval | FAIL → **Fix**; PASS → Conductor → **Lead gate** |
| **Fix** | HomeWorld Fix | Defect-linked paths only (from Test packet) | Scope creep, new features, re-design without Conductor re-packet | `Docs/handoffs/PDF_FIX_{slug}.md` → **Test** (re-Test) |

Handoffs use [HANDOFF_TEMPLATE.md](HANDOFF_TEMPLATE.md). **If it is not in a file under `Docs/handoffs/`, it did not happen** ([SWARM_OPS.md](SWARM_OPS.md) §3–§4).

---

## Hard rules (pointers only)

| Rule | Authority |
|------|-----------|
| Files-only handoffs | [SWARM_OPS.md](SWARM_OPS.md) §3, §4 |
| Exclusive ownership — no two writers on same path/collection | [SWARM_OPS.md](SWARM_OPS.md) §1 |
| Implementer does **not** self-complete; Lead stamps **`APPROVE *`** | [docs/human-use/OWNERSHIP.md](../docs/human-use/OWNERSHIP.md) · [SWARM_OPS.md](SWARM_OPS.md) §1 |
| DESKTOP evidence = **Conductor parent** only; Test writes packets and scores returned evidence | [SWARM_OPS.md](SWARM_OPS.md) §4a, §16 · [CLOUD_AGENT_PACKET.md](CLOUD_AGENT_PACKET.md) |
| **Fix** = defect-only; no scope creep | This doc §Stage table; Conductor refuses expanded Fix packets |
| **Metric ≠ visual** where both apply (e.g. grep PASS vs shot framing) | Score both; Lead eyeball for taste — see harness docs in `docs/Automation/` |

Cloud agents merge and **return**; they do not run DESKTOP Shell. Test requests DESKTOP proof via Conductor parent ([WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md)).

---

## Minimal wave packet (Conductor → stage owner)

Conductor fills one packet per lap; workers stop when handoff exists.

```
INPUTS (Conductor)
  - Packet ID: PDF-{track}_{slug}
  - Mode: SWARM | HYBRID (which stage runs where)
  - Read paths: canon row, prior handoff(s), PHASE_BOARD row if any
  - Write paths: exclusive list for this stage
  - Success: checklist + evidence paths required
  - Host: CLOUD | DESKTOP (DESKTOP tasks → Conductor parent only)

STAGE OUTPUT (owner)
  - Artifacts at listed paths
  - Docs/handoffs/PDF_{DESIGN|IMPL|TEST|FIX}_{slug}.md
  - Blockers → KNOWN_ERRORS / AUTOMATION_GAPS if applicable

NEXT (Conductor)
  - Design  → Implement (refuse if no spec paths)
  - Implement → Test (refuse if no artifact paths)
  - Test PASS → Lead gate recommendation (no invented APPROVE)
  - Test FAIL → Fix packet (defect IDs + paths only)
  - Fix → Test re-Test (same checklist; append § Re-verify when fixing prior hard-fail — SWARM_OPS §4c)
```

---

## Loop diagram

```
Lead steer ──► Conductor
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
  Design ──► Implement ──► Test ──► Lead APPROVE *
                  ▲            │
                  │            ▼ FAIL
                  └──── Fix ◄──┘
                         └──► re-Test
```

---

## Host Pulse (ops — not a product phase)

Tool-agnostic external heartbeat for pending Acts. Spec: [Docs/handoffs/HOST_PULSE.md](../Docs/handoffs/HOST_PULSE.md).

| Aggregate | Meaning | Chat |
|-----------|---------|------|
| `healthy` | Targets OK within stall threshold (default **300s**, floor 5m) | Quiet |
| `blocked` | Host/tool down during pending Act | Transition notify |
| `failed` | Explicit fail signal | Transition notify |

Product `soft_fail`/`closed_fail` remain Test-owned and apply only after Act. No `APPROVE *` for pulse. **Primary MVP:** Conductor **5m** pulse (direct re-check). Optional DESKTOP helper → `Saved/host_pulse.json` is nice-to-have, not mandatory. **Mid-Act DESKTOP stall:** hard recovery budgets in [HOST_PULSE.md § DESKTOP stall protocol](../Docs/handoffs/HOST_PULSE.md#desktop-stall-protocol-conductor-owned) (Conductor-owned; one recover cycle, ≤10 min before Lead). **Console-kill** (Lead closes attached UE log console) → **`blocked`**, not product fail — [HOST_PULSE.md § Console-kill](../Docs/handoffs/HOST_PULSE.md#console-kill-log-window-closes-ue).

**UE prove one-shot:** [Docs/UE_BIBLE.md](../Docs/UE_BIBLE.md) — HomeWorld DESKTOP/MCP do/don’t (logging, stall budgets, PS-C lessons, cheap-iterate locks); not a generic Unreal wiki. **Anti-ladder hard rules:** [UE_BIBLE §2b](../Docs/UE_BIBLE.md#2b-anti-ladder-harness-hard-rules) (Conductor/Lead — one repro before ladder PR; no third ladder).

---

## See also

| Doc | Role |
|-----|------|
| [Docs/UE_BIBLE.md](../Docs/UE_BIBLE.md) | DESKTOP/MCP prove operator bible (token-lean) |
| [SWARM_OPS.md](SWARM_OPS.md) | Full process, gates, QA law |
| [PHASE_BOARD.md](PHASE_BOARD.md) | Conductor-only status rows |
| [CLOUD_AGENT_PACKET.md](CLOUD_AGENT_PACKET.md) | Cloud assignee header + evidence |
| [docs/human-use/SWARM_MODE_ROUTING.md](../docs/human-use/SWARM_MODE_ROUTING.md) | SWARM / NON-SWARM / HYBRID |
| [START_HERE.md](../START_HERE.md) | Conductor boot |
