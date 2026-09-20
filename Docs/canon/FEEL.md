# FEEL.md

**Status:** PARTIAL — numbers from GDD; unknowns marked TODO  
**Sources:** `Docs/01_GDD_MVP.md` Appendix B; `Docs/03_GAMEPLAY_MVP.md`; `Docs/09_FALLBACK_GLIDE.md`

## Target feel

Warm, readable, handmade, hopeful. Routes feel like paths, not sims. Channels short. Soft fails only.

## Tunables (locked from GDD where listed)

| Tunable | Value | Notes |
|---|---|---|
| Cabin → lookout walk | ~15–25 s | V1 |
| Island circuit | ~45–90 s | V1 |
| FALLBACK glide duration | ~12–25 s (preferred constrained was 20–40; FALLBACK armed) | V2 |
| Gather channel | ~1.5–3 s | V3 |
| Portal channel+transit | ~3–6 s | V5 |
| Heal channel | ~2–4 s | V6 |
| Nurture channel | ~2–4 s | V7 |
| Dusk / dawn blend | ~4–8 s | NightMix |
| Tame bond wait | ~3–5 s | V4 |
| Inventory slots / stack | 6 / max 9 | SYS |

## TODO (propose + rationale — do not silently invent in code)

| Tunable | Proposed range | Rationale |
|---|---|---|
| Glide gravity scale / fall speed | 0.35–0.55× default gravity while on FALLBACK spline | Readable arc; not floaty moon-hop |
| Glide lateral influence | 0 if FALLBACK cinematic; else ≤15% corridor width | Canon: FALLBACK = no free steer |
| Camera arm length (3P) | 350–500 UU | Readable character + path |
| Camera pitch bias | −8° to −15° | Slight down for path/landing |
| Night length (full night phase) | 90–180 s real-time before rest prompt | Enough for portal+heal+nurture once |
| Gather node cooldown | Until dawn **or** 60–120 s | Match SYS “deplete until dawn” preference |

Stamp chosen values into `DECISIONS.md` when implemented.
