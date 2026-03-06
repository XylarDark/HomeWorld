# MVP gap analysis (polished-MVP readiness)

**Purpose:** Percentage-based gap between current state and a **polished MVP** (feature-complete, verification green, ready for you to do Editor polish). Also estimates how many more **task-list runs** before you should switch to in-Editor polishing.

**Date:** 2026-03-05 (after twenty-sixth list completed).

---

## 1. What “polished MVP” means here

- **One moment** (Claim homestead) and **one corner** (Homestead compound) locked and showable.
- **Pre-demo checklist** (§3 in VERTICAL_SLICE_CHECKLIST): Level, Character, Moment, Corner, Stability all **verified in PIE** (not just “documented when MCP not connected”).
- **No critical blockers** for a short playtest or demo: runnable build (Editor PIE or packaged exe), no crash in 2–5 min, key flows (place, harvest, night convert, HUD) working.
- **Ready for Editor polish:** You can focus on lighting, LOD, asset placement, animation tweaks, and UX polish instead of “finishing” systems.

---

## 2. Work completed so far (summary)

- **26 full 10-task list cycles** (all T1–T10 completed per list).
- **Act 1 core:** PCG forest, GAS (PrimaryAttack, Dodge, Interact, Place), BuildPlacementSupport, Week 1 playtest gate.
- **Homestead:** DemoMap layout, harvest (TryHarvestInFront, GA_Interact), place (GA_Place), agentic building prep; full agentic flow deferred.
- **Family:** Spawn (MEC + State Tree), Protector, Healer, Child role; role persistence; Defend positions (design + stub); return at dawn stub.
- **Day/night & astral:** TimeOfDay phase, astral death (RequestAstralDeath → AdvanceToDawn), spiritual power (collect, spend, persist), day buff (restore + bonus at night), LoveLevel (stub + persistence), SaveGame (TimeOfDay, spiritual power, day buff, LoveLevel).
- **Conversion:** Design (CONVERSION_NOT_KILL), ReportFoeConverted, ConvertedFoesThisNight, defeat wire (placeholder defeated → convert), converted foe role stub (Vendor/Helper/QuestGiver/Pet/Worker), HUD “Converted: N” and role.
- **Night encounters:** Waves at home (3 waves, configurable), wave counter, planetoid packs (design + spawn-away-from-home stub), key-point boss (design + stub).
- **Combat variety:** Defend = ranged/ground AOE (design + DefendCombatMode stub); planetoid = combos/single-target (design + PlanetoidCombatStyle/ComboHitCount stub); defenses-around-homestead (design + stub).
- **HUD:** Phase, spiritual power, wave, night countdown, astral HP, “Restored today”, “Love: N”, “Converted: N”, converted role, insufficient power, SpiritBurst/SpiritShield cooldown/cost.
- **Vertical slice:** Moment (Claim homestead) and corner (Homestead compound) locked; VERTICAL_SLICE_CHECKLIST §4 updated through twenty-sixth list; written sign-off exists (no demo clip).
- **Automation:** Loop, Watcher, Safe-Build, pie_test_runner, MCP harness; KNOWN_ERRORS, AUTOMATION_GAPS, session continuity docs.

**Still open / deferred:** Full agentic building flow (State Tree/Blueprint); packaged build Stage often fails (files in use); pre-demo §3 often not run with PIE (Editor/MCP not connected in many T9 runs); State Tree Defend branch and portal LevelToOpen have one-time manual steps in AUTOMATION_GAPS.

---

## 3. Percentage-based gap (by dimension)

| Dimension | Weight | Done | Gap | Notes |
|-----------|--------|------|-----|-------|
| **Core loop (explore → fight → build)** | 20% | ~95% | ~1% | Place, harvest, night spawn, convert, waves; combat intentionally placeholder. |
| **Day/night & astral systems** | 20% | ~90% | ~2% | TimeOfDay, astral death, day buff, LoveLevel, SaveGame persistence; day-activity gameplay is stub. |
| **Conversion & roles** | 15% | ~85% | ~2% | Defeat→convert, role stub, HUD; no vendor/helper behavior yet. |
| **Combat variety (defend vs planetoid)** | 10% | ~75% | ~2.5% | Design + stubs (DefendCombatMode, PlanetoidCombatStyle, defenses); no real abilities. |
| **Homestead & planetoid flow** | 10% | ~70% | ~3% | Design + homestead-landed stub; planetoid transition has manual/gap steps. |
| **Vertical slice verification** | 15% | ~50% | ~7.5% | §3 often not run with PIE; package fails at Stage; moment/corner locked. |
| **Stability & polish readiness** | 10% | ~55% | ~4.5% | No sustained 2–5 min PIE stability run; KNOWN_ERRORS/AUTOMATION_GAPS documented. |

**Weighted completion:** ~80% **complete** → **~20% gap** to polished MVP.

Rough interpretation:
- **~80%:** Feature set and design are in place; stubs and persistence exist; HUD and conversion flow work at a stub level.
- **~20%:** Mostly **verification and packaging** (pre-demo §3 green, packaged exe or accepted workaround, one solid PIE pass), plus any **hardening** (fix known issues, document manual steps).

---

## 4. What’s left before “go into Editor and polish”

1. **One full PIE verification pass**  
   Editor open, DemoMap (or Homestead) loaded, PIE running, `pie_test_runner.py` run, §3 checklist confirmed (Level, Character, Moment, Corner) and 2–5 min stability. Right now many T9 runs document “MCP not connected” so §3 isn’t actually executed.

2. **Packaged build**  
   Either: (a) Package succeeds (e.g. run Package-AfterClose.ps1 with nothing holding Stage files), or (b) you explicitly accept “no exe for now” and document it. Currently Stage often fails (files in use).

3. **Optional one-time manual steps**  
   If you want planetoid transition and family Defend behavior: LevelToOpen on portal and State Tree Defend branch per AUTOMATION_GAPS. Not required for “claim homestead + homestead compound” slice, but needed for full MVP flow.

4. **Switch to Prototype hardening**  
   When you’re ready for “polish soon,” the next list(s) should be **Prototype hardening** (more verification slots: PIE pre-demo, package, VERTICAL_SLICE_CHECKLIST, AUTOMATION_GAPS, KNOWN_ERRORS), not more rapid prototyping.

---

## 5. How many more task runs before Editor polish?

**Recommendation: 2–4 more task-list runs**, then you can go into the Editor for polishing.

| Runs | Focus | Outcome you’ll have |
|------|--------|----------------------|
| **1 run** | Next list (e.g. twenty-seventh) still in Rapid prototyping | More small features; verification light. You could already polish in Editor in parallel if you’re okay with §3 not fully green. |
| **2 runs** | One Rapid prototyping + one **Prototype hardening** | Hardening run: PIE pre-demo §3, package attempt, checklist and gaps docs. After 2 runs: ~85–90% “done” for polished MVP; good time to do Editor polish and manual verification. |
| **3 runs** | Two normal lists + one full hardening | Same as above plus buffer for a fix/retry (e.g. package or PIE pass). |
| **4 runs** | Three normal + one hardening, or two hardening | Maximum confidence: §3 green, package and KNOWN_ERRORS/AUTOMATION_GAPS updated, then you polish. |

**Practical suggestion:**
- **If you want to polish soon:** Plan for **1–2 more runs**, with the **last run** as **Prototype hardening** (switch PROJECT_STATE §0 to Prototype hardening and generate a verification-heavy list: PIE pre-demo, package, VERTICAL_SLICE_CHECKLIST §3/§4, AUTOMATION_GAPS, buffer). After that, treat the build as “feature-complete for MVP” and do Editor polish.
- **If you want one more feature push:** Do **one more rapid-prototyping list** (e.g. twenty-seventh), then **one hardening list** (run 2). So **2 more runs** → then into Editor for polish.

---

## 6. What to do in Editor for polish

After the fourth run (or when you switch to Editor polish), use this checklist for in-Editor work. Run through it when the build is feature-complete for MVP and you are ready to focus on look, feel, and stability.

| Category | What to do |
|----------|------------|
| **Lighting** | Lighting pass on DemoMap/Homestead: key light, fill, shadows; time-of-day preview if used. |
| **LOD** | LOD check: view distance for PCG/meshes; reduce pop-in where needed. |
| **Asset placement** | Tweak PCG density, exclusion zones, or manual actor placement for the homestead compound and key areas. |
| **Animation** | Animation polish: blend times, root motion, transition in/out of combat or harvest. |
| **UX / HUD** | HUD layout, readability, and feedback (e.g. wave count, spiritual power, converted count); any placeholder text or icons. |
| **Stability** | 2–5 min PIE run: play through moment + corner, confirm no crash or major hitch; note any repro steps for KNOWN_ERRORS. |

**Order:** Optional. Start with stability (2–5 min run), then lighting/LOD and asset placement, then animation and UX as needed.

**Full step-by-step:** For a single tutorial that walks through pre-demo verification, one-time manual steps (portal, State Tree Defend), and the Editor polish checklist, see **[EDITOR_POLISH_TUTORIAL.md](../EDITOR_POLISH_TUTORIAL.md)**.

---

## 7. Summary

- **Gap:** ~**20%** remaining to polished MVP (weighted: ~80% complete).
- **Remaining work:** Mostly **verification** (one full PIE pass of §3, 2–5 min stability) and **packaging** (or documented workaround); optionally one-time manual steps for planetoid/Defend.
- **Task runs before Editor polish:** **2–4** (recommend **2**: one optional feature list + one **Prototype hardening** list, then start Editor polish).

---

**See also:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3 (pre-demo), §4 (deliverables); [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) §0 (phase); [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md); [KNOWN_ERRORS.md](../KNOWN_ERRORS.md).
