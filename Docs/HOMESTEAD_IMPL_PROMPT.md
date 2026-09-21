# Homestead implementation prompt (agent / UE Copilot)

Source of truth: `Docs/HOMESTEAD_BIBLE.md`.

```
Implement HomeWorld homestead per Docs/HOMESTEAD_BIBLE.md. Change only hub/bounds/glide-start/craft-station files required. Do not invent recipe costs or full family AI — TODO or stub with logs.

LOCKED
- Homestead = safe hub: no combat/damage from combat systems.
- NPC family fantasy; NO co-op MVP.
- Leave island: edge paths → glide DOWN to planet (must land on map); OR moonlight portals (DAYNIGHT). No void-fall death. No invisible walls (rare immersive blockers only mid-map if ever).
- Dusk: no new glide start (DAYNIGHT).
- Limited placeables — not freebuild.
- Crafting outputs ONLY if implementing craft now: tent, torch, taming consumables, healing consumables, fishing consumables/gear. No weapon/armor tree. Schema costs before data.
- Keep bed sleep, store, nurture×2, shrine. Sacred props — don’t delete.
- Camera: Galaxy orbit on hub; iso when build/place (CAMERA_BIBLE).

DONE WHEN
- Edge glide start works from at least one path (or documented TODO with volume name)
- No invisible wall used for island rim
- Hub still non-combat
- If craft stub: one recipe path logs success without adding unrelated systems
- PLAYTEST: walk to edge → glide commit (day); walk hub; confirm no damage volume
```
