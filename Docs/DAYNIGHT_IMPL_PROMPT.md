# Day/night implementation prompt (agent / UE Copilot)

Source of truth: `Docs/DAYNIGHT_BIBLE.md`.

```
Implement HomeWorld day/night per Docs/DAYNIGHT_BIBLE.md. Change only time/form/portal/glide-gate/sleep files required. Do not invent day length numbers or torch economy — mark TODO or use existing cheats.

LOCKED
- One GameState (or equivalent) owns phase: Dawn → Day → Dusk → Night. Immersive full phases (taste). Lengths = TODO until Lead playtest stamp.
- Dusk = still day for rules. Buffer to reach sleep. Block NEW glide starts in dusk. Glide = down only (island→planet), body, FALLBACK/canon path.
- Spirit form ONLY via sleep: homestead bed OR campsite (cleared humanoid camp OR pitched tent+campfire). No auto-spirit on clock.
- Portals: active in moonlight/night; work for body AND spirit; between places AND up to HomeWorld island. Day = portals off.
- No torch + exposed darkness at night = soft kidnap to nearest shrine → teleport HomeWorld (skip/cut night). Not combat. Rare preparedness fail.
- Spirit still out at dawn → spirit sickness debuffs (magnitudes TODO).
- Homestead non-combat. No free-flight. No parallel time system. No dedicated FP.

DONE WHEN
- Phase can be set/observed (existing hw.TimeOfDay.SetPhase OK for prove)
- Sleep interact toggles spirit per bible; dusk blocks glide start
- Portal usable only when night/moonlight; proves body or spirit once
- Dark+no-torch path logs soft kidnap → shrine → home (or TODO stub with Lead-visible log)
- PLAYTEST note appended: one dusk buffer run + one sleep→spirit + one portal up (or listed TODOs if torch/camp not spawned yet)
```
