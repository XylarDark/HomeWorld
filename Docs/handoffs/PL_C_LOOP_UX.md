# PL-C Thin Loop UX — Handoff

| Field | Value |
|-------|-------|
| **Phase** | PL-C |
| **Status** | **OPEN / IN PROGRESS** — unlocked by Lead **`WAIVE PL-B`**, 2026-09-17 ET |
| **Lead gate** | **`APPROVE PL-C`** before PL-D |
| **Spec** | [16_PLAYABLE_LOOP.md](../16_PLAYABLE_LOOP.md) § PL-C |
| **Canon** | [GATHERABLES_WORLD_STORED.md](../../Lib/03_Gatherables/GATHERABLES_WORLD_STORED.md) |
| **Prior** | PA-07 deferred in [VP_C_POLISH.md](VP_C_POLISH.md) |

## Goal

1. **PA-07 store-transfer** — inventory unit ↔ Stored gatherable count (homestead Stored props).
2. **Thin inventory readout** — on-screen or log-backed 6-slot display — **no new masters**.

## Done criteria

- [ ] Store-transfer interact path works (Spend from inventory → Stored++; or reverse if specced)
- [ ] Inventory readout shows 6 RES_* slots (HUD widget or `INVENTORY:` log dump on key)
- [ ] DESKTOP smoke evidence in this handoff
- [ ] Safe-Build green if C++ touched

## Out of scope

New masters (stay at **10**); full RPG UI; combat; reopening PL-B greps.

## Hard rules

- Docs/07 CLOSED
- No free-flight
- No `.uasset` / `.umap` commits

---

*PL-C stub — OPEN after WAIVE PL-B.*
