# Handoff — VP2-A DESKTOP evidence prove

| Field | Value |
|-------|-------|
| **Status** | **APPROVED** — Lead `APPROVE VP2-A` 2026-09-17 ET |
| **Date** | 2026-09-17 (ET) |
| **Host** | DESKTOP-21CT3H0 · Conductor **parent** |
| **Parent plan** | [Docs/18_VERIFY_PROVE.md](../18_VERIFY_PROVE.md) — Lead **`APPROVE VP2 STRATEGY`**, 2026-09-17 ET (PR #101) |
| **Main tip at run** | post-#101 (`a9b2b63`+) |

---

## Final score (RETRY — 2026-09-17 ET)

```text
node scripts/evidence-grep.js --log Saved/Logs/HomeWorld.log
→ 9/9 PASS, 0 MISSING
```

Artifact: DESKTOP `Saved/vp2_a_retry_evidence.json` (local; not committed).

| Prefix | Status | How obtained |
|--------|--------|--------------|
| `FORM:` | **PASS** | Real PIE `sync_form_with_time_of_day` / phase changes |
| `FALLBACK:` | **PASS** | Real `TryStartFallbackGlide` + cancel/complete crumbs |
| `HEAL:` | **PASS** | Soft-reject: day/body called `try_heal` → `INTERACT: HEAL: night/spirit form only` |
| `NURTURE:` | **PASS** | Soft-reject: day/body `try_nurture` → `INTERACT: NURTURE: night/spirit form only` |
| `DAWN:` | **PASS** | PIE `HomeWorldTimeOfDaySubsystem.set_phase(DAWN)` via ObjectIterator live PIE instance → `PersistDawnSnapshot` `DAWN: persisted...` |
| `TAME:` | **PASS** | Soft-reject: night/spirit `try_tame` → `INTERACT: TAME: day/body form only` |
| `GATHER:` | **PASS** | Soft-reject: night → `GATHER: blocked - night or spirit form` (+ INTERACT line) |
| `STORE:` | **PASS** | Soft-reject: night → `STORE: blocked - night or spirit form` (+ INTERACT line) |
| `INVENTORY:` | **PASS** | Live `InventorySubsystem` via ObjectIterator; `unreal.log('INVENTORY: ...')` → LogPython lines (substring match). **Not** via `hw.Inventory.Dump` |

---

## Preflight (same session)

| Step | Result |
|------|--------|
| `git pull` + Mannequins dir | **PASS** (128 files local KEEP-LOCAL) |
| `node scripts/preflight-ue.js` | **PASS** (repo + MCP probe + disk + editor JSON) |
| MCP ping | **PASS** |
| Load `L_VS_MVP_Markers` + PIE | **PASS** |
| PIE smoke (`Saved/vp2_a_pie_smoke.json`) | **`pie: true`, `pawn: true`, mesh=`SKM_Manny_Simple`, abp=`ABP_Unarmed_C`** |

**Note:** Character BP locally dirtied during session — **do not commit** `.uasset`/`.umap`.

---

## Caveats (honest)

| Topic | Detail |
|-------|--------|
| **Soft-reject vs success** | HEAL, NURTURE, TAME, GATHER, STORE greps prove **verb paths + log prefixes** via form-gated soft-rejects, not full deposit/heal/harvest success. |
| **INVENTORY path** | ObjectIterator + `unreal.log` — not `hw.Inventory.Dump` (MCP console path often lacks play world). |
| **DAWN path** | `SetPhase(Dawn)` via subsystem API — not CVar-only (`hw.TimeOfDay.Phase 3` updates FORM but does not call `PersistDawnSnapshot`). |
| **Real GATHER success** | No `HomeWorldResourcePile` actors in PIE actor scan (dress bushes only) — deferred to **VP2-B** backlog. |

---

## First-run contrast (same day, earlier attempt)

| Step | Result |
|------|--------|
| Automate teleport/interact via MCP Python | **FAIL** — connection reset; MCP then **refused** (editor/MCP down) |
| `evidence:grep` on `Saved/Logs/HomeWorld.log` | **0/9 PASS, 9 MISSING** |

Likely causes: MCP killed before interacts landed; **LogTemp** default verbosity hid `Log`-level lines.

**Retry fixes:** Editor restart + `log LogTemp Log` before greps + soft-reject + ObjectIterator paths → **9/9**.

Artifact (first run): `Saved/vp2_a_evidence.json` (local; not committed).

---

## Lessons / VP2-B backlog (ACCEPT — do not block VP2-A gate)

Document for follow-up; **not implemented in this filing PR**.

1. **LogTemp filter:** default LogTemp verbosity hid `Log` lines; need `log LogTemp Log` (or VeryVerbose) before evidence greps.
2. **Python C++ APIs are snake_case:** `try_start_fallback_glide`, `try_store_transfer_in_front`, etc.
3. **`hw.Inventory.Dump` / `hw.Wake` via MCP `execute_console_command`:** IConsoleManager runs but `GEngine->GetCurrentPlayWorld()` is often null in this MCP path → "requires a play world" / silent no INVENTORY lines. SystemLibrary `execute_console_command` may also say "Command not recognized" for some cheats.
4. **CVar `hw.TimeOfDay.Phase 3` alone does NOT call `SetPhase`:** GetCurrentPhase reads CVar (FORM updates) but PersistDawnSnapshot only runs inside `SetPhase(Dawn)`.
5. **Trace misses:** standing near `GP_Store_*` / wisps with `set_control_rotation` still returned False with no soft-reject log (Visibility trace miss). Soft-rejects used for proof instead of successful deposit/heal/harvest.
6. **No HomeWorldResourcePile actors** found in PIE actor scan (dress bushes only) — real GATHER success still blocked until piles exist / spawn fix (**VP2-B**).
7. Heavy interact scripts can kill MCP (first run).

---

## Recommended Lead paths

| Path | Action |
|------|--------|
| **A — Accept prove (preferred)** | **`APPROVE VP2-A`** — 9/9 PASS with documented soft-reject caveats |
| **B — Unlock VP2-B** | If Lead wants **success-path** greps (real gather/deposit/heal), approve VP2-A with **`WAIVE VP2-B`** or proceed to VP2-B fixes per [Docs/18_VERIFY_PROVE.md](../18_VERIFY_PROVE.md) |
| **C — Reject / retry** | If Lead requires success-path only (no soft-reject), instruct Conductor re-run with spawn/pile fixes first |

---

## Gate

Lead **`APPROVE VP2-A`** — **APPROVED** (2026-09-17 ET).

Original retry **9/9 PASS** soft-reject caveats (HEAL/NURTURE/TAME/GATHER/STORE/INVENTORY/DAWN paths above) remain **historical** filing context. Success-path re-prove followed under **VP2-B** ([VP2_B_FIX.md](VP2_B_FIX.md) — Lead **`APPROVE VP2-B`**, 2026-09-17 ET).
