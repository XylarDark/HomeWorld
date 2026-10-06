# World metrics

One row per number. Bite 1 of `Docs/handoffs/CONTEXT_PACK_V1.md`. Docs only.

**Cite base:** every "file:line" below was rechecked on main `a32fe8a`. The route cites had moved one line since `2c786ac`. "Kept by #N" names the Lead interview that kept or changed the number. "Kept by #N" names the Lead interview that kept or changed the number. A number with no findable source reads `unsourced`. Route numbers marked "placeholder" stay placeholders until human testing, as the route says.

**Scope:** numbers written in `Docs/01_GDD_MVP.md`, `Docs/context/HOMEWORLD_ROUTE.md` and `Docs/handoffs/CLOUDS_WISPS_V1.md`. Level actor positions and sizes are not here; they come from `Docs/level/L_VS_MVP_Markers_manifest.json`.

**Use:** link to a row instead of copying its number. Existing copies stay in place; a mismatch is listed at the bottom, not edited.

## Descent (route and clouds)

| # | Metric | Value | Unit | Axis | Source |
|---|---|---|---|---|---|
| D1 | Drop from island to plains | 75 | m | −Z | `HOMEWORLD_ROUTE.md:45` (also `:24`, `:27`); kept by #3 (1A) and #4 (1B, 75 m launch ledge) |
| D2 | Descent duration, launch to landing | 30 | s | — | `01_GDD_MVP.md:79` (§4 V2, developer decision 2026-10-05), `:214` (§9), `:296` (Appendix B, changed by #8 8A) |
| D3 | Sink rate | 2.5 | m/s | −Z | `HOMEWORLD_ROUTE.md:24`; `CLOUDS_WISPS_V1.md:15` (250 cm/s); kept by #1 (1A) |
| D4 | Forward glide speed | 5 | m/s | along glide heading | `CLOUDS_WISPS_V1.md:15` (500 cm/s, `UHomeWorldGlideMovementComponent`) |
| D5 | Clear gap under the lowest cloud, down to the ground | 25 | m | −Z | `HOMEWORLD_ROUTE.md:24`, placeholder; kept by #1 (1A) and #3 (1A) |
| D6 | Straight-glide time through that gap | 10 | s | −Z | `HOMEWORLD_ROUTE.md:24` (25 m ÷ 2.5 m/s, no slowdown) |
| D7 | Cloud band height above the gap | 50 | m | +Z | `HOMEWORLD_ROUTE.md:27`, placeholder; `CLOUDS_WISPS_V1.md:43` (band from 25 m to 75 m above field ground); kept by #3 (1A) |
| D8 | Cloud layer heights inside the band | taste placeholder, no lock | — | +Z | `CLOUDS_WISPS_V1.md:43` ("the packet writes no layer heights"); #3 (1A) |
| D9 | Layer split inside the 50 m band | taste placeholder, no lock | — | +Z | `HOMEWORLD_ROUTE.md:32`; `CLOUDS_WISPS_V1.md:43` |
| D10 | Cloud diameter | 6–24 | m | horizontal | `HOMEWORLD_ROUTE.md:25`, placeholder |
| D11 | Cloud spacing, top layer | 3–4 | × diameter | horizontal | `HOMEWORLD_ROUTE.md:26`, placeholder |
| D12 | Cloud spacing, middle layer | 1.5–2.5 | × diameter | horizontal | `HOMEWORLD_ROUTE.md:26`, placeholder |
| D13 | Cloud spacing, bottom layer | 4–6 | × diameter | horizontal | `HOMEWORLD_ROUTE.md:26`, placeholder |
| D14 | Cloud layers, minimum | 2 | count | — | `CLOUDS_WISPS_V1.md:42` ("at least 2, no fixed number"); route `:32` sets no fixed count |
| D15 | Plains edge on the straight glide | 260 | m | straight-glide heading; +X or +Y open (Lead desk check). Past the edge: not written. Other directions: no edge (`:47`) | `HOMEWORLD_ROUTE.md:46` |
| D16 | Night flight height | 1.5 × D1 (112.5 m derived), placeholder | × first-jump drop | +Z | `HOMEWORLD_ROUTE.md:49`, changed by #11 (2A); the route writes no meters for it (`:51`, #11 1A) |
| D17 | Night flight neutral glide speed | 2/3 × first-jump neutral glide speed, placeholder | ratio | along glide heading | `HOMEWORLD_ROUTE.md:50`, changed by #11 (2A) |

## Loop durations (GDD)

| # | Metric | Value | Unit | Source |
|---|---|---|---|---|
| L1 | Cabin to lookout walk | ~15–25 | s | `01_GDD_MVP.md:69` (§4 V1) |
| L2 | Homestead walk circuit | 45–90 | s | `01_GDD_MVP.md:295` (Appendix B); `:69` |
| L3 | Gather, per node | ~1.5–3 | s | `01_GDD_MVP.md:89` (§4 V3) |
| L4 | Gather all six once | 90–180 | s | `01_GDD_MVP.md:297`; `:89` |
| L5 | Tame encounter read | ~5–10 | s | `01_GDD_MVP.md:99` (§4 V4) |
| L6 | Tame one beast | 20–45 | s | `01_GDD_MVP.md:298`; `:99` |
| L7 | Tame stage 0 Encounter | ~3–5 | s | `01_GDD_MVP.md:170` |
| L8 | Tame stage 1 Offer | ~2–3 | s | `01_GDD_MVP.md:171` |
| L9 | Tame stage 2 Bond (hold in calm radius ~3–5 s) | ~3–5 | s | `01_GDD_MVP.md:172` |
| L10 | Tame stage 3 Helper | ~2 | s | `01_GDD_MVP.md:173` |
| L11 | Portal, channel plus transit, each way | ~3–6 | s | `01_GDD_MVP.md:109` (§4 V5) |
| L12 | Night portal round trip | 6–12 | s | `01_GDD_MVP.md:299` |
| L13 | Heal, per heal | 2–4 | s | `01_GDD_MVP.md:119`, `:189` |
| L14 | Heal three | 15–40 | s | `01_GDD_MVP.md:300`; `:119` |
| L15 | Nurture, per nurture | ~2–4 | s | `01_GDD_MVP.md:129` |
| L16 | Nurture two | 10–20 | s | `01_GDD_MVP.md:301`; `:129` |
| L17 | Portal return | ~3–6 | s | `01_GDD_MVP.md:139` |
| L18 | Dawn transition | 4–8 | s | `01_GDD_MVP.md:302`; `:139` |

## Systems

| # | Metric | Value | Unit | Source |
|---|---|---|---|---|
| S1 | Inventory slots | 6 | slots | `01_GDD_MVP.md:228`, `:232` (§10) |
| S2 | Wisps carried | 1 per dung to mix | count | `HOMEWORLD_ROUTE.md:31` |
| S3 | Units per gather interact | 1 | unit | `01_GDD_MVP.md:156` |
| S4 | Resource types on the slice | 6 | count | `01_GDD_MVP.md:89`, `:297` |
| S5 | Food consumed per tame Offer | 1 | unit | `01_GDD_MVP.md:171` |
| S6 | Heals in the slice | 3 | count | `01_GDD_MVP.md:119`, `:300` |
| S7 | Nurture targets in the slice | 2 | count | `01_GDD_MVP.md:129`, `:301` |

## Mismatches found

All three found in this bite are resolved here.

| # | Where | Was | Now |
|---|---|---|---|
| M1 | `CLOUDS_WISPS_V1.md:75` | Stale note that Appendix B had no duration | Marked resolved (#286, #8 8A) |
| M2 | `HOMEWORLD_ROUTE.md:51` | "No meter height is written for the drop," against 75 m at `:24`, `:27`, `:45` | Reads "for the night flight" (#11 1A) |
| M3 | `HOMEWORLD_ROUTE.md:49`, `:50` | Ratios with no reference | Measured against the first jump (#11 2A) |

Also fixed under #11 (3A), not a number: `01_GDD_MVP.md:156` said "Node cooldown or deplete until dawn"; it now matches the route (no cooldown, dawn alone brings no pile back). The Source change to `HomeWorldResourcePile` is queued for the desktop session and needs Lead's yes to merge.

No other number in the three files disagrees with a row above.
