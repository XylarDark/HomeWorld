# Handoff: playtest, glider and the dawn glide

Written 2026-10-22 at the end of a playtest session that also carried source changes. The modularity pass is a separate handoff: [`SESSION_HANDOFF_MODULARITY.md`](SESSION_HANDOFF_MODULARITY.md). Another agent owns that work, so a playtest chat must not edit `Source/` or `Content/Python/`.

## Where the playtest stands

The order is the Now table in `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`. Do not restate it here; read the Now line.

- 22 Oct Night: in.
- 23 Oct Heal: in. One press starts one wisp; three presses healed three.
- 26 Oct `glider`: **open**. The craft at the armory table is the blocker.
- 27/29 Oct glide start and field landing: the `dawnglide` stop is built and set up, but the launch has not been played by a human yet. The meadow and the landing are not placed, so a glide that ends with no destination is expected.

## Last known session state

- Editor was running (PID 26300 at handoff), MCP answering on 55557.
- PIE was live at the `dawnglide` stop: glider crafted from the dawn chest, player at `V(X=1430.60, Y=60.86, Z=45100.00)`, 180 cm from `GP_GlideStart`, note "the launch is yours". **No launch was logged** before the session was interrupted.
- The other agent may have built since; a build taskkills the editor, so treat the above as last known, not current.

## Verified today, with the evidence

| Thing | Evidence |
|---|---|
| Pond step no longer strands the body in the zipline prop | `playtest_ff: 8 fish` (was `8 fish failed`) |
| The fast-forward reaches the armory stop | `playtest_ff: ready for glider ... dist 220` |
| Wall rule stops interaction through walls and windows | Lead: kettle refused through both the wall and the window. Pass. |
| Kettle sits on the 100 cm counter | `scene_placement: saved top 45000.0` after the seat was derived from `cabin_shell.BOXES` |
| Candle lights applied to the map | same save line; preset 1900 K, 900/700 cd, 2000 cm radius |

## Open, and not to be assumed

- **D1 cottage light is still too bright** at the candle preset. Lead has called it too bright twice at two different presets, so do not halve it again on instinct.
- **D2 armory table has no hover and no press.** Owned by the modularity handoff. The glider row cannot pass until it does.
- **The bonk rewrite is unverified by a human.** It is now one rise-cross-land flight. The old code teleported and then re-triggered in a loop; the log showed `opening_bonk: thrown back to the island` eight times in three seconds. Expected now: exactly one `opening_bonk: return to ...` then `opening_bonk: landed`.
- **The beat-stop gaze rule is unverified.** Every stop now aims at its target's bounds instead of a level gaze. The armory table hover is its test.

## Running a stop

1. End PIE if it is running. `Content/Python/d19_end_pie.py` writes the result to `Saved/d19_probe.txt`; read `pie=False` there to confirm.
2. The beat word is the first line of `Saved/opening_beat.txt`. Current value: `dawnglide`. Legal words are the `hw.Playtest.FastForward` row in `Docs/COMMANDS_AND_LOG_TAGS.md`.
3. Launch the editor with `Content/Python/start_editor.py --timeout 600`, then push `start_opening_beat.py` through MCP. Running `scene_placement.py` directly does nothing; its entry point is `apply_homestead_scene.py`.

Expected log for `dawnglide`:

```
playtest_ff: 8 fish
opening_glider: crafted (wood 0, silk 0, metal 0)
playtest_ff: ready for dawnglide - the launch is yours
playtest_ff: you are at V(...), target GP_GlideStart, dist 180
```

`8 fish failed` aborts the whole sequence and strands the player at the pond. That is the failure to watch for, not a cosmetic miss.

## Coordination

- Another agent owns `Source/HomeWorld/HomeWorldCharacter.cpp/.h`, `Content/Python/scene_placement.py`, and the shared-systems rows S1-S7 in `Docs/context/PLAY_TASKS.md`. Do not edit those files from a playtest chat.
- Any build moves the binary. Results recorded before a build must be re-checked before they count as passing.
- Nothing is committed: the map, seven `MI_Greybox_*` material instances (dirtied by the placer's paint step), the two Python placers, `HomeWorldCharacter.cpp/.h`, `HomeWorldOpeningReveal.cpp`, the HUD and two test files, several docs, and untracked `Content/Python/start_opening_beat.py`.
- Never `git reset --hard`, and do not commit a `.uasset` or `.umap` without the Lead's yes.
- `.\Tools\Safe-Build.ps1` only, and it closes the editor. Ask when the editor is open.

## What a pass needs

For `dawnglide`: the launch happens with the glider built, and the flight travels. A landing is not expected yet.

For the bonk: fall off the pad, see one continuous flight home, stay landed, and the log shows one `return to` and one `landed`.

For the glider row: the craft at the armory table and the descent refusing before it. Both blocked on D2 as of this handoff.
