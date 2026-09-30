# NAMING_CONTRACT — the three UserHarness names

**Status:** ACTIVE — from Lead rename of the GitHub repo, 2026-09-30
**Owner:** Conductor enforces A→ Lead gates renames A→ Implement updates every surface in one commit
**Why:** Three names are in play for one thing. Left unstated, the ambiguity regrows link rot — which is exactly what P5 had to clean up.

---

## The three names, and which is which

| # | Name | Where it lives | Mutable by |
|---|------|----------------|-----------|
| 1 | **`XylarDark/UserHarness`** | GitHub repo URL; `.gitmodules` `url`; `remote` in `config/userharness-pin.json`; "Remote" row in [CURSOR_DEV.md](../../docs/Setup/CURSOR_DEV.md) + [13b](../13b_HR2_B_COLD_CLONE.md) | **Lead only**, in GitHub UI. Not a commit. |
| 2 | **`UserHarness/`** | Submodule path on disk; gitlink entry in `git ls-tree`; `path` in `config/userharness-pin.json`; `submodule "UserHarness"` in `.gitmodules` | Commit (P5, done 2026-09-30) |
| 3 | **`DevHarness`** | `productName` in `config/userharness-pin.json`; the `## DevHarness (adopted layers)` heading in `AGENTS.md` | Commit |

**They are not synonyms and must not be interchanged.** 1 and 2 must match — a submodule whose path and URL disagree breaks cold clones. 3 is a prose label and is allowed to differ from 1 and 2.

## The rule that prevents rot

> **If a change touches one of names 1 or 2, it must touch the other in the same commit.**
> Name 3 may be changed independently and never implies a path or URL change.

This is the [PIN_SYNC_POLICY.md](PIN_SYNC_POLICY.md) four-surface rule, narrowed to the naming subset. The full four-surface bump (gitlink, registry, CURSOR_DEV, 13b) is still required when the **pinned SHA** moves. Renaming a path or URL without moving the SHA is a smaller change but obeys the same atomicity rule.

## 2026-09-30 rename, as executed

| Step | Action | Class |
|------|--------|-------|
| 1 | Lead renamed the GitHub repo → `XylarDark/UserHarness` (UI action, outside git) | — |
| 2 | Verified `git ls-remote` on the new URL returns the pinned `a9d1cc47` **before** writing anything | — |
| 3 | P5 had deliberately left the URL as `DevEnvTemplate`, because rewriting it before the rename existed would break every cold clone | — |
| 4 | Committed `435571e`: `.gitmodules` url, pin `remote` + `note`, CURSOR_DEV Remote row, 13b Remote row + its stale "repo has not been renamed" paragraph, PIN_SYNC_POLICY fitness greps, `swarm/SWARM_OPS.md` + `swarm/README.md` links | Name 1 |
| 5 | Re-proved a **real cold clone** of the branch: new URL fetched, landed on `a9d1cc47`, doctor CLI present, `verify-userharness-submodule.sh` exit 0 | — |

### The redirect trap

`https://github.com/XylarDark/DevEnvTemplate.git` **still resolves** — GitHub keeps a redirect for renamed repos, and it serves the same SHA. So a stale URL does not fail loudly. It fails by being *unfalsifiable*: a broken cold clone and a working redirect look identical from the outside.

**Therefore: never accept a green cold clone as proof that the URL is current.** The only check that distinguishes them is that `.gitmodules` and the pin registry *name* the current repo. This is why the cold-clone test above asserts the URL text, not just the resulting SHA.

### Signed archives are not current-state pointers

These still name the old repo and are **deliberately not updated** — they are dated Lead-gate records, and rewriting a signed audit is worse than a stale URL in an archive:

- [08b_HARNESS_GAP.md](../08b_HARNESS_GAP.md) — APPROVED audit
- [08_AUDIT_UPGRADE_STRATEGY.md](../08_AUDIT_UPGRADE_STRATEGY.md) — signed
- [11a_HR_MEASURES.md](../11a_HR_MEASURES.md) — dated measurements

If you are reading one of those for the *current* remote, read this contract instead.

## Enforcement

`scripts/verify-userharness-submodule.sh` checks surfaces 1–3 of the pin (gitlink, registry SHA, CURSOR_DEV) and that the checkout matches. It does **not** check the URL text — that gap is what the redirect trap exploits. Adding a URL assertion is the obvious next hardening step; it is a change to a tracked CI gate, so it needs its own PR.

## Not decided here

The `productName` value `DevHarness` (name 3) does not match either 1 or 2. Keeping it is a deliberate current choice, not an oversight, but it is unresolved branding. Raising it is a Lead taste call, not an agent decision.
