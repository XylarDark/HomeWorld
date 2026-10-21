# Tutorial island playtest

One pass, on foot, in the desktop editor. The island this pass judges is the `L_SizeTest` walk pad, the floor where the opening teaches the walk. The greybox island (180 × 100 m) is a different floor and is not this pass.

Current entry: [`PLAYTEST_INDEX.md`](PLAYTEST_INDEX.md). This file owns the movement pass only.

Map: `/Game/HomeWorld/Maps/SizeTest/L_SizeTest`.

The pad size and the start live in `Docs/level/L_SizeTest_METRICS.md`. Predicted times below come from `Docs/qa/TRAVERSAL_BUDGET.md` (generated 2026-10-17). A straight line is a lower bound. The trees and rocks make the real walk longer.

## What you are checking

The opening wheel has three speeds, from `ApplyOpeningWalkSpeed` against a 450 cm/s body walk: 150, 300, and 450 cm/s. Scroll down until it will not go slower, then up one step at a time. The middle step is 300 cm/s.

The placed approach, player start to the partner at the south door, is 49.9 m in a straight line.

| Step | Speed | Straight-line time |
|---|---|---|
| Slowest | 150 cm/s | 33.3 s |
| Middle | 300 cm/s | 16.6 s |
| Fastest | 450 cm/s | 11.1 s |

The circuit window is 12–20 s (`Docs/canon/FEEL.md`). One distance cannot land inside that window at all three speeds. The middle step is the one the window is checked against. The pad is 70 × 140 m. One lap of that pad at the middle speed is about 113 s, so this walk is a short approach on the pad, not a lap of the rim.

## Do this

1. Play `L_SizeTest` on foot. Stand on the pad. The field mesh under the island is not the floor.
2. From the south start, walk through the trees and rocks to the partner at the south door. Do not sprint.
3. Do that three times, once at each wheel step. Time each walk from the first step to arriving at the partner.
4. Stop. Do not play the herb, the heal, the kettle, the mist, or the glide. Those beats are not this pass.

## Pass

- You reach the partner without a hint and without getting stuck.
- The cottage stays hidden by the trees and rocks until you are through them.
- The middle walk feels like one short approach to the family, not a hike across the pad. Write the time. The straight-line prediction is 16.6 s, inside 12–20 s. A walked time a little over 20 s can still pass if the extra time is the copse. A walk that feels like a long crossing does not.
- The slowest step feels deliberately slow. The fastest step feels like the quick end of the same walk.

## Write down

- The three times, and which scroll step each one was.
- The commit you played, if you have it.
- One sentence: is this pad the right size for meeting the family and learning the walk?
- Anything that felt wrong. A clean arrival is not a pass by itself.

Bring those notes back to this chat. `Docs/canon/PLAYTEST.md` is the log, and it currently has other uncommitted edits, so do not have a second writer fill it in the same hour.
