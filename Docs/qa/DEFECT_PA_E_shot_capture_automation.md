# DEFECT — PA-E automated Shot 1/2 capture (NOT shotlist PASS)

| Field | Value |
|-------|-------|
| **Date** | 2026-09-22 (ET) |
| **Track** | PA-E (formal Shot 1 + Shot 2 per [00_SHOTLIST.md](../00_SHOTLIST.md)) |
| **Status** | **OPEN** — automation **not** shotlist PASS; Lead capturing manually |

## Symptom

DESKTOP attempts to produce Shot 1/2 stills via **UnrealEditor-Cmd** (`-ExecutePythonScript` + HighResShot) and/or host **ImageGrab** did not yield usable shotlist evidence: missing files, tiny PNGs, nearly black frames (path stones only), or full-desktop grabs with Message Log / chrome.

## Incident — 2026-09-22 ET (Conductor remote, Lead away)

Host Windows **ImageGrab** of the Unreal window during a remote PA-E Shot 1/2 attempt. Evidence staged under **`C:\Users\User\Desktop\HomeWorld_PA_E\`**:

| File | Size (approx.) | Actual content | Shotlist usable? |
|------|----------------|----------------|------------------|
| `Shot1_lookout.png` | ~525 KB | **Grok Bot chat** / Windows desktop — **not** lit viewport / lookout composition | **No** |
| `Shot2_cabin_garden.png` | ~376 KB | Unreal **Editor chrome** (Outliner, Content Browser, “Executing Python Script” banner); partial cabin glow only — **not** clean Shot 2 | **No** |

**Root cause:** Host ImageGrab cannot force a clean lit viewport when **another UI owns focus** (agent chat, panels, or desktop in front of the game view).

## Policy

- **Do not** invent still paths or mark Shot 1/2 **PASS** from automated captures alone.
- **Do not** call host ImageGrab shotlist **PASS** while another UI owns focus.
- **Track close (2026-09-22 ET):** Lead **`APPROVE PA-E`** closed Docs/32 with formal Shot 1/2 stills **deferred/accepted** — this defect and AUTOMATION_GAPS row stay **OPEN** for future automation (no shotlist PASS from ImageGrab files above).
- **Stop grinding remote ImageGrab for PA-E** — focus is not reliable unattended.
- **Future path:** Viewport-only capture API / GUI automation — see [docs/Automation/AUTOMATION_GAPS.md](../../docs/Automation/AUTOMATION_GAPS.md).

## References

- [docs/KNOWN_ERRORS.md](../../docs/KNOWN_ERRORS.md) — PA-E HighResShot / ImageGrab focus entries (2026-09-22)
- [docs/Automation/AUTOMATION_GAPS.md](../../docs/Automation/AUTOMATION_GAPS.md) — PA-E Shot 1/2 gap (2026-09-22)
- [Docs/handoffs/PA_D_IMPORT_PLACE.md](../handoffs/PA_D_IMPORT_PLACE.md) — PA-E owns formal shots; PA-D not CLOSED on shots alone
