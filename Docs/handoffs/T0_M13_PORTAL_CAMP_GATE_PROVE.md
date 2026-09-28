# T0_M13_PORTAL_CAMP_GATE - DESKTOP prove packet (Test)

| Field | Value |
|-------|-------|
| **Bite** | `T0_M13_PORTAL_CAMP_GATE_V1` (MUST #13) |
| **Map** | `Maps/VS_MVP` (homestead shrine / camp) |
| **Labels** | `NODE_PORTAL_HOME` / `NODE_PORTAL_CAMP` / `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT` |
| **CAP** | **PARKED** |
| **Impl** | Source wire: `UHomeWorldShrinePortalComponent::TryPortalTransitToDestination` + `AHomeWorldCharacter::TryPortalHomeToCamp` + console `hw.Portal.Camp` (existing `TryPortalTransit` / `HomeWorldShrinePortal*`; no parallel portal service) |
| **Design** | `Docs/handoffs/T0_M13_PORTAL_CAMP_GATE_V1.md` (**untouched**) |
| **Gate JSON (suggest)** | `Saved/t0_m13_portal_camp_gate.json` |

## Arrange

1. PIE `Maps/VS_MVP` -> homestead / body / Day if needed for rune path.
2. **Spirit prereq (#11 path):** `hw.Rune.Unlock` then `hw.Bed.SleepSpirit` -> expect `NODE_BED:` with `TOD_NIGHT_SPIRIT` `FORM_SPIRIT`. Confirm `GetIsSpiritForm`.
3. CAP **PARKED** -- no still product / mood bot PASS.
4. Portal: console `hw.Portal.Camp` (primary). Optional world: Interact (E) home shrine only scores #13 when camp destination wired via `TryPortalHomeToCamp` / camp label -- **not** when `GP_PortalA`<->`B` home<->planet alone.
5. **KEEP-LOCAL:** if `NODE_PORTAL_CAMP` / `GP_PortalCamp` / `GP_RS_HumanoidCamp` marker absent, console soft-latches prove labels -- do **not** commit `.uasset` / `.umap` to add camp marker for this Act.

## Act greps

| Expect | Grep / observe | soft_fail | closed_fail |
|--------|----------------|-----------|-------------|
| Spirit home->camp | Output log contains `NODE_PORTAL_HOME:` with `NODE_PORTAL_CAMP` `TOD_NIGHT_SPIRIT` `FORM_SPIRIT` | Extra already-granted re-log | No portal-camp line; or home<->planet alone scored as #13 |
| Spirit + night | `FORM_SPIRIT` + spirit phase (`GetIsSpiritPhase` / bed path) | Re-sync form noise | Body-form portal scored as #13 |
| Distinct from planet return | `GP_PortalA`<->`B` / `Shrine_Return` / `VS_MARKER_PortalPlanet` alone != #13 PASS | Unrelated FALLBACK Portal transit logs | Treating home<->planet return as home->camp |
| Existing module | Via `TryPortalTransit` / `TryPortalTransitToDestination` / `HomeWorldShrinePortal*` -- **no** parallel portal service | -- | New portal service / invent API |
| Dress-as-camp anti | Shrine dress / planet shrine alone != `NODE_PORTAL_CAMP` | -- | Scoring dress-as-camp as #13 |

## Pass bar (team)

- After #11 spirit path: `hw.Portal.Camp` -> greppable `NODE_PORTAL_HOME:` citing `NODE_PORTAL_CAMP` / `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT`.
- Via existing `HomeWorldShrinePortal*` -- **no** parallel portal service.
- **closed_fail** if home<->planet return alone, body portal, or shrine-dress-as-camp scored as MUST #13.
- KEEP-LOCAL soft latch OK when camp marker missing -- **never** commit `.uasset` / `.umap` for this prove.
- Other T0 MUST **DEFER** (do **not** open #14). Gate #12 auto-advance veto still void. Design invent left **untouched**. No PROP JSON invent.

## DESKTOP prove steps (paste)

1. PIE `Maps/VS_MVP`.
2. `hw.Rune.Unlock` then `hw.Bed.SleepSpirit` -> expect `NODE_BED: TOD_NIGHT_SPIRIT FORM_SPIRIT ...`.
3. **Negative (optional):** body form without spirit -> `hw.Portal.Camp` fails (`need FORM_SPIRIT`); do **not** score as #13.
4. **Negative (optional):** walk `GP_PortalA`<->`B` home<->planet alone -> FALLBACK Portal transit may log, but **no** `NODE_PORTAL_CAMP` prove line; do **not** score as #13.
5. `hw.Portal.Camp` -> expect `NODE_PORTAL_HOME: NODE_PORTAL_CAMP TOD_NIGHT_SPIRIT FORM_SPIRIT` (+ `hw.Portal.Camp ok`).
6. Optional: second `hw.Portal.Camp` -> already granted soft path (still greppable labels).
7. Confirm: `IsPortalHomeToCampGranted`.
8. Other T0 MUST **DEFER**. Optional gate JSON: write `Saved/t0_m13_portal_camp_gate.json` after greps.

## Source symbols (files-only greps)

`TryPortalHomeToCamp` / `IsPortalHomeToCampGranted` / `bPortalHomeToCampGranted` / `TryPortalTransitToDestination` / `TryPortalTransit` / `HomeWorldShrinePortalComponent` / `NODE_PORTAL_HOME` / `NODE_PORTAL_CAMP` / `TOD_NIGHT_SPIRIT` / `FORM_SPIRIT` / `hw.Portal.Camp` / `hw.Bed.SleepSpirit` / `hw.Rune.Unlock` / `closed_fail` (this packet + Design) / home<->planet / body portal / dress-as-camp (anti)

## Architecture Trade-Offs A-E (cite)

| Layer | Decision |
|-------|----------|
| **A - Contract** | Labels `NODE_PORTAL_HOME` · `NODE_PORTAL_CAMP` · `TOD_NIGHT_SPIRIT` · `FORM_SPIRIT`; home->camp pair not planet return |
| **B - Module** | Prefer existing `HomeWorldShrinePortal*` / `TryPortalTransit` -- **no** second portal service |
| **C - Evidence** | Greppable Source emit + this prove packet; CAP **PARKED** |
| **D - Seats** | Implement Act Source; Conductor owns MCP/PIE |
| **E - Stability** | Home<->planet / body / dress-as-camp as #13 = `closed_fail`; no invent portal/WP APIs; no PROP schema invent |

## Conductor note

Conductor owns MCP/PIE cam / still capture. Implement does **not** drive MCP. CAP **PARKED**. #11 bed spirit = **prereq** (run first; do not re-Act beyond unlock/sleep). Suggest gate JSON path: `Saved/t0_m13_portal_camp_gate.json`. Never commit `.uasset` / `.umap`. Design invent untouched. Do **not** open #14. Gate #12 auto-advance veto still void.