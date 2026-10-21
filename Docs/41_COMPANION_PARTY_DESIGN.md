# 41 - Companion party design

**Status:** APPROVED by Lead (Luke Thompson), 2026-10-20 ET; the build hold was lifted the same day. Built in #319 (`1e9b0e00`): party flags, outing clears, night teleport skip, follow leash. Invite hookup in progress. Play-confirm pending.
**Origin:** Cursor plan `C:\Users\User\.cursor\plans\companion_party_research_589ba261.plan.md` ("Companion party design"), scribed here as the one owner.
**Picks:** companion interview, 2026-10-20: `1A 2A 3A 4A 5A 6A 7A 8A` (all recommended).
**When to use:** Before any work on partner or child company, the party flags, their save fields, or the night family teleports.

Mode: solo. State: decide. Transition: Concept -> Greybox.

This doc is the owner of the companion party design. Do not copy it into the virtue bible, the canon map, or the vision board. The opening tutorial stays the next build ([Docs/context/PRINCIPLE_FIT_LOCK.md](context/PRINCIPLE_FIT_LOCK.md) picks 1 and 9).

## 1. Scope in one paragraph

An optional, post-rescue day party. You keep one possessed pawn. Partner and child are NPCs who can come with you on day gather and day travel only, as follow presence. Every test (stroke, night, rescue, cave) stays solo. The save stores who is home versus out, not positions. Night teleports skip anyone still out. No DO_NOT row changes.

## 2. What the picks decide

- **1A.** You keep the one pawn. Partner and child are NPCs. No second controller.
- **2A.** This design applies after the opening tutorial is playable. The tutorial stays solo after the door.
- **3A.** Solo through the rescue. After the loved one is home, day trips are opt-in. The child never enters the cave. The partner never re-enters that camp.
- **4A.** Spirit nights stay solo. Companions are home and asleep. The bed is still the only form change.
- **5A.** Nothing about pass or fail. A companion may change only what you see.
- **6A.** Solo on every test. Opt-in company only on day gather and day travel. Stroke, night, rescue, and the cave stay solo.
- **7A.** One solo encounter. The other three setups are that encounter plus a presence flag. No separate wind-up, point, or yield.
- **8A.** A bonk sends you home and ends the trip. They are home when you arrive. The save stores who is home versus out, not positions. A missing flag is solo.

5A's examples (wind-up, extra point, shove aimed at where they stand) are a ceiling for a stroke they are present at. 6A says they are not present at a stroke. This design does not use that ceiling. The only assist is follow presence on day gather and day travel.

## 3. Party record

Lives on `UHomeWorldFamilySubsystem` ([Source/HomeWorld/HomeWorldFamilySubsystem.h](../Source/HomeWorld/HomeWorldFamilySubsystem.h)), beside `RoleBySpawnIndex`. Roles stay roles. The record is two flags, default false:

- `bPartnerOut`
- `bChildOut`

The four setups are derived from the two flags, not stored:

| Setup | `bPartnerOut` | `bChildOut` |
|---|---|---|
| Solo | false | false |
| Partner | true | false |
| Child | false | true |
| All three | true | true |

### Invite rules

Invite sets a flag true only when every rule passes. A refused invite leaves the flags as they were.

- **Only after the rescue.** The rescue is done and the loved one is home. Until then both flags stay false. [HomeWorldOpeningReveal.h](../Source/HomeWorld/HomeWorldOpeningReveal.h) keeps the door, kettle, and room beats; those beats do not set Out.
- **By day, in body form.** Night, dusk-into-defend, and spirit form refuse the invite.
- **Never the child into the cave. Never the partner into the pine camp.** The child flag cannot be set for the cave; the partner flag cannot be set for the camp.
- A stroke, the rescue, and the cave are not invites. They are absences (section 5).

Clearing a flag is the trip end for that person. Both clear is solo. Clear does not write a position.

## 4. Allowed assist: follow presence only

- **Who:** an unpossessed `AHomeWorldOpeningWalker` ([HomeWorldOpeningWalker.h](../Source/HomeWorld/HomeWorldOpeningWalker.h)), the class the opening already uses. `WalkToward` feeds that pawn's movement. No `Possess`, no second `PlayerController`, no new player movement stack.
- **Driver:** not `AHomeWorldOpeningReveal` (its follow ends with the tutorial beat). The owner is the empty `AHomeWorldAIController` ([HomeWorldAIController.h](../Source/HomeWorld/HomeWorldAIController.h)), used only as the follow driver for a pawn already flagged Out. No Behavior Tree and no State Tree.
- **Where:** day gather and day travel, after the rescue, while the flag is Out.
- **How it reads:** they walk to a point one body-length behind you and stop. Starting gap is the opening's `FollowGapCm` (**160 cm**). They do not block the gather use. They do not add a `RES_*`, change gather time, carry a herb, hold the extra point, spend a bonk try, draw, or finish an ease. **No stroke or ease effect.**
- **Camera:** the locked orbit stays on the possessed player. No party framing.
- **Numbers:** wind-up, extra point, yield, and bonk tries stay the solo encounter (7A). Presence does not read them.

## 5. Per-activity absences

Company means the flag is Out and the walker is on the leash. Absent means the flag is false and the walker is at the home anchor for that role. The home anchor is the level's existing authored point for that person (bed, kettle, room, garden, as the beat already placed them). This design adds no coordinates and no saved transforms.

| Activity | Company | Rule |
|---|---|---|
| Homestead | home | They live here. Out is not a hub mode. Inviting happens at home; the leash starts when you leave on a day trip. |
| Opening tutorial | none | Scripted walkers only. Flags stay false. |
| Before the rescue | none | Both absent everywhere off the homestead, including the field. |
| Day gather and day travel, after the rescue | **opt-in** | The only opt-in: field gather and the walk between homestead and field. River, marsh, and lair are not this travel; they stay solo until a later lock names them. |
| Stroke (ease, generosity give, roost climb) | absent | Entering the stroke volume clears whoever is Out and sends them to the home anchor. The stroke runs solo. You are not blocked. |
| Pine camp, after the rescue | absent | The partner never re-enters. The child is not given camp company either; camp is not gather or travel. |
| Night, spirit stealth, rescue | absent | Both absent and asleep before the bed grants the form. The outing ends at dusk or at the bed, whichever comes first. Then the existing night runs solo. |
| Cave | absent | The child never enters. The cave is not day travel under 6A, so the partner is not invited either. |
| Bonk | ends trip | Same clear: both flags false, both walkers at home anchors, then the existing player glide home. They do not ride the glide. |

Clears that end an outing: stroke volume, camp, night, rescue, cave, dusk, bed, bonk.

## 6. Save flags

On `UHomeWorldSaveGame` ([HomeWorldSaveGame.h](../Source/HomeWorld/HomeWorldSaveGame.h)), next to `SavedRoleBySpawnIndex`:

- `bSavedPartnerOut`, default false
- `bSavedChildOut`, default false

`UHomeWorldFamilySubsystem` writes and reads them in `SerializeToSaveGame` / `DeserializeFromSaveGame`. No new slot. No position, rotation, or velocity fields.

Load rules, in order:

1. A missing field, or an old save, stays false. That is solo.
2. If the rescue is not complete, force both false.
3. If the loaded phase is night, or the player is in spirit form, force both false and place both at home anchors.
4. Otherwise restore the flags. Out means "with you" at load, beside you, not at a saved field coordinate (8A).

## 7. Night family-teleport exception

Today `TryMoveFamilyToDefendPositions` and `TryReturnFamilyFromDefendAtDawn` ([HomeWorldGameMode.cpp](../Source/HomeWorld/HomeWorldGameMode.cpp)) teleport every actor tagged `Family`. Under 4A the normal night has no one Out, because dusk or the bed already cleared the flags.

Two steps, so a missed clear cannot put a day companion on a defend marker:

1. **Clear first.** Before the defend teleport, end the outing: clear both flags and place those walkers on home anchors.
2. **Skip as backstop.** Inside both teleports, skip a `Family` actor the record still marks Out. Do not `SetActorLocation` them. Still set `bFamilyMovedToDefendThisNight` and `bFamilyReturnedThisDawn` so the once-guards do not retry. Log the skip with the actor name. If every family actor is skipped, log that none moved.

The skip is the backstop. The clear is the path 4A actually takes.

## 8. DO_NOT rows this design amends

**None.**

- Co-op drop-in on the hub stays forbidden. 1A does not add a second player.
- "Second CharacterMovement / parallel PlayerController" stays forbidden. Followers are unpossessed opening walkers, which already exist. This design does not possess them and adds no player movement stack.
- The camera bible's "other player" lines stay unused. This design does not delete them.
- One stroke, strict rescue, bed-only spirit form, and the five gates stay as written. Presence fails none of them because it is absent from every test.

## 9. Build order (only after the tutorial is playable and the Lead asks to build)

1. Flags on the family subsystem and the save, with the load forces above.
2. Outing clear on bonk, dusk, bed, stroke volume, camp, and cave.
3. Defend and dawn teleports skip anyone still Out.
4. Leash on the opening walker for day gather and day travel only.

## 10. Future-proofing and out of scope

- No State Tree, no squad command, no companion inventory, and no per-setup map.
- River, marsh, and lair travel stay solo until a later lock names them.
- 5A's assist ceiling (wind-up, extra point, shove) is recorded in section 2 but unused, because 6A keeps companions out of every stroke.
- Setups are derived from two flags over one solo encounter (7A), so no setup has its own tuning, map, or saved transform.
