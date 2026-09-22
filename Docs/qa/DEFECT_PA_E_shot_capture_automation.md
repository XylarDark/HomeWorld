# DEFECT — PA-E automated Shot 1/2 capture (NOT shotlist PASS)

| Field | Value |
|-------|-------|
| **Date** | 2026-09-22 (ET) |
| **Track** | PA-E (formal Shot 1 + Shot 2 per [00_SHOTLIST.md](../00_SHOTLIST.md)) |
| **Status** | **OPEN** — automation **not** shotlist PASS; Lead capturing manually |

## Symptom

DESKTOP attempts to produce Shot 1/2 stills via **UnrealEditor-Cmd** (`-ExecutePythonScript` + HighResShot) and/or host **ImageGrab** did not yield usable shotlist evidence: missing files, tiny PNGs, nearly black frames (path stones only), or full-desktop grabs with Message Log / chrome.

## Policy

- **Do not** invent still paths or mark Shot 1/2 **PASS** from automated captures alone.
- **Do not** claim **`APPROVE PA-E`** or close the PA track from this defect stub.
- **Current path:** Lead **manual viewport capture** for Shot 1 and Shot 2; attach to PA-E handoff when ready.

## References

- [docs/KNOWN_ERRORS.md](../../docs/KNOWN_ERRORS.md) — PA-E HighResShot / ImageGrab / Rotator entries (2026-09-22)
- [docs/Automation/AUTOMATION_GAPS.md](../../docs/Automation/AUTOMATION_GAPS.md) — PA-E Shot 1/2 gap (2026-09-22)
- [Docs/handoffs/PA_D_IMPORT_PLACE.md](../handoffs/PA_D_IMPORT_PLACE.md) — PA-E owns formal shots; PA-D not CLOSED on shots alone
