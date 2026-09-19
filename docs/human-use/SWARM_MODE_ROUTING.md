# Swarm vs non-swarm mode routing

**When to use:** At the **start of every task** (and when the ask pivots), choose a mode before loading Conductor kits, specialist role cards, or Blender MCP waves. Goal: **token efficiency** — do not pay swarm context tax for UE engineering, and do not run lookdev as a flat coding chat when specialists + gates are required.

**Canonical skill:** [.agents/skills/swarm-mode-routing/SKILL.md](../../.agents/skills/swarm-mode-routing/SKILL.md)  
**Research log:** [SWARM_ROUTING_RESEARCH.md](../Automation/SWARM_ROUTING_RESEARCH.md)  
**Swarm process:** [swarm/SWARM_OPS.md](../../swarm/SWARM_OPS.md) · **Boot:** [START_HERE.md](../../START_HERE.md)

---

## Modes (pick exactly one)

| Mode | What loads | Cost profile |
|------|------------|--------------|
| **NON-SWARM** | `AGENTS.md`, targeted `docs/` + source, MCP/Safe-Build as needed | Default — lowest context |
| **SWARM** | Conductor chat + thin role card + wave packet only; `PHASE_BOARD` row; Lead gates | Higher — specialists on demand |
| **HYBRID** | Non-swarm implement chat; Conductor (or Lead) only for gate / AD taste / board stamp | Medium — split chats by job |

Agents **do not invent** `APPROVE Pn` in any mode ([OWNERSHIP.md](OWNERSHIP.md)).

---

## Detection protocol (ordered)

Run top-down. **First match wins.** State the chosen mode in one line before heavy tool use.

### 1 → SWARM (or recommend Conductor boot)

Any of:

- User opened / asked for **Conductor**, pasted a **wave packet**, or typed Lead strings (`APPROVE P0`…`P7`, `FALLBACK FLIGHT`, `FIX {owner} {id}`, `STOP`).
- Primary artifact is **Blender kit / Lib / Maps/Preview_*** lookdev, art bible shot approval, or multi-role fan-out (ENV-H / PROP / LIT / AD / QA judge).
- Active **P0–P7** row on [PHASE_BOARD](../../swarm/PHASE_BOARD.md) is IN PROGRESS and the ask is that phase’s kit work.
- Ask needs **Art Director taste** or **QA judge** with no shared builder memory (shot reject / eight-verb script).

**Action:** If this chat is not Conductor, **alert + recommend** boot per START_HERE (or spawn one specialist via Conductor). Do not dump the full brief into a coding agent.

### 2 → NON-SWARM

Any of (and none of §1):

- Engine / tooling / CI / doctor / MCP bridge / Safe-Build / Python automation / C++ gameplay systems.
- Docs tracks under **`Docs/NN_*` strategy** that are CLOUD+DESKTOP engineering (e.g. U58 upgrade, feature-adoption matrix) with **no** specialist fan-out.
- Single-owner edits: `Config/`, `Source/`, `Content/Python/`, lowercase `docs/`, `.github/`.
- Bugfix, lint, PR merge ops, schema validation.

**Action:** Stay in this chat. Read `SESSION_SUMMARY` + `PHASE_BOARD` **headers only** for continuity — do not load all `.cursor/agents/*` or `HOMEWORLD_MVP_SWARM_BRIEF.md`.

### 3 → HYBRID

- Engineering enables a lookdev capability (plugins, CVars, scalability) **and** shot approval / kit authoring remains AD-gated.
- Board needs a status stamp while implementation stays non-swarm.

**Action:** Implement NON-SWARM; file a short handoff under `Docs/handoffs/`; recommend a **separate** Conductor/AD turn for taste. Do not pull AD role card into the engineering thread.

### 4 → Ambiguous

- Ask spans both lookdev and engine, or user said “proceed” without a clear artifact class.

**Action:** Prefer **NON-SWARM** for the next atomic step; ask one Steer question only if the wrong mode would waste a specialist wave or a full rebuild. Default lean: **token-cheap first**.

---

## Model class routing (after mode)

Pick a **model class** (advice to human + agent — not a hard CI pin). Classes: **Auto** | **Mid** | **Frontier** | **Explore**. Details: [SWARM_ROUTING_RESEARCH.md](../Automation/SWARM_ROUTING_RESEARCH.md).

| Task class | Mode hint | Model class | Context load |
|------------|-----------|-------------|--------------|
| Conductor / phase gate synthesis | SWARM | Mid (Frontier only if gate is hard) | Board row + checklist paths |
| Kit fan-out specialist (ENV/PROP/LIT) | SWARM | Mid / role default | One role card + packet |
| Art Director taste / shot reject | SWARM | Frontier | AD card only |
| QA judge (independent) | SWARM | Mid–Frontier | QA card + evidence paths |
| Engine / C++ / Python / CI / Safe-Build | NON-SWARM | Auto → Mid | Targeted source/docs |
| Architecture / subtle multi-file bug | NON-SWARM or HYBRID | Frontier one-shot, then drop | Targeted files |
| Explore / parallel search | any | Explore (fast subagent) | Isolated window |
| Bulk renames / boilerplate | NON-SWARM | Auto / Composer | Minimal |

Aligns with [token-efficient-context](../../.agents/skills/token-efficient-context/SKILL.md) (plan strong → implement cheap).

---

## Progressive disclosure checklist

Studio-aligned (Cursor / Claude / Codex / Copilot):

- [ ] Always-on = short facts only (`AGENTS.md`) — **no** new `alwaysApply: true` routing rule
- [ ] Procedures live in skills; skill **description** carries triggers (like Copilot `infer` / Windsurf `model_decision`)
- [ ] SWARM workers get **one** role card + packet paths — never the full brief
- [ ] Mode flip → new chat (do not drag Conductor history into a C++ fix)

---

## Explicit non-triggers (do not enter SWARM for these alone)

- Reading or updating `PHASE_BOARD` / `SESSION_SUMMARY` after a NON-SWARM track.
- Mention of “MVP”, “VS_MVP”, or “Reap-Sow” without kit / shot / multi-role work.
- Enabling a plugin or CVar that lookdev will use later (U58F-style) — that is NON-SWARM or HYBRID, not a P-phase wave.
- Quarantined pre-swarm loops (`Start-AllAgents*`, agent-company) — never resurrect.

---

## Token budget rules

| Do | Don't |
|----|--------|
| Load one role card + packet paths when SWARM | Paste full brief into every worker |
| One specialist Task/subagent per packet | Flat group of all `.cursor/agents` |
| New chat when mode flips | Drag Conductor wave history into a C++ fix |
| HYBRID = two thin chats | One mega-thread “doing everything” |

~60k token smart zone for implementation ([token-efficient-context](../../.agents/skills/token-efficient-context/SKILL.md)).

---

## CI / merge vs mode choice

Waiting on **self-hosted** `build-win64` is a **merge hygiene** choice, not a swarm-mode requirement. Do not block NON-SWARM product or harness work on queued runners unless the user asked to merge that PR first. Validate/python-lint on ubuntu is the fast signal; build-win64 needs the Windows UE runner ([ci.yml](../../.github/workflows/ci.yml)).

---

## Output contract

Before heavy tool use, state **two** lines:

```text
Mode: NON-SWARM|SWARM|HYBRID — <reason>
ModelClass: Auto|Mid|Frontier|Explore — <reason>
```

---

## Checklist (agent)

- [ ] Mode named: `NON-SWARM` | `SWARM` | `HYBRID`
- [ ] ModelClass named: `Auto` | `Mid` | `Frontier` | `Explore`
- [ ] First-match rule applied from this doc
- [ ] SWARM → Conductor/specialist path only; no full-brief dump
- [ ] NON-SWARM → no specialist role cards loaded
- [ ] HYBRID → handoff path noted for AD/Lead gate
