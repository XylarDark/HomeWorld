# DEFECT — PA-E automated Shot 1/2 capture (NOT shotlist PASS)

| Field | Value |
|-------|-------|
| **Date** | 2026-09-22 (ET) |
| **Track** | PA-E formal Shot 1 + Shot 2 per [00_SHOTLIST.md](../00_SHOTLIST.md) |
| **Status** | **OPEN** — automation **not** shotlist PASS until DESKTOP proves capture script |

## Symptom

DESKTOP attempts to produce Shot 1/2 stills via **UnrealEditor-Cmd** (`-ExecutePythonScript` + HighResShot) and/or host **ImageGrab** did not yield usable shotlist evidence: missing files, tiny PNGs, nearly black frames (path stones only), or full-desktop grabs with Message Log / chrome. **2026-09-22 follow-up:** scripts used non-doc **`HighResShot` order** (resolution before `filename=`) and **short file waits** while PNGs could land **~268s** later — see [CAPTURE_REDUNDANCY.md](../../docs/Automation/CAPTURE_REDUNDANCY.md) and KNOWN_ERRORS (parameter-order + wait race).

## Incident — 2026-09-22 ET (Conductor remote, Lead away)

Host Windows **ImageGrab** of the Unreal window during a remote PA-E Shot 1/2 attempt. Evidence staged under **`C:\Users\User\Desktop\HomeWorld_PA_E\`**:

| File | Size (approx.) | Actual content | Shotlist usable? |
|------|----------------|----------------|------------------|
| `Shot1_lookout.png` | ~525 KB | **Grok Bot chat** / Windows desktop — **not** lit viewport / lookout composition | **No** |
| `Shot2_cabin_garden.png` | ~376 KB | Unreal **Editor chrome** (Outliner, Content Browser, “Executing Python Script” banner); partial cabin glow only — **not** clean Shot 2 | **No** |

**Root cause:** Host ImageGrab cannot force a clean lit viewport when **another UI owns focus** (agent chat, panels, or desktop in front of the game view).

## Incident — 2026-09-22 ET post-#157 (DESKTOP prove, document only)

Live Editor run on **`C:\dev\HomeWorld`** after **#157** (~12:46 ET). Report: **`Saved/pa_e_capture_report.json`**, **`ok: false`**. Absolute paths + **`game_view: true`**; **`AutomationEditorTask` `task_done: false`**; **`file_missing`**; **`pil_available: false`**; no new PNGs under **`Saved/Screenshots/PA_E/`**. **Not** shotlist PASS.

## Incident — 2026-09-22 ET post-#159 (DESKTOP prove, document only)

After **#159** merged (~12:51–13:01 ET), same host path. Console **`HighResShot`** with absolute `filename=` for Shot 1 + Shot 2; **`_focus_level_viewport`** OK; **no PNG** after ~120s wait per shot. Fallback **AutomationLibrary**: **`task_done: false`**, **`file_produced_by: null`**, both shots fail. MCP **600s timeout** / Editor **Not Responding** during **`_final_drain`**; **no** new **`pa_e_capture_report.json`** (prior report renamed pre-run). **No** new **`Shot*.png`** under **`Saved/Screenshots/PA_E/`**. Defect **still OPEN**; **rung 1 HighResShot variants exhausted** unless Lead gates SCOUT/BUILD. **Not** shotlist PASS.

## Incident — 2026-09-22 ET post-#163 (DESKTOP prove, document only)

After **#163** merged @ **`d0d074d`**, MCP **`execute_python_script("capture_shotlist_viewport.py")`** on **`C:\dev\HomeWorld`** (~14:45–14:53 ET / log UTC 18:45–18:52). Level load OK. Shot 1 + Shot 2: **AutomationLibrary** path with **`kwargs_delay_force_gv`**; **`AutomationEditorTask` `task_done: false`** after ~90s poll each; **no PNG** after ~120s file wait; Editor **Not Responding** throughout; session killed during **`final_drain`** (~75s). **No** **`Saved/pa_e_capture_report.json`**; **no** new **`Shot1_lookout.png`** / **`Shot2_cabin_garden.png`**. **Likely cause:** blocking **`time.sleep`** / poll on Editor Python **main thread** prevents Slate ticks required for async **`take_high_res_screenshot`**. **Next rung 1:** **`unreal.register_slate_pre_tick_callback`** wait (see [AUTOMATION_GAPS.md](../../docs/Automation/AUTOMATION_GAPS.md) research log). Defect **OPEN** — **not** shotlist PASS; do **not** treat AutomationLibrary primary as proven.

## Incident — 2026-09-22 ET post-#166 (DESKTOP prove, document only)

After **#166** @ **`ee32888`**, MCP **`capture_shotlist_viewport.py`** (AL + Slate pretick): Editor **Responding**; report **`ok: false`** — near-black PNGs (luminance gates fail). **Lead (in Editor):** rotating viewport shows **lit homestead** — near-black stills are **wrong capture binding** (pose / game-view / pilot / empty buffer), **not** absent content. **Next:** MRQ primary [capture_shotlist.py](../../Content/Python/capture_shotlist.py); keep AL bug **OPEN** for fix/diagnostic. Defect **OPEN** until **lit non-black** stills (not file-exists-only).

## Policy

- **Do not** invent still paths or mark Shot 1/2 **PASS** from automated captures alone.
- **Do not** call host ImageGrab shotlist **PASS** while another UI owns focus.
- **Track close (2026-09-22 ET):** Lead **`APPROVE PA-E`** closed Docs/32 with formal Shot 1/2 stills **deferred/accepted** — this defect and AUTOMATION_GAPS row stay **OPEN** until DESKTOP proves the capture ladder (no shotlist PASS from ImageGrab files above).
- **Stop grinding remote ImageGrab for PA-E** — focus is not reliable unattended.

## Automation path (2026-09-22 — capture tooling track)

Follow [docs/Automation/CAPTURE_REDUNDANCY.md](../../docs/Automation/CAPTURE_REDUNDANCY.md) (**Lead-gated global ladder** + shotlist instance):

1. **Rung 1 (no gate):** [Content/Python/capture_shotlist_viewport.py](../../Content/Python/capture_shotlist_viewport.py) — **`AutomationLibrary.take_high_res_screenshot`** primary with **non-blocking** async wait (**`register_slate_pre_tick_callback`** — not main-thread `time.sleep` poll); `finish_loading_before_screenshot`, kwargs `delay` / `force_game_view` → `Saved/pa_e_capture_report.json`. **Post-#163 DESKTOP FAIL** until tick-callback prove.
2. **Rung 2:** Free-tool **SCOUT backlog** (names only) — requires Lead **`APPROVE TOOL SCOUT <name>`**; **no auto-install**.
3. **Rung 3:** Net-new custom stacks — requires Lead **`APPROVE TOOL BUILD <name>`**; not host ImageGrab for PASS.

**Done when (automation gap):** DESKTOP run → report `ok: true` + PNGs under `Saved/Screenshots/PA_E/` and copied to `HomeWorld_PA_E` — Conductor verifies; cloud agents do **not** claim DESKTOP PASS.

## References

- [docs/Automation/CAPTURE_REDUNDANCY.md](../../docs/Automation/CAPTURE_REDUNDANCY.md) — Lead policy ladder
- [docs/KNOWN_ERRORS.md](../../docs/KNOWN_ERRORS.md) — PA-E HighResShot / ImageGrab focus entries (2026-09-22)
- [docs/Automation/AUTOMATION_GAPS.md](../../docs/Automation/AUTOMATION_GAPS.md) — PA-E Shot 1/2 gap (2026-09-22)
- [Docs/handoffs/PA_E_SHOTS.md](../handoffs/PA_E_SHOTS.md) — track closed; automation gap open
- [Docs/handoffs/P6_FIX_shot1.md](../handoffs/P6_FIX_shot1.md) — Shot 1 camera pose
- [Content/Python/capture_viewport.py](../../Content/Python/capture_viewport.py) — generic viewport capture helper
