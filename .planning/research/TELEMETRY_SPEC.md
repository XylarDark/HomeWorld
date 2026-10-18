# Telemetry spec (research deliverable)

**Source:** Phase 8 research (R-8-1), 2026-10-17.  
**Status:** Draft — pending Lead adoption.  
**Canon impact:** none yet. Engineering spec, not canon.

## Instrumentation order

1. **Session + onboarding telemetry** — before public playtests.
2. **Level-funnel events** — before Early Access.
3. **Full attribution** (UTM, traffic sources) — before paid spend.

## Minimum demo funnel (for EA)

- [ ] Wishlist velocity tracked weekly (not just total).
- [ ] Traffic source breakdown: organic / paid / social, separately.
- [ ] Steam UTM cost-per-wishlist divided by 2–4× (attribution undercounts) before trusting.
- [ ] Session + onboarding telemetry live before next public playtest.
- [ ] First-time player completion rate measured; flag if <70%.
- [ ] Owned channel (email list) independent of Steam notifications.

## Custom game events (HomeWorld-specific)

| Event | When | Metadata |
|-------|------|----------|
| `session_start` | Game launched | commit sha, map, timestamp |
| `form_change` | Body ↔ spirit | trigger (bed/sleep/dawn/bonk), stacks before/after |
| `bonk` | Player bonked home | location, stacks, context (gather/ease/glide) |
| `gather` | Resource gathered | RES_ID, node type, inventory before/after |
| `tame_attempt` | Beast encounter | outcome (tamed/charge/booted), herb in hand, threat level |
| `heal` | Spirit healed | spirit id, resource spent, count healed so far |
| `nurture` | Target nurtured | target id (crop/stored), resource spent |
| `portal` | Portal transit | direction (home→planet / planet→home / home→camp) |
| `glide` | Cloud descent | duration, wisp collected, landing success |
| `ease` | Camp actor eased | actor id (guard/sleeper A/B), outcome (success/weak hit/bonk), stacks |
| `rescue_attempt` | Free captive attempted | gate state (all 3 calm?), outcome (freed/refused) |
| `loop_complete` | Dawn after night loop | resources gathered, spirits healed, nurtured count, time taken |
| `drop_off` | Player quits mid-session | last event, location, time in session |

## Save system design (unspecified — needs decision)

- **Autosave cadence:** on form change (bed sleep, dawn), on rescue, on zone transition. Not continuous.
- **Failure recovery:** if save corrupt, fall back to last valid save + log. Never lose more than one loop.
- **Slots:** single slot for MVP (no multiplayer, no multiple saves). EA may add 3 slots.
- **Cloud saves:** Steam Cloud for EA (standard).

## Stack recommendation

- **MVP (free/cheap):** Steam Stats (aggregated ints/floats) + a simple custom event log written to a local file, uploaded on next session start. No backend needed initially.
- **EA:** PlayFab or a lightweight custom pipeline (Azure/Supabase) for real-time analytics. One developer can build this in weeks (AWS Breakaway precedent).
- **Privacy:** Steam data rules; disclose in store page; no PII beyond Steam ID.