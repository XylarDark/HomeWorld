# Docs/08e — WAVE E Upgrade Pass

| Field | Value |
|-------|-------|
| **Board status** | WAVE E — UPGRADE PASS COMPLETE (awaiting Lead gate) |
| **Date** | 2026-09-17 |
| **Author** | Audit executor (HomeWorld) |
| **Parent plan** | [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md) |
| **Prior waves** | [08d_CONTENT_CANON.md](08d_CONTENT_CANON.md) (PR #14 merged — WAVE D APPROVED) |
| **Hard rules honored** | Docs/07 CLOSED not reopened; FALLBACK FLIGHT armed; no WAVE F deletes; no new off-slice features |

**Gate:** stop for Lead **`APPROVE WAVE E`**

---

## 1. Board status — WAVE E

| Item | Status |
|------|--------|
| **WAVE A–D** | COMPLETE — inventory, harness, boot health, content canon |
| **WAVE E** | **THIS DELIVERABLE** — slice-touching code/doc upgrades per [08d §7](08d_CONTENT_CANON.md#7-recommended-wave-e-upgrade-targets-slice-touching-only) |
| **WAVE F** | NOT STARTED — blocked until Lead `APPROVE WAVE E` then `SIGN OFF AUDIT` |

WAVE E scope: repoint default Python orchestration to VS_MVP + Docs/04 import; add soft PIE checks; minimal C++ NightMix hook; quarantine banners on legacy map/PCG docs; defer Editor-dress items (glide BP, master node graphs, full level dress).

---

## 2. §7 target table (slice-touching only)

| Target | Status | What changed | Evidence |
|--------|--------|--------------|----------|
| **`Source/HomeWorld/`** GameMode + TOD/NightMix | **PARTIAL** | `TimeOfDaySubsystem`: `SetNightMixScalar`, `ApplyNightMixForPhase`; `SetPhase` pushes NightMix to `MPC_HomeWorld_Time`. `GameMode::BeginPlay` recognizes VS_MVP slice levels for morning Phase Day. Glide/portal/shrine BP wiring **DEFERRED** (Editor dress). | `HomeWorldTimeOfDaySubsystem.h/.cpp`, `HomeWorldGameMode.cpp` — Safe-Build on **DESKTOP-21CT3H0** (UE not on cloud VM) |
| **`BP_HomeWorldCharacter`** + **`ABP_HomeWorldCharacter`** | **DEFERRED** | CRUMB glide + spirit/body swap need Editor Blueprint dress; FALLBACK armed in docs only. | `Docs/03_GAMEPLAY_MVP.md` FALLBACK appendix; no BP binary changes |
| **`GA_Interact`**, **`GA_Heal`**, **`GA_Place`** | **DEFERRED** | Reparent to C++ ability classes unchanged this wave; no combat GA depth. | Existing `setup_gas_abilities.py` / init path unchanged |
| **`BP_GameMode`** | **PARTIAL** | NightMix driven from C++ subsystem on phase change (GameState BP hook optional later). Portal/shrine on Docs/04 meshes **DEFERRED**. | TimeOfDaySubsystem NightMix API |
| **`/Game/HomeWorld/Materials/Masters/M_*`** + **`MI_*`** | **PARTIAL** | New `create_master_materials_stub.py` — idempotent empty Material shells (script-only, no binary commit). Full master node graphs **DEFERRED** (TA/Editor). | `Content/Python/create_master_materials_stub.py` |
| **`/Game/HomeWorld/Maps/VS_MVP/`** dressed level | **DEFERRED** | Markers/MPC script path unchanged; full SM_* dress at ANCHOR_* needs Windows Editor + imported FBX. | `place_vs_mvp_markers.py`; PIE soft checks |
| **`init_unreal.py`** | **DONE** | Comment block: VS_MVP primary; no heavy import on load; NightMix note. | `Content/Python/init_unreal.py` |
| **`pie_test_runner.py`** | **DONE** | Soft checks: `check_vs_mvp_level_asset`, `check_mpc_homeworld_time`, `check_vs_mvp_markers_in_level` — pass with SKIP when assets missing. | `Content/Python/pie_test_runner.py` |
| **`docs/PCG/*`**, **`docs/Maps/*`** | **DONE** | Quarantine banners → Docs/08d + Maps/VS_MVP primary. | `docs/Maps/DEMO_MAP.md`, `HOMESTEAD_MAP.md`, `docs/PCG/PCG_SETUP.md`, `PCG_QUICK_SETUP.md` |
| **`bootstrap_project.py`** | **DONE** | Default Step 5: `batch_import_asset_creation` + `place_vs_mvp_markers`; legacy `setup_level`/PCG opt-in via `run_pcg=True` only. | `Content/Python/bootstrap_project.py` |

**Bonus (WAVE E helpers):**

| Script | Status | Role |
|--------|--------|------|
| `wire_nightmix_mpc_note.py` | **DONE** | Logs NightMix phase map + ensures MPC via shared helper |
| `create_master_materials_stub.py` | **DONE** | Ten empty `M_*` materials under `/Game/HomeWorld/Materials/Masters/` |

---

## 3. Verification

| Check | Environment | Result | Notes |
|-------|-------------|--------|-------|
| **Safe-Build / C++ compile** | Cloud VM | **NOT RUN** | UE 5.7 Editor/toolchain not installed on cloud agent VM |
| **Safe-Build / C++ compile** | **DESKTOP-21CT3H0** (Windows) | **REQUIRED** | Run `.\Tools\Safe-Build.ps1` after merge; validates TimeOfDaySubsystem NightMix additions |
| **Python lint / CI** | GitHub Actions | Expected PASS | Doc + Python path changes only |
| **Editor: bootstrap_project.py** | Windows Editor | **REQUIRED** | Confirms VS_MVP import + markers path |
| **Editor: pie_test_runner.py** | Windows Editor PIE on VS_MVP | **RECOMMENDED** | Soft checks log SKIP or marker counts in `Saved/pie_test_results.json` |

---

## 4. Explicitly out of scope (honored)

- Full VS_MVP mesh dress in Content binaries
- Mass/family, combat GA depth, sample pack deletes (**WAVE F**)
- Reopening **Docs/07**
- Free-flight gameplay (FALLBACK CRUMB glide only, not implemented in C++/BP this wave)

---

## 5. Gate — APPROVE WAVE E

| | |
|---|---|
| **Gate** | Lead types **`APPROVE WAVE E`** on the WAVE E PR |
| **Unlocks** | **WAVE F** — archive/delete per [08d §8](08d_CONTENT_CANON.md#8-wave-f-delete-candidates-names-only--no-deletes-in-wave-d) → `Docs/08_AUDIT_SIGN_OFF.md` |
| **Do not start** | WAVE F deletes until gate granted |

```
STOP — Lead approval required
Type: APPROVE WAVE E
```

---

## 6. Hard rules (unchanged)

| Rule | Status |
|------|--------|
| **Docs/07 vertical slice sign-off** | **CLOSED** — do not reopen |
| **FALLBACK FLIGHT** | **ARMED** — CRUMB glide + portal both ways |
| **No new features during audit WAVEs** | Honored — upgrade/repoint only |
| **No Content binary deletes in WAVE E** | Honored — WAVE F only |
| **Exclusive file ownership / handoffs** | Durable notes under `Docs/handoffs/` |

---

## Board / Actions / Gate / Next (for Lead)

| | |
|---|---|
| **Board** | WAVE E deliverable ready — slice upgrade pass doc + repo-safe code/doc changes per 08d §7 |
| **Actions** | Review PR; run Safe-Build on DESKTOP-21CT3H0; comment **`APPROVE WAVE E`** to unlock WAVE F |
| **Gate** | `APPROVE WAVE E` — do not start WAVE F deletes until granted |
| **Next (after gate)** | WAVE F — archive/delete quarantined DemoMap/PCG/Mass/scripts per 08d §8; `Docs/08_AUDIT_SIGN_OFF.md` |
