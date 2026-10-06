# POLISH_ASSET_BOARD_HOW_TO

Mechanical fill-in for `docs/qa/POLISH_ASSET_BOARD.json`. No taste calls here; the stage ladder is the taste contract, in `Docs/37_POLISH_PASS_PROCESS.md` section 3.

1. Open the board: `docs/qa/POLISH_ASSET_BOARD.json`.
2. For each of the 10 rows, find the material in Unreal Editor by its `name` (e.g. `M_BeastStylized`). Look at it in the scene, not from memory.
3. Set `stage` to the rung it has actually reached: `S0`, `S1`, `S2`, `S3`, `S4`, or `S5`. Anything else is rejected, not counted.
4. Set `priority` to the order you want to review these in (1–10). The point is a batch at S2, not a queue through S3.
5. Leave `notes` alone unless what you saw changes the claim.
6. Do not invent rows. `M_FamilySilhouette` and `M_ValleyNight` stay off this board until an art decision says otherwise.
7. Save. The gate reads this file; a typo fails closed, and a null means "not looked at yet."
