# PL-C Thin Loop UX — Handoff

| Field | Value |
|-------|-------|
| **Phase** | PL-C |
| **Status** | **IN PROGRESS / PENDING DESKTOP Safe-Build + smoke** — unlocked by Lead **`WAIVE PL-B`**, 2026-09-17 ET |
| **Lead gate** | **`APPROVE PL-C`** before PL-D |
| **Spec** | [16_PLAYABLE_LOOP.md](../16_PLAYABLE_LOOP.md) § PL-C |

## Shipped (repo)

| Item | Path |
|------|------|
| Store-transfer component | `HomeWorldStoreTransferComponent` — deposit/withdraw, `STORE:` logs |
| Store prop actor | `AHomeWorldStoreProp` |
| Interact wire | `TryStoreTransferInFront` before harvest (day/body) |
| HUD readout | Six `Inv[n]: RES_* xN` lines on `AHomeWorldHUD` |
| Console | `hw.Inventory.Dump` → `INVENTORY:` lines |
| Placement | `Content/Python/place_vs_mvp_store_transfer.py` (6× `GP_Store_*`) |

## DESKTOP smoke (Conductor)

1. Pull tip → Safe-Build
2. Open `L_VS_MVP_Markers` → MCP `place_vs_mvp_store_transfer.py`
3. PIE: grant/harvest resource → face `GP_Store_*` → **E** → expect `STORE: deposit`
4. **E** again when inventory cannot accept deposit path → `STORE: withdraw`
5. Confirm HUD Inv lines + `hw.Inventory.Dump`

## Done criteria

- [x] Store-transfer interact path in C++
- [x] Inventory readout (HUD + log dump)
- [ ] DESKTOP Safe-Build + smoke evidence
- [ ] Lead **`APPROVE PL-C`**

## Hard rules

- Docs/07 CLOSED; no free-flight; no new masters; no `.uasset` commits

---

*PL-C impl filed — awaiting DESKTOP smoke + Lead APPROVE PL-C.*
