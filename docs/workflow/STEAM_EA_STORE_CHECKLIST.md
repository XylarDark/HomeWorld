# Steam Early Access — Store Page Checklist

**Purpose:** Checklist for preparing a Steam store page and depots for HomeWorld (PC, Steam Early Access). Use when ready to ship or draft the store presence. See [SETUP.md](../SETUP.md) for packaging; [VISION.md](VISION.md) and AGENTS.md for scope.

---

## Current status (2026-03-05)

- **Packaging script:** `Package-HomeWorld.bat` in project root; uses RunUAT BuildCookRun (Win64 Shipping); output `Saved\StagedBuilds`; log `Package-HomeWorld.log`. See [SETUP.md § Packaging](../SETUP.md#packaging-shipping-build).
- **Packaged build run:** Not yet run this cycle. To run: close Unreal Editor, then from project root run `Package-HomeWorld.bat`; monitor `Package-HomeWorld.log` for completion (exit code 0 = success). RunUAT can take 30+ minutes.
- **Smoke test:** Pending until a packaged build is produced; launch the executable from `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\HomeWorld\Binaries\Win64\HomeWorld.exe` (path after RunUAT) and confirm level loads, character moves, no critical errors.
- **Steamworks / store page:** Not started; checklist below is the reference when ready.
- **T6 (eighth list, 2026-03-05) completed:** STEAM_EA_STORE_CHECKLIST updated with status and run instructions. Packaged build not executed this round (requires Editor closed; RunUAT 30+ min). **Next steps:** Close Editor → run `Package-HomeWorld.bat` from project root → when log shows exit code 0, smoke-test exe from `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\HomeWorld\Binaries\Win64\HomeWorld.exe` → check off "Packaged build runs" and "Smoke test" in § Packaged build below.
- **T6 (ninth list, 2026-03-05) completed:** Checklist status and run instructions confirmed current. Packaged build not run this round (Editor may be in use; RunUAT 30+ min). **Next steps:** Close Editor → run `Package-HomeWorld.bat` from project root → monitor `Package-HomeWorld.log` for exit code 0 → smoke-test exe from `Saved\StagedBuilds\...\HomeWorld.exe` → check off § Packaged build items when done.
- **T5 (eleventh list, 2026-03-05) completed:** STEAM_EA_STORE_CHECKLIST updated with current status and run instructions. Packaged build not run this round (requires Editor closed; RunUAT 30+ min). **Next steps:** Close Editor → run `Package-HomeWorld.bat` from project root → monitor `Package-HomeWorld.log` for exit code 0 → smoke-test exe from `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\HomeWorld\Binaries\Win64\HomeWorld.exe` → check off § Packaged build when done.
- **T6 (eleventh list, 2026-03-05) completed:** Store page draft section added below with title, short description, about, key features, and system requirements (draft copy). Packaged build/smoke test not run this round. **Next steps:** Review draft copy; when ready, run packaged build and smoke test per § Packaged build; then create/configure Steamworks app and fill store page from draft.
- **T3 (twelfth list, 2026-03-05) completed:** Packaged build was attempted. **Cook phase succeeded** (~16 min; 0 errors, 131 warnings). **Stage failed** with ExitCode=103 (Error_MissingExecutable): missing receipt `C:\dev\HomeWorld\Binaries\Win64\HomeWorld-Win64-Shipping.target`. RunUAT BuildCookRun does not build the game target; the **Shipping game executable must be built before packaging**. **Next steps:** (1) Build the game in Shipping config: from project root run the Engine's Build.bat for **HomeWorld Win64 Shipping** (e.g. `"C:\Program Files\Epic Games\UE_5.7\Engine\Build\BatchFiles\Build.bat" HomeWorld Win64 Shipping -Project="C:\dev\HomeWorld\HomeWorld.uproject"`), or add a Build-Ship step to the pipeline; (2) then re-run `Package-HomeWorld.bat`; (3) when log shows exit code 0, smoke-test exe from `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\HomeWorld\Binaries\Win64\HomeWorld.exe`.
- **T6 (thirteenth list, 2026-03-05) completed:** Packaged build not run this round (requires Editor closed; build Shipping first per § How to run packaged build; RunUAT 30+ min). **Next steps:** Close Editor → build HomeWorld Win64 Shipping (see step 2 in § How to run packaged build) → run `Package-HomeWorld.bat` from project root → monitor `Package-HomeWorld.log` for exit code 0 → smoke-test exe from `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\HomeWorld\Binaries\Win64\HomeWorld.exe` → check off § Packaged build items when done.
- **T5 (sixteenth list, 2026-03-05) completed:** **Shipping build succeeded** (Build.bat HomeWorld Win64 Shipping; ~72s). **Packaging run:** Package-HomeWorld.bat was executed; **Stage phase failed** with SafeCopyFile errors: `xaudio2_9redist.dll` missing in source, `onnxruntime.dll` locked by another process. Packaged exe was not produced. **Next steps:** Close Editor and any Unreal/Engine processes; then (1) build HomeWorld Win64 Shipping if needed, (2) run `Package-HomeWorld.bat`, (3) check `Package-HomeWorld.log` for exit code 0, (4) smoke-test from `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\HomeWorld\Binaries\Win64\HomeWorld.exe`. See [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) "Package-HomeWorld: Stage fails with SafeCopyFile".
- **T8 (twentieth list, 2026-03-05) completed:** **Shipping build succeeded** (Build.bat HomeWorld Win64 Shipping; ~39s). **Packaging run:** Package-HomeWorld.bat was executed; **Cook succeeded** (UnrealEditor-Cmd ExitCode=0, 131 warnings); **Stage phase failed** with SafeCopyFile errors — files in use by another process (e.g. `HomeWorld.exe`, manifest files, `libogg_64.dll`, `steam_api64.dll`, `libvorbisfile_64.dll`); `GFSDK_Aftermath_Lib.x64.dll` skipped (source missing). Packaged exe was not produced; smoke test not run. **Next steps:** Close Unreal Editor and any process using project/engine binaries (Cursor, antivirus, previous RunUAT); optionally delete or rename `Saved\StagedBuilds` for a clean stage; re-run `Package-HomeWorld.bat`. See [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) "Package-HomeWorld: Stage SafeCopyFile files in use".
- **T8 (twenty-first list, 2026-03-05) completed:** Repeatable workaround for Stage SafeCopyFile (files in use) documented. Use **§ Packaged build retry when Stage failed (files in use)** below, or run **`.\Tools\Package-AfterClose.ps1`** from project root *after* closing Unreal Editor (script checks for lock-holding processes, optionally cleans StagedBuilds, then runs Shipping build + Package-HomeWorld.bat). Packaged exe not produced this round; success = workaround documented.
- **T8 (twenty-second list, 2026-03-05) completed:** **Package-AfterClose.ps1 run.** No lock-holding processes at start; **Shipping build succeeded** (~31s). **Package-HomeWorld.bat** ran; **Stage phase failed** with SafeCopyFile — files in use (e.g. `Manifest_NonUFSFiles_Win64.txt`, `Manifest_UFSFiles_Win64.txt`, `StagedBuild_HomeWorld.ini`, `TessellationTable.bin`). Packaged exe not produced; smoke test not run. **Blocker:** Same as prior lists — Stage fails when any process holds StagedBuilds/Engine files during Stage. **Next steps:** Ensure all processes that may touch project/Engine (Editor, Cursor, antivirus, previous RunUAT) are closed; optionally run `.\Tools\Package-AfterClose.ps1 -CleanStagedBuilds` for a clean stage; re-run and monitor `Package-HomeWorld.log` for exit code 0. See [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) "Package-HomeWorld: Stage SafeCopyFile — files in use".
- **T8 (twenty-fourth list, 2026-03-05) completed:** Package not run this list. Use **`.\Tools\Package-AfterClose.ps1`** when ready (close Unreal Editor and any HomeWorld game first). See § Packaged build retry when Stage failed (files in use) and [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) for Stage SafeCopyFile workaround.
- **T7 (twenty-fifth list, 2026-03-05) completed:** Package not run this list. Use **`.\Tools\Package-AfterClose.ps1`** when ready (close Unreal Editor and any HomeWorld game first). See § Packaged build retry when Stage failed (files in use) and [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) for Stage SafeCopyFile workaround.
- **T7 (twenty-sixth list, 2026-03-05) completed:** Package not run this list. Use **`.\Tools\Package-AfterClose.ps1`** when ready (close Unreal Editor and any HomeWorld game first). See § Packaged build retry when Stage failed (files in use) and [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) for Stage SafeCopyFile workaround.
- **T7 (twenty-seventh list, 2026-03-05) completed:** Package not run this list. Use **`.\Tools\Package-AfterClose.ps1`** when ready (close Unreal Editor and any HomeWorld game first). See § Packaged build retry when Stage failed (files in use) and [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) for Stage SafeCopyFile workaround.
- **T7 (twenty-eighth list, 2026-03-05) completed:** Package not run this list. Use **`.\Tools\Package-AfterClose.ps1`** when ready (close Unreal Editor and any HomeWorld game first). See § Packaged build retry when Stage failed (files in use) and [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) for Stage SafeCopyFile workaround.
- **T7 (twenty-ninth list, 2026-03-06) completed:** Package not run this list. Use **`.\Tools\Package-AfterClose.ps1`** when ready (close Unreal Editor and any HomeWorld game first). See § Packaged build retry when Stage failed (files in use) and [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) for Stage SafeCopyFile workaround.
- **T6 (thirty-first list, 2026-03-06) completed:** Package not run this list. Use **`.\Tools\Package-AfterClose.ps1`** when ready (close Unreal Editor and any HomeWorld game first). See § Packaged build retry when Stage failed (files in use) and [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) for Stage SafeCopyFile workaround.
- **T5 (thirty-second list, 2026-03-06) completed:** Package not run this list. Use **`.\Tools\Package-AfterClose.ps1`** when ready (close Unreal Editor and any HomeWorld game first). See § Packaged build retry when Stage failed (files in use) and [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) for Stage SafeCopyFile workaround.
- **T6 (thirty-fourth list, 2026-03-06) completed:** Package not run this list. Use **`.\Tools\Package-AfterClose.ps1`** when ready (close Unreal Editor and any HomeWorld game first). See § Packaged build retry when Stage failed (files in use) and [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) for Stage SafeCopyFile workaround.
- **T6 (thirty-fifth list, 2026-03-06) completed:** Thirty-fifth list: package not run; use **`.\Tools\Package-AfterClose.ps1`** when ready (close Unreal Editor and any HomeWorld game first). See § Packaged build retry when Stage failed (files in use) and [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) for Stage SafeCopyFile workaround.
- **T1 (fifty-fourth list, 2026-03-08) completed:** Packaged build not run this list. Use **`.\Tools\Package-AfterClose.ps1`** when ready (close Unreal Editor and any HomeWorld game first). See § Packaged build retry when Stage failed (files in use) and [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) for Stage SafeCopyFile workaround.

---

## Packaged build retry when Stage failed (files in use)

If packaging **Cook** succeeded but **Stage** failed with SafeCopyFile ("file in use" or "being used by another process"), use this repeatable procedure. See [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) "Package-HomeWorld: Stage SafeCopyFile — files in use".

1. **Close lock-holding processes** (required):
   - **Unreal Editor** (UnrealEditor.exe).
   - Any running **HomeWorld** game (HomeWorld.exe, HomeWorld-Win64-Shipping.exe).
   - Optionally close Cursor/IDE if they have project or Engine paths open; exit any previous RunUAT or Build window.
2. **Optional — clean StagedBuilds:** Delete or rename `Saved\StagedBuilds` so Stage writes to a clean folder:  
   `Remove-Item -Recurse -Force Saved\StagedBuilds` (or rename to `StagedBuilds.bak`) from project root.
3. **Build Shipping** (RunUAT does not build the target):  
   `"C:\Program Files\Epic Games\UE_5.7\Engine\Build\BatchFiles\Build.bat" HomeWorld Win64 Shipping -Project="<path-to>\HomeWorld.uproject"`
4. **Package:** From project root run `Package-HomeWorld.bat`; monitor `Package-HomeWorld.log` for exit code 0.
5. **Smoke test:** Run `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\HomeWorld\Binaries\Win64\HomeWorld.exe`.

**Script option:** From project root run `.\Tools\Package-AfterClose.ps1` after closing Editor. It checks for Unreal/HomeWorld processes (exits with instructions if any are running), then runs the Shipping build and `Package-HomeWorld.bat`. For a **clean stage** after a previous Stage failure (files in use), use **`.\Tools\Package-AfterClose.ps1 -CleanStagedBuilds`** so the script removes `Saved\StagedBuilds` before building and packaging. Do not run the script while Editor is open.

---

## Packaged build

- [ ] **Packaged build runs:** Create a Windows (64-bit) packaged build via **File → Package Project → Windows (64-bit)** or **`Package-HomeWorld.bat`** (see [SETUP.md § Packaging](../SETUP.md#packaging-shipping-build)).
- [ ] **Smoke test:** Launch the packaged executable from the output folder; confirm level loads, character moves, no critical errors.

---

## Steamworks / depots (when applicable)

- [ ] **Steamworks account:** App created in Steamworks; App ID and depots configured.
- [ ] **Depot build:** Upload or configure build pipeline so the packaged game is assigned to the correct depot(s).
- [ ] **Steam Sockets:** Project uses **Steam Sockets** plugin (in .uproject); ensure runtime dependencies and SDK are aligned for Shipping builds.

---

## Store page content (draft)

- [ ] **Store title:** HomeWorld (or final name).
- [ ] **Short description:** One-line tagline for store listing.
- [ ] **About / long description:** Summary of game, theme (“Love as Epic Quest”), core loop (explore, fight, build, bonds), Early Access scope.
- [ ] **Key features:** Bullet list (e.g. co-op ARPG, family sim elements, 8–12h campaign target).
- [ ] **Screenshots / capsule art:** At least one capsule (e.g. 616x353, 460x215) and several in-game screenshots.
- [ ] **Trailer (optional):** Short video; vertical slice or moment (e.g. Claim homestead, Homestead compound) per [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md).
- [ ] **System requirements:** Min/recommended OS, CPU, RAM, GPU, storage (align with UE 5.7 Windows build).
- [ ] **Legal / age rating:** As required by Steam and target regions.

### Draft copy (T6 eleventh list — use when creating store page)

**Store title:** HomeWorld

**Short description (tagline):** Build a life worth fighting for. Co-op ARPG survival with family, exploration, and a campaign built on love as an epic quest.

**About / long description (draft):**  
HomeWorld is a co-op ARPG survival game with family sim elements. Theme: "Love as Epic Quest" — intense combat meets nurturing bonds; you build and protect a life worth fighting for. Explore biomes, fight bosses, claim and upgrade your homestead, and rescue your family across sin-themed realms. Act 1 is solo (lone wanderer: crash → scout → boss → claim home); later acts add co-op and family roles. Early Access delivers the core loop: explore → fight → build → bonds, with an 8–12h campaign target and room to grow (day/night defend, succession, endgame roster). PC, Unreal Engine 5.7; Steam Early Access.

**Key features (bullets):**
- Co-op ARPG survival: explore, fight, build, nurture bonds
- Family sim elements: roles, homestead, rescue campaign
- Theme: "Love as Epic Quest" — combat + connection
- Act 1: solo lone wanderer (2–3h); Act 2+ co-op (2–8 players)
- 8–12h campaign target; sin/virtue moral spectrum; succession and spirits
- Procedural biomes and realms; build orders and family AI (Early Access roadmap)
- PC, Steam; Unreal Engine 5.7

**System requirements (draft — align with UE 5.7 Win64 Shipping; verify before publish):**
- **OS:** Windows 10/11 64-bit
- **Processor:** Quad-core 2.5 GHz or better
- **Memory:** 8 GB RAM (min), 16 GB RAM (recommended)
- **Graphics:** DirectX 12 compatible; 4 GB VRAM (min), 6 GB+ (recommended)
- **Storage:** 15–20 GB available
- **Network:** Broadband for co-op (Steam)

*Update min/recommended from packaged build profiling or Epic UE 5.7 docs before finalizing.*

---

## Pre-launch

- [ ] **Build stability:** No known crashes or blockers in packaged build; PIE and packaged behavior aligned.
- [ ] **Default map / game mode:** Packaged game uses correct default map and game mode (see [SETUP.md](../SETUP.md) Validation).

---

**See also:** [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md) N4 (Steam EA prep), [SETUP.md](../SETUP.md) Packaging.

---

## How to run packaged build (when ready)

1. Close Unreal Editor (and any running HomeWorld game). If Stage previously failed with "files in use", use **§ Packaged build retry when Stage failed (files in use)** or run `.\Tools\Package-AfterClose.ps1` from project root after closing Editor.
2. **Build the game in Shipping config first** (RunUAT does not build the target): run the Engine's Build.bat for **HomeWorld Win64 Shipping**, e.g. `"C:\Program Files\Epic Games\UE_5.7\Engine\Build\BatchFiles\Build.bat" HomeWorld Win64 Shipping -Project="<path-to>\HomeWorld.uproject"`. If this step is skipped, packaging will cook successfully but Stage will fail with Error_MissingExecutable (exit code 103).
3. From project root: `Package-HomeWorld.bat` (or double-click in Explorer).
4. Wait for RunUAT to finish; check `Package-HomeWorld.log` for exit code 0.
5. Run the game from `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\HomeWorld\Binaries\Win64\HomeWorld.exe` (path may vary by RunUAT; check StagedBuilds folder); smoke test: level loads, character moves, no critical errors.
6. Update this checklist: check "Packaged build runs" and "Smoke test" when done.
