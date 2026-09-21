# Movement implementation prompt (agent / UE Copilot)

Source of truth: `Docs/MOVEMENT_BIBLE.md`.

```
Implement HomeWorld movement per Docs/MOVEMENT_BIBLE.md NOW section only. Change only character / glide / mantle / mount-mode files required. Do not implement procgen, spirit flight, or full parkour.

LOCKED NOW
- One CharacterMovementComponent (or equivalent). No second mover.
- Body: readable walk, hold sprint mild boost, small jump, 1–2 mantle/vault max.
- Mount/companion early: speed mode on SAME CMC after tame — no parallel movement system.
- Island→planet: FALLBACK glide down only; edge commit; dusk blocks new glide start; must hit planet map.
- Spirit NOW: floatier walk + short blink/teleport to shrine/anchors. No spirit flight. Possess = stub only if touched.
- No invisible walls on island rim. Soft reset on long falls.
- Keep day reap / night sow. Camera-relative move (CAMERA_BIBLE).

LATER (do not build): PoE map gen, full parkour, spirit flight, deep possess, swim.

DONE WHEN
- Sprint + one vault/mantle work on tutorial path
- Edge glide down still works (FALLBACK)
- One spirit blink after sleep (or TODO log with named hook)
- Mount/boost mode uses one CMC
- PLAYTEST sentence: day walk→vault→edge glide; night sleep→spirit blink
```
