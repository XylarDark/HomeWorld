# Docs/17g — HS-G Conductor/DESKTOP Ops Diet

| Field | Value |
|-------|-------|
| **Status** | **DRAFT** — await Lead **`APPROVE HS-G`** |
| **Date** | 2026-09-17 |
| **Author** | Conductor |
| **Parent** | [17_HS_AUDIT_SIGN_OFF.md](17_HS_AUDIT_SIGN_OFF.md) **CLOSED** · [18_VERIFY_PROVE.md](18_VERIFY_PROVE.md) **ACTIVE** (VP2-A PENDING; VP2-B IN PROGRESS success-path) |

**Gate:** Lead **`APPROVE HS-G`**. Do **not** stamp APPROVE in this PR.

---

## Goal

Lock **three** Conductor/DESKTOP ops rules to cut token waste (cloud UE compile ping-pong, soft-reject-as-PASS, MCP/UE hang thrash, status spam) **without** reopening the Docs/17 WAVE audit or inventing a full harness rewrite.

---

## In (only)

| # | Rule | Spec |
|---|------|------|
| **1** | **Evidence policy** | **Soft-reject** (partial greps, MCP crash mid-run, diagnostic-only tables) = **diagnostic** — not a Lead-gate PASS. Lead gates (**`APPROVE VP2-A`**, **`APPROVE VP2-B`**, etc.) require **success-path** log greps (`evidence:grep` PASS or honest MISSING with cause) **or** explicit Lead **`ACCEPT SOFT-REJECT`**. See [17d_HS_EVIDENCE.md](17d_HS_EVIDENCE.md). |
| **2** | **DESKTOP MCP/UE hang budget** | Conductor-parent DESKTOP: **~3 min** wait on MCP/Editor hang → **one** relaunch (Editor + MCP reconnect) → if still hung, **escalate to Lead** with last 40 lines of terminal capture. **No** flag roulette, repeated kill/restart loops, or status spam. |
| **3** | **Cloud UE 5.7 compile hygiene** | Before claiming Safe-Build will pass: cite [docs/KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md) / `unreal-cpp.mdc` pitfalls for the failing API (e.g. `FHitResult`/`ANY_PACKAGE`, `FPaths::IsRelative`, handle APIs). **One fix per compile-fail reply** — no multi-fix shotgun PRs that burn review tokens. |

---

## Out

Doctor rewrite · branch protection apply · new gameplay verbs · AnimGraph work · full Docs/19 harness · HS-H+ product tracks.

**Hard rules unchanged:** Docs/07 CLOSED · FALLBACK only · no combat · no `.uasset`/`.umap` commits · exactly 10 masters.

---

## Deliverables when APPROVED (not in this PR)

| Item | On approve |
|------|------------|
| **Conductor checklist** | Point at Grok Bot skill **HomeWorld desktop prove** (Conductor-owned; not in git) **or** treat **Appendix A** below as canonical |
| **Cross-links** | One-liner from [17d_HS_EVIDENCE.md](17d_HS_EVIDENCE.md) and [18_VERIFY_PROVE.md](18_VERIFY_PROVE.md) prove notes → this doc |
| **UE 5.7 gotchas** | Optional 8–12 lines in an existing CONSOLE/HS-B doc if natural; else keep in **Appendix B** here |

**Board:** HS-G **DRAFT** → on Lead **`APPROVE HS-G`**, stamp this doc **APPROVED / COMPLETE** in-place. Implementation = policy doc + checklist/skill — **no multi-PR WAVE**.

---

## Appendix A — Conductor checklist (repo self-contained)

1. Pull `main`; confirm VP2/HS gate doc open on disk matches PHASE_BOARD.
2. CLOUD: docs/C++ only — no MCP/PIE claims; one compile fix per failure; cite KNOWN_ERRORS first.
3. DESKTOP: Conductor **parent** only; `preflight:ue` exit 0 before PIE; MCP port 55557 green.
4. Run prove → `evidence:grep` → file handoff with honest PASS/MISSING — soft-reject is diagnostic until Lead **`ACCEPT SOFT-REJECT`**.
5. Hang: ~3 min → one relaunch → escalate to Lead; append SESSION_SUMMARY; do not invent next product track.

---

## Appendix B — UE 5.7 gotchas (compile/review)

- **`ANY_PACKAGE`** removed — use `nullptr` in `FindObject`/`LoadObject`.
- **`FPaths::IsRelativePath`** → **`FPaths::IsRelative`**.
- **Python `get_actor_bounds()`** — UE 5.7 returns `(origin, extent)` tuple; old out-param form silently fails.
- **MCP `blueprint_name`** — short name only; never full `/Game/...` path (Editor crash).
- **Global name collisions** — prefix project constants; avoid bare `BufferSize`-style names in headers.

Full table: [docs/KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md) · [unreal-cpp.mdc](../.cursor/rules/unreal-cpp.mdc).

---

*DRAFT — await Lead **`APPROVE HS-G`**. Does not reopen Docs/17 or change VP2-A/B gate strings.*
