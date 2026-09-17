# PL-C Thin Loop UX — Handoff

| Field | Value |
|-------|-------|
| **Phase** | PL-C |
| **Status** | **EVIDENCE COMPLETE — PENDING LEAD `APPROVE PL-C`** |
| **Lead gate** | **`APPROVE PL-C`** before PL-D |
| **Spec** | [16_PLAYABLE_LOOP.md](../16_PLAYABLE_LOOP.md) § PL-C |
| **Tip** | `ade3aaf` (PR #80 + #81) — DESKTOP **DESKTOP-21CT3H0** |

## Shipped (repo)

| Item | Path |
|------|------|
| Store-transfer | `HomeWorldStoreTransferComponent` — `STORE: deposit` / `STORE: withdraw` |
| Store prop | `AHomeWorldStoreProp` |
| Interact | `TryStoreTransferInFront` (day/body, before harvest) |
| HUD | Six `Inv[n]:` lines |
| Console | `hw.Inventory.Dump` → `INVENTORY:` |
| Placement | `place_vs_mvp_store_transfer.py` |

## DESKTOP evidence (2026-09-17 ET)

| Check | Result |
|-------|--------|
| Safe-Build | **PASS** — exit 0 (~13:02 ET); log `Saved/PL_C_safe_build.txt` |
| Place script | **PASS** — `StorePlace: DONE 6/6`; `Saved/PL_C_place.json` `ok: true` |
| Classes | `GP_Store_{WOOD,FIBER,STONE,BERRY,HERB,SEED}` = `HomeWorldStoreProp` |
| PIE deposit/withdraw greps | **PENDING Lead** (human Alt+P or console in PIE) — automation PIE still unreliable; not invented |

## Done criteria

- [x] Store-transfer interact path in C++
- [x] Inventory readout (HUD + log dump)
- [x] DESKTOP Safe-Build + placement smoke
- [ ] Lead **`APPROVE PL-C`** (optional: one PIE deposit line when back)

## Hard rules

- Docs/07 CLOSED; no free-flight; no new masters; no `.uasset` commits

---

*PL-C — stop for Lead **`APPROVE PL-C`** before PL-D.*
