# Docs/10 — Post-Audit Wrap (CLOSED)

| Field | Value |
|-------|-------|
| **Status** | **CLOSED** — post-audit track complete |
| **Date** | 2026-09-17 |
| **Parent** | [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md) |
| **Scope** | Finish Docs/08 “Next” leftover: master material graphs + NightMix wiring |

---

## 1. What this wrap closed

| Track | Deliverable | Status |
|-------|-------------|--------|
| **Docs/05** | UE import first pass, VS_MVP markers, `MPC_HomeWorld_Time` NightMix stub | **DONE** |
| **Docs/06** | VS_MVP dress spec / handoff | **DONE** |
| **Docs/09** | FALLBACK glide + portal contracts (PR #19/#20) | **DONE** |
| **Docs/08e leftover** | Ten `M_*` master material graphs + NightMix from MPC | **DONE** (this wrap) |

**NightMix runtime:** `UHomeWorldTimeOfDaySubsystem::ApplyNightMixForPhase` / `SetNightMixScalar` pushes phase values to `MPC_HomeWorld_Time` scalar **NightMix** (Day=0, Dusk=0.35, Night=0.85, Dawn=0.15). Masters read the same scalar via **CollectionParameter** in material graphs.

**Editor automation:** `Content/Python/create_master_materials.py` (stub entry: `create_master_materials_stub.py`) — idempotent create/upgrade of all ten masters under `/Game/HomeWorld/Materials/Masters/` from `Lib/06_Materials_Master/M_*.json` with day→night overlay (tint + desaturate + value_mul; no second texture set).

---

## 2. Checklist — landed in repo

- [x] Ten named masters only (`M_StylizedGrass` … `M_Nurtured`) — no 11th master
- [x] Parameters: BaseColor, Roughness, Variation, NightMix, Emissive (Docs/02)
- [x] NightMix: `Max(MPC CollectionParameter, local ScalarParameter)` for runtime + MI demo
- [x] `M_SpiritUnlit`: Unlit / emissive-forward path
- [x] `M_FoliageCard`: BLEND_MASKED + opaque opacity stub (card alpha texture deferred)
- [x] MPC consistency: `place_vs_mvp_markers.create_nightmix_mpc` + `wire_nightmix_mpc_note.py` use scalar **NightMix**
- [x] No `.uasset` / `.umap` binaries committed — graphs built on Windows Editor only
- [x] Post-audit closeout doc (this file)

---

## 3. Explicitly OUT of wrap (do not reopen here)

| Item | Reason |
|------|--------|
| **V3–V8 SYS** gather / tame / heal / nurture inventory | Lead scope — not post-audit wrap |
| **Docs/07** vertical-slice sign-off | CLOSED — do not reopen |
| **Form swap / glide / portal BP dress** | Editor dress wave; FALLBACK docs only |
| **Lumen / Nanite gates** | Deferred per Docs/04 |
| **Free-flight** | Not in MVP; FALLBACK CRUMB glide only |
| **WAVE F deletes / archive** | Separate Lead gate after audit sign-off |
| **NIGHTMIX_DEMO sphere row screenshot** | Blender/Editor lookdev evidence — optional follow-up |

---

## 4. How to run (Windows DESKTOP)

1. Open project in **Unreal Editor 5.7** on Windows.
2. Ensure MPC exists (once): run `place_vs_mvp_markers.py` or `wire_nightmix_mpc_note.py`.
3. Build masters: **Tools → Execute Python Script** → `Content/Python/create_master_materials.py`  
   Or MCP: `execute_python_script("create_master_materials.py")`.
4. Re-run is safe (idempotent). To rebuild graphs: `create_master_materials.py` with `--force`.
5. Verify Output Log prefix `create_master_materials:` — expect `created`/`upgraded`/`skipped` counts.
6. Optional PIE: `TimeOfDaySubsystem` phase changes should log `HomeWorld: NightMix=…`.

See also: [handoffs/POST_AUDIT_MASTER_MATERIALS.md](handoffs/POST_AUDIT_MASTER_MATERIALS.md).

---

## 5. Next — Lead next-phase audit

Post-audit backlog for this track is **closed**. Do **not** invent new WAVE numbers here.

**Lead action:** Start the **next-phase audit** (product / lookdev / UE dress priorities) on a fresh gate — outside this wrap doc. WAVE F archive/delete remains gated on prior audit sign-off per [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md) when Lead chooses to run it.

```
POST-AUDIT WRAP: CLOSED
Next owner: Lead — next-phase audit (no new WAVE id in Docs/10)
```
