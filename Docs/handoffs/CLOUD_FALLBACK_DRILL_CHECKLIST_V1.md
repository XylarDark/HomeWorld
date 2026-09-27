# CLOUD_FALLBACK_DRILL_CHECKLIST_V1

**Parent EXIT:** EXIT CLOUD_FALLBACK_DRILL_V1  
**Tip at authoring:** `689563f` (#219)  
**Pin HOLD (do not bump):** `8c4442a`  
**Host:** `CLOUD`  
**Date / TZ:** 2026-09-27 ET  
**Operator:** Conductor-parent  
**Trigger:** `forced-degrade`  
**trigger_kind:** PROXY  
**Actor:** Conductor-parent  
**desktop_claimed:** N  

ProveOps B docs-only. Contents API is CLOUD file I/O degrade only — not a DESKTOP shell.

---

## Preconditions

- [x] Conductor ACCEPT + Lead greenlight
- [x] Pin HOLD `8c4442a`
- [x] CAP-002 Do HELD; no EA SCOUT invented
- [x] Host = CLOUD
- [x] Write path exclusive: this checklist + optional PHASE_BOARD note
- [x] No Task executor; no cloud agent on these paths (forced-degrade)
- [x] Seats quiet; one Conductor digest at Act end
- [x] Writer = Contents API (no local clone push)

---

## Steps

- [x] 1 Record trigger PROXY forced-degrade
- [x] 2 GET SHAs via Contents API
- [x] 3 Branch `cursor/cloud-fallback-drill-b3a5` from main
- [x] 4 PUT this checklist
- [x] 5 Optional PHASE_BOARD Host/ball note (Bite 2)
- [ ] 6 Open PR (filled below)
- [ ] 7 CI validate + python-lint
- [ ] 8 One Conductor digest
- [ ] 9 Lead merge or park

Bite 3 (§14 pointer) **skipped** (reformat risk).

---

## Evidence

```
EVIDENCE CLOUD_FALLBACK_DRILL_V1 | result=PENDING | path=gh Contents API | trigger=forced-degrade | trigger_kind=PROXY | host=CLOUD | desktop_claimed=N | actor=Conductor-parent | digest_count=1 | PR=pending | branch=cursor/cloud-fallback-drill-b3a5 | merge_sha=pending | files=Docs/handoffs/CLOUD_FALLBACK_DRILL_CHECKLIST_V1.md,swarm/PHASE_BOARD.md | pin_hold=8c4442a | cap002=HELD
```

---

## Pass/fail (fill at digest)

| Gate | Bar | Result |
|------|-----|--------|
| H1 Illegal DESKTOP via API | desktop_claimed=N | PASS |
| H2 Host tag | Host=CLOUD | PASS |
| H3 Sanctioned path | path=gh Contents API + trigger token | PASS |
| H4 Writer surface | ⊆ checklist + PHASE_BOARD | PASS (pending PR diff) |
| H5 Pin / blob | pin 8c4442a unchanged | PASS |
| H6 CAP / product | no CAP/EA/Source/Content | PASS |
| W1 G12 | digest_count=1 this Act | PASS (this digest) |
| W2 G9–G11 | non-ball ≤5; @everyone=0 | PASS (seats quiet) |
| C1 CI | validate + python-lint | pending |
| C2 Sample | one PR | pending |
| C3 Single writer | no dual cloud+API | PASS |

**Verdict:** _FALLBACK_OK | FAIL | MEASURE_HOLD (wake)_ — set at digest after CI.

---

## Blockers

none

---

## Did not attempt

MCP · Safe-Build · Editor Python · PIE · DESKTOP Shell · Source/ · Content/ · CAP · pin bump · AGENTS dump · alwaysApply · queue #6–#9 · cloud agent on these paths · Bite 3 §14 rewrite

---

## PR / CI

| Field | Value |
|-------|-------|
| PR URL | pending |
| Branch | `cursor/cloud-fallback-drill-b3a5` |
| Merge SHA | pending |
| CI | pending |
