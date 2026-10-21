# 43 - Clouds and wisps design

**Status:** APPROVED by Lead (Luke Thompson), 2026-10-20 ET. Design only. Implementation of anything still missing waits until Lead asks.
**Origin:** Cursor plan `clouds_wisps_design_0dd1e156` ("Clouds wisps design"), scribed here as the one owner.
**Picks:** interview #2, 2026-10-05: `1A` (clouds plus wisps are the first route packet; the fertilizer loop stays out). Interview #3, 2026-10-05: `1A 2A` (layers inside the 300 m band; clouds are pass-through).
**Follow-up:** 2026-10-20: `1A 2A 3A`.
**When to use:** Before any work on the cloud field, a cloud wisp, or the descent those two ride.

Mode: solo. State: decide. Transition: Concept -> Greybox.

This doc is the owner of the clouds-and-wisps route packet. Do not copy it into the vision board, the GDD, or the route file. The canon map keeps one pointer row. Meters stay in [HOMEWORLD_ROUTE.md](context/HOMEWORLD_ROUTE.md). Look stays in [CLOUD_CONTEXT.md](art/CLOUD_CONTEXT.md). The home pool stays in [42_HOME_LOOP_DESIGN.md](42_HOME_LOOP_DESIGN.md). Companions stay in [41_COMPANION_PARTY_DESIGN.md](41_COMPANION_PARTY_DESIGN.md).

[CLOUDS_WISPS_V1.md](handoffs/CLOUDS_WISPS_V1.md) stays the old packet. This file replaces it as the owner. It uses the 6× band (150 m gap, 300 m of cloud, 450 m drop). The old packet's 50 m / 25 m band is retired here. `AHomeWorldCloudField`'s header comment still describes that 50 m band. `BuildClouds` already pins the lowest cloud bottom to 150 m and the top of the band to 450 m. This scribe does not edit that header.

## 1. Scope in one paragraph

The player steers a glider down through spirit-blue clouds and lands in the existing field. A cloud can carry a cloud wisp. At night the player may collect up to two of those wisps. One is for the homestead wound. One is for fertilizer. The day glide collects nothing. The fertilizer mix, the spread, and the morning pile stay in the route file. Healed task wisps are the home pool, and they are a different population.

## 2. What the earlier picks decide

- **Interview #2, 1A.** Clouds plus wisps get this route packet. The fertilizer loop is out of the packet.
- **Interview #3, 1A.** Every cloud layer sits inside the 300 m band. The 150 m gap under the lowest cloud stays clear. The 450 m drop and the 30 s descent stay as they are.
- **Interview #3, 2A.** Clouds are pass-through. They overlap the pawn. They do not block, and they are not a surface to stand on. The wisp keeps its own pickup overlap.

## 3. What the 2026-10-20 follow-up decides

- **1A.** Collection is the night descent only. The carry cap is two: one cloud wisp for the homestead wound, one to mix with one dung as fertilizer. The day glide has no pickup. Lead yesed that GDD sentence on 2026-10-20. It is [01_GDD_MVP.md](01_GDD_MVP.md) §9 step 3.
- **2A.** There is no fixed count of clouds that show a wisp, so a missed cloud can still leave another to find. The player still holds at most two, and only on the night glide.
- **3A.** The field's horizontal spread stays a taste placeholder. The locked horizontal edge is the 1560 m plains edge on the straight-glide heading only. Past that edge the plains end on that heading. Other headings have no edge. Clouds do not draw a ring. The code default of 80 m (`HorizontalExtentCm` = 8000) is not the route.

## 4. Route lines

Each line names the axis, the distance, and what is past the edge. The numbers match the GDD's 30 s descent and the route's 6× meters. A number the route already calls a placeholder stays a placeholder.

- **Down, world −Z, 450 m.** From the glide start to the field ground. The sink is 15 m/s, so the drop is 30 s ([01_GDD_MVP.md](01_GDD_MVP.md) §9 and Appendix B). Past the lower edge: walk control on the existing field. Steering has no rail, corridor, or bound. The descent stays a glider. It adds no flight HUD and no energy meter.
- **Cloud band, world −Z, 300 m.** Clouds sit entirely between 150 m and 450 m above the field ground. More than one layer, and the layer count is not fixed. Those layers are not a split of the 300 m into a second band. Past the bottom of the lowest cloud: 150 m of clear air, with no slowdown, then the field. Past the top of the highest cloud: the glide start on the island.
- **Straight glide, one heading, 1560 m.** That distance is the plains edge on that heading only. Past it: the plains end on that heading. Other headings have no edge. A cloud ring does not draw the line. Follow-up 3A.
- **Across.** Each cloud is 36–144 m. Spacing, as a multiple of that diameter: top 3–4, middle 1.5–2.5, bottom 4–6. The route marks these as placeholders until a human pass. The 72 m sample in the cloud context is the field's current default. It is not a new lock.

The day glide and the night spirit glide share this drop and this steer. Companions do not ride either glide.

## 5. Three populations

- **Cloud wisp.** A bit of the signature spirit blue on a cloud. It is not one of the three wisps at the wound. `CollectCloudWisp` already requires an active descent and night, and it refuses a third carry. Follow-up 1A and 2A are that rule. The two jobs are named here and specified in the route file: one heals the homestead wound, one mixes with one dung. Mixing, spreading, and the morning pile are the fertilizer loop, and interview #2 left that loop out of this packet.
- **Wound wisps.** The heal verb's three. The route says that once they are healed they follow, and that those followers are the night flight that spreads fertilizer. This doc does not place the wound. The GDD still sites those three at a planet wound. The route sites a homestead wound, seen by day and healed at night by one cloud wisp. Both sentences stay where they are.
- **Home pool.** Healed task wisps, assigned to a station, a plot, or cleaning. [42_HOME_LOOP_DESIGN.md](42_HOME_LOOP_DESIGN.md) follow-up 1A. A cloud wisp is not a member of that pool. The home-pool sign and water path are [42_HOME_LOOP_DESIGN.md](42_HOME_LOOP_DESIGN.md) section 10.1; a cloud wisp does not enter that path.

## 6. Placeables

[LEVEL_RULES.md](context/LEVEL_RULES.md) rule 2: a placeable actor needs a scene root and a keep-transform check. This scribe records the rule and the code as it is. It does not change Source.

- `AHomeWorldCloudField` already has a scene-component root. One placed field lays the clouds out. Its layer heights inside the band are a setting. The lowest layer's Z is the 150 m pin.
- `AHomeWorldCloud` currently uses the visual mesh as its root. The next build gives it a scene-component root and hangs the mesh under that root.
- The surface wisp already attaches with `KeepWorldTransform`. The next build checks that the attach leaves the wisp's world location unchanged.
- Collision stays interview #3, 2A: query overlap on the pawn, never a block.
- Look stays the cloud context: an ambient cloud, and a larger wisp cloud with the wisp readable inside it. The master is the existing `M_SpiritUnlit`. The playtest mesh is the engine sphere. This doc adds no `.uasset` and no `.umap`.

A later placement, when Lead asks, is one `AHomeWorldCloudField` on the descent from the glide start. That placement is a level change of its own. It is not part of this scribe.

## 7. Sentences this doc leaves in place

- **GDD §12** lists night flight as out of scope. The route's night spirit glide uses this same drop and the same steer, and follow-up 1A collects there. The fertilizer spread stays out of this packet on either reading.
- **GDD §6** places three hurt wisps at a planet wound site. The route's homestead wound is a different sentence. This doc moves neither.
- **The old packet** said to collect on the way down, one wisp per dung. The 2026-10-07 night cap replaced that line: two cloud wisps a night, and no third. Follow-up 1A keeps the cap.
- **The field header comment** still says the layers sit in a 50 m band between 25 m and 75 m. `BuildClouds` uses 150 m and 450 m. The route and this doc use 150 m and 450 m.

## 8. Taste-pass placeholders

Lead has not locked these. A later build uses them as written until a taste pass replaces them.

- Cloud diameter 36–144 m. Field default 72 m, which is the cloud-context sample.
- Spacing factors inside the bands in section 4. Code defaults: top 3.5, middle 2.0, bottom 5.0.
- Layer-center heights inside the 300 m band, except the lowest layer, which the 150 m pin owns.
- Horizontal spread of the field. Follow-up 3A. The 80 m code default is not a route distance.

## 9. Out of scope

- The fertilizer mix, the night spread, and any morning pile.
- Home-loop stations, dust, plots, and meal buffs.
- Companion party rules. They do not ride the glide.
- A GDD edit, a route-file edit, a Source edit, a `.uasset`, or a `.umap`.
- A new material master, a flight energy meter, or a rail on the descent.
- A fixed count of clouds, of layers, or of wisp clouds. The carry cap of two is the lock. The count of clouds that wear a wisp is not.
