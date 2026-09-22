# DEFECT — PA-E automated Shot 1/2 capture (NOT shotlist PASS)

| Field | Value |
|-------|-------|
| **Date** | 2026-09-22 (ET) |
| **Track** | PA-E formal Shot 1 + Shot 2 per [00_SHOTLIST.md](../00_SHOTLIST.md) |
| **Status** | **OPEN** — automation **not** shotlist PASS until DESKTOP proves capture script |

## Symptom

DESKTOP attempts to produce Shot 1/2 stills via **UnrealEditor-Cmd** (`-ExecutePythonScript` + HighResShot) and/or host **ImageGrab** did not yield usable shotlist evidence: missing files, tiny PNGs, nearly black frames (path stones only), or full-desktop grabs with Message Log / chrome.

## Incident — 2026-09-22 ET (Conductor remote, Lead away)

Host Windows **ImageGrab** of the Unreal window during a remote PA-E Shot 1/2 attempt. Evidence staged under **`C:\Users\User\Desktop\HomeWorld_PA_E\`**:

| File | Size (approx.) | Actual content | Shotlist usable? |
|------|----------------|----------------|------------------|
| `Shot1_lookout.png` | ~525 KB | **Grok Bot chat** / Windows desktop — **not** lit viewport / lookout composition | **No** |
| `Shot2_cabin_garden.png` | ~376 KB | Unreal **Editor chrome** (Outliner, Content Browser, “Executing Python Script” banner); partial cabin glow only — **not** clean Shot 2 | **No** |

**Root cause:** Host ImageGrab cannot force a clean lit viewport when **another UI owns focus** (agent chat, panels, or desktop in front of the game view).

## Policy

- **Do not** invent still paths or mark Shot 1/2 **PASS** from automated captures alone.
- **Do not** call host ImageGrab shotlist **PASS** while another UI owns focus.
- **Track close (2026-09-22 ET):** Lead **`APPROVE PA-E`** closed Docs/32 with formal Shot 1/2 stills **deferred/accepted** — this defect and AUTOMATION_GAPS row stay **OPEN** until DESKTOP proves the capture ladder (no shotlist PASS from ImageGrab files above).
- **Stop grinding remote ImageGrab for PA-E** — focus is not reliable unattended.

## Automation path (2026-09-22 — capture tooling track)

Follow the **capture redundancy ladder** — [docs/Automation/CAPTURE_REDUNDANCY.md](../../docs/Automation/CAPTURE_REDUNDANCY.md):

1. **UE built-ins:** [Content/Python/capture_shotlist_viewport.py](../../Content/Python/capture_shotlist_viewport.py) — `L_VS_MVP_Markers`, Shot 1/2 poses (keyword `Rotator`, P6 / graybox fallbacks), lit + game view, `take_high_res_screenshot(..., force_game_view=True)`, keep_alive, `Saved/pa_e_capture_report.json`.
2. **Free tools:** Document in ladder if built-ins fail on DESKTOP.
3. **Project Python / GUI:** Harden scripts or ref-image automation — not host ImageGrab for PASS.

**Done when (automation gap):** DESKTOP run → report `ok: true` + PNGs under `Saved/Screenshots/PA_E/` and copied to `HomeWorld_PA_E` — Conductor verifies; cloud agents do **not** claim DESKTOP PASS.

## References

- [docs/Automation/CAPTURE_REDUNDANCY.md](../../docs/Automation/CAPTURE_REDUNDANCY.md) — Lead policy ladder
- [docs/KNOWN_ERRORS.md](../../docs/KNOWN_ERRORS.md) — PA-E HighResShot / ImageGrab focus entries (2026-09-22)
- [docs/Automation/AUTOMATION_GAPS.md](../../docs/Automation/AUTOMATION_GAPS.md) — PA-E Shot 1/2 gap (2026-09-22)
- [Docs/handoffs/PA_E_SHOTS.md](../handoffs/PA_E_SHOTS.md) — track closed; automation gap open
- [Docs/handoffs/P6_FIX_shot1.md](../handoffs/P6_FIX_shot1.md) — Shot 1 camera pose
- [Content/Python/capture_viewport.py](../../Content/Python/capture_viewport.py) — generic viewport capture helper
