# PIN_SYNC_POLICY — DevEnvTemplate pin / sync

**Status:** ACTIVE — from Research EXIT `PIN_SYNC_POLICY_V1` (Lead Do 2026-09-27 ET)  
**Owner:** Conductor proposes · Lead gates SHA · Implement lands four-surface bump PR  
**Pin branch:** DET **`master`** only (`config/devenv-template-pin.json` → `branch`)

Cite: [CURSOR_DEV.md](../../docs/Setup/CURSOR_DEV.md) · EXIT archive Co · dual-source A–E `SYNC.md` fitness greps.

---

## Measured lock (do not treat DET `main` as pin)

| Ref | Role |
|-----|------|
| HW gitlink + `config/devenv-template-pin.json` + CURSOR_DEV table + 13b **canonical** row | Same SHA — contracted pin |
| DET **`master`** | Pin branch tip — must equal pin when healthy |
| DET **`main`** | May diverge (Class D / wrong-base PRs). **Never** point gitlink at `main` while pin.json says `master`. |

Current expected: pin = DET `master`. Tip-vs-`main` “ahead” is **not** automatically a HW pin-hygiene fail.

---

## Change classes

| Class | Meaning | Policy |
|-------|---------|--------|
| **D** Docs-only / fitness-doc (`SYNC.md` greps, CHANGELOG, lean-extra prose, guides) | **MAY_DRIFT** until Lead gate | HW may copy markdown without bump |
| **S** Skills-extras / canon blob (writer `SKILL.md`, `hash-object` Canon line) | **MUST_BUMP_PIN** after commit is on DET **`master`**, same HW PR or immediate follow-up **+** copy extras | Submodule records writer commit |
| **C** Doctor / CLI / dist / sync-layers that inject into HW / package engine | **MUST_BUMP_PIN** (same PR) + `npm run doctor:build` when Class C | Checkout SHA **is** the CLI |
| Rules migration touching alwaysApply trio `07`/`08`/`20` | **NEVER_AUTO** | Wait ALWAYSAPPLY_AUDIT |
| DET PR base `main` while pin is `master` | **NEVER_AUTO** | DET hygiene; merge onto `master` first |
| CAP / EA / product on DET | **NEVER_AUTO** | No pin coupling |

**Default when unsure: NEVER_AUTO.** Conductor names the class; Lead picks SHA from **`master`**.

---

## Four pin surfaces (one HW PR)

| # | Surface | Notes |
|---|---------|--------|
| 1 | git submodule gitlink `DevEnvTemplate` | `git ls-tree HEAD DevEnvTemplate` |
| 2 | `config/devenv-template-pin.json` | `sha`, `shortSha`, `updated`, `note`; `branch` stays `"master"` |
| 3 | `docs/Setup/CURSOR_DEV.md` pin table | Full SHA (CI greps) |
| 4 | `Docs/13b_HR2_B_COLD_CLONE.md` **canonical** SHA row only | Keep dated historical evidence blocks |

Optional same PR: HW extras `SKILL.md` / `SYNC.md` when Class **S** (dual-source sync — not a fifth pin surface).

---

## Ownership

| Act | Who |
|-----|-----|
| Detect class + measure master vs pin vs main | Conductor |
| Propose bump phrase | Conductor |
| Gate / pick SHA / reject `main`-only tips | Lead |
| Four-surface PR (+ doctor:build if C) | Implement |
| Merge HW pin PR | Lead (or Lead-named after greenlight) |
| Land DET commits on **`master`** | Lead (Conductor may open DET PR; base **must** be `master`) |
| eggbot / Design / Test / Fix | Quiet on pin unless Class C changes doctor exit semantics |

---

## Fitness greps (Conductor)

```bash
# A) Pin-surface equality (HW root)
PIN=$(python3 -c "import json; print(json.load(open('config/devenv-template-pin.json'))['sha'])")
BRANCH=$(python3 -c "import json; print(json.load(open('config/devenv-template-pin.json'))['branch'])")
GITLINK=$(git ls-tree HEAD DevEnvTemplate | awk '{print $3}')
test "$PIN" = "$GITLINK"
grep -q "$PIN" docs/Setup/CURSOR_DEV.md
# B) DET pin branch tip
gh api "repos/XylarDark/DevEnvTemplate/commits/$BRANCH" --jq .sha | grep -q "$PIN" || echo "WARN: master tip != pin"
# C) Do not treat DET main as pin
gh api repos/XylarDark/DevEnvTemplate/commits/main --jq .sha   # informational only
# D) A–E canon (when Class S)
git hash-object .agents/skills-extras/architecture-trade-offs-design-depth/SKILL.md
# expect Canon blob from SYNC.md (107a511… until Lead ack change)
```

CI: `scripts/verify-devenv-submodule.sh` enforces surfaces 1–3.

---

## Pin bump now?

**HOLD** unless Lead names a **`master`** SHA that is Class **S** or **C** ahead of current pin.  
Class **D** on DET `main` alone → copy docs or merge onto `master` first — **no** HW pin bump.

---

## Forbidden co-changes

Source/ · Content/ · CAP writers · alwaysApply trio growth · A–E `SKILL.md` body edits unrelated to a Class S bump · AGENTS body dump · pointing pin at DET `main`.

---

## child Research

**N** unless doctor/CLI pin semantics are proven to differ from gitlink+pin.json (then `DOCTOR_PIN_SEMANTICS` only).
