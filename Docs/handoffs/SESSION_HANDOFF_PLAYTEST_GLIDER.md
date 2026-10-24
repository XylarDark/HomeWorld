# Handoff: playtest queue, glider row

Written 2026-10-24. Start the next chat from this file and the newest block in `docs/SESSION_NOW.md`. The pass lives in `Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md`: read the Now line, then `## The glider`. Do not open vision, the asset queue, or either critical path. Do not copy the Now table into this file.

Play one pass. Fill its result. Stop.

## This pass

The next dated row is 26 Oct, `glider`. `Saved/opening_beat.txt` is already `glider`. Legal words are the `hw.Playtest.FastForward` row in `Docs/COMMANDS_AND_LOG_TAGS.md`. A word that `list` does not print is not a new command.

`hw.Playtest.FastForward glider` runs the earlier opening beats, then stops at the stocked armory before the craft. The note in `HomeWorldPlaytestBeats.cpp` is `E at the armory: craft the glider`, 220 cm from the actor tagged `NODE_ARMOR_TABLE`.

Expected log:

```
playtest_ff: ready for glider - E at the armory: craft the glider
```

plus the stand line at about 220 cm. `playtest_ff: 8 fish failed` aborts the sequence at the pond and never reaches the armory.

Lead plays the hover and the E. Write the three result fields in `## The glider`. A green host test does not fill that table. `HomeWorld.Opening.GliderCraft` already passed on 2026-10-21 and is not this pass.

## Machine, checked 2026-10-24

- `main` at `7c6c9201`, clean, one commit ahead of `origin/main`. That commit is docs only. Do not push.
- No other worktree. No `UnrealEditor` process.
- Desktop `Binaries/Win64/UnrealEditor-HomeWorld.dll` is still 2026-10-23 13:58 (3,463,680 bytes). It does not contain `f68332d9` (exact fast-forward words, 18:40), `efeb6754` / `14b087be` / `2881d283` (hover and fish registry, 20:08–21:01), or `b5e90720` (bonk lands on the nearest pad edge, 23:41).
- A spare-worktree build of `584e98e3` already passed: Build.bat Succeeded, 221 tests, 217 passed, 4 warnings, 0 failed. That worktree is gone, so this desktop DLL is not that binary. `7c6c9201` adds no game code on top of `584e98e3`.

Build once with `.\Tools\Safe-Build.ps1` from the repo root before PIE, so the play is of current main. The editor is closed, so the script's editor close has nothing to kill. If an editor is open when the next chat starts, stop and hand the close to Lead. One build. Do not build again in the same reply.

## Open beside this pass

- **Armory hover and press are not play-confirmed.** The aim frame is screen center (`GetOpeningLookCenterNdcY` returns 0, `e7dce3aa`). That line is inside the 13:58 DLL. The hover scan after it is not. The glider row is the human check: the frame on the table, then E. The same on-screen fail twice stops the reply. Say what was not in the binary.
- **Cottage light is still too bright** at the candle preset. Lead has called it too bright twice. Do not halve it. It is not this pass.
- **The bonk landing in `b5e90720` is not play-confirmed.** The 2026-10-18 bonk pass is an older flight. Fast-forward runs that flight on the way to the armory. One `opening_bonk: return to` and one `opening_bonk: landed` is the log to expect. A loop of throws is the old failure.
- **Dawn glide is a later row.** The 2026-10-22 session had a crafted glider 180 cm from `GP_GlideStart` and no human launch. That PIE is gone. Do not play `dawnglide` in this chat.

## Do not

- Do not edit `Source/` or `Content/Python/` from this playtest chat.
- Do not commit a `.uasset` or `.umap`. Never `git reset --hard`.
- Do not replay Night, Heal, or any passed midday row.
- The meadow, the nodes, and the clearing are not on the map. Delivery, day camp, and the later stops wait.
