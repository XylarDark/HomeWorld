# Taste profile (durable)

Reviewed, versioned summary of Lead/process taste and locked decisions.
**Product bible stays authoritative** — this file holds pointers + prefs + rolling outcomes, not palette chips.

**Track:** [Docs/29_TASTE_PROFILER.md](../../Docs/29_TASTE_PROFILER.md)  
**Updates:** Stage in `Saved/taste_profile_session.json`; promote only after Lead/AD confirm or `APPROVE *`.  
**Precedence:** latest Lead chat / `APPROVE *` > this file > never invent.

**Last promoted:** 2026-10-15 (attribute and zone lock)

---

## 1. Canon pointers

| Topic | Path |
|-------|------|
| Map / verbs / locks | [Docs/00_CANON.md](../../Docs/00_CANON.md) |
| Art tone / palette / shape | [Docs/02_ART_BIBLE.md](../../Docs/02_ART_BIBLE.md) |
| Shot list (five shots only) | [Docs/00_SHOTLIST.md](../../Docs/00_SHOTLIST.md) |
| Last closed feel interview | [Docs/26_TASTE_NEXT.md](../../Docs/26_TASTE_NEXT.md) — Night Feel |
| Night Feel Build | [Docs/27_NIGHT_FEEL_BUILD.md](../../Docs/27_NIGHT_FEEL_BUILD.md) — CLOSED |
| Taste Gates harness | [Docs/28_TASTE_GATES.md](../../Docs/28_TASTE_GATES.md) — CLOSED |

**Feel target (Docs/26, locked):** Stranger in ~3s reads **safe home above a living world** via night lookdev + dusk/dawn form swap; soft handmade VFX + audio sting backlog only on explicit ask.

---

## 2. Lead process prefs

| Pref | Value (seeded) |
|------|----------------|
| Question budget | Max **2** Q per turn (Docs/26-style) |
| Timebox bias | Prefer thin slice; no `APPROVE` needed to close a *harness* slice |
| Evidence bar | DESKTOP / Saved evidence or explicit Lead accept of prior pack |
| Stills / AD | AD or Lead waive for shot accept/reject — do not self-approve |
| Next **product** track | Lead-named or Taste Gate interview — do not invent |
| Next **harness** track | Agent picks and proceeds. No gate, no ask |
| Harness / code / architecture | **Agent-owned.** Decide, then log in [AGENT_DECISIONS.md](../decisions/AGENT_DECISIONS.md). Do not raise a Taste Gate for these |
| Test bar | Human-owned and unchanged: what "done" means, rubrics, verify command, ship/no-ship, beat acceptance |
| Isolation / permissions | Human-owned Steer: isolation, web reach, permission posture |

---

## 3. Locked decisions (rolling)

| Date | Phrase / source | Outcome |
|------|-----------------|--------|
| 2026-10-15 | Lead, attribute interview rounds 1–13 | **Interview complete.** Picks are in [`Docs/context/ATTRIBUTE_ZONE_INTERVIEW.md`](../../Docs/context/ATTRIBUTE_ZONE_INTERVIEW.md) and scribed into the virtue bible. A mark is a visible interaction. Armor is for one encounter. A paradox runs both poles at once. |
| 2026-10-15 | Lead, chat, scribe | **Attribute and zone lock.** Rules in [`Docs/VIRTUE_ATTRIBUTE_BIBLE.md`](../../Docs/VIRTUE_ATTRIBUTE_BIBLE.md). Poles have runes. A paradox mark occupies one axis. Armor is interaction. The second forest opens after the camp, then the river, then the marsh. Unnamed beats stay unnamed. The bed rune stays removed. |
| 2026-10-11 | Lead, chat, after walking `L_SizeTest` | **Open cabin greybox.** The size-test home stays the block plan in `Docs/level/L_SizeTest_ROOM_PLAN.md`: 17.5 by 17 m, a 4 m porch, the great room open to the kitchen, bedrooms on the north. Preferred over the equal-box cottage. Block meshes stay the layout test. The 9 by 11 m card in `Docs/art/SCALE.md` stays the art lock until a cottage sheet is kept. |
| 2026-10-11 | Size-test next, chat | **Sittings in order.** Facing and the garden sheet, then a walkable greybox interior, then Space on the existing jump and a greybox shoulder sphere. A verify script between sittings. The cottage sheet, texture off, stays the next art file. |
| 2026-10-11 | Lead, chat | **Authorship.** A new character or asset is designed by the developer and written into context before a picture. Generate that design from scratch. `VisionBoard/KeyArt/homestead_dusk_baseline.jpg` is a fit check after that design exists. It is not the design source, and an older asset is not either. A smooth blob fails. A crystal-cut outline fails. Meters stay in `Docs/art/SCALE.md`. |
| 2026-10-01 | `TG-ZONE-VOCABULARY` 4/4 (2 rounds) | **Env-art prototype: `spirit` is first**, and the greybox **authors the see-through gap** in real topology (four posts + lintel, ~200 tris) — a proportion metric cannot satisfy spirit's signature, which was the reason to ask. Correct the existing `SM_Shrine_Homestead` / `SM_Shrine_Return` assemblies **in place**; do not author rival shrines beside them. **No `Content/` promote** — drafts only per Docs/20. |
| 2026-10-01 | `TG-ZONE-VOCABULARY` 2/2 | **Env-art lock LIFTED**, scoped to one greybox prototype. `PHASE_BOARD` Current phase = "harness idle; env-art prototype is the live ball"; the 2026-09-27 lock is superseded, not deleted. **The 7 mechanic families ARE the zone-type vocabulary.** `EBiomeType` (Desert/Forest/Marsh/Canyon) drops to terrain dressing + weather and leaves the art vocabulary; `EPlanetoidAlignment` is not a zone type. Neither C++ enum is deleted. Art bible §8 keys off family. |
| 2026-10-01 | `TG-GRAYBOX-SILHOUETTE` 2/2 | **Silhouette distinctness is mechanical, not polish.** Seven locked per-family silhouettes (gather / nurture_tame / heal / spirit / stealth / build_place / combat) — art bible §8 gains the table. **Traversal is the spine**: no silhouette of its own, inherits neighbouring material, excluded from the assertion. Hub volumes carry `family: build_place`; the cabin is that family's signature landmark, **not** an eighth family. |
| 2026-09-19 | `APPROVE TP-E` | Docs/29 Taste Profiler CLOSED; profile + skills stay live |
| 2026-09-19 | `APPROVE TP-D` | Docs/29 prove accepted; next product track still TBD (no invent) |
| 2026-09-19 | `APPROVE TG-E` | Docs/28 Taste Gates CLOSED; skill stays live |
| 2026-09-19 | `APPROVE NF2-E` | Docs/27 Night Feel Build CLOSED |
| 2026-09-19 | `APPROVE NF-A` | Docs/26 Night Feel CLOSED |
| 2026-09-16 | P2 art bible LOCKED | Tone: warm / handmade / hopeful |
| 2026-10-01 | Ownership reset (Lead decision, not an `APPROVE` stamp) | Taste = art + mechanics only. Architecture, code design and harness refactor moved to the agent, which records them in [AGENT_DECISIONS.md](../decisions/AGENT_DECISIONS.md). **Test** and isolation/permissions unchanged — still human. Prior `APPROVE *` stamps on harness/architecture work are history, not live gates |

*(Keep last ~10; older rows may archive to SESSION_SUMMARY.)*

---

## 4. Open gaps

| Id | Fork | Handoff |
|----|------|---------|
| — | Next **product** Docs track TBD | Use Taste Gate / Lead name — see TP-D prove when active |

The next **harness** Docs track is not a gap. The agent picks it.

---

## 5. Do-not

**Art and mechanics (human taste — the agent must not invent these):**

- Photoreal; grimdark; sci-fi; cutesy-infantile (art bible)
- Smooth blobs and crystal-cut outlines, scored only after a developer design exists (2026-10-11)
- Replacing the size-test cabin with the equal-box 9 by 11 m or 13 by 16 m plans (2026-10-11)
- Designing a new character or asset from the measure or from a previous asset
- Sixth shot / expand shot list without Lead
- Deep combat systems (placeholder only)
- Invent next Docs product track while PHASE_BOARD says TBD
- Mesh Terrain replace of VS_MVP Landscape without gate
- Self-approve a still, a beat, or a mechanic

**Process (unchanged):**

- Auto-promote session candidates; Cursor Memories as canon
- Resurrect WAVE F `Start-AllAgents*`
- Dual Epic MCP

**The agent now owns these — do not gate them, but do not do them silently:**

- Module boundaries, directory map, shared utils, new skills, harness refactoring,
  which metric to optimize. Each needs a decision-log entry, not a human approval.
  A decision made in place of a gate that is *not* written down is the failure this
  reset could produce.
