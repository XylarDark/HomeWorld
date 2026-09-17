# Handoff

- **ID:** P{n}_{ROLE}_{slug}
- **Phase:**
- **Role:**
- **Owner agent:**
- **Status:** DONE | BLOCKED | PARTIAL
- **Date:**

## Artifacts written (paths)

-

## Names created

| Name | Type | Master material | Collection |
|---|---|---|---|
| | SM / M / FX / CAM / LIT | | |

## Phase exit boxes I claim

- [ ]

## What I did not invent

- [ ] No extra biome
- [ ] No extra beast or resource
- [ ] No new master shader family
- [ ] No free-flight model
- [ ] No combat
- [ ] Did not edit another owner's path

## Inputs I used

-

## Blockers

- (If blocked by a real failure or automation gap, link [docs/KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md) or [docs/Automation/AUTOMATION_GAPS.md](../docs/Automation/AUTOMATION_GAPS.md) entry)

## Risks for the next owner

-

## Evidence

Gate claims without evidence are invalid. List checkable artifacts:

- Repo-relative paths (files, handoffs, preview READMEs):
- Screenshot / frame / render / checklist output:
- Test or verify notes (command run + outcome):

---

## Cloud agent PR (HR / post-audit)

Use when a **Cursor cloud agent** ships a PR (no UE/MCP on the VM). Full packet: [CLOUD_AGENT_PACKET.md](CLOUD_AGENT_PACKET.md).

### Branch & PR

- **Branch:** `cursor/<descriptive-name>-b3a5` (lowercase kebab; suffix required)
- **PR URL:**
- **Merge SHA:** (after squash-merge to `main`)
- **CI:** `validate` + `python-lint` — pass/fail + link

### Cloud VM — do NOT

- [ ] MCP / UnrealMCP on cloud VM
- [ ] `.\Tools\Safe-Build.ps1` or C++ build on cloud VM
- [ ] Editor Python / GUI automation on cloud VM
- [ ] `.uasset` / `.umap` commits

**Windows follow-up:** [docs/Setup/WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) — **Conductor parent only** on DESKTOP-21CT3H0 (Task executors **FAIL**). Cloud agents do not claim DESKTOP Shell.

### Evidence paths (repo-relative)

-

### DESKTOP evidence (HR3-D — when host = DESKTOP-21CT3H0)

| Field | Value |
|-------|-------|
| **Host** | DESKTOP-21CT3H0 |
| **Grep prefixes** | (phase-specific — e.g. VP-A: `FORM:`, `FALLBACK:`, …) |
| **Log source** | `Saved/Logs/HomeWorld.log` |
| **Pass/fail table** | One row per prefix — PASS / FAIL / WAIVED + excerpt |
| **Preflight** | `npm run preflight:ue` exit code |

Re-verify after blocker-fix: append **§ Re-verify** to prior handoff — [HR3_D_EVIDENCE_LANE.md](../Docs/handoffs/HR3_D_EVIDENCE_LANE.md).


### ResourceExhausted / Contents API fallback (HS-B)

- [ ] Hit ResourceExhausted (or clone fail)? → used sanctioned **`gh` Contents API** (no invented second clone)
- [ ] Did **not** claim DESKTOP Shell / MCP / PIE from cloud VM or Task executor
- Notes:

### Lead-facing digest (prefer phase-end)

- [ ] Phase-end digest prepared (status + PR links + SHAs) — not per-CI spam
- Digest / PR URLs:
