# Tooling redundancy ladder (Lead-gated)

**Policy (Lead lock-in, 2026-09-22):** Applies to **any** automation / tooling gap — screenshots, PIE harnesses, GUI automation, MCP extensions, host utilities — not only shotlist stills. Agents **must** follow rung order and **Lead gates** before rungs 2–3.

**Canonical gap log:** [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) · **Shotlist instance:** § [Shotlist / PA-E capture](#shotlist--pa-e-capture-instance) below.

---

## Global ladder (all tooling gaps)

### Docs-first (Lead policy, 2026-09-22)

Applies to **all** tooling gaps on this ladder (not only capture).

**Before** using or hardening Unreal **console commands**, **Editor Python APIs**, or similar tooling: read the **official Epic (or vendor) documentation** for that command/API **first**, unless the exact usage is already recorded in repo policy (e.g. [KNOWN_ERRORS.md](../KNOWN_ERRORS.md), this file) or durable agent memory.

- Match documented **parameter order**, **required context** (e.g. PIE vs editor viewport), and **default save paths**.
- Do **not** learn or lock in usage **only** from failed DESKTOP proves — consult docs (or `/parallel-extract` on Epic URLs per [11-parallel-plugin.mdc](../../.cursor/rules/11-parallel-plugin.mdc)) before adding retries, alternate command strings, or wait logic.

**Reference docs (capture examples):**

- Epic [Taking Screenshots](https://dev.epicgames.com/documentation/en-us/unreal-engine/taking-screenshots-in-unreal-engine) — e.g. `HighResShot filename=PATH (XxY OR Multiplier) …`, PIE/standalone framing
- Epic [AutomationLibrary (Python API)](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/AutomationLibrary?application_version=5.8) — e.g. `take_high_res_screenshot`

**Motivating miss (2026-09-22):** Automation issued `HighResShot 1920x1080 filename="…"` without a docs-first check; Epic documents **`filename=` before dimensions**.

**Undocumented console strings:** If Epic docs do not cover a string the repo uses (e.g. **`FOCUSVIEWPORT`** / **`focus`** for viewport focus), log in [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) and prefer Editor subsystem APIs when exposed — do not invent new console aliases.

---

### Rung 1 — Built-in / already-in-repo (no gate)

**Exhaust first, every time.** Re-try when the engine, MCP plugin, or repo scripts change (e.g. UE 5.8 `AutomationLibrary` improvements). **Docs-first** (above) applies before hardening any rung-1 console/API call.

| Allowed without a new gate | Examples |
|----------------------------|----------|
| Epic / UE Editor APIs | `AutomationLibrary`, console commands, Editor Python subsystems |
| MCP + scripts already in the repo | `execute_python_script`, [Content/Python/](../../Content/Python/) orchestrators |
| Idempotent hardening of **existing** Editor Python that calls rung-1 APIs | [capture_shotlist_viewport.py](../../Content/Python/capture_shotlist_viewport.py), [capture_viewport.py](../../Content/Python/capture_viewport.py) |
| Documented GUI automation **already** under [Content/Python/gui_automation/](Content/Python/gui_automation/) | Ref-image clickers shipped with the repo |

**Gate guards (rung 1):** No new third-party installs; no new parallel automation frameworks.

---

### Rung 2 — Scout free / open third-party (Lead gate required)

**Only after rung 1 is exhausted** on DESKTOP (or logged failure with evidence).

| Lead gate string | Meaning |
|------------------|---------|
| **`APPROVE TOOL SCOUT <name>`** | Agent may **research** named tool(s), document fit/license, and propose install — **not** auto-install |
| Explicit chat **yes** to scout (same intent) | Same as above; record in gap research log |

**Gate guards (rung 2):**

- **Do not** auto-download, auto-install, or add paid SaaS without Lead approval.
- **Do not** treat “listed in research doc” as permission to install.
- Scout output = **backlog entry** (name, license, why, rejection/adoption note) in [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) research log or § SCOUT backlog below.

Prefer **MIT / Apache / BSL-free** when Lead approves scout.

---

### Rung 3 — Custom tools / new stacks (Lead gate required)

**Only after rung 1 exhausted and (if applicable) rung 2 scouted with Lead approval.**

| Lead gate string | Meaning |
|------------------|---------|
| **`APPROVE TOOL BUILD <name>`** | Agent may implement **new** automation beyond rung-1 hardening (new host stack, new MCP plugin, large new subsystem) |
| Explicit chat **yes** to build (same intent) | Record scope in gap log |

**Gate guards (rung 3):**

- **Do not** invent new automation stacks, new host daemons, or broad ref-image/GUI frameworks **unprompted**.
- Extending **existing** Editor Python that only wraps UE built-ins (same PR family as `capture_shotlist_viewport.py`) = **rung 1**, not rung 3.
- New C++ commandlets, new npm tooling gates, or net-new GUI automation **kits** = rung 3 unless already on repo roadmap with Lead ack.

---

## Shotlist / PA-E capture instance

Formal stills for [Docs/00_SHOTLIST.md](../../Docs/00_SHOTLIST.md), PA-E evidence, and related QA gates **use the global ladder** with this mapping:

### Rung 1 (in scope for current PR — no new gate)

| Item | Notes |
|------|--------|
| Console **`HighResShot`** via `execute_console_command` | **Primary** — doc order **`HighResShot filename=<abs forward-slash path> 1920x1080`** first; one form per tick, **wait up to ~330s for PNG** before next form (Epic: global one-request flag). Search `Saved/Screenshots/PA_E/`, **`Windows`**, **`WindowsEditor`**, Engine Win64. [Taking Screenshots](https://dev.epicgames.com/documentation/en-us/unreal-engine/taking-screenshots-in-unreal-engine) |
| `AutomationLibrary.take_high_res_screenshot(..., delay≈0.35, force_game_view=True)` | **Fallback** after console ladder misses; call **`finish_loading_before_screenshot()`** first; **`is_task_done()` false is non-fatal** while file wait continues |
| `AutomationLibrary.set_editor_viewport_view_mode` (Lit) | Preferred over console `viewmode lit` when exposed |
| Viewport focus (best-effort) | LevelEditorSubsystem / UnrealEditorSubsystem APIs when present; console **`FOCUSVIEWPORT`** / **`focus`** — **undocumented / unverified** (no Epic console doc); do not invent new console aliases |
| `EditorPythonScripting.set_keep_python_script_alive(True)` | [vnp_editor_keep_alive.py](../../Content/Python/vnp_editor_keep_alive.py) |
| Lit + game view | AutomationLibrary Lit when exposed; else `viewmode lit`; `UnrealEditorSubsystem.editor_set_game_view(True)` when exposed |
| Inter-shot spacing | Extra Slate tick settle between Shot 1 and Shot 2 so HighResShot requests are not stomped |
| **Canonical script** | [capture_shotlist_viewport.py](../../Content/Python/capture_shotlist_viewport.py) → `Saved/Screenshots/PA_E/`, `Saved/pa_e_capture_report.json`, copy to `C:/Users/User/Desktop/HomeWorld_PA_E/` |
| **Utility** | [capture_viewport.py](../../Content/Python/capture_viewport.py) |

Epic: [Taking Screenshots](https://dev.epicgames.com/documentation/en-us/unreal-engine/taking-screenshots-in-unreal-engine) · [Scripting the Unreal Editor Using Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python) · [FULL_AUTOMATION_RESEARCH.md](FULL_AUTOMATION_RESEARCH.md) §10b.

**Wait race (DESKTOP 2026-09-22):** Shot2 PNG appeared ~268s after AutomationLibrary invoke while an earlier 120s script timeout had already given up — rung-1 scripts now use **330s file-first wait** and treat AutomationEditorTask stall as non-fatal until the wait ends.

### Rung 2 — SCOUT backlog only (not installed; needs `APPROVE TOOL SCOUT`)

Candidates to document if UE rung-1 path fails on DESKTOP — **names + why only**:

| Name | Why consider | License / notes |
|------|----------------|-----------------|
| **NirCmd** `savescreenshot` | HWND-targeted host still if Editor API never writes PNG | Free util; see [FULL_AUTOMATION_RESEARCH.md](FULL_AUTOMATION_RESEARCH.md) §11 |
| **OBS CLI** | Frame export from recorded viewport session | Free; heavier than still API |
| **UnrealMCPToolkit** `take_screenshot` | Only if **already** on DESKTOP and returns viewport pixels | Ecosystem; not auto-added |
| **Epic Screenshot Comparison Tool** | Golden/regression **after** a PNG exists | Engine-adjacent; compare not capture |

**No auto-install.** Lead **`APPROVE TOOL SCOUT <name>`** before download or pilot.

### Rung 3 — Future custom work (needs `APPROVE TOOL BUILD`)

Examples **not** in current PR scope:

- Net-new host capture daemon or desktop automation stack beyond shipped `gui_automation/`
- Large golden-compare pipeline or CI screenshot farm
- Replacing UE capture with a custom render path

**Allowed now (rung 1):** Harden `capture_shotlist_viewport.py` / `capture_viewport.py` only.

---

## Banned for shotlist PASS (unchanged)

| Method | Why |
|--------|-----|
| Host **PIL ImageGrab** / full-desktop **PyAutoGUI** when another UI may own focus | Grok chat, Outliner, Content Browser — not lit viewport ([KNOWN_ERRORS.md](../KNOWN_ERRORS.md), PA-E 2026-09-22) |
| **Tiny / missing / near-black** Cmd HighResShot treated as PASS | PA-E / NF2-B |

[capture_editor_screenshot.py](../../Content/Python/capture_editor_screenshot.py) — host diagnostics **only**; not PA-E / shotlist success path.

---

## PA-E failure history (cross-links)

| Date | Issue | Doc |
|------|--------|-----|
| 2026-09-19 | NF2-B Cmd HighResShot — shot1/2 missing | [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) §Gap NF2-B |
| 2026-09-22 | Cmd ok but missing/tiny/black | [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) · [DEFECT_PA_E_shot_capture_automation.md](../../Docs/qa/DEFECT_PA_E_shot_capture_automation.md) |
| 2026-09-22 | ImageGrab → chat/desktop/chrome | [PA_E_SHOTS.md](../../Docs/handoffs/PA_E_SHOTS.md) (track closed; automation gap **OPEN**) |
| 2026-09-22 | `Rotator` positional mis-pose | [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) — keyword `pitch` / `yaw` / `roll` |

**Track status:** Lead **`APPROVE PA-E`** closed Docs/32; formal Shot 1/2 stills **deferred/accepted**. Automation gap **OPEN** until DESKTOP proves rung-1 script + report (Conductor — not cloud).

**Poses:** [P6_FIX_shot1.md](../../Docs/handoffs/P6_FIX_shot1.md) · [CAM_Hero.md](../../Lib/00_Core/CAM_Hero.md) · [00_SHOTLIST.md](../../Docs/00_SHOTLIST.md).
