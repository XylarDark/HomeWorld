# Cloud agent packet — Conductor → Cursor cloud agent

**When to use:** Conductor assigns a **docs-only** or **C++-touching** task to a Cursor cloud agent (Linux VM, no UE/MCP). Fill this packet and attach paths from [HANDOFF_TEMPLATE.md](HANDOFF_TEMPLATE.md).

**Process authority:** [SWARM_OPS.md](SWARM_OPS.md) · **Windows follow-up:** [docs/Setup/WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) · **HR3-A lane:** [Docs/handoffs/HR3_A_WINDOWS_EXEC.md](../Docs/handoffs/HR3_A_WINDOWS_EXEC.md) · **HR3-D evidence lane:** [Docs/handoffs/HR3_D_EVIDENCE_LANE.md](../Docs/handoffs/HR3_D_EVIDENCE_LANE.md)

---

## Packet header

| Field | Value |
|-------|-------|
| **Packet ID** | HR-{phase}_{slug} or NP-{id}_{slug} |
| **Assigner** | CND (Conductor) |
| **Target** | Cursor cloud agent |
| **Branch** | `cursor/<descriptive-kebab-name>-b3a5` |
| **Base branch** | `main` (fetch before branch) |
| **Hard rules** | Docs/07 CLOSED · FALLBACK armed · default KEEP-LOCAL Content; allowlist per [Docs/20](../Docs/20_UASSET_AI_POLICY.md) · docs/swarm only unless packet says otherwise |

---

## Branch naming (cloud agents)

```
cursor/<descriptive-name>-b3a5
```

- Prefix **`cursor/`** required for cloud-agent branches.
- Suffix **`-b3a5`** required (case-insensitive filesystem safety).
- Lowercase kebab-case only.
- One logical change per PR; push with `git push -u origin <branch>`.

---

## Evidence paths (required in PR)

| Evidence | Where |
|----------|--------|
| **PR URL** | GitHub PR link in handoff + PHASE_BOARD note |
| **Merge SHA** | Squash-merge commit on `main` after Lead/Conductor merge |
| **CI status** | `validate` + `python-lint` green (required for **all** PRs) |
| **`ci.yml` / `build-win64`** | **Required** when PR touches C++ paths: `Source/**`, `**/*.Build.cs`, `*.uproject`, `Plugins/**/Source/**` — self-hosted `windows`/`ue58` runner on **DESKTOP-21CT3H0**. **Lead waiver:** PR body `Lead waiver: build-win64` or label `lead-waiver-build-win64` — see [CI_POLICY.md](../docs/Setup/CI_POLICY.md) (HR2-C) |
| **Windows validation** | **DESKTOP owner = Conductor parent only** — not cloud VM, not Task executors. Safe-Build → Editor → MCP on DESKTOP-21CT3H0 after merge |

List repo-relative paths for every deliverable (files created/changed). Gate claims without paths are invalid per SWARM_OPS.

---

## Handoff PR contract (HR3-D — required fields)

Every cloud-agent PR that files swarm evidence must include in **PR body** and **`Docs/handoffs/*.md`**:

| Field | CLOUD example | DESKTOP follow-up example |
|-------|---------------|---------------------------|
| **Host** | `CLOUD` (Linux VM) | `DESKTOP-21CT3H0` |
| **Grep prefixes** | N/A for docs-only | `FORM:`, `FALLBACK:`, `HEAL:`, `NURTURE:`, `DAWN:`, `TAME:`, `GATHER:` |
| **Evidence path** | `Docs/handoffs/HR3_D_EVIDENCE_LANE.md` | `Docs/handoffs/VP_A_PIE.md` + `Saved/Logs/HomeWorld.log` |
| **Pass/fail table** | Deliverable checklist (DONE/PENDING) | One row per prefix — PASS / FAIL / WAIVED + excerpt |

Full spec: [SWARM_OPS.md](SWARM_OPS.md) §4b · [HR3_D_EVIDENCE_LANE.md](../Docs/handoffs/HR3_D_EVIDENCE_LANE.md).

### Re-verify (cloud agents do not run this)

After a **blocker-fix** DESKTOP phase (e.g. **VP-B**), Conductor parent **re-runs prior hard-fail greps** (VP-A) before unlocking **VP-C**. Cloud agents document the rule only; DESKTOP owner executes re-verify. See [14_VP_VERIFY_POLISH.md](../Docs/14_VP_VERIFY_POLISH.md) § Re-verify.

---

## Cloud VM checklist — do NOT on cloud

Cloud agents run on **Linux without Unreal Engine**. Do **not** attempt:

- [ ] **MCP** / UnrealMCP tools (Editor not running)
- [ ] **`.\Tools\Safe-Build.ps1`** or any C++ build on the cloud VM
- [ ] **`execute_python_script`** / Editor Python (no Editor)
- [ ] **GUI automation** (`Content/Python/gui_automation/`) — Windows Editor only
- [ ] Commit **`.uasset`** / **`.umap`** outside [Docs/20 allowlist](../Docs/20_UASSET_AI_POLICY.md) — default KEEP-LOCAL; binary work on DESKTOP

**Do on cloud:** docs, markdown, validate.yml-safe JSON, C++ source edits, Python scripts (untested in Editor until Windows handoff).

**Windows handoff:** After merge, **Conductor parent only** (not Task executor) follows [WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) and [HR3_A_WINDOWS_EXEC.md](../Docs/handoffs/HR3_A_WINDOWS_EXEC.md) for DESKTOP Shell, build, dress, PIE, MCP validation. Cloud agent **returns after merge** — does not claim Windows Shell. Task workers **FAIL** DESKTOP routing (HS-B / HR3-A).

**HR3 gate refs:** Lead **`APPROVE HR3-A`** per [Docs/15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md) before DESKTOP exec implementation PRs. Task executors **cannot** route Shell to DESKTOP — see HR3-A handoff failure modes.

---

## ResourceExhausted — sanctioned Contents API fallback (HS-B)

If clone / cloud workspace hits **ResourceExhausted** (or equivalent checkout failure):

1. **Do not** invent a second full clone strategy or claim DESKTOP Shell from the cloud VM.
2. Complete **docs-only** work via GitHub **Contents API** — e.g. `gh api repos/<owner>/<repo>/contents/<path>` (get / put / create branch / open PR). **No local clone required.**
3. Still honor hard rules: Docs/07 CLOSED · FALLBACK armed · no combat · KEEP-LOCAL Content (allowlist per Docs/20) · exclusive write paths.
4. Record in handoff **Blockers** or Evidence: `ResourceExhausted → gh Contents API` (path is **sanctioned**, not a waiver theater).

This is the same path used for Docs/17a inventory and Docs/17b ops filings.

---

## No DESKTOP for executors / Task workers (HS-B)

| Actor | DESKTOP Shell / MCP / PIE |
|-------|---------------------------|
| **Conductor parent** | **YES** — only happy path ([WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md)) |
| **Task executor / worker subagent** | **NO** — tools missing; prior Linux-`cursor` claims unreliable |
| **This cloud packet target** | **NO** — return after merge; Conductor parent runs Windows follow-up |

Do **not** assign DESKTOP evidence to Task executors. See [HR3_A_WINDOWS_EXEC.md](../Docs/handoffs/HR3_A_WINDOWS_EXEC.md).

---

## Batch digest preference (HS-B)

Prefer **phase-end digests** for Lead-facing updates:

- One short digest at phase gate: status · PR URL(s) · merge SHA(s) · next gate string
- **Avoid** per-CI / per-push spam in Lead chat
- Stamp-only PRs for Lead `APPROVE *` remain valid; Conductor batches the narrative

---

## Return handoff

On completion, Conductor files `Docs/handoffs/<packet_id>.md` using [HANDOFF_TEMPLATE.md](HANDOFF_TEMPLATE.md) § Cloud agent PR section.

**Gate:** Active track **Docs/17 HS** — Lead **`APPROVE HS-*`** per [Docs/17_HS_AUDIT_STRATEGY.md](../Docs/17_HS_AUDIT_STRATEGY.md). Closed refs: **`APPROVE HR3-*`** ([Docs/15](../Docs/15_HR3_A_PLUS.md)), **`APPROVE HR2-*`** ([Docs/13](../Docs/13_HR2_HARNESS_REFINE.md)), legacy **`APPROVE HR-*`** ([Docs/11](../Docs/11_SWARM_HARNESS_REFINE.md)).
