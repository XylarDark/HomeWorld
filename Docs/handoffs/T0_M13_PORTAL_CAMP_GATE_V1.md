# T0_M13_PORTAL_CAMP_GATE_V1 — MUST #13 Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED (Lead stamp 2026-10-07)** - Design frozen; camp-portal half + PROP JSON labels are the tracked impl gaps |
| **Bite id** | `T0_M13_PORTAL_CAMP_GATE_V1` |
| **MUST** | #13 — Home portal → camp portal (spirit) |
| **Present?** | **Partial** (Design SoT = ACCEPTED gap walk `T0_GAP_INVENTORY_WALK_V1` row #13 — home↔planet shrine present; camp portal missing; labels ∉ PROP JSON) |
| **CAP** | **CAP PARKED** |
| **Host** | **CLOUD** docs-only (Contents API) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Mechanic inventory freeze — Arrange + DONE-WHEN + prove labels for **Test files-only** / future **Implement Act**. **Not** a Source Act. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q) · `PROTOTYPE_FEATURE_LIST_V1` · `T0_GAP_INVENTORY_WALK_V1` #13 · `PROP_INVENTORY_V1` (JSON gap: `NODE_PORTAL_HOME` / `NODE_PORTAL_CAMP` ∉ MUST-ENV-GREYBOX `props[]`) |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze MUST #13 **spirit home→camp portal pair** when Present?=**Partial** (home↔planet present; camp missing; PROP JSON gap), so Test scores files-only and Implement Act can open later — without Source/Content in this bite?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision (inventory, **not** API invent) |
|-------|------------------------------------------|
| **A — Contract** | Prove labels `NODE_PORTAL_HOME` · `NODE_PORTAL_CAMP` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT`. Chain = spirit home portal → **camp** portal — not home↔planet return alone. |
| **B — Module** | Portal pair = **Layer B** deep module (+ **A**). Prefer existing `HomeWorldShrinePortal*` / `GP_PortalA`↔`B` — **no** parallel portal service; return shrine ≠ camp pair. |
| **C — Evidence** | Law = home→camp portal greps on named labels. CAP **PARKED**. No DESKTOP PASS/FAIL from Design. |
| **D — Seats** | Design freezes here; Test files-only. Implement Act = **later** (Conductor opens). PROP JSON gap noted — no schema invent this bite. |
| **E — Stability** | Home↔planet-only / body portal / shrine-dress-as-camp scored as #13 = **`closed_fail`**. Bounded fail — no invent-retry. |

**15-q:** Do **not** invent portal/WP APIs or add PROP rows this bite. Prefer cite existing shrine portal hooks. **No new schema.**

---

## Inventory freeze (labels ⊆ feature-list ∩ gap)

| Label | Role |
|-------|------|
| `NODE_PORTAL_HOME` | Spirit home-side portal for camp route |
| `NODE_PORTAL_CAMP` | Spirit camp-side portal (missing today) |
| `TOD_NIGHT_SPIRIT` | Portal prove on night spirit path |
| `FORM_SPIRIT` | Spirit form while portaling |

Labels ⊆ `PROTOTYPE_FEATURE_LIST_V1` ∩ gap #13. **Honesty:** `NODE_PORTAL_HOME` / `NODE_PORTAL_CAMP` ∉ `PROP_INVENTORY_V1` MUST-ENV-GREYBOX `props[]` — feature-list freeze still owns labels; PROP JSON gap stays open (not filled by this Design bite).

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | Spirit · night · home portal → **camp** portal pair (`NODE_PORTAL_HOME` ↔ `NODE_PORTAL_CAMP`). |
| **Found (gap SoT = Partial)** | Umap: `GP_PortalA`↔`GP_PortalB`, `VS_MARKER_PortalHome`/`PortalPlanet`, shrine dress, `HomeWorldShrinePortal*`. Home↔**planet** return pair present. **No** camp portal. Labels ∉ PROP JSON. Present?=**Partial**. |
| **Arrange** | Spirit · `FORM_SPIRIT` · `TOD_NIGHT_SPIRIT` · `NODE_PORTAL_HOME` → `NODE_PORTAL_CAMP` · CAP **PARKED** |
| **DONE-WHEN** | § below — Test files-only; **no DESKTOP Act** from Design |
| **Depends / HOLD** | Other T0 MUST **DEFER**. Home↔planet return cite only — does **not** satisfy #13. |
| **Anti** | Home↔planet alone ≠ home→camp · body portal ≠ #13 · PROP-missing ≠ invent schema this bite · no Content/Python/Source · no DESKTOP PASS/FAIL from Design · Design does not self-APPROVE |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → night spirit (`TOD_NIGHT_SPIRIT` / `FORM_SPIRIT`).
2. **`NODE_PORTAL_HOME` → `NODE_PORTAL_CAMP`:** spirit portal pair home→**camp** (world — **not** home↔planet return pair alone).
3. Prefer existing shrine portal path (`HomeWorldShrinePortal*` / portal markers) when Act opens — camp side must exist.
4. **Negatives = `closed_fail`:** scoring home↔planet return as #13 · body-form portal as #13 · shrine dress alone as camp portal.
5. Prove class: mechanic inventory — **not** mood/taste. CAP **PARKED**.

---

## DONE-WHEN (Test files-only)

### Law

- Spirit home→camp portal is the **named pair** `NODE_PORTAL_HOME` · `NODE_PORTAL_CAMP`
- Prove labels: `NODE_PORTAL_HOME` · `NODE_PORTAL_CAMP` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT`
- Present?=**Partial** (gap SoT) — home↔planet present; camp portal missing; labels ∉ PROP JSON
- Home↔planet-only / body portal / dress-as-camp = **`closed_fail`**

### Grep strings

`NODE_PORTAL_HOME` · `NODE_PORTAL_CAMP` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT` · `Arrange` · `DONE-WHEN` · `CAP PARKED` / `PARKED` · `Present?=Partial` · `closed_fail`

### Negative / Anti

- Do **not** treat `GP_PortalA`↔`B` home↔planet return alone as home→camp
- Do **not** invent PROP JSON rows / schema in this Design bite
- No Content / Python / Source / `.uasset` / `.umap` · no DESKTOP PASS/FAIL from Design · Design does **not** self-APPROVE · other T0 MUST **DEFER**

### Future Implement note (cite only)

Gap Partial → Implement Act for `NODE_PORTAL_CAMP` + home→camp wire (and optional PROP row later under Conductor/Design scope) opens **only** after Conductor routes. This packet does **not** open Source Act or schema invent.

---

## Ball

**Test files-only** after draft PR. Do not merge from Design. Conductor routes next.

---

*Repo path: `Docs/handoffs/T0_M13_PORTAL_CAMP_GATE_V1.md` · Bite: `T0_M13_PORTAL_CAMP_GATE_V1` only · Present?=Partial · exclusive path.*
