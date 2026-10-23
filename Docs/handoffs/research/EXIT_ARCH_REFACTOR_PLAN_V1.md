# EXIT ARCH_REFACTOR_PLAN_V1

Filed 2026-10-22 by Grok Bot. Prompt: Docs/handoffs/research/PROMPT_ARCH_REFACTOR_PLAN_V1.md. Source: the answer in Cursor chat "Software architecture optimization" (Ask, Grok 4.7 Extra High), copied with the message copy button to q2/arch_answer.md. The answer below is verbatim; it predates this filing and was not written to the EXIT section shape (Diagnosis / Do bites / Accept checklist), so fitness grep B is not expected to pass. Not an ACCEPTed EXIT.

---

Mode: solo · State: agent. The time cost is one new prop having to teach five owners the same fact. Finish the interaction contract already started in `HomeWorldCharacter.cpp`, then make quest facts, playtest stops, and placement read that same record.

A new opening prop today is edited in the pawn, in the interact ability’s ordered chain, in the quest-fact copy, in the fast-forward placer, and often again in Python. Those copies disagree. The armory table had its tag and still had no hover, because look, reach, and the wall test are still separate opinions. The kettle sank for the same reason: the shell knew the counter height and the seat math did not.

`AHomeWorldCharacter` is about 7,900 lines, with on the order of fifty `Try…` methods. `UHomeWorldInteractAbility::ActivateAbility` then walks two hand-ordered chains (one for `SizeTest`, one for every other level). `HomeWorldInteract::FSpec` already says a prop carries reach, look, wall, and hover. Most verbs do not use it yet.

## Do these, in this order

| Order | System | What becomes reusable | What a later prop costs |
|---|---|---|---|
| 1 | Opening interaction | One resolver. Verbs only perform the action. | A tag and a spec row |
| 2 | Quest facts | The pawn stops hand-copying booleans into the tracker | One fact id on that same row |
| 3 | Playtest fast-forward | One beat table: skip, stand distance, gaze | One row, not a new branch in `DebugFastForwardOpening` |
| 4 | Placement and lights | One constants module for height, standoff, tags, and named light presets | The shell, the placer, and the reveal move together |
| 5 | Session save | Each subsystem captures and applies its own slice | A new persisted field does not grow `UHomeWorldSaveGame` by hand |
| 6 | Automation fixture | Every beat test uses `HomeWorldTestWorld` | A new test spawns a tagged actor and calls the resolver |

Rows S1–S7 in `Docs/context/PLAY_TASKS.md` already specify 1 and 4, plus the actor registry and the centered gaze rule. That pass is the architecture change. A second framework beside it would add another opinion about “in reach.”

## 1. Interaction resolver

`FSpec` is the right boundary. It is still local to the character file, and `TrySpecFor` only fills the node id. Reach, look, wall, and hover stay at the defaults, while `FindOpeningProximityTarget` still special-cases herbs, the bed, night wisps, and delivery.

```170:181:Source/HomeWorld/HomeWorldCharacter.cpp
namespace HomeWorldInteract
{
	struct FSpec
	{
		HomeWorldT0BeatNodes::ENode Node = HomeWorldT0BeatNodes::ENode::Kettle;
		bool bBeatNode = false;
		float ReachCm = 280.f;
		bool bLook = true;
		bool bWall = true;
		bool bHover = true;
	};
```

`ActivateAbility` then ignores that spec and tries pawn methods until one returns true. The `SizeTest` chain and the default chain can drift: a verb added to one is easy to miss on the other.

That violates the two principles that actually save time here.

- **Open/closed.** A new prop should be data. Today it is a new `Try…InFront`, a new slot in both chains, and often a new branch in the proximity scan.
- **Single responsibility.** The pawn currently owns movement, camera, every verb, quest refresh, and playtest placement. The ability’s job is “commit, resolve one target, run that target’s action.”

The reusable tool is one `ResolveOpeningTarget` plus a verb registered on the spec’s node. The bed, the hot spring, and the fish stop owning their own reach and line-of-sight. Priority becomes a field on the spec, so overlap is data instead of source order. The target actor can own the action through a small interface; the pawn does not grow a method per prop.

**Dependency inversion** shows up one level up as well. `UHomeWorldHomeLoopSubsystem::TryOpeningKettleBrew` calls back into `AHomeWorldCharacter::TryBrewNodeKettleTea`. The station action should be callable by both the resolver and the home-loop subsystem. The subsystem should not know the pawn’s method list.

Smart Objects is already a candidate in `Docs/tools/GAME_TOOL_CATALOG.md`. It pays off only after this contract exists. Adopting it first would be a third definition of reach and look.

## 2. Quest facts

`RefreshOpeningQuest` copies pawn fields into `FHomeWorldOpeningQuestFacts` one boolean at a time, and it only runs when the level name contains `SizeTest`.

```3590:3609:Source/HomeWorld/HomeWorldCharacter.cpp
	FHomeWorldOpeningQuestFacts Facts;
	Facts.bSpiritClaimed = bOpeningSpiritClaimed;
	Facts.HerbsGathered = OpeningHerbsGathered;
	Facts.bHerbFromWest = bOpeningHerbFromWest;
	Facts.bHerbFromEast = bOpeningHerbFromEast;
	Facts.bKettleBrewed = bOpeningKettleBrewed;
	Facts.bDogSlow = bOpeningDogSlowLatched;
	Facts.bTracingDove = bOpeningDogDrawActive;
	Facts.bHasMixedHerb = OpeningMixedHerbs > 0;
	Facts.bBackpack = bOpeningArmorGiftGiven;
	Facts.bFishCaught = bOpeningFishCaught;
	Facts.bSlept = bOpeningNightSpirit;
	// ...
	QuestLog->SetChain(TEXT("Opening"), UHomeWorldQuestLog::BuildOpeningSteps(Facts));
```

`UHomeWorldQuestLog` is already a good, dumb tracker: it stores chains and builds steps from facts. The coupling is the copy. A new tutorial step means a new field on the pawn, a new fact, a line in `BuildOpeningSteps`, and a coverage row.

Publish facts from the verb that just succeeded. The log subscribes. The pawn stops being the quest database. The host checks you already have (`quest_preflight.py`, `quest_coverage.py`) then guard one fact list instead of a hand-maintained mirror.

The home-loop chain is closer to this already: the subsystem reports four flags and the log only formats them. Opening should follow that shape.

## 3. Playtest fast-forward

`DebugFastForwardOpening` and `PlaceForOpeningPlaytest` are a situation tool written as pawn code. Each beat hard-codes a distance. S3 exists because the 220 cm armory stop put the table under a look box that did not see it.

The catalog already says a new situation is a beat word, a skip, a place to stand, and one queue sentence. The implementation is still a C++ branch. Put that in one beat record next to the interaction spec: tag, standoff intent, gaze-from-bounds, and which earlier verbs must already have succeeded. A new dated row in the playtest queue then needs a host test against that record, not a new placement function and a one-off `t0_m*.py`.

There are about 226 Python scripts under `Content/Python/`. The catalog’s rule is to extend `apply_homestead_scene.py`, `start_opening_beat.py`, and `hw.Playtest.FastForward`. More prove scripts repeat bootstrap and placement instead of calling the beat record.

## 4. Placement and lights

S5 and S6. `cabin_shell.BOXES` is the shell’s height. `scene_placement.py` now reads `COUNTER_BOX_INDEX` when seating, after a 90 cm constant seated the kettle through a taller counter and blocked the save. Light intensity, radius, and temperature are still written inline.

One module owns height, standoff, tag names, and presets (`candle`, `lamplight`, `night`). The shell, the placer, and `HomeWorldOpeningReveal.cpp` read it. A height change then moves every dependent prop in the same run, which is what the failed kettle save cost in manual fixes.

## 5. Save, after the verbs settle

`UHomeWorldSaveGameSubsystem::CaptureNPSessionState` already walks inventory, tame, heal, and nurture, but `UHomeWorldSaveGame` is a flat list of `Saved*` fields, including `bSavedN1Nurtured` and `bSavedN2Nurtured` as separate booleans. Each new persisted thing is a property plus a capture line plus an apply line.

Give each subsystem a capture/apply pair and let the save object store slices. Inventory’s `CopySlotsTo` / `RestoreSlotsFrom` is the pattern. Opening herbs, the glider, and wisp carry are not in that snapshot yet; bolting them on as more pawn fields would repeat the quest-fact problem. Do this after the verb and fact record exists, so the slice key is the same id the quest log uses.

## 6. Tests

`HomeWorldTestWorld` exists because copied `CreateWorld` fixtures leaked and failed a later, unrelated test. Party, home-loop, form-gate, and conversion tests still construct their own worlds. One fixture, one tagged-actor spawn, one call to the resolver, is the test for every future prop. The quest coverage matrix then points at that fixture instead of a new `*Tests.cpp` per beat.

## Leave these as they are

Inventory (`TryAddResource`, `SpendResource`), time of day, the family and spirit-roster subsystems, the zone generator, and the GAS bases (`UHomeWorldGameplayAbility`, `UHomeWorldAttributeSet`) are already the right size. Glide, traversal, stealth, and stress are already components on the pawn. The bonk return flight is the local model: one `BeginBonkReturn(Target)`, and a new bonk is a call.

Splitting `HomeWorld` into more Unreal modules would not shorten the next prop. The boundary that saves time is the beat record, not a new module.
