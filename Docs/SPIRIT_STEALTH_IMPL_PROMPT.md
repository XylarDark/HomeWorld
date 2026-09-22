# Spirit stealth implementation prompt (agent / UE Copilot)

Source of truth: `Docs/SPIRIT_STEALTH_BIBLE.md`.

**Gate:** **SS-A** — separate from **MV-A** (Movement, GitHub **#130**). Do **not** fold spirit stealth into MV-A scope; open SS-A only after Lead **`APPROVE SS STRATEGY`** (or equivalent).

```
Implement HomeWorld spirit stealth per Docs/SPIRIT_STEALTH_BIBLE.md NOW (SS-A) only.

LOCKED NOW (SS-A)
- Applies to SPIRIT FORM ONLY after sleep→spirit (DAYNIGHT_BIBLE). Body form ignores spirit lit/alert except body torch darkness kidnap (unchanged).
- Default: spirit player hidden / stealth fantasy — NO crouch verb, NO sneak stance, NO kill-on-detect.
- Reveal: thin overlap volumes on campfire, NPC-carried torch (placeholder volume on NPC), spirit torch — entering sets spirit LIT.
- Found-out = A2: alert/pressure rises in LIT; player flees light or finishes interact before peak — NOT shrine kidnap, NOT combat.
- Two torch systems: body/mundane torch = mundane light + body darkness safety ONLY; spirit torch volume = light AND reveals spirits — do not merge into one undifferentiated flag.
- Logs (minimum): STEALTH: LIT enter | STEALTH: ALERT | STEALTH: CLEAR on state transitions / threshold ticks.
- Optional: haste window — interact completion must finish before alert peak when lit (stub timer OK).
- Volumes only for NOW — no full AI vision cones unless implemented as thin overlap proxies.
- HOMESTEAD: no detection combat. COMBAT_DREAM minigames unchanged.

FORBIDDEN IN SS-A
- Crouch stealth
- Spirit flight escape
- Homestead alert/combat
- Merging body torch reveal with spirit torch reveal
- Replacing body no-torch kidnap with spirit alert peak

LATER (do not build in SS-A): NPC torch AI carry, full alert UI, spirit torch craft recipe, detection VFX polish.

DONE WHEN
- Spirit enters campfire (or stub torch) volume → STEALTH: LIT enter
- Alert rises while lit → STEALTH: ALERT (at least once)
- Exit volume → STEALTH: CLEAR
- No crouch binding added
- PLAYTEST sentence: sleep→spirit→skirt campfire edge→lit→alert→back to dark→clear
- MV-A (#130) PR explicitly does NOT claim this done-when — SS-A only
```
