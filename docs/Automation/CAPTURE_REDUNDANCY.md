# Universal tooling redundancy and practice (Lead-gated)

**Canonical doc (filename legacy: `CAPTURE_REDUNDANCY.md`):** Lead policy for **any** automation / tooling gap — console and Editor Python APIs, PIE harnesses, GUI automation, MCP extensions, host utilities, builds, commandlets, wait/retry logic. **Not** scoped to screenshots or shotlist; those are one **instance** below.

**Canonical gap log:** [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) · **Instance (shotlist / PA-E):** § [Shotlist / PA-E capture](#shotlist--pa-e-capture-instance).

**Cursor rule mirror:** [.cursor/rules/automation-standards.mdc](../../.cursor/rules/automation-standards.mdc).

---

## Universal practice suite (Lead lock-in, 2026-09-22)

Apply in order **before** escalating rungs or asking Lead open-ended “does anyone else hit this?”

| # | Practice | Summary |
|---|----------|---------|
| 1 | **Docs-first** | Official vendor docs for any tool surface before inventing/hardening (unless already in repo policy / agent memory). Parameter order, required context, save paths. |
| 2 | **Proven-results first** | Patterns that already work for others (docs + community/industry) before custom ladders, long blocking waits, or novel stacks. |
| 3 | **Research on dead-ends** | After rung-1 hardening **fails with evidence**, one proactive **public** research pass (forums, issues, known bugs) — record in gap research log — **before** recommending SCOUT/BUILD or bouncing the question to Lead. |
| 4 | **Gated redundancy ladder** | Rung 1 built-in / in-repo → **`APPROVE TOOL SCOUT`** → **`APPROVE TOOL BUILD`**; **no auto-install**; no unprompted new frameworks. |

Details below. Rung gates unchanged from prior Lead lock-in.

---

## Global ladder (all tooling gaps)

### Docs-first (Lead policy, 2026-09-22)

**Before** using or hardening **any** automation tool surface — Unreal console commands, Editor Python APIs, MCP tools, commandlets, host scripts, CI steps: read **official Epic (or vendor) documentation** first, unless exact usage is already in repo policy ([KNOWN_ERRORS.md](../KNOWN_ERRORS.md), this file) or durable agent memory.

- Match documented **parameter order**, **required context** (PIE vs editor, subsystem vs actor, etc.), and **default output paths**.
- Do **not** lock in syntax or retry logic **only** from failed DESKTOP proves — use docs or `/parallel-extract` on vendor URLs ([11-parallel-plugin.mdc](../../.cursor/rules/11-parallel-plugin.mdc)) before adding alternate strings, waits, or variant ladders.
- **Undocumented strings/APIs:** If vendor docs do not cover something the repo uses, log in [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) and prefer documented subsystems — do not invent aliases.

#### Examples (non-exhaustive)

- Epic [Taking Screenshots](https://dev.epicgames.com/documentation/en-us/unreal-engine/taking-screenshots-in-unreal-engine) — `HighResShot filename=PATH` before dimensions; motivating miss: `HighResShot 1920x1080 filename="…"` without docs-first.
- Epic [AutomationLibrary (Python API)](https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/AutomationLibrary?application_version=5.8) — e.g. `take_high_res_screenshot`.

---

### Proven-results first (Lead policy, 2026-09-22)

**Before** inventing custom automation for **any** gap (long blocking waits, multi-variant hunts, net-new orchestration, novel host stacks):

1. **Official vendor docs** — **Docs-first** above.
2. **Proven community / industry patterns** for the same goal (Epic forums staff posts, common studio practice, [GAP_SOLUTIONS_RESEARCH.md](GAP_SOLUTIONS_RESEARCH.md), [FULL_AUTOMATION_RESEARCH.md](FULL_AUTOMATION_RESEARCH.md)).

**Extend or invent** only when those are checked and clearly unfit, **or** Lead gates rung 2–3. Prefer shipped MCP/Python/`gui_automation/` and Epic-recommended test patterns before bespoke timeout farms.

**Relationship to rungs:** Docs-first + proven-results are **preconditions** on rung-1 hardening.

#### Examples (non-exhaustive)

| Domain | Proven lane | Avoid when untried |
|--------|-------------|-------------------|
| Editor stills / evidence PNGs | Slate-tick **`AutomationLibrary.take_high_res_screenshot`** (one request per tick) | Stacked console form ladders with **full** blocking wait after each failure (incl. engine **`Bad input`**) |
| Same | **Movie Render Queue** one-frame / short Level Sequence stills | Ad-hoc multi-minute console-only proves |
| Host fallback | Third-party util (e.g. **NirCmd**) | Auto-install — requires **`APPROVE TOOL SCOUT`** |
| PIE / verbs | Documented automation test / latent patterns | Custom verb farms with ad-hoc timeouts only |

Motivating instance (2026-09-22): post-**#161** DESKTOP ~30+ min on per-form **330s** `HighResShot` waits while **MRQ** / tick-spaced AutomationLibrary were standard untried lanes — [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) research log.

---

### Research on dead-ends (Lead policy, 2026-09-22)

When **rung-1** hardening (with Docs-first + proven-results applied) **still fails on DESKTOP** with logged evidence:

1. Run **one proactive public research pass** before proposing rung 2/3 or asking Lead “does anyone else hit this?” — Epic forums, AnswerHub-style threads, GitHub issues (engine/plugin/MCP), `/parallel-search` with **UE 5.8** in the query per [ue58-sources.mdc](../../.cursor/rules/ue58-sources.mdc).
2. **Record** findings (links, one-line takeaway, adopt/reject) in [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) **Research log** — even if inconclusive.
3. **Then** either: adjust rung-1 using a cited pattern, log the gap with suggested automation, or request **`APPROVE TOOL SCOUT`** / **`APPROVE TOOL BUILD`** with scout/build note referencing the research.

Do **not** skip this step to jump straight to custom stacks or Lead ping-pong.

#### Examples (non-exhaustive)

- **`AutomationEditorTask` never completes** — search Epic/issues for `take_high_res_screenshot` + Editor Python + 5.8 before inventing new wait ladders.
- **MCP property not found** — forum/issue search + [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) before new plugin scout.

---

### Rung 1 — Built-in / already-in-repo (no gate)

**Exhaust first, every time.** Re-try when the engine, MCP plugin, or repo scripts change. **Docs-first**, **Proven-results first**, and **Research on dead-ends** (after failure) apply before rung 2/3.

| Allowed without a new gate | Examples |
|----------------------------|----------|
| Epic / UE Editor APIs | `AutomationLibrary`, console commands, Editor Python subsystems |
| MCP + scripts already in the repo | `execute_python_script`, [Content/Python/](../../Content/Python/) orchestrators |
| Idempotent hardening of **existing** Editor Python that calls rung-1 APIs | [capture_shotlist_viewport.py](../../Content/Python/capture_shotlist_viewport.py), [capture_viewport.py](../../Content/Python/capture_viewport.py) |
| Documented GUI automation **already** under [Content/Python/gui_automation/](Content/Python/gui_automation/) | Ref-image clickers shipped with the repo |

**Gate guards (rung 1):** No new third-party installs; no new parallel automation frameworks.

---

### Rung 2 — Scout free / open third-party (Lead gate required)

**Only after rung 1 is exhausted** on DESKTOP (logged failure with evidence) **and** **Research on dead-ends** (above) is recorded in the gap research log.

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

**Only after rung 1 exhausted, dead-end research logged, and (if applicable) rung 2 scouted with Lead approval.**

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
| **`AutomationLibrary.take_high_res_screenshot`** + **Slate pre-tick wait** | **OPEN bug — viewport capture path (not PASS primary).** Pretick can write PNGs that are **near-black** while Lead **sees lit homestead** when rotating the viewport → wrong **pose / game-view / camera pilot / HighResShot buffer**, not absent content. Diagnostic: [capture_shotlist_viewport.py](../../Content/Python/capture_shotlist_viewport.py). Quality bar unchanged: **lit non-black** stills required. |
| **Movie Render Queue (MRQ) one-frame still** | **Primary (canonical).** [capture_shotlist.py](../../Content/Python/capture_shotlist.py) → [capture_shotlist_mrq.py](../../Content/Python/capture_shotlist_mrq.py): in-level **CAM_Hero** / **CAM_CabinClose** possessable + camera-cut (with preroll for warm-up), **deferred lit** PNG pass, `MoviePipelineAntiAliasingSetting` engine/GPU warm-up, `MoviePipelinePIEExecutor`, Slate pre-tick + keep_alive. **PASS** = luminance + bytes gates + visible homestead — **not** file-exists-only. Plugins: **MovieRenderPipeline**, **MovieRenderPipelineEditor**, **SequencerScripting**. **Gap OPEN** until DESKTOP re-prove. |
| Console **`HighResShot`** multi-form ladder | **Retired as shotlist primary** — post-#161 DESKTOP burned ~30+ min on five forms × **330s** waits (incl. after immediate **`Bad input`**). Epic doc order still valid for ad-hoc console use; not the canonical shotlist script path. [Taking Screenshots](https://dev.epicgames.com/documentation/en-us/unreal-engine/taking-screenshots-in-unreal-engine) |
| `AutomationLibrary.set_editor_viewport_view_mode` (Lit) | Preferred over console `viewmode lit` when exposed |
| Viewport focus (best-effort) | LevelEditorSubsystem / UnrealEditorSubsystem APIs when present; console **`FOCUSVIEWPORT`** / **`focus`** — **undocumented / unverified** (no Epic console doc); do not invent new console aliases |
| `EditorPythonScripting.set_keep_python_script_alive(True)` | [vnp_editor_keep_alive.py](../../Content/Python/vnp_editor_keep_alive.py) |
| Lit + game view | AutomationLibrary Lit when exposed; else `viewmode lit`; `UnrealEditorSubsystem.editor_set_game_view(True)` when exposed |
| Inter-shot spacing | Extra Slate tick settle between Shot 1 and Shot 2 so a second capture is not fired while the first is in flight |
| **Canonical script** | [capture_shotlist.py](../../Content/Python/capture_shotlist.py) (MRQ) → `Saved/Screenshots/PA_E/`, `Saved/pa_e_capture_report.json`, copy to `C:/Users/User/Desktop/HomeWorld_PA_E/`. Diagnostic: [capture_shotlist_viewport.py](../../Content/Python/capture_shotlist_viewport.py) |
| **Utility** | [capture_viewport.py](../../Content/Python/capture_viewport.py) — may still console-first for generic viewport stills; shotlist instance follows AutomationLibrary primary |

Epic: [Taking Screenshots](https://dev.epicgames.com/documentation/en-us/unreal-engine/taking-screenshots-in-unreal-engine) · [Scripting the Unreal Editor Using Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python) · [FULL_AUTOMATION_RESEARCH.md](FULL_AUTOMATION_RESEARCH.md) §10b.

**Wait policy (2026-09-22+, proven-results-first):** Shot2 PNG appeared ~268s after a **single** AutomationLibrary invoke on an earlier run; **multi-form 330s console ladders** were the anti-pattern. **Blocking-wait anti-pattern (post-#163 DESKTOP, #164):** synchronous **`time.sleep`** / settle loops while waiting for **`AutomationEditorTask`** or disk on the **main thread** are **not** “Slate tick spacing”; they **block** ticks under MCP (Editor **Not Responding**, no PNG). **Rung-1 fix (#165):** **`register_slate_pre_tick_callback`** + `set_keep_python_script_alive(True)` ([vnp_editor_keep_alive.py](../../Content/Python/vnp_editor_keep_alive.py)) in [capture_shotlist_viewport.py](../../Content/Python/capture_shotlist_viewport.py). **One invoke + ~120s tick-driven file wait per shot** + **~75s final drain** — extend budget on DESKTOP only with evidence, not by multiplying forms or blocking the main thread. Research + options (MRQ, NirCmd): [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) research log post-#163.

**Post-#165 pretick prove (~15:01 ET, 2026-09-22):** Pretick kept Editor **Responding** and wrote **`Shot1_lookout.png`** (~38KB) quickly, but report **`file_missing`** because **`MIN_BYTES` gated the wait probe** (not just `_validate_png`) and nested **`POSED`** re-entry fired multiple invokes. Follow-up hardening: **`PREPARING`** phase lock at prepare entry; **`_find_fresh_capture_path`** on timeout/final drain (mtime ≥ `capture_since` authoritative); **`MIN_BYTES` validation-only**.

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
| 2026-09-22 | **post-#163** AL primary + MCP blocking wait → Not Responding, no PNG/report | [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) · [DEFECT_PA_E_shot_capture_automation.md](../../Docs/qa/DEFECT_PA_E_shot_capture_automation.md) · AUTOMATION_GAPS research log |

**Track status:** Lead **`APPROVE PA-E`** closed Docs/32; formal Shot 1/2 stills **deferred/accepted**. Automation gap **OPEN** until DESKTOP proves **MRQ one-frame** ([capture_shotlist.py](../../Content/Python/capture_shotlist.py)) with **lit non-black homestead** stills (mean luminance ≥ gate). **Separate OPEN bug:** AL/HighResShot near-black while viewport shows content — fix pose/game-view/pilot/buffer; do **not** lower quality targets.

### DESKTOP prove bar (non-negotiable)

| Requirement | Not sufficient |
|-------------|----------------|
| Both `Shot1_lookout.png` + `Shot2_cabin_garden.png` under `Saved/Screenshots/PA_E/` | PNG exists but near-black |
| `Saved/pa_e_capture_report.json` **`ok: true`** | `ok: false` or missing luminance |
| Mean luminance ≥ **8** (0–255 scale) per shot | “File wrote so PASS” |
| Lead-visible homestead framing (CAM_Hero / CAM_CabinClose) | Empty/unlit capture buffer |

Report includes **`prove_criteria`** and **`desktop_conductor_checklist`** from [capture_shotlist_mrq.py](../../Content/Python/capture_shotlist_mrq.py).

**Poses:** [P6_FIX_shot1.md](../../Docs/handoffs/P6_FIX_shot1.md) · [CAM_Hero.md](../../Lib/00_Core/CAM_Hero.md) · [00_SHOTLIST.md](../../Docs/00_SHOTLIST.md).
