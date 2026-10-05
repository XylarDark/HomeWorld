# Continue the cloud route in OpenCode

This is the handoff for the work in progress on 2026-10-04. Read this file, then `Docs/context/HOMEWORLD_ROUTE.md` **on main** — get it with `git show HEAD:Docs/context/HOMEWORLD_ROUTE.md`, not by reading the file. Do not start a build.

The working copy of that route file is dirty on purpose. It now holds **2** bullets, held pending a Lead ruling — the other 10 were reconciled on 2026-10-04, six committed and four dropped. Reading the file instead of `HEAD` is how the last two research EXITs inherited the 33.75 s window and the 1.5x drop as settled facts.

The 2 held bullets:

1. The dung and wisp chain — one dung plus one wisp makes one spirit fertilizer, mixed at the homestead, spread at night, one herb pile per dung in the morning. **Also carries the 260 m line, and restates `dc1b551` in longer form.**
2. The homestead-to-field window — 15 s now, 1.5x the drop, neutral glide two thirds, **33.75 s target**, a later boost. **Do not commit this bullet as written; the 33.75 s target is conditional, not a set value.**

Bullet 1 is a bundle: five of its sentences duplicate what is already on main. If it is accepted, it has to be split — one new sentence per commit, not the whole bullet.

A third bullet, "the autonomous route is driven by curiosity", was **dropped** on 2026-10-04: it already exists at `UserHarness/docs/human-use/route-context.md:59`. Do not re-add it.

## Where

- Repo: `C:\dev\HomeWorld`, branch `main`, GitHub `XylarDark/HomeWorld`.
- Desktop name: DESKTOP-21CT3H0.
- UserHarness is the submodule. Its branch is `master`.
- PowerShell on this machine does not accept `&&`.
- HomeWorld `AGENTS.md` stays the 23-line floor. Do not shrink it.
- Do not restore deleted `UserHarness/python/`.

## What this bite is

A steered glide down through spirit-blue clouds, then the existing field. A WoW ring-glide is an example of the feel only. It is not a circle around the island.

The job right now is to record facts that are already a yes, one sentence at a time, into `Docs/context/HOMEWORLD_ROUTE.md` on main. It is not a cloud build, not a mesh edit, and not a Design packet. No packet has been named. Do not tell anyone to implement, and do not place clouds, until a Design packet names the apply.

## Already on main

HEAD is `ba2b6b5`. These are the recorded lines on main. Do not rewrite them.

- The gap under the lowest cloud, down to the ground, is 5 seconds of straight glide at the standard speed, with no slowdown in that gap. That height is 25 m, from the 75 m drop over the 15 second window. It is a placeholder until human testing. Commit `565aa45`.
- Clouds are 6-24 m across. It is a placeholder until human testing. Commit `0733a48`.
- Cloud spacing is top 3-4 times the diameter, middle 1.5-2.5, and bottom 4-6. It is a placeholder until human testing. Commit `92669a6`.
- The cloud layer above the 25 m gap is 50 m tall, the 75 m drop minus that gap. It is a placeholder until human testing. Commit `169cfe0`.
- Any jump has more than one spirit-blue cloud, and there is no fixed count. Commit `7daa205`.
- The bottom of the cloud layer is the exit, and the landing stays in the existing field. Commit `ba269b8`.
- The wisp is a bit of the signature spirit blue on a cloud, not one of the three wisps at the spirit wound. Commit `d0234f0`.
- You collect the wisp on the way down, it stays with you, and you hold one per dung you will mix. Commit `8766851`.
- There is more than one cloud layer, and there is no fixed count of layers. That is not a split of the 50 m layer. Commit `35fb44d`.
- The descent is a steered glide, not a new flight mode. Commit `dc1b551`.

The 25 m gap, the 6-24 m size, the spacing bands, and the 50 m layer are placeholders until human testing. Do not replace them with new numbers.

## Ruling on the three research files — 2026-10-04

Lead ruled. Do not re-ask this.

| File | Ruling |
|------|--------|
| `PROMPT_WISP_CLOUD_RING_V1.md` | The instruction. Nothing to rule on |
| `EXIT_WISP_CLOUD_RING_V1.md` | **Accepted as superseded.** Its 6-24 m range and three spacing multipliers are already on main. Its extras stay unset |
| `EXIT_WISP_CLOUD_LOOK_V1.md` | **Refused.** Cites figures that were never accepted as locked, and delivers a taste call |

Three traps, so the next session does not fall in them:

- **Do not write RING's bite doc.** `WISP_CLOUD_LAYER_PLACEHOLDERS_V1.md` is specified to carry the size-range table, which holds per-band diameters (A 14-24, B 8-16, C 6-10) and jitter (±40/50/30%). Following that bite promotes barred figures into canon by document.
- **LOOK's "locked inputs" are not locked.** Line 63 lists per-band diameters; line 66 calls the 33.75 s window unchanged. Per-band diameters are barred below. The window is 15 s on main — 33.75 s is a *target*, conditional on the glide keeping its shape, and it exists only in the dirty working copy.
- **RING is not a ring around the island.** The name means the WoW ring glide as an example of the fall. `PROMPT:15` and `EXIT:65` both rule the circle out. Do not refuse it on that basis.

Both EXITs pin `0177c76` and read the dirty working copy. Every uncommitted figure they treat as a route fact — the 33.75 s window, the 1.5× drop — is not canon.

The Astroneer planetoid benchmark is **not accepted**. RING's own line 26 holds: the look stays a human call, research describes and does not steer.

## Next sentence, not written yet

None queued. The steered-glide sentence is on main as `dc1b551`. The next sentence is Design's to name — do not reach for the next number, and do not reuse 33.75 s or the 1.5x drop as though they were accepted.

The same idea still sits in the local working copy in longer form: that descent stays a glide you can steer through a spirit-blue cloud to take one wisp, and it is not a new flight. That is the same fact as `dc1b551`, not a second one. Do not commit the working file to get it.

## How to add one sentence

The working copy of `Docs/context/HOMEWORLD_ROUTE.md` is dirty on purpose. It holds older route facts that are not this commit. Do not commit that whole file.

1. Copy the working file to `%TEMP%\HOMEWORLD_ROUTE.working.md`.
2. Take `git show HEAD:Docs/context/HOMEWORLD_ROUTE.md`.
3. Add one new bullet under `## Recorded`, after the last bullet, and nothing else.
4. Write that text back as UTF-8 without a BOM.
5. Commit only `Docs/context/HOMEWORLD_ROUTE.md` and push `main`.
6. Copy the temp file back over the working file.

A sentence is not written until Lead says yes to that exact sentence. One sentence per commit.

## Do not commit these

- The dirty working copy of `Docs/context/HOMEWORLD_ROUTE.md`.
- `docs/handoffs/research/EXIT_WISP_CLOUD_LOOK_V1.md`
- `docs/handoffs/research/EXIT_WISP_CLOUD_RING_V1.md`
- `docs/handoffs/research/PROMPT_WISP_CLOUD_RING_V1.md`
- `blender/floating_island_homestead_LIB.blend1`
- This handoff, unless Lead asks to commit it.

Those three research files were ruled on 2026-10-04 — see the ruling table above. None of them is a licence to build.

## Not a yes

Do not ask for these, and do not write them.

- A split of the 50 m layer into top, middle, and bottom. That split is taste. Do not use equal thirds. Do not write 112.5 m or 37.5 m. No new height.
- A fixed count of clouds, or a fixed count of layers.
- A cap of five wisps.
- Jitter, band cuts, per-band diameters, or the share of wisp clouds to clouds that are not wisps. The generator sets that share. Later mechanics may change it. They are not this bite.
- Shooting clouds, or changing their spawn.
- A later speed boost. Not this bite.
- Island spec, mesh, `.blend`, `.uasset`, `.umap`, fall reset, or `HomeWorldGameInstance.cpp`.
- `Docs/qa/HUMAN_TUTORIAL.md`. It is not on disk.

## Working copy, leave it dirty

These older facts live only in the uncommitted working copy. They are not a license to bulk-commit. Design names the next sentence. If Design says the next thing is taste, stop. Taste is human testing at the desktop, not another number.

- Polish gate rows are red only. A row is not allowed to pass as a warning.
- Farming lives on the homestead.
- In the zones, day and night, you collect and nurture so the place provides the plants and animals the homestead needs.
- Taming for now is one small barn that holds one big bull, and the fur is what that bull sheds.
- The autonomous route is driven by curiosity.
- Gathering a pile takes one from a pool of piles. There is no cooldown.
- One dung and one wisp make one spirit fertilizer. Mix is at the homestead. The spirit spreads it at night. In the morning one herb pile appears per dung, at random in the field. Dawn alone does not bring a pile back. That night flight is not the locked first flight.
- The first flight still ends inside the field. The 75 m drop is how high the island sits above the plains, so every jump off the homestead drops that.
- The homestead-to-field window is 15 seconds now. Height is one and a half times the current drop. Neutral glide speed is two thirds. The target window is 33.75 seconds if the glide keeps the same shape. No meter height is written for that product. Fall rate, height, and zone sizes stay placeholders until human testing.
- The stage name stays polish.
- Shooting clouds and changing their spawn are later.

## When you are finished

Stop when the next missing piece is taste, or when Design still has not named a packet. Do not invent the packet. Do not open a glider build to fill the gap.

A fresh discovery chat is a different handover. It uses one idea line, then `Docs/context/DISCOVERY_START.md`. It does not open `Docs/context/ROUTE_START.md`, and it does not write a yes.
