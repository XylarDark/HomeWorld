# UE Project Bible — HomeWorld DESKTOP/MCP prove

| Field | Value |
|-------|-------|
| **Audience** | Conductor parent, Test, Fix (DESKTOP prove operators) |
| **Not** | Generic Unreal wiki, Epic tutorial dump, or new product phase |
| **Engine** | **UE 5.8 only** on DESKTOP-21CT3H0 |
| **Canon ops** | [HOST_PULSE.md](handoffs/HOST_PULSE.md) · [PDF_CYCLE.md](../swarm/PDF_CYCLE.md) |

One-shot reference for token-efficient prove: hard gates, stall law, logging, PS-C lessons, do/don’t.

---

## 1. Purpose

HomeWorld prove runs on **DESKTOP** via **warm Editor + MCP (55557)** and `execute_python_script` — not cloud Shell, not Task subagents. This bible compresses **project-specific** cause→avoid rules from PA-E / PS-C DESKTOP runs so operators do not re-learn Slate/MCP/console footguns each session.

**Success shape:** Arrange+map OK → single Act → gate JSON + logs/PNGs under `Saved/` → honest `blocked` / `soft_fail` / `closed_fail` (never invent PASS).

---

## 2. Hard gates (Test / Fix)

| Gate | Rule |
|------|------|
| **Docs-first** | Epic 5.8 docs + in-repo policy before new console syntax, waits, or Editor Python APIs ([CAPTURE_REDUNDANCY.md](../docs/Automation/CAPTURE_REDUNDANCY.md), [automation-standards.mdc](../.cursor/rules/automation-standards.mdc)). |
| **Forums / research** | After rung-1 fail with evidence, one public research pass → log in [AUTOMATION_GAPS.md](../docs/Automation/AUTOMATION_GAPS.md); no invented console commands without docs check. |
| **No invented greps** | Evidence tables from real `Saved/Logs/HomeWorld.log` / gate JSON — see [18_VERIFY_PROVE.md](18_VERIFY_PROVE.md). |
| **Fix scope** | Defect-linked paths only ([PDF_CYCLE.md](../swarm/PDF_CYCLE.md)); re-Test same checklist. |
| **Tooling ladder** | Rung 1 in-repo hardening only unless Lead **`APPROVE TOOL SCOUT`** / **`APPROVE TOOL BUILD`**. |

---

## 3. Keep editor up

| Prefer | Avoid |
|--------|--------|
| **Warm session:** Editor already open, MCP green, map loaded (`L_VS_MVP_Markers` for PS/PA tracks) | Cold launch at start of every micro-step |
| **One prove Act** per MCP script invocation when possible | Chaining long blocking scripts on MCP main thread |
| **Cold start + recover** only under [HOST_PULSE § DESKTOP stall protocol](handoffs/HOST_PULSE.md#desktop-stall-protocol-conductor-owned): **one** kill+relaunch cycle, UE **5.8** binary | Second hang, third kill, flag roulette |

After recover: wait MCP ≤3 min → re-run **one** Arrange+Act, then stop if still stuck (`blocked`).

---

## 4. Logging

| Item | Rule |
|------|------|
| **Primary log** | `Saved/Logs/HomeWorld.log` (+ filtered copies under `Saved/Logs/` when Watcher runs — see [AUTOMATION_EDITOR_LOG.md](../docs/Automation/AUTOMATION_EDITOR_LOG.md)). |
| **ABSLOG / launch** | Prove launches must keep **attached** logging visible to operators (project **ABSLOG** / `-log` discipline on DESKTOP). |
| **Never** | Separate **closeable** external `-log` console as the only prove log sink — if Lead closes it, Conductor loses stall evidence (**console-kill**). |
| **Lead** | Do **not** close the attached prove console during a pending Act → treat as **`blocked`** (same class as host/tool down mid-Act). |
| **Gate artifacts** | `Saved/*_prove_gate.json`, capture reports, `Saved/ps_stills/manifest.json` — KEEP-LOCAL, not git. |

Before greps: `log LogTemp Log` in PIE when scoring verbs ([CONSOLE_COMMANDS.md](../docs/CONSOLE_COMMANDS.md)).

---

## 5. Stall budgets

Aligned with [HOST_PULSE.md](handoffs/HOST_PULSE.md) (5m pulse, 300s floor) and **DESKTOP stall protocol**:

| Budget | Limit |
|--------|--------|
| MCP up (after relaunch) | ≤ **3 min** |
| Act / script wall clock | ≤ **5 min** |
| Recover cycles | **1** only |
| Total stall before Lead | ≤ **10 min** |
| `stall_threshold_sec` (any target) | **≥ 300** (floor; do not set below 300) |

**Scoring while stalled:** host/MCP/tool down or mid-Act drop → **`blocked`**, never product **`closed_fail`**. Product outcomes apply only after Arrange+map OK and Act finished.

---

## 6. PS-C lessons (Cause → Avoid)

| Cause | Avoid |
|-------|--------|
| **FAppTime / no inherited time context** mid-Act on MCP main thread; blocking `time.sleep` + console HighResShot wait → ~**300s** empty/hang (**Fix PS-C-1**) | Marshal capture onto **game thread / Slate tick**: `register_slate_pre_tick_callback`, `keep_python_script_alive`, `console_high_res_invoke_once`, tick **file probe**; **absolute** paths under `Saved/ps_stills/` ([PS_C_METRICS.md](handoffs/PS_C_METRICS.md), [KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md) § PA-E rows). |
| **Stuck / black stills** with visible homestead in viewport | **Arrange + map evidence** before **`closed_fail`**; dark/missing PNG → **`soft_fail`** / `png_missing`; prove loop (inventory → aim → capture → inspect). |
| **Skip Restore** dialog after crash | Click **once**, then wait; else kill + relaunch **UE 5.8 once** (no thrash). |
| **Editor modal** blocking UI | **`blocked`** until Lead dismisses; Fix only if Act caused modal (e.g. dirty shutdown). |
| **MCP `bad_response` or ~300s empty** while `pending_act` | **`blocked`** until MCP healthy + Lead ack; verify port **55557** and Editor process before relaunch. |
| **MCP disconnect ≠ Editor dead** | Check process, port, PNG/report mtimes before kill ([KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md)). |
| **Wrong engine** (5.7 vs 5.8 BuildId) | **`blocked`** / fix association — prove on **UE 5.8** only after Safe-Build on DESKTOP. |
| **Relative HighResShot paths** | **`os.path.abspath`** project_dir + dest; engine CWD trap ([PS_C_METRICS.md](handoffs/PS_C_METRICS.md)). |
| **Metric ≠ visual** | Auto metrics ≠ Lead framing; near-black ≠ “scene is black” if viewport shows geometry ([33_PLACEMENT_STILLS.md](33_PLACEMENT_STILLS.md)). |

**Primary PS-C Act:** `execute_python_script("ps_placement_prove.py")` after `ps_arrange_gate.json` **`ready_for_ps_c: true`**.

---

## 7. Do / Don’t (Conductor prove operators)

### Do

| Do | Why |
|----|-----|
| Confirm world = **`L_VS_MVP_Markers`** before Arrange/Act | Wrong world → false FAIL ([KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md)). |
| Run **Arrange gates** (`ps_arrange_gate`, PA-E preflight) before capture/MRQ | `ready: false` → stop, don’t score product fail. |
| Use **absolute** screenshot paths under `{Project}/Saved/…` | Win64 engine CWD writes otherwise. |
| Prefer **Slate pre-tick** drivers for async capture on MCP thread | Blocking wait freezes ticks → Not Responding. |
| Stamp **`blocked`** for host/MCP/console-kill/modal | Protects Test sheet from false **`closed_fail`**. |
| Tail **`Saved/Logs/HomeWorld.log`** + gate JSON for evidence | Files-only handoffs ([SWARM_OPS.md](../swarm/SWARM_OPS.md)). |
| One **UE 5.8** relaunch recover per stall protocol | HOST_PULSE hard cap. |

### Don’t

| Don’t | Why |
|-------|-----|
| Invent **`APPROVE *`** or new product phases | Lead gates only. |
| Claim PASS without DESKTOP gate file + honest outcomes | No invented greps/stills. |
| **`closed_fail`** on black still when Arrange was ready | Lead policy → **`soft_fail`** + prove loop. |
| Run **`capture_shotlist_mrq.main()`** on `threading.Thread` | MCP must stay on game thread. |
| Close attached **prove `-log` / ABSLOG** console | **console-kill** → **`blocked`**. |
| Auto-install tools / NirCmd / parallel capture stacks | Ladder gates ([CAPTURE_REDUNDANCY.md](../docs/Automation/CAPTURE_REDUNDANCY.md)). |
| Third kill / parallel Fix invent after budget exhausted | Park Act; notify Lead. |

---

## 8. Pointers (repo-relative)

| Doc | Role |
|-----|------|
| [handoffs/HOST_PULSE.md](handoffs/HOST_PULSE.md) | Pulse states, 300s floor, DESKTOP stall protocol |
| [../swarm/PDF_CYCLE.md](../swarm/PDF_CYCLE.md) | Design → Implement → Test → Fix loop |
| [../docs/KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md) | Cause→Avoid rows (§ PA-E DESKTOP prove misses) |
| [handoffs/PS_C_METRICS.md](handoffs/PS_C_METRICS.md) | PS-C metrics, stills, prove checklist |
| [33_PLACEMENT_STILLS.md](33_PLACEMENT_STILLS.md) | PS track canon |
| [handoffs/PA_E_SHOTS.md](handoffs/PA_E_SHOTS.md) | PA-E shot prove (shared capture lessons) |
| [../docs/Automation/CAPTURE_REDUNDANCY.md](../docs/Automation/CAPTURE_REDUNDANCY.md) | Docs-first, redundancy ladder |
| [../docs/Setup/WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) | Cloud vs DESKTOP split |
| [../docs/Setup/MCP_SETUP.md](../docs/Setup/MCP_SETUP.md) | MCP 55557 |
| [18_VERIFY_PROVE.md](18_VERIFY_PROVE.md) | VP2 DESKTOP grep prove (closed; pattern reference) |
| [../Content/Python/ps_placement_prove.py](../Content/Python/ps_placement_prove.py) | PS-C Act (read-only for operators) |
| [../.cursor/skills/pcg-validate/SKILL.md](../.cursor/skills/pcg-validate/SKILL.md) | PCG validate when prove touches PCG |

---

**Maintainers:** HomeWorld Design / Conductor — append rows when DESKTOP prove adds a new recurring miss; keep one-line Cause→Avoid in [KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md), link here.
