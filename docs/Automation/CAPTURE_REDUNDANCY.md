# Universal tooling redundancy and practice (Lead-gated)

**Canonical doc (filename legacy: `CAPTURE_REDUNDANCY.md`):** Lead policy for **any** automation / tooling gap — console and Editor Python APIs, PIE harnesses, GUI automation, MCP extensions, host utilities, builds, commandlets, wait/retry logic. **Not** scoped to screenshots or shotlist; those are one **instance** below.

**Canonical gap log:** [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) · **Instance (shotlist / PA-E):** § [Shotlist / PA-E capture](#shotlist--pa-e-capture-instance).

**Cursor rule mirror:** [.cursor/rules/automation-standards.mdc](../../.cursor/rules/automation-standards.mdc).

---

## Universal practice suite (Lead lock-in, 2026-09-22)

Apply in order **before** escalating rungs or asking Lead open-ended “does anyone else hit this?”

**KNOWN_ERROR_LOG:** [automation-standards.mdc](../../.cursor/rules/automation-standards.mdc) v1.10 § KNOWN_ERROR_LOG; bullets in [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) § PA-E DESKTOP prove misses.

### Testing preconditions (Lead lock-in — **all** automation, not capture-only)

Before trusting **any** pass/fail output (CI, Editor Python, MCP harness, MRQ, screenshots, PIE tests, commandlets):

| Step | Verify |
|------|--------|
| 1 | **Content in level** — required actors/assets are present in the **loaded** level/world, not assumed from paths alone. |
| 2 | **Camera aim** — viewport/shot cameras point at that content (e.g. bounds centroids), not void or stale hardcoded poses. |
| 3 | **Lighting / TOD / view mode** — time-of-day phase, lighting, and editor view mode match **test or shotlist intent**; **record** phase/commands used in the report (implicit `hw.TimeOfDay.Phase 2` without doc alignment is a precondition smell). |
| 4 | **Capture / inspect** — run the tool, then inspect artifacts and logs before claiming PASS or closed FAIL. |

PA-E capture maps step 1–2 to [pa_e_homestead_capture_diagnostic.py](../../Content/Python/pa_e_homestead_capture_diagnostic.py) and `LEAD_PROVE_LOOP` in [pa_e_shotlist_common.py](../../Content/Python/pa_e_shotlist_common.py). Shotlist stills: **thematic readable night** for Shot 1–2 per [00_SHOTLIST.md](../Docs/00_SHOTLIST.md) — **`homestead_night_environment`** in `Saved/pa_e_capture_report.json` (Phase 2 + PRESET tune + stack verify); **not** day phase and **not** Phase 2 without tune.

### P0 Arrange gate (blocks capture — 2026-09-22)

**API:** `arrange_pa_e_shotlist()` / alias `assert_environment_ready()` in [pa_e_shotlist_common.py](../../Content/Python/pa_e_shotlist_common.py). **Artifact:** `Saved/pa_e_arrange_gate.json` (`ready`, `blocked_reasons`, `inventory`, `aim`, `lighting`, `tool_readiness`).

After `load_level`, capture scripts (**must not** start MRQ/AL until `ready: true`):

1. Inventory homestead dress in the **loaded** level (`inventory_ok`).
2. **Relocate** `CAM_*` from per-shot **`aim_bounds`** (`homestead_bounds_relocate` / shotlist doc meters), then **look_at** centroid; **`forward_ray_hits_dress_aabb`** required for `aim_ok`. In-level rotate-only is fallback. Exclude **Cliff** (and Fence/Rock) from aim needles — see KNOWN_ERRORS.
3. Phase 2 + PRESET tune + verify moon/skylight/cabin stack; **re-seed** session TMP fixtures under `VS_MVP/TMP_PA_E_Arrange` when stack missing after load (no .umap commit required).
4. Lit + game view + `finish_loading_before_screenshot` when exposed.
5. MRQ path: `probe_mrq_tool_readiness()` — missing types → `mrq_unavailable`; plugins enabled but subsystem null → `editor_restart_required`.

When `ready: false`, scripts write `Saved/pa_e_capture_report.json` with **`prove_loop_status: "blocked"`**, **`closed_fail: false`** — **not** a closed FAIL. Task list: [HARNESS_ARRANGE_TASKLIST.md](HARNESS_ARRANGE_TASKLIST.md).

**Three-state outcomes (P1):** Reports add **`capture_outcome`**: `pass` | `soft_fail` | `closed_fail` (+ **`capture_outcome_open`** when soft). **`ok: true`** only on full **`pass`**. **`capture_pass`** = **harness** (luminance + framing intent) — **not** visual framing alone; **`visual_framing_pass`** requires Lead **`lead_visual_framing_approved`**. Near-black / missing preconditions ⇒ **`soft_fail`**, not closed FAIL.

**Assert (post-#170 + P1):** **`validate_png`** (luminance) then **`finalize_shot_validation`** (wide anchor / **`aim_ok`** / ray AABB). Luminance PASS ≠ framing PASS. **`shot_pair_validation`** rejects identical scrap. **`closed_fail`** when proved wrong (void after **`visible_sky_stack_ok`**, aim miss with lit scrap). Conductor **`conductor_mrq_capture_preflight`** before MRQ `main()`: Markers world, VNP module reload, **`probe_mrq_tool_readiness()`**, **`MRQ_LATENT_WAIT_CONTRACT`**, **`reset_mrq_session_guards()`**. Night gate prefers **`visible_sky_stack_ok`** over bare **`stack_ok`** on MRQ PIE path.

**P2 industry harness (PA-E / MRQ):** Session fixtures under `VS_MVP/TMP_PA_E_Arrange` + editor **`PA_E_MRQ_*`** — **`inventory_pa_e_session_fixtures`**, **`reseed_pa_e_tmp_fixtures_for_capture`**, optional **`teardown_pa_e_session_fixtures`** (editor only; does not delete saved dress). Reports stamp **`artifact_stamps`** (PNG/report/gate mtimes). Full shot PNG purge only when **`PA_E_FRESH_PROVE=1`** at prove start. Task list: [HARNESS_ARRANGE_TASKLIST.md](HARNESS_ARRANGE_TASKLIST.md) P2.

**P3 harness audit (prove scripts):** Full script → gate matrix in [HARNESS_ARRANGE_TASKLIST.md](HARNESS_ARRANGE_TASKLIST.md) P3 table. **Exempt** scripts document one-line **Harness P3 exempt** in module docstring (generic utility, host-only, PIE-instruction JSON, HR preflight, legacy spikes) — not shotlist Arrange.

**MRQ PIE lighting (docs-first):** `MoviePipelinePIEExecutor` renders a **PIE** world. `load_map` / MRQ can **respawn** the level so Editor TMP lights under `VS_MVP/TMP_PA_E_Arrange` do not carry sky/atmo into the render — **cabin warm can read while sky is void black**. Before each job: `reapply_night_environment_for_mrq_shot` → `apply_mrq_pie_homestead_night_stack` (Phase 2 + moon **AtmosphereSunLightIndex 1** + SkyLight fill + **RecaptureSky** + SkyAtmosphere + exposure Min/Max cvars; MRQ job also adds `MoviePipelineConsoleVariableSetting` when available). Epic/community: enable **Atmosphere Sun Light** on the moon directional; Sky Atmosphere present; RecaptureSky after TOD/atmo changes — **do not switch to day**. See `mrq_pie_lighting_note` in arrange gate / capture report.

| # | Practice | Summary |
|---|----------|---------|
| 1 | **Docs-first** | Official vendor docs for any tool surface before inventing/hardening (unless already in repo policy / agent memory). Parameter order, required context, save paths. |
| 2 | **Proven-results first** | Patterns that already work for others (docs + community/industry) before custom ladders, long blocking waits, or novel stacks. |
| 3 | **Research on dead-ends** | After rung-1 hardening **fails with evidence**, one proactive **public** research pass (forums, issues, known bugs) — record in gap research log — **before** recommending SCOUT/BUILD or bouncing the question to Lead. |
| 4 | **Gated redundancy ladder** | Rung 1 built-in / in-repo → **`APPROVE TOOL SCOUT`** → **`APPROVE TOOL BUILD`**; **no auto-install**; no unprompted new frameworks. |
| 5 | **Lead-correction → harness** | Proven Lead corrections become **blocking gates / `PROVE_CRITERIA` in code** in the same PR window — compact thresholds, not chat-only checklists. Examples: Arrange before assert; wrong stills ⇒ fix gate + setup (do not move on); global mean alone insufficient (center crop, non-black fraction, shot uniqueness). |

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
| **Movie Render Queue (MRQ) one-frame still** | **Primary (canonical).** [capture_shotlist.py](../../Content/Python/capture_shotlist.py) → [capture_shotlist_mrq.py](../../Content/Python/capture_shotlist_mrq.py): in-level **CAM_Hero** / **CAM_CabinClose** possessable + camera-cut (with preroll for warm-up), **deferred lit** PNG pass, `MoviePipelineAntiAliasingSetting` engine/GPU warm-up, `MoviePipelinePIEExecutor`, Slate pre-tick + keep_alive. **PASS** = bytes + **mean + center-crop + bright-pixel fraction + shot-pair diversity** — **not** file-exists-only or global-mean speckle. Per-shot night reapply before each job. Plugins: **MovieRenderPipeline**, **MovieRenderPipelineEditor**, **SequencerScripting**. **Gap OPEN** until DESKTOP re-prove lit homestead. |
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

**Lead hard rule — prove loop before any failure claim:** Do **not** treat near-black stills as a **closed FAIL**. Required order:

1. **Inventory** — confirm homestead dress/mesh actors are **in** the loaded level (`DRESS_*`, cabin/island kit).
2. **Aim** — point viewport/shot cameras at **confirmed actor bounds centroids** (MRQ uses in-level `CAM_Hero` / `CAM_CabinClose` with re-aim at framing bounds; avoid hardcoded poses into void).
3. **Lighting / TOD / view mode** — phase and lit game view match **shotlist intent**; report **`time_of_day`** (PA-E shots 1–2: **Night** phase 2 per [00_SHOTLIST.md](../Docs/00_SHOTLIST.md), not undocumented implicit console).
4. **Capture + inspect** — run [capture_shotlist.py](../../Content/Python/capture_shotlist.py) (MRQ primary); read mean luminance; near-black ⇒ loop continues.
5. **Bug-fix** — pose / lighting / game-view / pilot / buffer until stills show intended homestead.

**Diagnostic (steps 1–2 only):** MCP `execute_python_script("pa_e_homestead_capture_diagnostic.py")` → `Saved/pa_e_homestead_capture_diagnostic.json` (camera vs homestead centroids).

| Requirement | Not sufficient |
|-------------|----------------|
| Both `Shot1_lookout.png` + `Shot2_cabin_garden.png` under `Saved/Screenshots/PA_E/` | PNG exists but near-black |
| `Saved/pa_e_capture_report.json` **`ok: true`** (capture PASS) | `ok: false` with **`closed_fail: false`** and **`prove_loop_status: in_progress`** — near-black only; **not** a closed automation FAIL |
| Mean luminance ≥ **8** (0–255 scale) per shot | “File wrote so PASS” |
| Lead-visible homestead framing (CAM_Hero / CAM_CabinClose aimed at inventory bounds) | Empty/unlit capture buffer |

Report includes **`lead_prove_loop`**, **`prove_criteria`**, **`closed_fail`**, **`prove_loop_status`**, and **`desktop_conductor_checklist`** from [capture_shotlist_mrq.py](../../Content/Python/capture_shotlist_mrq.py).

**Poses:** [P6_FIX_shot1.md](../../Docs/handoffs/P6_FIX_shot1.md) · [CAM_Hero.md](../../Lib/00_Core/CAM_Hero.md) · [00_SHOTLIST.md](../../Docs/00_SHOTLIST.md).
