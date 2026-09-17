# Handoff — HS-D Evidence & Re-verify (Conductor parent DESKTOP)

| Field | Value |
|-------|-------|
| **Phase** | HS-D |
| **Status** | **EVIDENCE FILED (docs/scripts)** — DESKTOP proof **PENDING Conductor parent** |
| **Lead gate** | **`APPROVE HS-D`** — **not claimed** |
| **Spec** | [Docs/17d_HS_EVIDENCE.md](../17d_HS_EVIDENCE.md) |
| **Host (DESKTOP)** | **DESKTOP-21CT3H0** — Conductor **parent** only ([HR3_A_WINDOWS_EXEC.md](HR3_A_WINDOWS_EXEC.md)) |
| **Host (CLOUD)** | Linux — docs + `evidence:grep` unit tests + `preflight:ue --assets-only` |
| **Grep prefixes** | `FORM:` `FALLBACK:` `HEAL:` `NURTURE:` `DAWN:` `TAME:` `GATHER:` `STORE:` `INVENTORY:` |
| **Evidence path** | This file + `Saved/Logs/HomeWorld.log` (DESKTOP) + optional `Saved/hs_d_evidence_grep.json` |
| **Preflight** | `npm run preflight:ue` (DESKTOP); cloud: `--skip-mcp --assets-only` |
| **Prior lanes** | [HR3_B_UE_PREFLIGHT.md](HR3_B_UE_PREFLIGHT.md) · [HR3_D_EVIDENCE_LANE.md](HR3_D_EVIDENCE_LANE.md) |

**Executor note:** Cursor Task / cloud agents **must not** claim DESKTOP Shell, MCP, or PIE. Steps below are for the **Conductor parent** session only. Do **not** invent Output Log greps.

---

## Cloud / PR evidence (already landable without DESKTOP)

| Check | Command | Expected |
|-------|---------|----------|
| Assets-only preflight | `npm run preflight:ue -- --skip-mcp --assets-only` | exit **0** |
| Preflight unit tests | `npm run preflight:ue:test` | exit **0** |
| Evidence-grep unit tests | `node --test scripts/evidence-grep.test.js` | exit **0** |

Paste CI / local cloud results into PR body when available. Leave DESKTOP rows blank until parent runs them.

---

## Conductor parent — DESKTOP checklist (do not fake)

Machine: **DESKTOP-21CT3H0** · `machineId` per [WINDOWS_BRIDGE.md](../../docs/Setup/WINDOWS_BRIDGE.md).

### A. Host hygiene

- [ ] `git pull` on branch/PR merge tip (or `main` after merge)
- [ ] If C++ changed: `.\Tools\Safe-Build.ps1` exit **0**
- [ ] Open Editor (`HomeWorld.uproject`); MCP green on port **55557**

### B. Preflight (HR3-B lane)

```powershell
# MCP: execute_python_script("preflight_ue_editor.py")
npm run preflight:ue -- --require-editor
```

| Step | Exit | Notes |
|------|------|-------|
| `preflight_ue_editor.py` | _pending_ | Writes `Saved/preflight_ue_editor.json` |
| `preflight:ue -- --require-editor` | _pending_ | Must be **0** before verb PIE |

### C. Optional PIE + markers (human or console — still not a farm)

Map: `/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers`

| Prefix | How to provoke (cue) | Pass? | Excerpt |
|--------|----------------------|-------|---------|
| `FORM:` | Phase / form path per Docs/12c | | |
| `FALLBACK:` | Glide + portals | | |
| `HEAL:` | Spirit / heal path | | |
| `NURTURE:` | N1/N2 | | |
| `DAWN:` | Dawn phase | | |
| `TAME:` | Beast pad | | |
| `GATHER:` | Ore / wood / herb | | |
| `STORE:` | Deposit/withdraw at store prop | | |
| `INVENTORY:` | Console `hw.Inventory.Dump` | | |

Runbooks: [12c](../12c_NP_C_FORM_V1.md) · [12d](../12d_NP_D_SYS_V3_V4.md) · [12e](../12e_NP_E_SYS_V6_V8.md) · [PL_C_LOOP_UX.md](PL_C_LOOP_UX.md).

### D. Scripted score (after log exists)

**Before greps:** in PIE run **`log LogTemp Log`** so `Log`-level verb lines are captured. VP2 success-path runbook: [VP2_B_FIX.md](VP2_B_FIX.md).

```powershell
npm run evidence:grep -- --log Saved/Logs/HomeWorld.log --json Saved/hs_d_evidence_grep.json
# Optional strict (exit 1 if any required prefix MISSING):
# npm run evidence:grep -- --log Saved/Logs/HomeWorld.log --strict
```

Paste stdout table + JSON path here. **MISSING** rows without Lead **WAIVE** block polish unlocks that depend on those greps ([SWARM_OPS.md](../../swarm/SWARM_OPS.md) §4c · [17d](../17d_HS_EVIDENCE.md)).

### E. Re-verify reminder

If filing evidence after a blocker-fix that superseded a prior hard-fail (e.g. historical VP-A):

1. Append **§ Re-verify** to the **prior** handoff (keep original FAIL/WAIVE).
2. Update [PHASE_BOARD.md](../../swarm/PHASE_BOARD.md) re-verify row.
3. Unlock polish only on PASS or Lead per-prefix WAIVE.

---

## Pass/fail summary (fill after DESKTOP)

| Layer | Result | SHA / time (ET) |
|-------|--------|-----------------|
| Cloud preflight + evidence:grep tests | _pending CI_ | |
| DESKTOP preflight `--require-editor` | _pending parent_ | |
| DESKTOP evidence:grep table | _pending parent_ | |
| Lead **`APPROVE HS-D`** | **PENDING** | |

---

## Hard rules

- Docs/07 CLOSED — no reopen
- No free-flight / flight HUD
- No invented greps
- No `.uasset` / `.umap` commits
- No DESKTOP claims from Task executors or cloud VMs
- Do **not** claim **`APPROVE HS-D`** in this handoff

---

*HS-D handoff — DESKTOP proof steps for Conductor parent. Executor filing is docs/scripts only.*

## DESKTOP Conductor-parent smoke (2026-09-17 ET)

Host: **DESKTOP-21CT3H0** · main tip `2bc2ce4` (PR #92 merged) · MCP ping **OK**.

| Check | Result |
|-------|--------|
| `npm run evidence:grep:test` | **6/6 PASS** |
| `node scripts/evidence-grep.js --log Saved/Logs/HomeWorld.log` | Tool runs; current log **0/9** verb prefixes (**MISSING** — no fresh PIE this session) |
| Full PIE verb table | **NOT RUN** this session — checklist remains for optional Lead/Conductor PIE before or after **`APPROVE HS-D`** |

Honest: HS-D deliverable = host-side tooling + re-verify policy. Fresh Alt+P greps are **not** claimed.

