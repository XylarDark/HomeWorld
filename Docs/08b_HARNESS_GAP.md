# Docs/08b — WAVE B Harness Gap Analysis

| Field | Value |
|-------|-------|
| **Board status** | WAVE B — HARNESS GAP COMPLETE (awaiting Lead gate) |
| **Date** | 2026-09-17 |
| **Author** | Audit executor (HomeWorld) |
| **Parent plan** | [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md) |
| **Inventory input** | [08a_INVENTORY.md](08a_INVENTORY.md) |
| **Companion repo** | [XylarDark/DevEnvTemplate](https://github.com/XylarDark/DevEnvTemplate) |
| **Hard rules honored** | Docs/07 CLOSED not reopened; FALLBACK FLIGHT armed; no Source/ gameplay rewrite; no binary Content; no WAVE C/D work |

**Gate:** stop for Lead **`APPROVE WAVE B`**

---

## Executive summary

HomeWorld adopts DevEnvTemplate as a **git submodule** (agent-context + operational-memory layers + doctor). The host **AGENTS.md**, **Safe-Build** stack, **MCP** setup, **session ops** (`SESSION_LOG`, `DAILY_STATE`), and **swarm ops** (`swarm/SWARM_OPS.md`) are **intentionally richer** than the template baseline — the template is a generic doctor; HomeWorld is a UE 5.7 game with a signed MVP swarm canon in capital **`Docs/`**.

This WAVE closes **documentation pointer gaps** (README, AGENTS, build policy, quarantine banners) and records remaining harness diffs for WAVE C/F. No gameplay C++ was changed.

---

## Gap table

| Area | HomeWorld (current) | DevEnvTemplate (companion) | Gap | Proposed fix |
|------|---------------------|----------------------------|-----|--------------|
| **Entry / canon gravity** | `AGENTS.md` opens with VisionBoard + `docs/TaskLists/`; MVP swarm section is mid-file | Lean `AGENTS.md` (~200 lines); host writes own; no game canon | Newcomers/agents miss **`START_HERE` + `Docs/`** as MVP truth | **Done (this PR):** AGENTS + README lead with START_HERE / Docs/; TaskLists demoted to session ops |
| **Always-applied rules** | 20+ `.cursor/rules/*.mdc` always-on (00–20, ue57-*) | Zero always-applied rules; glob-scoped only | ~3k+ tokens/turn vs template budget | **Accepted decline** (08a); migrate in dedicated pass — not WAVE B |
| **Build policy** | `Tools/Safe-Build.ps1` wraps `Build-HomeWorld.bat`; protocol in `docs/Editor/EDITOR_BUILD_PROTOCOL.md` | No UE build scripts (Node `npm run build` only) | Some docs still say “run Build-HomeWorld.bat” without Safe-Build | **Done (this PR):** [docs/Setup/BUILD_POLICY.md](../docs/Setup/BUILD_POLICY.md); AGENTS Commands bullet clarified |
| **MCP setup** | `Setup-MCP.bat`, `docs/Setup/MCP_SETUP.md`, `.cursor/mcp.json.example`, port 55557 | `docs/guides/mcp-hygiene.md`, `.cursor/mcp.json.example` | HomeWorld Quick start still says Build-HomeWorld.bat post-setup | **Partial (this PR):** MCP_SETUP quick start → Safe-Build; full path audit deferred WAVE F |
| **Session log / DAILY_STATE** | Massive `docs/SESSION_LOG.md`; `docs/TaskLists/DAILY_STATE.md` for daily ops | No session log; human-use CYCLE only | Session ops treated as product canon in places | **Done (this PR):** AGENTS labels TaskLists/SESSION_LOG as **session ops**, not GDD; quarantine note on 30-day lists |
| **Swarm ops** | `swarm/SWARM_OPS.md`, Conductor, PHASE_BOARD, `Docs/07` CLOSED | Optional `docs/guides/multi-agent-swarm.md` (generic) | Two agent OSes: swarm vs **agent company** loop | **Done (this PR):** quarantine banner on `docs/Automation/AGENT_COMPANY.md`; START_HERE already distinguishes |
| **DevEnvTemplate submodule** | Gitlink pinned; checkout often **empty** until init | Full repo with `dist/` prebuilt in clone | `npm run doctor` fails on fresh clone | **Documented below;** init commands; pin update optional WAVE F |
| **Doctor / sync** | Root `package.json` → `DevEnvTemplate/dist/...` | Node 24+; `npm run doctor`, `sync` CLI | Pinned SHA **behind** template `main`; EBADENGINE on Node 22 accepted | WAVE F: evaluate bump gitlink after `doctor:build` smoke on Lead machine |
| **KNOWLED/errors** | `docs/KNOWN_ERRORS.md` (UE-heavy, large) | Stub + fold UE into host | HomeWorld correctly owns UE errors | **KEEP** — no merge |
| **Human Use** | `docs/human-use/OWNERSHIP.md`, CYCLE | Same layer via sync | Aligned | **KEEP** |
| **Skills** | `.agents/skills/` localized (Safe-Build, UE paths) | Core six + extras catalog | Portability callouts present | **KEEP**; refresh via `npm run sync:apply` when bumping submodule |
| **VisionBoard/MVP** | Pre-swarm gap lists, duplicate sign-off | N/A | Fights **`Docs/01`–`07`** | **Done (this PR):** `VisionBoard/MVP/README.md` quarantine pointer |

---

## Build policy (canonical)

**Policy:** Agents and autonomous scripts use **`.\Tools\Safe-Build.ps1`**. Humans may call **`Build-HomeWorld.bat`** directly when the Editor is already closed.

| Script | Role |
|--------|------|
| **`Tools/Safe-Build.ps1`** | **Preferred for agents.** Closes Editor if running → invokes `Build-HomeWorld.bat` → retries once on Live Coding / exit code 6. Optional `-LaunchEditorAfter` for MCP. |
| **`Build-HomeWorld.bat`** | Low-level UE **Build.bat** wrapper; writes `Build-HomeWorld.log`. Called **by** Safe-Build — not a rival entry point. |
| **`py Content/Python/run_automation_cycle.py`** | Orchestrator; applies same Editor-close protocol when build is enabled. |

Full protocol: [docs/Editor/EDITOR_BUILD_PROTOCOL.md](../docs/Editor/EDITOR_BUILD_PROTOCOL.md).  
Short agent note: [docs/Setup/BUILD_POLICY.md](../docs/Setup/BUILD_POLICY.md).

---

## DevEnvTemplate submodule — init / pin status

| Item | Value |
|------|-------|
| **Remote** | `https://github.com/XylarDark/DevEnvTemplate.git` |
| **Path** | `DevEnvTemplate/` (git submodule) |
| **Pinned SHA (HomeWorld main gitlink)** | `213673ff181743a703ab390af0d43097f889a0f9` |
| **Pinned commit message** | `feat(agents): put the human on steer, taste, and test` |
| **Template `main` HEAD (2026-09-17 fetch)** | `2efd7569a698e73a04279feaebaae1eb55c4e1c0` (`Merge pull request #29 … multi-agent-swarm-guide`) |
| **Drift** | HomeWorld pin is **behind** template main (includes multi-agent-swarm guide, sync fixes). Bump is **optional** — evaluate in WAVE F after smoke `npm run doctor:build`. |
| **Fresh clone symptom** | Empty `DevEnvTemplate/` → `npm run doctor` fails (no `dist/scripts/doctor/cli.js`) |

### Init commands (safe — does not force-push template)

```bash
# From HomeWorld repo root
git submodule update --init --recursive DevEnvTemplate

# Verify pin
git submodule status DevEnvTemplate
# Expected: 213673ff181743a703ab390af0d43097f889a0f9 DevEnvTemplate

# One-time: build doctor CLI inside submodule (if dist missing)
npm run doctor:build

# Health check (Node 20+; template prefers 24+ — EBADENGINE warning accepted)
npm run doctor
```

**Do not** force-push DevEnvTemplate from HomeWorld automation. Template releases flow through the companion repo; HomeWorld only updates the **gitlink** commit when Lead approves a pin bump.

---

## Recommended pointer fixes (this PR)

| File | Change |
|------|--------|
| [AGENTS.md](../AGENTS.md) | Lead with START_HERE + Docs/ MVP canon; session ops vs product canon; build policy one-liner; quarantine links |
| [README.md](../README.md) | Getting started → START_HERE, Docs/, swarm; demote old workflow-only paths |
| [docs/Setup/BUILD_POLICY.md](../docs/Setup/BUILD_POLICY.md) | **New** — Safe-Build → Build-HomeWorld.bat |
| [docs/Setup/MCP_SETUP.md](../docs/Setup/MCP_SETUP.md) | Quick start build step → Safe-Build |
| [docs/Automation/AGENT_COMPANY.md](../docs/Automation/AGENT_COMPANY.md) | Quarantine banner → prefer swarm Conductor |
| [VisionBoard/MVP/README.md](../VisionBoard/MVP/README.md) | **New** — historical/quarantine pointer to Docs/ |
| [Docs/README.md](README.md) | Link 08b + gate |

**Deferred (WAVE C/F):** Bump DevEnvTemplate gitlink; retire always-applied rules migration; MCP_SETUP full audit; archive `Tools/Start-AllAgents*` after Lead SIGN OFF AUDIT.

---

## Parallel status — PR #10 (Docs/05 markers)

| Field | Value |
|-------|-------|
| **PR** | [#10 — Docs/05: place_vs_mvp_markers + first-pass handoff](https://github.com/XylarDark/HomeWorld/pull/10) |
| **State** | OPEN, GitHub **mergeable** |
| **CI** | **validate** job **FAILED** — missing `docs/workflow/30_DAY_SCHEDULE.md` (path moved to `docs/TaskLists/` per DOCS_LAYOUT) |
| **Action** | **Not merged** — dirty CI; does not block WAVE B. Fix CI on #10 branch or merge after validate green. |

---

## Board / Actions / Gate / Next (for Lead)

| | |
|---|---|
| **Board** | WAVE B deliverable ready — harness gap doc + pointer-align PR |
| **Actions** | Review PR; comment **`APPROVE WAVE B`** on PR to unlock WAVE C (boot health) |
| **Gate** | `APPROVE WAVE B` — do not start WAVE C/D until granted |
| **Next (after gate)** | WAVE C — Editor opens UE 5.7.x without assert; Safe-Build green; close GoToBed/Meal boot-health class |

```
STOP — Lead approval required
Type: APPROVE WAVE B
```

Hard rules remain: **Docs/07 CLOSED** · **FALLBACK FLIGHT armed** · no gameplay rewrite in WAVE B.
