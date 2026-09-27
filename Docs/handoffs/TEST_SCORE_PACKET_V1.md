# TEST_SCORE_PACKET_V1 — Test score extract contract

**Parent EXIT:** EXIT TEST_GATE_SCHEMA_LEAN_V1  
**Tip at authoring:** `95618e4` (#220)  
**Pin HOLD (do not bump):** `8c4442a`  
**Schema:** `hw.test_score_packet/v1` → [test_score_packet.schema.json](../../docs/Automation/schemas/test_score_packet.schema.json)

Test scores this **extract packet**, not the full writer dump under `Saved/`. Writers stay fat (DESKTOP Fix). No Python Do in this track.

**PROXY** = docs/schema bind. **OBSERVED** = values copied from disk after Act.

---

## LOAD-BEARING (must remain on disk; packet copies these)

| Field | Surface | Why |
|-------|---------|-----|
| `ready` | PA-E arrange gate | Pre-Act. `false` → **block Act**, not closed FAIL. |
| `ready_for_ps_c` | PS arrange gate | Map → `arrange.ready` in packet. Do not rename writer. |
| `blocked_reasons[]` | gates + blocked report | Missing setup vs quality miss. |
| `capture_outcome` ∈ {`pass`,`soft_fail`,`closed_fail`} | capture report | Canon three-state. |
| `ok` | capture report | `true` **only** on full `pass`. |
| `closed_fail` | report + validation | Proved-wrong only. Arrange block stays `false`. |
| `prove_loop_status` ∈ {`blocked`,`in_progress`,`pass`} | report | Arrange block → `blocked` + `closed_fail: false`. |
| `capture_pass` | report | Harness only ≠ visual. |
| `visual_framing_pass` | report | Needs Lead `lead_visual_framing_approved`. |
| `capture_outcome_open` | report | `true` iff `soft_fail`. |
| `artifact_stamps.*.bytes` + `mtime` (+ `mtime_iso`) | stamps | Score bar. **`exists` alone is not PASS** (`file_exists_alone_is_not_pass`). |
| `artifact_stamps.*.exists` | stamps | Necessary but **insufficient**. |
| luminance metrics + `luminance_pass` | validation | Real metrics. |
| `shot_pair` diversity | report | Blocks identical-scrap false PASS. |
| `visible_sky_stack_ok` | lighting | Soft vs void closed. |
| `aim_ok` + `forward_ray_hits_dress_aabb` | aim / framing | Aim miss with lit scrap → closed. |

**Must NOT delete** from writers or canon: the rows above plus `file_exists_alone_is_not_pass` language in CAPTURE_REDUNDANCY / PROVE_CRITERIA.

---

## REDUNDANT for Test packet (LEAVE on writers)

`lead_prove_loop`, `universal_testing_preconditions`, `prove_criteria` prose, `desktop_conductor_checklist`, `capture_outcome_semantics`, `policy`, `mrq_pie_lighting_note`, embedded `MRQ_LATENT_WAIT_CONTRACT`, nested inventory/aim poses/full lighting dumps, `Saved/pa_e_homestead_capture_diagnostic.json` as score input.

---

## Packet shape (`hw.test_score_packet/v1`)

```yaml
schema: hw.test_score_packet/v1          # PROXY
act_sha: <40-hex>                        # PROXY bind — Act packet / git tip (writer emit = child park)
track: PA-E | PS | <named>
artifact_class: gate | metrics | stills | docs
score_paths:
  arrange_gate: Saved/*_arrange_gate.json | Saved/*_gate.json
  capture_report: Saved/*_capture_report.json | Saved/*_gate.json
arrange:
  ready: bool                            # PS: ready_for_ps_c → ready
  blocked_reasons: [string]
three_state:
  capture_outcome: pass | soft_fail | closed_fail
  ok: bool
  closed_fail: bool
  prove_loop_status: blocked | in_progress | pass
  capture_pass: bool
  visual_framing_pass: bool
  lead_visual_framing_approved: bool
stamps:
  - path: string
    exists: bool
    bytes: int | null                    # required if exists
    mtime: number | null                 # required if exists
metrics:
  luminance_pass: bool | null
  mean_luminance: number | null
  center_crop_mean_luminance: number | null
  fraction_l_gt_1: number | null
  fraction_l_gt_8: number | null
```

---

## Three-state mapping (locked — do not invert)

| Condition | `capture_outcome` | `ok` | `closed_fail` | `prove_loop_status` |
|-----------|-------------------|------|---------------|---------------------|
| Arrange `ready:false` / blocked report | `soft_fail` | false | **false** | `blocked` |
| File present, black/dark/empty RT, setup ready | `soft_fail` | false | false | `in_progress` |
| Harness green, Lead visual not stamped | `soft_fail` | false | false | `in_progress` |
| Harness + `lead_visual_framing_approved` | `pass` | **true** | false | `pass` |
| Missing/wrong setup after Act attempted | `closed_fail` | false | **true** | `blocked` |
| Proved wrong (`void_still_after_visible_sky_stack`, `framing_aim_proven_miss`) | `closed_fail` | false | true | `blocked` |
| `exists:true` and no bytes/mtime/metrics | **FAIL the score** (exists-only) — never emit `pass` | — | — | — |

**Arrange-block ≠ closed FAIL.** Canon: CAPTURE_REDUNDANCY + `write_blocked_capture_report`. (testing-standards skill drift → queue #7 — not this bite.)

---

## One score per Act SHA

1. Bind `act_sha` from Act packet / `git rev-parse HEAD` at Act start (PROXY).
2. Second score on same SHA without Fix Research EXIT → **reject**.
3. Arrange missing or `ready`/`ready_for_ps_c` false → soft_fail / block. No invent retry.
4. Stamps missing `bytes` or `mtime` when `exists` → score invalid (exists-only process fail).
5. Else read `capture_outcome`. Do not infer `pass` from `exists`.
6. Taste / framing → `visual_framing_pass` false until Lead `APPROVE-*`.

---

## PROXY vs OBSERVED

| Item | Label |
|------|-------|
| This card + JSON Schema | PROXY |
| `act_sha` on packet | PROXY (writer emit parked) |
| `ready`, three-state, stamps bytes/mtime, luminance | OBSERVED (already written) |

---

## Greps (Conductor / Test)

```bash
grep -E 'soft_fail|closed_fail|mtime|bytes|capture_outcome' \
  Docs/handoffs/TEST_SCORE_PACKET_V1.md \
  docs/Automation/schemas/test_score_packet.schema.json
grep -n 'prove_loop_status\|closed_fail: false\|exists-only\|file_exists_alone_is_not_pass\|never exists-only' \
  Docs/handoffs/TEST_SCORE_PACKET_V1.md
```
