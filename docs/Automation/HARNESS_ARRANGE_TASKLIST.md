# Harness Arrange gate — task list (Lead plan)

**P0 (this PR):** Blocking Arrange gate before PA-E capture Act/Assert.

| ID | Task | Status |
|----|------|--------|
| P0-1 | Shared gate API `arrange_pa_e_shotlist` / `assert_environment_ready` in `pa_e_shotlist_common.py` | Done (PR) |
| P0-2 | Write `Saved/pa_e_arrange_gate.json`; block MRQ/AL when `ready: false` | Done (PR) |
| P0-3 | TMP night fixture re-seed after `load_level` (`vnp_night_tune_and_evidence.reseed_pa_e_tmp_night_fixtures`) | Done (PR) |
| P0-4 | Diagnostic single-write JSON (`level_loaded`, `homestead_night_environment`, `arrange_gate`) | Done (PR) |
| P0-5 | Docs: CAPTURE_REDUNDANCY, KNOWN_ERRORS, AUTOMATION_GAPS, automation-standards | Done (PR) |

**P1 (follow-up):** Three-state reports everywhere (`blocked` / `in_progress` / `pass`) with consistent `closed_fail` semantics across PIE harnesses and NF2-B evidence scripts.

**P2 (follow-up):** Golden-image compare pipeline after a trusted capture path produces lit PNGs (Epic Screenshot Comparison Tool — scout only until Lead gate).

**P3 (follow-up):** Full harness audit — every Editor Python “prove” script calls Arrange or documents why not (non-shotlist tests).

**References:** [CAPTURE_REDUNDANCY.md](CAPTURE_REDUNDANCY.md) § P0 Arrange gate · [pa_e_shotlist_common.py](../../Content/Python/pa_e_shotlist_common.py) · [Docs/00_SHOTLIST.md](../../Docs/00_SHOTLIST.md)
