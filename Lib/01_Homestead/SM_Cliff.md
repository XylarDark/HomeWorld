# SM_Cliff — Layered Torn-Earth Cliff Spec

**Kit:** `Lib/01_Homestead`  
**Canon name:** `SM_Cliff` (module family)  
**Graybox map:** `SM_Cliff_LookoutFace`, `SM_Cliff_CabinFace`, `SM_Cliff_Rear` → kit modules below  
**Date:** 2026-09-16 · **ID:** P3_ENVH_kit · **Owner:** ENV-H

---

## 1. Role

**Layered torn-earth** cliff under the island rim. Readable strata and jagged underside for Shot 1 / key art. **Not** a pancake disc edge. **Not** a cylinder plug.

Separate from `SM_IslandTop` — cliff owns rock mass only.

---

## 2. Shape language (locked)

- Blocky **staggered strata** / horizontal sediment layers
- Vertically oriented torn faces with cool gray-violet read at night
- Jagged underside (ripped-from-earth)
- Modules or **layered slabs** that stack with offsets — never a single smooth extrusion

Art bible: cool purple-gray / charcoal in shadow; readable strata. Material: **M_CliffRock**.

---

## 3. Module set (layered — not pancake)

Prefer modular pieces that compose the three graybox faces. Each module is a slab or torn chunk; assemble with 0.1–0.3 m overlap.

| Module | Size guide (X×Y×Z m) | Graybox anchor origin | Role |
|---|---|---|---|
| **SM_Cliff_Slab_A** | 3.0 × 1.2 × 1.5 | reusable | Primary horizontal stratum slab |
| **SM_Cliff_Slab_B** | 2.5 × 1.0 × 1.2 | reusable | Mid stratum offset |
| **SM_Cliff_Slab_C** | 2.0 × 0.9 × 1.0 | reusable | Thin torn lip / shelf |
| **SM_Cliff_Chunk_Torn** | 2.5 × 2.0 × 3.0 | reusable | Vertical torn face chunk |
| **SM_Cliff_LookoutFace** | 6.0 × 2.5 × 8.0 envelope | (7.5, −5.5, −4.0) | Assembled right/front under lookout |
| **SM_Cliff_CabinFace** | 5.0 × 2.0 × 6.0 envelope | (−7.0, −4.5, −3.0) | Assembled left underside under cabin |
| **SM_Cliff_Rear** | 12.0 × 2.0 × 5.0 envelope | (0.0, 5.0, −2.5) | Rear massing; kills cylinder read |

**Assembly rule:** Lookout / Cabin / Rear faces are either (a) hero assemblies of slabs+chunks, or (b) single meshes that **internally** show layered slab topology. Do not ship smooth lofted cylinders.

Optional small crumb: `SM_Cliff_IsletHint` (1.0 × 0.8 × 0.6) — homestead rim debris only; transit islets remain WLD/ENV-P.

---

## 4. Origin & attach

| Property | Value |
|---|---|
| Module origin | Ground/contact or attach face — document per mesh; prefer **lower-back** of chunk at attach |
| Face assemblies | Match graybox origins (table above); top of cliff meets island rim ≈ Z 0 |
| Attach sockets on top | `SOCKET_CliffAttach_*` on `SM_IslandTop` |
| Units | Meters; **apply scale** |

---

## 5. Materials

| Slot | Master | Notes |
|---|---|---|
| All cliff rock | **M_CliffRock** | Warm/cool instance tweaks within cliff palette; Variation for strata contrast |
| Emissive | off | Cool moonlight is LIT, not rock emissive |

No grass on cliff body (grass stays on `SM_IslandTop`). Thin soil lip optional as top-cap only if separate from grass plate — prefer leave to top mesh.

---

## 6. Layering recipe (authoring)

1. Stack 3–5 horizontal slabs with ±0.2–0.5 m X/Y stagger.
2. Break front with 1–2 vertical torn chunks.
3. Undercut underside with irregular boolean or hand-cut wedges.
4. Thumbnail silhouette must fail “cylinder” and “coin” tests.

---

## 7. Naming / export

- Family prefix: `SM_Cliff_*`
- Collection: `Lib/01_Homestead`
- Cite master: `M_CliffRock` on every rock mesh

---

## 8. Gate

- [x] Spec mandates **layered** modules/slabs  
- [x] Explicit reject of pancake/cylinder  
- [x] Graybox faces mapped into kit canon `SM_Cliff`

---

## 9. Rejects

Pancake island edge; cylinder extrusion; merged top+cliff monolith; photoreal rock scans; unique cliff shader; planet valley rock kits in this folder.
