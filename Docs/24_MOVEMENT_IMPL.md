# Docs/24 — Movement implementation (MV)

| Field | Value |
|-------|-------|
| **Status** | **MV STRATEGY APPROVED** — Lead **`MV-A`** / **`APPROVE MV STRATEGY`**, 2026-09-21 ET; **MV-A IN PROGRESS** (await Lead **`APPROVE MV-A`**) |
| **Date** | 2026-09-22 |
| **Bible** | [MOVEMENT_BIBLE.md](MOVEMENT_BIBLE.md) · [MOVEMENT_IMPL_PROMPT.md](MOVEMENT_IMPL_PROMPT.md) |
| **Parallel tracks** | [23_COMBAT_DREAM_IMPL.md](23_COMBAT_DREAM_IMPL.md) **CLOSED** · [22_GATHER_CRAFT_IMPL.md](22_GATHER_CRAFT_IMPL.md) **CLOSED** |
| **Prefix** | **MV** — do not reuse GC / CD / RS gate strings |

---

## Gate

Lead **`APPROVE MV STRATEGY`**, 2026-09-21 ET — **GRANTED** (chat: Lead typed **`MV-A`** → strategy unlock + MV-A work; **do not** stamp MV-A APPROVED until Lead closes track).

**MV-A:** Implementation in flight on branch `cursor/mv-a-traversal-stubs-9f77`. Lead **`APPROVE MV-A`** closes Docs/24 track (same pattern as CD-A on Docs/23).

**Do not stamp phase APPROVED in a PR** — Lead types the gate string in chat.

---

## Goal (MV-A NOW)

Traversal stubs on **one CMC** per locked bible: body sprint + parkour-lite mantle/vault, FALLBACK glide preserved, spirit blink (no flight), mount speed mode after tame.

| Deliverable | Log tags |
|-------------|----------|
| Hold sprint (Shift / IA_Dodge Started/Completed) | `MOVE: form_tune` · MaxWalkSpeed bump (no separate mover) |
| Mantle / vault (jump at ledge or `hw.Move.Mantle`) | `MOVE: MANTLE` · `MOVE: VAULT` |
| Spirit blink (spirit form + R / `hw.Move.Blink`) | `MOVE: SPIRIT_BLINK` or hook line if no anchor |
| Mount / companion boost after tame | `MOVE: mount_boost on` |
| Long fall | `MOVE: soft_reset fall` |
| FALLBACK glide | existing `FALLBACK:` logs; **dusk** blocks new start |

**PLAYTEST sentence:** day walk → sprint → vault/mantle → edge glide down; night sleep → spirit blink toward shrine anchor.

---

## Tracks (Lead gates)

| Track | Name | Host | Status | Gate |
|-------|------|------|--------|------|
| **MV STRATEGY** | Bible + impl unlock | Lead | **APPROVED** | Lead **`APPROVE MV STRATEGY`** / **`MV-A`** unlock, 2026-09-21 ET |
| **MV-A** | NOW traversal stubs | CLOUD+DESKTOP | **IN PROGRESS** | Lead **`APPROVE MV-A`** (pending) — [handoffs/MV_A_TRAVERSAL.md](handoffs/MV_A_TRAVERSAL.md) |

---

## Code map

| Piece | Path |
|-------|------|
| Traversal (MV-A) | `Source/HomeWorld/HomeWorldTraversalComponent.*` |
| Character wiring | `HomeWorldCharacter.*` (Jump → mantle, sprint, spirit blink) |
| FALLBACK dusk gate | `HomeWorldFallbackGlideComponent.cpp` |
| Mount hook | `HomeWorldBeastTameComponent.cpp` → `SetMountBoostActive` |
| Cheats | `hw.Move.Mantle`, `hw.Move.Blink` in `HomeWorld.cpp` |
| Handoff | [handoffs/MV_A_TRAVERSAL.md](handoffs/MV_A_TRAVERSAL.md) |

---

## DONE-WHEN (MV-A)

- [ ] DESKTOP: `.\Tools\Safe-Build.ps1` compile C++
- [ ] PIE day: hold Shift sprint; jump or `hw.Move.Mantle` at ledge → `MOVE: MANTLE` or `MOVE: VAULT`
- [ ] PIE day: interact glide start → `FALLBACK: StartGlide`; dusk (`hw.TimeOfDay.SetPhase 1`) blocks new start
- [ ] PIE night: `hw.GoToBed` or bed → spirit form; R or `hw.Move.Blink` → `MOVE: SPIRIT_BLINK` (or hook log if no anchor)
- [ ] After tame near player → `MOVE: mount_boost on`; walk speed uses same CMC
- [ ] Lead **`APPROVE MV-A`** → track **CLOSED / COMPLETE**

**Grep:** `MOVE:` · `FALLBACK:` in Output Log / `Saved/Logs/HomeWorld.log`

---

## Approval ladder

| Step | Lead action | Unlocks |
|------|-------------|---------|
| 0 | **`APPROVE MV STRATEGY`** (or **`MV-A`** unlock chat) | MV-A stubs — **DONE** 2026-09-21 ET |
| 1 | **`APPROVE MV-A`** | Docs/24 track complete — **pending** |

```
Docs/23 Combat & Dream: CLOSED / COMPLETE — Lead APPROVE CD-A 2026-09-21 ET
Docs/24 Movement: MV STRATEGY APPROVED — MV-A IN PROGRESS
```

---

## MV-B+ (locked — not NOW)

PoE-scale procgen, spirit flight, full parkour kit, swim, second CMC, free-flight upgrade of FALLBACK — **do not implement** without a new Lead track.

**Future (not MV-A):** spirit stealth + spirit torches — locked in [SPIRIT_STEALTH_BIBLE.md](SPIRIT_STEALTH_BIBLE.md) (**SS-A** later); MV-A does not implement torch detection, stealth meters, shadow volumes, or found-out fail loops.
