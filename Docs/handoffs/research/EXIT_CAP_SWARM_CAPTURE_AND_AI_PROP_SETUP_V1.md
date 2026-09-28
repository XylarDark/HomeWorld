# EXIT CAP_SWARM_CAPTURE_AND_AI_PROP_SETUP_V1

**From:** Lead / Conductor  
**Date:** 2026-09-27  
**HW main:** `e3bc693` · DET pin `0a27306` · prove host `DESKTOP-21CT3H0` (parent MCP/PIE only)  
**Prompt:** `Docs/handoffs/research/PROMPT_CAP_SWARM_CAPTURE_AND_AI_PROP_SETUP_V1.md`

## Diagnosis
Capture stills are weak for semantic prop look / composition / night mood. Reliable bot signals are inventory presence, golden transforms, AABB/overlap/ground, Arrange readiness, and luminance-as-confirm only. Stills-first CAP product Do is folly until identification/scoring clears a high bar; industry practice favors math-first placement with captures as confirm-only.

## Decision table
| Decision | Verdict | Why |
|----------|---------|-----|
| CAP product Do (SC2D revive, stills-first loop, CAP-001 unpark) | **PARK** | Capture ID/scoring not strong enough for swarm develop; Lead reframed |
| Swarm prop develop loop | **Math-first** | inventory → golden transforms → AABB/overlap/ground_z/ray → gate JSON |
| Stills (MRQ / AL diagnostic) | Confirm-only after `Arrange ready: true` | Bots do not PASS semantic look, composition, night mood |
| Prop lighting default | Bright / day | Night lookdev = human later |
| `ready: false` | ≠ closed_fail | Exists-only PNG/JSON ≠ PASS |

## Do bites
### Bite 1 — CAP-INV-SCHEMA (this lap)
- **Host:** CLOUD · **artifact_class:** docs · **prove_size:** one_gate_family · **ladder_step:** 1_cam N/A
- **one unknown:** What frozen fields Design must emit so Implement/Test can score prop presence + pose without a still.
- **Exclusive paths:** `docs/Automation/schemas/prop_inventory.schema.json` (new) · `Docs/handoffs/PROP_INVENTORY_V1.md` (new) · `docs/Automation/ONE_SHOT_BITES.md` (one short subsection pointer only)
- **Forbidden:** Content/Python/** · MRQ/AL/SC2D · .uasset/.umap · Saved/ writers · CAP-001/002 · night stack · ImageGrab · new seats · AGENTS dump · T0 Acts · TOOL SCOUT · marketplace · DESKTOP Act · CAP-PROP-GATE this lap
- **Schema required keys per prop item:** label, class, mesh, golden_transform, aabb, look_at, tod_light, overlap, ground, prove_labels (see Lead BOT CHAT for field constraints)
- **PROP_INVENTORY_V1.md must state:** prove labels ⊆ inventory ∩ world or block Act (soft_fail, closed_fail false); math-first scoring; bright/day default; stills confirm-only later; one PROXY example; pointers to CAPTURE_REDUNDANCY / TEST_SCORE_PACKET / this EXIT
- **child Research:** N

### Bite 2 — CAP-PROP-GATE (after Bite 1 Test PASS — next Conductor paste)
- schemas `prop_arrange_gate.schema.json` · `PROP_ARRANGE_GATE_V1.md` · one CAPTURE_REDUNDANCY policy row
- Still no Python writer, no stills Act, no night bot PASS

## eggbot
N/A

## child Research
N

## Accept checklist
- [x] Diagnosis ranked; math-first vs capture limits split
- [x] PARK CAP product; Do bites one-unknown
- [x] No implement-now / DESKTOP Act / run the prove
- [x] Bright-default + math-first in Decision
- [x] EXIT filed under `Docs/handoffs/research/`
