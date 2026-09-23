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
| **Before brute force** | **Epic 5.8 docs + UE forums / proven patterns** (repo rung 1, CAPTURE_REDUNDANCY) **before** custom wait ladders, console variants, or novel stacks — Test/Fix do not “try harder” first. |
| **Docs-first** | Same policy for new Editor Python APIs, MCP usage, commandlets ([automation-standards.mdc](../.cursor/rules/automation-standards.mdc)). |
| **Forums / research** | After rung-1 fail **with evidence**, one public pass → [AUTOMATION_GAPS.md](../docs/Automation/AUTOMATION_GAPS.md); no invented console commands. |
| **No invented greps** | Evidence tables from real `Saved/Logs/HomeWorld.log` / gate JSON — see [18_VERIFY_PROVE.md](18_VERIFY_PROVE.md). |
| **Fix scope** | Defect-linked paths only ([PDF_CYCLE.md](../swarm/PDF_CYCLE.md)); re-Test same checklist. |
| **Tooling ladder** | Rung 1 in-repo hardening only unless Lead **`APPROVE TOOL SCOUT`** / **`APPROVE TOOL BUILD`**. |

---

## 3. Keep editor up

| Prefer | Avoid |
|--------|--------|
| **Warm session:** Editor already open, MCP green, map loaded (`L_VS_MVP_Markers` for PS/PA tracks) | Cold launch after every Python tweak |
| **One prove Act** per MCP script invocation when possible | Chaining long blocking scripts on MCP main thread |
| **Cold start + recover** only under [HOST_PULSE § DESKTOP stall protocol](handoffs/HOST_PULSE.md#desktop-stall-protocol-conductor-owned): **one** kill+relaunch, UE **5.8** binary | Second hang, third kill, flag roulette |
| **Full Editor relaunch + Safe-Build** only when C++ **reflection** changes (`UCLASS` / `UFUNCTION` / `UPROPERTY`, new reflected types) | Restarting UE for `.cpp` **body-only** fixes (use Live Coding — §3b) |

After recover: wait MCP ≤3 min → re-run **one** Arrange+Act, then stop if still stuck (`blocked`).

---

## 3b. Cheap iterate (Lead locks)

**Split:** **VS Code / Cursor** = edit files; **DESKTOP Editor** = live world + MCP. **Act** always **`execute_python_script("<script>.py")`** on the warm session ([MCP_SETUP.md](../docs/Setup/MCP_SETUP.md)) — not a one-off local `py` against a cold Editor for prove scoring.

| Cause | Avoid |
|-------|--------|
| Restart UE after each Python edit | Edit `Content/Python/` in IDE → **`importlib.reload(module)`** in orchestrator path → re-run **same Act** via MCP; **never** `reload(unreal)` |
| Safe-Build for every C++ typo in a function body | **Live Coding** for implementation-only `.cpp` / `.h` body edits |
| Live Coding after new `UProperty` / RPC / class spec | **Full rebuild** (`Safe-Build` on DESKTOP) for **`UCLASS` / `UFUNCTION` / `UPROPERTY`** (reflection/schema); then relaunch if MCP/module load requires it |
| Prove from cloud shell or non-MCP Python | Cloud merges/docs; **Conductor parent** runs Act on **DESKTOP-21CT3H0** only ([WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md)) |
| Brute-force capture/console before docs | §2 **before brute force** — forums + Epic 5.8 + in-repo pretick/MRQ patterns first |

---

## 4. Logging

| Item | Rule |
|------|------|
| **Primary log** | `Saved/Logs/HomeWorld.log` (+ filtered copies under `Saved/Logs/` when Watcher runs — see [AUTOMATION_EDITOR_LOG.md](../docs/Automation/AUTOMATION_EDITOR_LOG.md)). |
| **ABSLOG + Saved/Logs** | Prove truth in **`Saved/Logs/HomeWorld.log`** and attached **ABSLOG** discipline on DESKTOP — not a detached log elsewhere. |
| **Never** | **Closeable** standalone `-log` console as the only sink; Lead closing attached prove log = **console-kill** → score **`blocked`**, not product fail. |
| **Lead** | Do **not** close the attached prove console during a pending Act (same as host down mid-Act). |
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
| **IDE edit** → **`importlib.reload`** → MCP **re-run Act** on warm Editor | Cheap Python iterate without cold start. |
| **Live Coding** for C++ body fixes during Fix lap | Full Safe-Build only when reflection surface changes. |

### Don’t

| Don’t | Why |
|-------|-----|
| Invent **`APPROVE *`** or new product phases | Lead gates only. |
| Claim PASS without DESKTOP gate file + honest outcomes | No invented greps/stills. |
| **`closed_fail`** on black still when Arrange was ready | Lead policy → **`soft_fail`** + prove loop. |
| Run **`capture_shotlist_mrq.main()`** on `threading.Thread` | MCP must stay on game thread. |
| **`reload(unreal)`** or restart Editor for every `.py` save | Breaks MCP session; use `importlib.reload` on project modules only. |
| Cold-start **`py Content/Python/...`** for scored prove | Act must be MCP against live DESKTOP session. |
| Brute-force waits/console before Epic + forums + rung 1 | §2 hard gate for Test/Fix. |
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
| [../docs/Setup/BUILD_POLICY.md](../docs/Setup/BUILD_POLICY.md) | Safe-Build vs Live Coding on DESKTOP |
| [../.cursor/rules/00-core-principles.mdc](../.cursor/rules/00-core-principles.mdc) | `importlib.reload` idempotency |
| [18_VERIFY_PROVE.md](18_VERIFY_PROVE.md) | VP2 DESKTOP grep prove (closed; pattern reference) |
| [../Content/Python/ps_placement_prove.py](../Content/Python/ps_placement_prove.py) | PS-C Act (read-only for operators) |
| [../.cursor/skills/pcg-validate/SKILL.md](../.cursor/skills/pcg-validate/SKILL.md) | PCG validate when prove touches PCG |

---

**Maintainers:** HomeWorld Design / Conductor — append rows when DESKTOP prove adds a new recurring miss; keep one-line Cause→Avoid in [KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md), link here.
