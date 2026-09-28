# T0_M4_BACKPACK_GATE_V1 — MUST #4 Design packet (Arrange + DONE-WHEN freeze)

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — Design files-only; Design does **not** self-APPROVE |
| **Bite id** | `T0_M4_BACKPACK_GATE_V1` |
| **MUST** | #4 — Equip backpack → inventory |
| **Present?** | **Partial** (Design SoT = ACCEPTED gap walk `T0_GAP_INVENTORY_WALK_V1` row #4 — inventory-lite present; equip actor gap) |
| **CAP** | **CAP PARKED** |
| **Host** | **CLOUD** docs-only (Contents API) |
| **Map** | `Maps/VS_MVP` |
| **DET** | HOLD `0a27306` |
| **Packet class** | Mechanic inventory freeze — Arrange + DONE-WHEN + prove labels for **Test files-only** / future **Implement Act**. **Not** a Source Act. |
| **Cite** | HomeWorld Co ops · [Architecture Trade-Offs A–E](sand-workflow:architecture-trade-offs-design-depth) (15-q) · `PROTOTYPE_FEATURE_LIST_V1` · `T0_GAP_INVENTORY_WALK_V1` #4 · `PROP_INVENTORY_V1` (`NODE_BACKPACK` · `ENV_T0_HOME`) |

---

## One unknown (closed by this packet)

What Arrange + DONE-WHEN + prove labels freeze MUST #4 **equip backpack → inventory** on `NODE_BACKPACK` when Present?=**Partial** (inventory-lite present; equip actor gap), so Test scores files-only and Implement Act can open later — without Source/Content in this bite?

---

## Architecture Trade-Offs A–E (cite only — 15-q)

| Layer | Decision (inventory, **not** API invent) |
|-------|------------------------------------------|
| **A — Contract** | Prove labels `NODE_BACKPACK` · `TOD_DAY` · `FORM_BODY`. Chain = **equip** backpack actor → inventory access — not inventory-lite alone. |
| **B — Module** | Backpack equip gate = **Layer B** deep module (+ **A**). Prefer existing `UHomeWorldInventorySubsystem` — **no** parallel inventory service; equip is the named gate. |
| **C — Evidence** | Law = equip→inventory greps on named labels. CAP **PARKED**. No DESKTOP PASS/FAIL from Design. |
| **D — Seats** | Design freezes here; Test files-only. Implement Act = **later** (Conductor opens). |
| **E — Stability** | Ungated inventory-lite / PROXY-as-equip scored as #4 = **`closed_fail`**. Bounded fail — no invent-retry. |

**15-q:** Do **not** invent backpack/WP APIs. Prefer cite existing inventory subsystem. **No new schema.**

---

## Inventory freeze (labels ⊆ feature-list ∩ gap)

| Label | Role |
|-------|------|
| `NODE_BACKPACK` | Homestead equip-backpack interact (world actor — not PROXY alone) |
| `TOD_DAY` | Equip prove on Day |
| `FORM_BODY` | Body form while equipping |

Labels ⊆ `PROTOTYPE_FEATURE_LIST_V1` ∩ gap #4. PROP: `NODE_BACKPACK` · envelope `ENV_T0_HOME`.

---

## Expected · Found · Arrange · DONE-WHEN · Depends · Anti

| Field | Value |
|-------|-------|
| **Expected (T0)** | Day · body · equip backpack at `NODE_BACKPACK` → inventory access gated by that equip. |
| **Found (gap SoT = Partial)** | `UHomeWorldInventorySubsystem` (6-slot RES_*) present. PROXY `NODE_BACKPACK` / `SM_ProxyBackpack` (**not on disk**). **0** backpack equip path. Inventory-lite present; **not** gated by equip-backpack actor. Present?=**Partial**. |
| **Arrange** | Day · `FORM_BODY` · homestead · `NODE_BACKPACK` equip interact → inventory gated · CAP **PARKED** |
| **DONE-WHEN** | § below — Test files-only; **no DESKTOP Act** from Design |
| **Depends / HOLD** | Other T0 MUST **DEFER**. |
| **Anti** | Inventory-lite alone ≠ equip gate · PROXY ≠ world equip · no Content/Python/Source · no DESKTOP PASS/FAIL from Design · Design does not self-APPROVE |

---

## Arrange (normative)

1. Map: `Maps/VS_MVP` → Day · body (`FORM_BODY`) · homestead.
2. **`NODE_BACKPACK` interact:** equip backpack (world actor — **not** PROXY `SM_ProxyBackpack` alone).
3. Inventory access is **gated** by that equip — ungated inventory-lite alone does **not** satisfy #4.
4. **Negatives = `closed_fail`:** scoring inventory-lite without equip · PROXY-as-equip.
5. Prove class: mechanic inventory — **not** mood/taste. CAP **PARKED**.

---

## DONE-WHEN (Test files-only)

### Law

- Equip backpack → inventory is the **named gate** on `NODE_BACKPACK`
- Prove labels: `NODE_BACKPACK` · `TOD_DAY` · `FORM_BODY`
- Present?=**Partial** (gap SoT) — inventory-lite present; **0** equip path; PROXY ≠ world equip
- Ungated inventory-lite / PROXY-as-equip = **`closed_fail`**

### Grep strings

`NODE_BACKPACK` · `TOD_DAY` · `FORM_BODY` · `Arrange` · `DONE-WHEN` · `CAP PARKED` / `PARKED` · `Present?=Partial` · `closed_fail`

### Negative / Anti

- Do **not** treat ungated inventory-lite as equip→inventory
- Do **not** treat PROXY `SM_ProxyBackpack` as world equip
- No Content / Python / Source / `.uasset` / `.umap` · no DESKTOP PASS/FAIL from Design · Design does **not** self-APPROVE · other T0 MUST **DEFER**

### Future Implement note (cite only)

Gap Partial → Implement Act for `NODE_BACKPACK` equip actor + gate inventory behind equip opens **only** after Conductor routes. This packet does **not** open Source Act.

---

## Ball

**Test files-only** after draft PR. Do not merge from Design. Conductor routes next.

---

*Repo path: `Docs/handoffs/T0_M4_BACKPACK_GATE_V1.md` · Bite: `T0_M4_BACKPACK_GATE_V1` only · Present?=Partial · exclusive path.*
