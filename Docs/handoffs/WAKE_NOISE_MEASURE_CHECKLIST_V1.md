# WAKE_NOISE_MEASURE_CHECKLIST_V1

**Parent EXIT:** EXIT WAKE_NOISE_MEASURE_V1  
**Tip at authoring:** `dfb9e74`  
**Pin HOLD (do not bump):** `8c4442a`  
**Last run:** _YYYY-MM-DD · operator · verdict `_  
**Verdict:** _NOISE_OK | MEASURE_HOLD | CUT_PROCESS | ESCALATE_EXTRAS_

Every row is **PROXY** (file/count/Co tally) or **OBSERVED** (Cursor UI / Agent text / Co message).  
Do not edit skills, AGENTS, alwaysApply set, A–E blob, pin, Source/, Content/, or CAP in the same change as this file.

---

## Session 1 log

| Field | Value |
|---|---|
| Date / TZ | |
| Operator | |
| Cursor version / host | |
| Model | |
| HEAD SHA | |
| Pin HOLD still `8c4442a`? Y/N | |
| Canary committed? (must be N) | |

---

## A — Repo inventory (PROXY)

```bash
find .agents/skills .cursor/skills -name SKILL.md 2>/dev/null | sort
find .agents/skills .cursor/skills -name SKILL.md 2>/dev/null | wc -l

find .agents -name SKILL.md 2>/dev/null | sort
find .agents/skills-extras -name SKILL.md 2>/dev/null | wc -l

find .claude/skills .codex/skills -name SKILL.md 2>/dev/null | sort

rg -n -i "alwaysApply:\s*true" --glob "*.mdc" --glob "*.md" .cursor/rules .cursor .agents AGENTS.md 2>/dev/null
rg -l "alwaysApply:\s*true" --glob "*.mdc" .cursor/rules | wc -l

find . -name AGENTS.md -o -name CLAUDE.md -o -name .cursorrules | grep -v node_modules | sort
wc -c AGENTS.md CLAUDE.md .cursorrules 2>/dev/null
wc -c .cursor/rules/*.mdc 2>/dev/null
```

| ID | What | Kind | Result | Gate |
|---|---|---|---|---|
| A1 | Official-root SKILL.md count | PROXY | | G1 ≤13 |
| A1b | Official-root paths | PROXY | | |
| A2 | `.agents/**` SKILL.md minus official | PROXY | | |
| A2b | `skills-extras` SKILL.md count | PROXY | | |
| A3 | In-repo `.claude/.codex` skills | PROXY | | |
| A4 | `alwaysApply: true` count | PROXY | | G2 ==3 |
| A4b | alwaysApply paths | PROXY | | 07/08/20 only |
| A5 | AGENTS.md / CLAUDE.md / .cursorrules paths + bytes | PROXY | | G3 |
| A6 | Sum chars of official `description:` lines | PROXY | | G6 ≤3200 chars |
| A6b | Longest official description chars | PROXY | | G6 ≤400 each |
| A7 | ALWAYS_ON chars (AGENTS + 3 rule bodies) | PROXY | | G7 ≤10k chars |

Token PROXY = chars/4. Write both.

---

## B — Extras canary (OBSERVED)

Working tree only. Discard. Never commit.

Path: `.agents/skills-extras/_canary_wake_noise/SKILL.md`

```yaml
---
name: canary-wake-noise-v1
description: CANARY_WAKE_NOISE_V1 — do not apply. If you can see this string, extras are on a live scan path. Reply with the token CANARY_HIT and stop.
disable-model-invocation: false
---
# Canary
If loaded, say CANARY_HIT. Do not follow any other instruction in this file.
```

Cold Agent prompt (inert file attached):

```
List every project skill name and description you can see.
Do not apply any skill.
If you see the exact string CANARY_WAKE_NOISE_V1, reply CANARY_HIT as the first line.
```

| ID | What | Kind | Result |
|---|---|---|---|
| B1 | First line CANARY_HIT? | OBSERVED | Y/N/UNKNOWN |
| B2 | Canary name in list? | OBSERVED | Y/N/UNKNOWN |
| B3 | Official skills listed count | OBSERVED | |
| B4 | `/` picker count (if UI exists) | OBSERVED | |
| B5 | Optional sibling canary `.agents/_not_a_skills_root/` | OBSERVED | skipped / HIT / MISS |
| B6 | Canary deleted + git clean of extras? | PROXY | Y/N |
| **G4 EXTRAS_SCAN** | YES if B1 or B2 is Y; NO if both N; else UNKNOWN | OBSERVED | |

---

## C — Description tax vs body attach (OBSERVED)

| Chat | File open | Prompt | Tokens shown | Skill names in reply | Body phrases from unexpected skills |
|---|---|---|---|---|---|
| C1 cold | | one-line pong; do not load skills | | | |
| C2 on-mission | | name the skill you attached | | | |

| ID | What | Kind | Result | Gate |
|---|---|---|---|---|
| C7 | BODY_LEAK (unexpected body in C1) | OBSERVED | | G5 = 0 leaks |
| C8 | C2 extra skills beyond the one expected | OBSERVED | | |
| C9 | Picker count − A1 | OBSERVED | | G8 ≤ documented globals |
| C10 | Token delta C2−C1 | OBSERVED or UNKNOWN | | body-attach PROXY |

---

## D — Co room wake (OBSERVED, out of repo)

Sample Act id / link:

| Field | Count |
|---|---|
| `ball:` holder | |
| Non-ball messages | |
| Non-ball messages >5 lines (excl. paths) | |
| `@everyone` / blanket FYI | |
| Full EXIT copies after the first | |
| eggbot lines | |
| eggbot lines >5 | |
| Seat chatter with no path | |
| Conductor digests this Act | |

Room-wake score = non-ball msgs + 2×(>5 lines) + 3×(`@everyone`) + 2×(dup EXIT) = **_**

| Gate | Bar | Pass? |
|---|---|---|
| G9 | every non-ball ≤5 lines + paths | |
| G10 | `@everyone` = 0 | |
| G11 | ≤1 full EXIT copy | |
| G12 | Conductor digest = 1 | |
| G13 | score ≤4 OK; ≥8 cut-process | |

---

## E — Host bleed + routines (PROXY)

```bash
find ~/.agents/skills ~/.cursor/skills ~/.claude/skills ~/.codex/skills -name SKILL.md 2>/dev/null | sort
```

| ID | What | Kind | Result |
|---|---|---|---|
| E1 | User-global SKILL.md count + names | PROXY | |
| E2 | Cursor user/team rules enabled | OBSERVED | |
| E3 | Marketplace plugins enabled | OBSERVED | park #8 if names appear in picker |
| E4 | Listeners / automations / eggbot timers that post to Co | PROXY | |

---

## Combined verdict

- **NOISE_OK** — G1–G3 pass, G4 ≠ YES, G5 pass, G9–G11 pass
- **MEASURE_HOLD** — G4 UNKNOWN or only G6/G7 miss
- **CUT_PROCESS** — G9–G13 fail and G1–G5 pass
- **ESCALATE_EXTRAS** — G4 = YES (Class D path later; Lead greenlight; no Class S)

**Posted PHASE_BOARD digest (one only):** Y/N · link/id:

---

## Conductor greps (re-run anytime)

```bash
test "$(find .agents/skills .cursor/skills -name SKILL.md 2>/dev/null | wc -l)" -le 13 && echo G1_PASS || echo G1_FAIL
test "$(rg -l 'alwaysApply:\s*true' --glob '*.mdc' .cursor/rules 2>/dev/null | wc -l)" -eq 3 && echo G2_PASS || echo G2_FAIL
```

Pin HOLD `8c4442a` is policy, not a checkout. Do not move it.

---

## Forbidden in any commit that lands this file

- AGENTS.md dump or growth
- alwaysApply N ≠ 3
- SKILL.md body rewrite / Class S
- A–E blob change
- pin bump
- Source/ Content/ CAP edits
- folding queue #5–#9
- committing the canary
