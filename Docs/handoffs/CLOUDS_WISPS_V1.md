# CLOUDS_WISPS_V1 — Design packet (clouds plus wisps, first route packet)

| Field | Value |
|-------|-------|
| Status | READY for Implement. Lead locked interview #3 as 1A 2A (Oct 5 2026). Design does not self-approve. |
| Lead lock | Interview #2, answer 1A (Oct 5 2026): clouds plus wisps get the first route packet. Fertilizer loop stays out of scope. Interview #3, 1A 2A (Oct 5 2026): layers inside the 50 m band, clouds pass-through. |
| Base | `main` @ `d704b0e` |
| Map | `L_VS_MVP_Markers` (placement is level work: OpenCode on the desktop, not Implement) |
| Facts source | `Docs/context/HOMEWORLD_ROUTE.md` § Recorded. This packet adds no new facts. |

## Already on main (do not redo)

| Piece | Where |
|-------|-------|
| Glide movement mode, forward 3000 cm/s, sink 1500 cm/s (30 s to ground; ×6 world-scale pass 2026-10-07) | `UHomeWorldGlideMovementComponent` (`8e33dd4`, `c38e68e`) |
| Descent start from `GP_GlideStart`, day/body | `AHomeWorldCharacter::TryStartCloudDescent` (`f10bbee`) |
| Wisp pickup and carry through landing | `AHomeWorldCloudWisp`, `CollectCloudWisp`, `CarriedCloudWisps` (`f10bbee`) |
| Landing hands back walk control | glide `PhysCustom` → `ProcessLanded` |

## Not built (this packet)

No cloud actor exists, and no wisp is placed in any map.

## Route facts this packet uses (quoted, placeholders until human testing)

1. Clouds are 36-144 m across. (×6 world-scale pass 2026-10-07.)
2. Cloud spacing is top 3-4 times the diameter, middle 1.5-2.5, and bottom 4-6. (Ratios unchanged by the ×6 pass.)
3. The cloud layer above the 150 m gap is 300 m tall, the 450 m drop minus that gap. (×6 pass.)
4. The gap under the lowest cloud, down to the ground, is 150 m ... with no slowdown in that gap. (×6 pass.)
5. Any jump has more than one spirit-blue cloud, and there is no fixed count.
6. There is more than one cloud layer, and there is no fixed count of layers. That is not a split of the 300 m layer. (×6 pass.)
7. The bottom of the cloud layer is the exit, and the landing stays in the existing field.
8. The wisp is a bit of the signature spirit blue on a cloud, not one of the three wisps at the spirit wound.
9. You collect the wisp on the way down, it stays with you, and you hold one per dung you will mix.
10. Steering is unrestricted by rails, corridors, or artificial bounds throughout the descent.

## Source (Implement PR)

1. **`AHomeWorldCloud`**: one spirit-blue cloud. Diameter is a setting clamped to 36-144 m (fact 1). Look uses a runtime dynamic instance of the existing `M_SpiritUnlit` master (`Docs/02_MATERIAL_SHEET.md` §2.9); no new master, and no `.uasset` from Implement.
2. **Wisp on a cloud**: a cloud can carry an `AHomeWorldCloudWisp` at its surface (fact 8). Reuse the existing class unchanged. Which clouds carry one is a setting, with no fixed count (facts 5, 9).
3. **`AHomeWorldCloudField`**: one placed actor that lays out clouds from settings:
   - layer count, at least 2, no fixed number (fact 6);
   - all layers sit inside the 300 m band, between 150 m and 450 m above the field ground, and the 150 m gap stays clear (interview #3, 1A; ×6 pass 2026-10-07). Each layer's height inside that band is a setting to tune in Lead's taste pass; the packet writes no layer heights;
   - spacing band per position, top 3-4x, middle 1.5-2.5x, bottom 4-6x diameter (fact 2);
   - the lowest cloud's bottom sits 150 m above the field ground, and nothing is placed in that gap (fact 4; ×6 pass);
   - horizontal extent is a setting, covering the descent path out from `GP_GlideStart`. No bounds, rails, or corridors are added (fact 10).
4. **Collision**: pass-through (interview #3, 2A). Clouds never block the player and cannot be stood on; they only register an overlap. The wisp keeps its existing pickup overlap.
5. **Automation** `HomeWorld.Transit.CloudDescent.CloudField`: field builds 2+ layers and 2+ clouds; every diameter is within 36-144 m; spacing is within its band; the lowest cloud bottom is 150 m above ground; every cloud sits entirely between 150 m and 450 m above ground; at least one wisp sits on a cloud; no cloud blocks the player pawn (overlap only).

## Level (OpenCode on desktop, after the Source PR merges)

Place one `AHomeWorldCloudField` in `L_VS_MVP_Markers` above the descent from `GP_GlideStart`.

## DONE-WHEN (Test scores; Conductor runs PIE)

| # | Check |
|---|-------|
| 1 | Build succeeds; `CloudField` automation reports Success, 0 errors. |
| 2 | Existing `UnrestrictedSteeringAndWispCarry` test still passes unchanged. |
| 3 | PIE: launch from `GP_GlideStart`, glide through visible spirit-blue clouds in 2+ layers without being stopped by any, collect a wisp. |
| 4 | PIE: land in the existing field; log shows `CLOUD_DESCENT: landed ... carried wisps=` 1 or more. |
| 5 | Diff touches no glide speed, sink, or carry code. |

## Anti

Glide speed, sink, or carry changes. Fixed cloud, wisp, or layer counts. Layer heights written as numbers. Layers above the 50 m band. Clouds that block the player or can be stood on. Rails, corridors, or bounds. Fertilizer, barn, bull. New material master. `.uasset`/`.umap` from Implement. Design self-approve.

## Locked by Lead (interview #3, Oct 5 2026)

1. **1A**: extra cloud layers sit inside the 300 m band with the 150 m gap kept clear, so the 450 m drop and 30 s descent stay unchanged (×6 world-scale pass 2026-10-07).
2. **2A**: clouds are pass-through and only register an overlap.

## Doc note

Resolved: `Docs/01_GDD_MVP.md` Appendix B reads 30 s, matching §9 (#286, interview #8, 8A).
