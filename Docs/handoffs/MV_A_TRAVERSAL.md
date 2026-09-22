# MV-A — Movement traversal stubs (handoff)

| Field | Value |
|-------|-------|
| **Status** | **IN PROGRESS** — await Lead **`APPROVE MV-A`** |
| **Track** | MV-A |
| **Gate** | Lead **`APPROVE MV STRATEGY`** — **GRANTED** 2026-09-21 ET (Lead typed **`MV-A`**) |
| **Close gate** | Lead **`APPROVE MV-A`** (pending) |
| **Impl doc** | [24_MOVEMENT_IMPL.md](../24_MOVEMENT_IMPL.md) |
| **Bible** | [MOVEMENT_BIBLE.md](../MOVEMENT_BIBLE.md) |

---

## Scope

- **One CMC** — `UHomeWorldTraversalComponent` tunes the existing `CharacterMovementComponent` only
- Body: sprint (Shift hold), jump + mantle/vault lite, soft fall reset
- Spirit: floatier gravity + blink to tagged anchors (no flight)
- Tame → mount boost on same CMC
- FALLBACK glide unchanged path; **dusk** blocks new glide start
- Possess remains CD stub — do not deepen

---

## DESKTOP chain

```text
.\Tools\Safe-Build.ps1
# PIE VS_MVP / markers map — LogTemp / LogHomeWorld
```

| Step | Action | Expected log |
|------|--------|--------------|
| 1 | Day PIE: hold Shift, walk | faster MaxWalkSpeed (no extra log required) |
| 2 | Face low ledge, jump or `hw.Move.Mantle` | `MOVE: MANTLE` or `MOVE: VAULT` |
| 3 | `GP_GlideStart` interact (day) | `FALLBACK: StartGlide` |
| 4 | `hw.TimeOfDay.SetPhase 1` (dusk), retry glide | `FALLBACK: StartGlide blocked — dusk buffer` |
| 5 | `hw.GoToBed` or bed interact | `FORM: spirit` |
| 6 | Press R (spirit shield key) or `hw.Move.Blink` | `MOVE: SPIRIT_BLINK` or hook if no anchor |
| 7 | Tame beast to `tamed` near player | `MOVE: mount_boost on` |

**Cheats:** `hw.Move.Mantle` · `hw.Move.Blink`

---

## Spirit anchors

Blink targets actors tagged **`SpiritAnchor`**, **`SpiritBlink`**, **`Shrine_POI`**, or **`ShrinePortal`**. If none in level, blink logs a **named hook** so placement can be added later (`GP_SpiritAnchor` editor label also resolved in editor builds).

---

## Files touched (MV-A)

| Area | Files |
|------|-------|
| C++ | `HomeWorldTraversalComponent.*`, `HomeWorldCharacter.*`, `HomeWorldFallbackGlideComponent.cpp`, `HomeWorldBeastTameComponent.cpp`, `HomeWorld.cpp` |
| Docs | `24_MOVEMENT_IMPL.md`, `canon/DECISIONS.md`, this handoff |

---

## Done criteria

- [ ] Sprint + mantle/vault log `MOVE:*`
- [ ] FALLBACK glide still works; dusk blocks new start
- [ ] Spirit blink once after sleep/spirit form (`MOVE: SPIRIT_BLINK` or hook)
- [ ] Mount boost uses one CMC after tame
- [ ] Lead **`APPROVE MV-A`** → [Docs/24](../24_MOVEMENT_IMPL.md) **CLOSED / COMPLETE**

---

## Forbidden (recheck)

Procgen, spirit flight, full parkour kit, second CMC, swim, free-flight upgrade of FALLBACK, invisible rim walls.
