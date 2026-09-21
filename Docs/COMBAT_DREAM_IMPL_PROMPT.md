# Combat & dream implementation prompt (agent / UE Copilot)

Source of truth: `Docs/COMBAT_DREAM_BIBLE.md`.

```
Implement HomeWorld combat/dream stubs per Docs/COMBAT_DREAM_BIBLE.md NOW section only. Docs-first on cloud; DESKTOP Editor for volumes/assets. Do not implement full boss AI, weapons, HP trash UX, GAS combat kit, or homestead combat.

LOCKED NOW
- Win condition everywhere: seal / banish / end evil — NEVER kill/murder fantasy win.
- Homestead: NO combat volumes, NO minigames, NO boss triggers (HOMESTEAD_BIBLE).
- Non-boss planet encounters: four minigame stub interacts with log tags:
  MINIGAME:HEAL, MINIGAME:NURTURE, MINIGAME:GROW, MINIGAME:POSSESS
- Polish-first minigame = Possess (Lead may swap — keep other three as log-only stubs).
  Bridge MOVEMENT possess stub + Docs/21 dream-convert naming; one clearer feedback path for possess only.
- Model boss NOW = placeholder only:
  * Place overlap volume on tutorial planet OR VS_MVP path (Content/DESKTOP — not required in docs-only PR).
  * On enter: read day/night from DAYNIGHT owner → flag DayBoss or NightBoss.
  * Log BOSS:PHASE_DAY or BOSS:PHASE_NIGHT.
  * Optional seal interact → log BOSS:SEAL stub; exit without trash AI or weapon systems.
- Boss day phase design lock: reuse MOVEMENT parkour lite + world interacts (no second CMC).
- Boss night phase design lock: spirit blink / possess / heal-strip on evil’s dream (stub logs OK).
- Forbidden: weapons, HP-primary trash HUD, aggro packs, kill win, second movement component.

FILES (typical — adjust to repo)
- Interact/minigame: extend existing interact or C++ interact ability with idempotent planet markers.
- Boss placeholder: trigger volume actor or BP + overlap handler; phase query from existing day/night subsystem.
- Logging: use project log category (e.g. LogHomeWorld) with exact tags above for PLAYTEST grep.

LATER (do not build): full day+night boss siege, weak-point art, siege objects, polished heal/nurture/grow kits, deep possess puzzles.

DONE WHEN
- One MINIGAME:* log from planet interact
- Possess path once (polished feedback OR stub log MINIGAME:POSSESS)
- Boss volume: day enter → BOSS:PHASE_DAY; night enter → BOSS:PHASE_NIGHT
- Optional BOSS:SEAL stub without full fight
- Homestead still non-combat
- PLAYTEST: planet minigame log → sleep/spirit if testing night boss flag → boss volume day/night logs
```
