# Steam Early Access — Store Page Checklist

**Purpose:** Checklist for preparing a Steam store page and depots for HomeWorld (PC, Steam Early Access). Use when ready to ship or draft the store presence. See [SETUP.md](../SETUP.md) for packaging; [VISION.md](VISION.md) and AGENTS.md for scope.

---

## Current status (2026-03-05)

- **Packaging script:** `Package-HomeWorld.bat` in project root; uses RunUAT BuildCookRun (Win64 Shipping); output `Saved\StagedBuilds`; log `Package-HomeWorld.log`. See [SETUP.md § Packaging](../SETUP.md#packaging-shipping-build).
- **Packaged build run:** Not yet run this cycle. To run: close Unreal Editor, then from project root run `Package-HomeWorld.bat`; monitor `Package-HomeWorld.log` for completion (exit code 0 = success). RunUAT can take 30+ minutes.
- **Smoke test:** Pending until a packaged build is produced; launch the executable from `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\HomeWorld\Binaries\Win64\HomeWorld.exe` (path after RunUAT) and confirm level loads, character moves, no critical errors.
- **Steamworks / store page:** Not started; checklist below is the reference when ready.
- **T6 (eighth list, 2026-03-05) completed:** STEAM_EA_STORE_CHECKLIST updated with status and run instructions. Packaged build not executed this round (requires Editor closed; RunUAT 30+ min). **Next steps:** Close Editor → run `Package-HomeWorld.bat` from project root → when log shows exit code 0, smoke-test exe from `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\HomeWorld\Binaries\Win64\HomeWorld.exe` → check off "Packaged build runs" and "Smoke test" in § Packaged build below.

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

---

## Pre-launch

- [ ] **Build stability:** No known crashes or blockers in packaged build; PIE and packaged behavior aligned.
- [ ] **Default map / game mode:** Packaged game uses correct default map and game mode (see [SETUP.md](../SETUP.md) Validation).

---

**See also:** [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md) N4 (Steam EA prep), [SETUP.md](../SETUP.md) Packaging.

---

## How to run packaged build (when ready)

1. Close Unreal Editor.
2. From project root: `Package-HomeWorld.bat` (or double-click in Explorer).
3. Wait for RunUAT to finish; check `Package-HomeWorld.log` for exit code 0.
4. Run the game from `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\HomeWorld\Binaries\Win64\HomeWorld.exe` (path may vary by RunUAT; check StagedBuilds folder); smoke test: level loads, character moves, no critical errors.
5. Update this checklist: check "Packaged build runs" and "Smoke test" when done.
