# TASTE_GATE_SCOPE_R4

- **Id:** SCOPE-R4
- **Date:** 2026-09-24
- **Status:** RESOLVED 2026-09-24 — harness now; reference compare waits for a stamped reference and `APPROVE TOOL SCOUT`
- **Picker:** reuse the still harness; no golden diff in this slice
- **Chat revision:** a still compared to an already-established reference image may be the cheap check
- **Candidate:** `TP-CAND-SCOPE-R4` staged (not promoted)
- **Prior:** Round 3 promoted — special cases out; one day-and-night loop

Owner: human — what an automated “looks proper” check is allowed to decide
Job: taste
Recommend: reuse the still harness in `Content/Python/pa_e_shotlist_common.py` (`analyze_png_luminance_content`); framing and mood stay PS-D eyeball ([Docs/33_PLACEMENT_STILLS.md](../33_PLACEMENT_STILLS.md))
After you pick: promote or reject; do not build a suite in this turn
