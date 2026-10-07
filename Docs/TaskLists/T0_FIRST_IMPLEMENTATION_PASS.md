# T0 implementation pass — first blockout + mechanics wiring

Each item is two phases: a **research phase** (what the industry does, which
default we pick) and an **implementation phase** (the build work). Style choices
already argued in the Lead conversation are recorded as "decided"; nothing is
implemented against an unrecorded default.

Rules:

- Props, characters, and trigger radii stay human-scale; the **world** is ×6.
- Nothing is declared done until its `HomeWorld.T0.*` / `HomeWorld.Transit.*`
  automation and its `Lib/02_Zones/*/*.json` spec agree.
- A research default picked here must be written into the relevant spec before
  code is written against it.

---

## 1. Spirit-stealth read — blue ring, Shadowlands palette

**Research defaults considered**
- Metal Gear vision cones: strong readability, but a cone needs an AI aim
  policy and a HUD; we don't have either.
- Arkane hidden-eye meter: reads well in first person; we are third-person
  follow with a big field.
- **WoW Shadowlands detection: spirit-blue pools that light up where you
  *stand*, not a beam from the source.** DECIDED (Lead 2026-10-07).

**Implementation**
- Each spirit-blue light source (`SM_Camp_Fire` blue pool, guard's torch pool)
  paints a ground ring: soft blue fill, hard blue border (Lead, 2026-10-07).
- Ring alpha rises into the player when inside it. Outside the ring: nothing.
- No HUD, no cone mesh, no meter. The ring *is* the HUD.
- A torch ring travels with the guard; the fire ring is fixed 4 m.
- Done-when: standing inside either ring reads as "seen" against the locked
  Shadowlands palette; `UHomeWorldSpiritStealthComponent::EvaluateSpiritTouch`
  still emits the documented refusal/verdict logs, no behaviour change to M14.

## 2. Bull threat & tame — real-animal, no turn at speed

**Industry defaults considered**
- Minecraft feeding: too simple, no threat.
- Pokémon Ranger timing minigames: fun but a QTE, not a chase.
- Red Dead horse taming: raise a bar along a straight line from ahead; steady
  hand. Closest, but it's a meter, not a world verb.
- **Herb-in-hand approach, stand-still freeze, movement compounds threat,
  meter full → quick charge → boot home.** DECIDED (Lead 2026-10-07).

**Implementation**
- Bull actor comes out with a stance-readable threat stance + a walk-up by the
  player carrying `RES_HERB`.
- While a herb is held the boot-charge is suppressed; any motion sample from
  the player raises threat; a still sample decays it.
- Tamed: bull rideable, follows the 1 barn / 1 bull route until a player
  uses it, then the rune stone transports rider + bull to homestead as a pet.
- Bull turning: turn rate inverse to travel speed — near-zero at 3× sprint,
  full at walk. "A real animal." DECIDED.
- No combat, no death, no flee-to-edge.

## 3. Wound wisps — healed wisps become follower companions

**Defaults considered**
- Soft-emissive in place: communicates state, gives nothing.
- **Ni No Kuni style: the healed wisp leaves the wound and follows the player.**
  DECIDED (Lead 2026-10-07). Companions ring the player at a small offset so
  all three can be present.
- QTE bar before the swap: not used.

**Implementation**
- Wound wisps are actors placed in the field (3 total). Interact spends 1×
  `RES_HERB` / `RES_SEED` in spirit form at night; on success the wisp re-homes
  to a player-follower slot and stops counting as a wound case.
- Reward for all three: the spirit flight buff for the night slot (this is the
  Lead-recorded "given to the spirit wisps" loop).

## 4. Guest-beat: camp by day — boot home

**Defaults considered**
- "Caught!" → caught-screen → retry home.
- "Walk home": too forgiving, the day camp's whole job is to eject.
- **Eject player to homestead as an instant boot, companion kidnapped.**
  DECIDED. `EJECT_TRIGGER_GUARD_WAKES` (6 m sphere at the guard's post) is the
  trigger; M8/M10 cover the reverse paths. Implementation note only: player is
  booted, not slain, so there is no "death" string.

## 5. Night flight — disperse dung+wisp over herb sites

**Defaults considered**
- Area-of-effect paint on mouse: fine for a cursor game, not ours.
- **Trailing swath along the glide path, same way Farming Simulator's seeder
  works.** DECIDED — a constant-rate deposit along the 30-second descent's
  ground track, landing only on soil / herb site; empty on water, cliff, or
  out-of-bounds. Cost is the carried `RES_SEED`+wisp pair.

**Implementation**
- Route: the player spirit-flies the night descent; the soil call happens
  automatically along the ground-track. The trail is the feedback.
- Morning: herb sites that were inside the swath are the new gatherable; the
  rest are the old positions. (The old "morning pile per dung" is superseded —
  route updated.)

## 6. Field blockout — 420×420 m, four edges, variable scatter

**Defaults considered**
- Dense fight-game style cover everywhere: hides the guiding edges.
- **Empty meadow with four distinct edges; plants, dung, herds, 4 beast pads
  distributed with the Lead's variable-spacing rule (common ~30 m, duals at
  25% density, triples at 5%).** Locked.

**Implementation**
- In Blender: island-top replaced by the ×6 meadow; four edges read as
  cliff / river / pine / pine, the two pines identical per `FIELD.json`.
- AHomeWorldCloudField stays untouched (cloud sizes already ×6).
- FIELD.json's `world_bounds_m` is already 420×420.

## 7. Camp blockout — 108 m clearing, modules from CAMP.json

**Defaults considered**
- A small tent-camp operation: the stealth scene can't breathe.
- **The guard's patrol ring interpolates around the fire with the 4/6 m ring
  visibility rule. 108 m clearing, one guard, two sleepers, the lashings
  (companion), then the portal out.** Locked.

**Implementation**
- In Blender: five modules per `CAMP.json.modules` (fire, guard stake, two
  bedrolls, lashings) are shaped from the Appendix A photo targets.
- Actor positions follow the CAMP.json offset table.
- Camp world origin stays where `CAMP.json` has it.

## 8. Camp art modules — photo-targeted placeholders

**Defaults considered**
- Photo-matched high-poly gorget: not the placeholder's job.
- **Each module is the Appendix A photo target's simple version: plane +
  implied mass + lighting read, family-correct silhouette.** Locked.

**Implementation**
- From photo → simple placeholder, in Blender, five modules. Done-when:
  `graybox_spec_reader` reports each one's silhouette matching its locked band
  at 20 m. No one-off materials — the ten masters only.

## 9. Companion / family hint (5.1)

**Defaults considered**
- Full dialogue tree: Q19 was Lead-clear: **one-line contextual hint, travels
  with you, no tree.** Locked. The companion is the actor `NODE_CAPTIVE` by
  alias, not a separate system.

**Implementation**
- Deferred until it fits the first playable-chain pass. Noted so it is not
  lost.

## 10. Prove runs — M2/M3/M4/M6/M7/skybox, and M8/M10/M11/M12/M13/M14

Not a mechanic; an evidence problem. The camp node actors are now placed, the
geometry is the only thing that stood between the six `NO_VERDICT` scripts and
a real run. Once 7 and 8 land, the 10 scripts get a Geometry to run against:
every prove row moves from `NO_VERDICT`/`BLOCKED` to a recorded result.

**Implementation**: after 7/8, run every `Content/Python/t0_m*_prove.py` in the
automated editor; record the six remaining `NO_VERDICT` rows as PASS/FAIL.

---

## 11. Whole chain — field → forest → day camp → eject → spirit → stealth →
soothe → free

Locked, pending 2, 6, 7, 8, 10. Done-when: a reviewer plays it without a guide.
