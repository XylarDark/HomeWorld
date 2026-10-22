# Handoff: modularity pass on opening interactions

Written 2026-10-22 at the end of a playtest session. The job is to collapse the opening interaction and placement code into shared systems, so a new prop does not re-decide what "in reach", "looked at", and "blocked by a wall" mean.

## Why this pass exists

Adding one prop — the armory table — stalled a whole playtest. The table carries its tag, the candidate filter accepts it, and it still gives no hover and no press. Nothing about the prop is exotic; the interaction code simply has several opinions about when a prop is interactable, and they disagree.

The same shape showed up four times in one evening on the bonk: a teleport, then a launch, then a re-trigger loop, then two copies of the same math. It ended as one `BeginBonkReturn(Target)` flight. That is the pattern to repeat here.

## Start here

1. This file.
2. `Docs/context/PLAY_TASKS.md`, section **Shared systems**. Rows S1-S7 carry the evidence counts and the definition of done. Do not restate them anywhere else.
3. `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`, section **The glider**. That row is what exposed the defect.

## Live state at handoff

- Build green at the last run; **source changed 2026-10-22 and has not been rebuilt or tested.** The editor is open, PIE ended at 18:14. `Saved/opening_beat.txt` says `dawnglide` (the Lead's test), not `glider`; restore `glider` before the armory verification.
- `L_SizeTest.umap` saved with candle-warm lights (1900 K, 900/700 cd, 2000 cm radius, 25 cm source) and the kettle reseated on the 100 cm counter.
- Nothing is committed.

## Two live defects

**D1 — the cottage light is still too bright.** Candle preset at 1900 K, 900/700 cd, 2000 cm radius. Lead has now called it too bright twice (at 2900 K/2200 cd and again at 1900 K/900 cd). Do not halve it a third time on instinct; either find the exposure the preset is fighting or set the level by eye with the Lead watching.

**D2 — the armory table has no hover and no press.** Evidence gathered today, in order:

- The stop finds the actor by tag, so `NODE_ARMOR_TABLE` is present on `SM_Size_ArmorTable`.
- `ActorHasInteractableComponent` asks `HomeWorldInteract::TrySpecFor`, which reads the beat-node tag table, so the table enters `FindOpeningProximityTarget`'s candidate loop.
- No `opening_los:` line appeared in the log. That probe logs only on a refusal, so the wall gate did not refuse the table.
- No `opening_station: armor table` line appeared either, and the Lead never pressed E — the complaint is the missing hover.
- `ResolveOpeningAim` is nothing but `FindOpeningProximityTarget()`, so hover and press share one path.
- The Lead tested it on 2026-10-22: the hover appears only when aiming **above** the table, not at it. That confirms the look frame, not the wall gate and not the tag.
- Why: the frame was pitch-compensated and sat at NDC −0.5 (the top 10-40% of the screen). At the armory stop the gaze rule pitches to −20.6°, which slides the frame off the top of the screen; the table center (45 cm above the floor) lands at NDC −0.07, about 0.42 below the frame. Looking up drops the 4 m camera boom and brings it in.
- Picked by the Lead on 2026-10-22: the frame is **screen center** (NDC 0, half-extent 0.3), with **no pitch slide**. `GetOpeningLookCenterNdcY()` returns 0 and the HUD fallback is 0. The stop keeps aiming at the target's bounds. This is in source, **not yet built or verified**.

Confirmed 2026-10-22: the look test rejects a low prop at the stop. The wall gate and the tag are not the cause.

## Where the code is

| Area | File |
|---|---|
| Five verb paths that each re-check reach, look, and wall | `Source/HomeWorld/HomeWorldCharacter.cpp`: `FindOpeningProximityTarget`, `FindInteractTargetInCone`, `TryOpeningBedInFront`, `TryOpeningHotSpringHealInFront`, `TryOpeningFish` |
| Wall test and its temporary probe | same file: `HasOpeningLineOfSight`, log tag `opening_los` |
| Candidate admission | same file: `ActorHasInteractableComponent` (asks `HomeWorldInteract::TrySpecFor`) |
| Interaction spec | same file: `HomeWorldInteract::FSpec`, `TrySpecFor` |
| Actor discovery | same file: `FindOpeningNamed`, `FindOpeningTaggedActor` |
| Beat stops and their placement | same file: `DebugFastForwardOpening`, `PlaceForOpeningPlaytest*` |
| Shared return flight (done) | same file: `BeginBonkReturn`, `TickBonkReturn` |
| Counter and kettle constants | `Source/HomeWorld/HomeWorldOpeningReveal.cpp` |
| Placement rules, tags, light preset | `Content/Python/scene_placement.py`: `seat_props`, `place_opening_reveal`, the light loop |
| Shell box table and counter index | `Content/Python/cabin_shell.py`: `BOXES`, `COUNTER_BOX_INDEX` |

## The placement script has the same problem

The Lead's words: the placer should understand how the systems that cause interactions to gain or lose function, not just where things stand.

Today is the proof. The counter grew from 90 to 100 cm. `cabin_shell.BOXES` knew the new height; `seat_props` still seated the kettle at `top + 90.0`. The kettle sank 10 cm, a clip check failed, the placer printed `not saved`, and the candle lights never reached the map. Two hand fixes followed (derive the seat from the box height; reseat). That is a placement model that does not know the interaction it is placing.

Treat S5 as this: one constants source for height, standoff, and tag names, read by the shell, the placer, and the reveal. Then a height change moves the things that depend on it in the same run.

## Interaction contract (S1/S2)

A prop carries attributes; it does not get a verb path. The first slice is in source:

- `HomeWorldInteract::FSpec` at the top of `HomeWorldCharacter.cpp`: `Node`, `bBeatNode`, `ReachCm` (280 default), `bLook`, `bWall`, `bHover`.
- `HomeWorldInteract::TrySpecFor(Actor, Spec)` derives the spec from `HomeWorldT0BeatNodes::TagsPerNode()`. A new beat prop needs its node tag, nothing else.
- `ActorHasInteractableComponent` asks `TrySpecFor`; it no longer carries a separate beat-tag branch.
- `FindInteractTargetInCone` walks every actor and asks the gate. Its static `InteractTags` list is gone; the table, the bed, and every future tagged prop are candidates without editing the cone.

Still S1/S2:

1. `FindOpeningProximityTarget` still has per-prop branches (`bHerb`, `bBed`, `bNightWisp`, `bDelivery`). Move their reach/look differences into `FSpec` overrides and delete the branches.
2. `TryOpeningBedInFront`, `TryOpeningHotSpringHealInFront`, and `TryOpeningFish` still own their own reach and line-of-sight terms. Give each a spec (`ReachCm` 280 / 600 / bounds+200, `bLook=false` where the path has no look) and route them through one `ResolveOpeningTarget` call.
3. Add the registry for `FindOpeningNamed`/`FindOpeningTaggedActor`: build on `BeginPlay`, invalidate on tag or visibility change, no per-frame world scan.
4. The verbs dispatch on `Spec.Node`; they keep only the action.

## Done when

- S1-S3 and S5-S7 are closed by their own criteria in `Docs/context/PLAY_TASKS.md`, not by a new call site.
- The interaction spec is the only place a prop's reach, look, wall, and hover are decided.
- The armory table hovers at the beat stop and crafts on E, and the next prop added needs data, not a new verb path.
- `.\Tools\RunTests.ps1` passes, and `.\Tools\RunTests.ps1 -QuestCheck` exits 0 if the stops changed.
- The cottage light is signed off by eye, not by a number alone.

## Locks

- Never `git reset --hard`. Do not revert uncommitted work you did not write.
- Do not commit any `.uasset` or `.umap` without the Lead's yes. The map and seven `MI_Greybox_*` material instances are dirty from `apply_homestead_scene.py`'s paint step.
- `.\Tools\Safe-Build.ps1` only, from the repo root. It taskkills `UnrealEditor`; ask first when the editor is open.
- Editor MCP is on port 55557. Entry points that work: `Content/Python/start_editor.py` to launch, `apply_homestead_scene.py` to place and save (`scene_placement.py` defines `run()` but has no module entry, so running it directly does nothing), `start_opening_beat.py` to start PIE and fire the beat named in `Saved/opening_beat.txt`.
- The `opening_los` log is a temporary probe. Do not ship it; put it behind a cvar or delete it with S7.

## Verify the stop

`Saved/opening_beat.txt` holds `glider`. Expected log at the end of the run:

```
playtest_ff: 8 fish
playtest_ff: ready for glider - E at the armory: craft the glider
playtest_ff: you are at V(...), target SM_Size_ArmorTable, dist 220
```

A failed pond step aborts the whole fast-forward, so `8 fish` (not `8 fish failed`) is what proves the run reached the armory.

Bonk, if touched: falling off the pad must log exactly one `opening_bonk: return to ...` followed by `opening_bonk: landed`, never a repeat.
