# Capture redundancy ladder (shotlist / evidence stills)

**Policy (Lead lock-in, 2026-09-22):** Every automated or semi-automated still for [Docs/00_SHOTLIST.md](../../Docs/00_SHOTLIST.md), PA-E evidence, or QA gates must follow this order. **Do not** skip rungs or claim shotlist **PASS** from host desktop grabs.

---

## 1. UE built-ins first (every time)

Re-evaluate on each engine bump — UE 5.8 improves Editor capture APIs.

| Priority | API | Notes |
|----------|-----|--------|
| **Primary** | `unreal.AutomationLibrary.take_high_res_screenshot(res_x, res_y, filename, camera=None, force_game_view=True)` | Viewport/game view, not chrome. **One capture per shot per frame** — wait for async completion before the next shot. |
| **Cmd / latent** | `unreal.EditorPythonScripting.set_keep_python_script_alive(True)` | Required for UnrealEditor-Cmd so screenshots finish before process exit. Helper: [Content/Python/vnp_editor_keep_alive.py](../../Content/Python/vnp_editor_keep_alive.py). |
| **Settle** | Slate/editor tick between pose changes | Short sleep + optional `automation_wait_for_loading`; do **not** fire multiple `take_high_res_screenshot` calls in the same frame. |
| **Viewport** | Lit view mode + game view | `viewmode lit` console; `UnrealEditorSubsystem.editor_set_game_view(True)` when exposed. |
| **Fallback built-in** | `HighResShot` console | Only after AutomationLibrary fails; same async wait-for-file rules. |

**Canonical PA-E script:** [Content/Python/capture_shotlist_viewport.py](../../Content/Python/capture_shotlist_viewport.py) — loads `L_VS_MVP_Markers`, poses Shot 1/2, writes `Saved/Screenshots/PA_E/` + copies to `C:/Users/User/Desktop/HomeWorld_PA_E/` (CopyToBox allowlist), report `Saved/pa_e_capture_report.json`.

**Lightweight utility:** [Content/Python/capture_viewport.py](../../Content/Python/capture_viewport.py) — generic viewport capture + `Saved/screenshot_result.json`.

Epic: [Scripting the Unreal Editor Using Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python) · project [FULL_AUTOMATION_RESEARCH.md](FULL_AUTOMATION_RESEARCH.md) §10b.

---

## 2. Scout free / open tools (if built-ins fail)

Document what was tried before adopting a tool. Prefer **MIT / Apache / BSL-free**; no paid SaaS for MVP evidence.

| Candidate | Role | Status |
|-----------|------|--------|
| **NirCmd** `savescreenshot` | HWND-targeted still (host) | Listed in [FULL_AUTOMATION_RESEARCH.md](FULL_AUTOMATION_RESEARCH.md) §11 — evaluate only if UE built-ins fail on DESKTOP |
| **OBS CLI** | Free recording / frame export | Evaluate if batch stills need video-derived frames |
| **UnrealMCPToolkit** `take_screenshot` | Ecosystem MCP | Use only if already installed and returns viewport pixels (not desktop) |
| **Epic Screenshot Comparison Tool** | Regression / golden compare | Optional compare after capture exists — see NF2-B notes in [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) |

Log evaluation outcomes in [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) research log when a candidate is rejected or adopted.

---

## 3. Build / maintain our own (if free tools fail)

Harden **Editor Python** under `Content/Python/` (idempotent, log-driven validation, keyword `Rotator` args per [KNOWN_ERRORS.md](../KNOWN_ERRORS.md)).

- Extend `capture_shotlist_viewport.py` (poses, validation, golden compare).
- Reuse patterns from [vnp_night_tune_and_evidence.py](../../Content/Python/vnp_night_tune_and_evidence.py) (camera bind, wait for `Saved/Screenshots`).
- GUI automation last resort within this rung: [Content/Python/gui_automation/](Content/Python/gui_automation/) with ref images (Message Log closed, game view maximized).

---

## 4. Banned for shotlist PASS

| Method | Why |
|--------|-----|
| Host **PIL ImageGrab** / full-desktop **PyAutoGUI** when another UI may own focus | Captured Grok chat, Outliner, Content Browser — not lit viewport ([KNOWN_ERRORS.md](../KNOWN_ERRORS.md), PA-E 2026-09-22) |
| Treating **tiny / missing / near-black** Cmd HighResShot output as PASS | Documented PA-E / NF2-B failures |

Host [capture_editor_screenshot.py](../../Content/Python/capture_editor_screenshot.py) remains for **non-shotlist** host diagnostics only — not PA-E success path.

---

## PA-E failure history (cross-links)

| Date | Issue | Doc |
|------|--------|-----|
| 2026-09-19 | NF2-B Cmd HighResShot — shot1/2 PNGs missing; shot5 OK | [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) §Gap NF2-B |
| 2026-09-22 | Cmd ok but missing/tiny/black frames | [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) · [DEFECT_PA_E_shot_capture_automation.md](../../Docs/qa/DEFECT_PA_E_shot_capture_automation.md) |
| 2026-09-22 | ImageGrab → chat/desktop/chrome under `HomeWorld_PA_E` | Same defect · [PA_E_SHOTS.md](../../Docs/handoffs/PA_E_SHOTS.md) (track closed; automation gap **OPEN**) |
| 2026-09-22 | `Rotator` positional arg mis-pose | [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) — use `pitch=` / `yaw=` / `roll=` keywords |

**Track status:** Lead **`APPROVE PA-E`** closed Docs/32 — formal Shot 1/2 stills were **deferred/accepted**; automation gap stays **OPEN** until DESKTOP proves `capture_shotlist_viewport.py` PASS (Conductor / DESKTOP — not cloud).

**Pose references:** Shot 1 live pose [Docs/handoffs/P6_FIX_shot1.md](../../Docs/handoffs/P6_FIX_shot1.md) · [Lib/00_Core/CAM_Hero.md](../../Lib/00_Core/CAM_Hero.md) · [Docs/00_SHOTLIST.md](../../Docs/00_SHOTLIST.md).
