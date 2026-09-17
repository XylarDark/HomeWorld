# HOMEWORLD SWARM OPS

**Runtime for the conductor.** This is the coordination script.  
Canon stays in `HOMEWORLD_MVP_SWARM_BRIEF.md`. If ops and canon conflict, **canon wins on design**, **ops wins on process**.

Aligned with [DevEnvTemplate](https://github.com/XylarDark/DevEnvTemplate) **files-only** practices and HomeWorld [docs/human-use/](../docs/human-use/) (steer / taste / test). UE automation company rules stay in [AGENTS.md](../AGENTS.md) and `docs/` — this file governs the MVP lookdev swarm only.

## 1. Architecture (locked)

Two-tier only. No flat peer chat. No shared scratch file that every agent writes.

```
Human Lead   (steer / taste / test — see docs/human-use/OWNERSHIP.md)
 └── CND Conductor   (assigns, gates, merges; does not model or code features)
      ├── Phase graph with exit checkboxes
      ├── Fan-out workers with exclusive file/collection ownership
      └── QA judge with no shared memory of builder chat
```

**Human Use (Lead gates):** Phase gates (`APPROVE P0` … `APPROVE P7`) and cut decisions (e.g. `FALLBACK FLIGHT`) are **human Test/Steer jobs**. Conductor and workers **alert + recommend** at a gate; they **do not invent** Lead approval or tick sign-off. If a gate checklist is incomplete, stop and show evidence gaps — do not advance. Catalog: [docs/human-use/](../docs/human-use/).

Patterns allowed:

| Pattern | When |
|---|---|
| Chain | Phase 0 → 1 → 2 |
| Fan-out | Independent owners inside one phase (ENV-H / PROP / LIT) |
| Pipeline + gate | Every phase exit |
| Supervisor | Conductor reroute on failed QA |

Forbidden:

- Group-chat design debates after Phase 0
- Two agents editing the same Blender collection or the same UE map actor
- Implementer marking its own phase complete
- Dumping the entire brief into every worker prompt

## 2. Tooling (what to actually use)

| Layer | Tool | Job |
|---|---|---|
| Human + files | This kit + git | Source of truth |
| Conductor host | Cursor Project coordinator **or** one long Conductor chat | Assign / refuse / merge |
| Workers | Cursor subagents from `swarm/agents/` + Blender MCP | Build artifacts |
| Isolation | One owner per collection / folder; worktrees if two agents might touch the same `.blend` | Prevent overwrite |
| Optional later | LangGraph around phase flags | Resume after crash |
| Optional later | CrewAI only as a role wrapper | Not required |
| Do not start on | AutoGen group chat, OpenAI Swarm, MetaGPT studio sim | Wrong pattern |

MCP: Blender for art phases. GitHub if the repo is connected. No extra SaaS required for MVP.

## 3. Shared state (the only legal shared memory)

Agents do not brief each other in chat. They read files.

| File | Who writes | Who reads |
|---|---|---|
| `HOMEWORLD_MVP_SWARM_BRIEF.md` | Human Lead only after Phase 0 | Everyone |
| `swarm/PHASE_BOARD.md` | Conductor only | Everyone |
| `Docs/**` | Role listed on the packet | Downstream roles |
| `Docs/handoffs/*.md` | Completing worker | Conductor + QA + next owner |
| `.blend` collections | Exclusive owner in the packet | Downstream, read-only until handoff |

If it is not in a file, it did not happen.

## 4. Handoff contract

Every finished task writes `Docs/handoffs/P{phase}_{ROLE}_{slug}.md` using `HANDOFF_TEMPLATE.md`.

Conductor **refuses** the next task if any of these are missing:

- Artifact path (every deliverable — **paths only; “done” without a path is invalid**)
- Object / material name list
- Owner
- Phase exit boxes the worker claims
- Blockers (link to [docs/KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md) or [docs/Automation/AUTOMATION_GAPS.md](../docs/Automation/AUTOMATION_GAPS.md) when a real failure or automation impossibility blocked work)
- **Evidence** — screenshot, frame, checklist output, or test notes with a repo-relative path or log reference (see handoff template)
- “Did not invent” checklist (no extra biome, beast, shader family, flight model)

**Gate evidence:** A phase gate closes only when every exit checkbox is backed by **checkable artifacts** (file exists, handoff lists paths, QA or Conductor can verify without builder chat). Narrative completion is not evidence.

QA may not edit kits. QA only files defects against canon + shot list + verb list.

### 4a. Host owner lane (HR3-D)

[PHASE_BOARD.md](PHASE_BOARD.md) names **Host** per active HR/VP row: **CLOUD** | **DESKTOP** | **Lead**.

| Tag | Runs evidence |
|-----|----------------|
| **CLOUD** | Cursor cloud agent — docs, C++ source, `validate` / `python-lint` CI |
| **DESKTOP** | **DESKTOP-21CT3H0** — Conductor **parent** only ([HR3_A_WINDOWS_EXEC.md](../Docs/handoffs/HR3_A_WINDOWS_EXEC.md)); not Task executors |
| **Lead** | GitHub Settings, **`APPROVE *`** stamps |

Cloud agents **return after merge**; they do not claim DESKTOP Shell, MCP, or PIE. See [CLOUD_AGENT_PACKET.md](CLOUD_AGENT_PACKET.md).

### 4b. DESKTOP / cross-host handoff PR contract

Handoff markdown **and** PR body for DESKTOP or cross-host phases must include:

| Field | Required content |
|-------|------------------|
| **Host** | `DESKTOP-21CT3H0` or `CLOUD` (Linux VM) |
| **Grep prefixes** | Log tokens to grep (HS-D / VP-A class: `FORM:`, `FALLBACK:`, `HEAL:`, `NURTURE:`, `DAWN:`, `TAME:`, `GATHER:`, `STORE:`, `INVENTORY:`) |
| **Evidence path** | Repo-relative handoff path + log file (e.g. `Saved/Logs/HomeWorld.log`) |
| **Pass/fail table** | One row per prefix/check — **PASS**, **FAIL**, or **WAIVED** (Lead only) with excerpt or line count |
| **Preflight** | `npm run preflight:ue` exit code when DESKTOP PIE applies ([UE_PREFLIGHT.md](../docs/Setup/UE_PREFLIGHT.md)) |
| **PR URL + merge SHA** | After squash-merge to `main` |

Example VP-A table: [VP_A_PIE.md](../Docs/handoffs/VP_A_PIE.md). Full lane spec: [HR3_D_EVIDENCE_LANE.md](../Docs/handoffs/HR3_D_EVIDENCE_LANE.md).

### 4c. Re-verify rule (blocker-fix → re-prove) — HS-D

When phase **B** fixes a blocker that caused hard-fail in phase **A**:

1. File **B** evidence; Lead **`APPROVE`** when satisfied.
2. **Re-run A's grep checklist** on current `main` (DESKTOP = Conductor **parent**); append **§ Re-verify** to A's handoff — do not erase the original fail / WAIVE record.
3. Prefer host scoring: `npm run evidence:grep -- --log Saved/Logs/HomeWorld.log` (optional `--json Saved/hs_d_evidence_grep.json`; `--strict` for gate scripts). Paste table into the handoff — **never invent** Output Log lines.
4. **Unlock downstream polish / presentation** only when A re-verify shows **PASS** on all required prefixes **or** Lead **WAIVED** per prefix (named, not silent).

Canonical VP chain: **VP-B complete → VP-A greps re-prove → VP-C unlock**. See [14_VP_VERIFY_POLISH.md](../Docs/14_VP_VERIFY_POLISH.md) § Re-verify · [17d_HS_EVIDENCE.md](../Docs/17d_HS_EVIDENCE.md) · [HR3_D_EVIDENCE_LANE.md](../Docs/handoffs/HR3_D_EVIDENCE_LANE.md).

Conductor **refuses** any polish phase tied to prior hard-fail greps until re-verify is filed or Lead waives. Preflight before PIE: [UE_PREFLIGHT.md](../docs/Setup/UE_PREFLIGHT.md) (HR3-B). DESKTOP checklist: [HS_D_EVIDENCE.md](../Docs/handoffs/HS_D_EVIDENCE.md).

## 5. Phase graph

```
P0 Canon freeze
    DES + AD + CND
    GATE: Docs/00_CANON.md + Docs/00_SHOTLIST.md + folders exist
P1 GDD + graybox
    DES then WLD (chain)
    GATE: lookout camera sees landing, roofs, path; walk times written
P2 Materials + bible
    AD + TA (fan-out, different files)
    GATE: 10 masters + parameter sheet + NightMix demo
P3 Homestead kit
    ENV-H + PROP + LIT (fan-out, different collections)
    GATE: Preview_Homestead_Night matches key art tests
P4 Planet + transit
    ENV-P + WLD + LIT (WLD places, ENV-P builds, LIT presets)
    GATE: Shots 3–4; same masters; glide path visible
P5 Verbs + life
    CHA + PROP leftovers + GP + SYS
    GATE: 8 verbs executable on graybox + kits
P6 Integrate
    INT + CND + TA
    GATE: leave island, reach planet, return by portal
P7 Sign-off
    QA + AD + DES + Human Lead
    GATE: Docs/07_VERTICAL_SLICE_SIGN OFF.md
```

Never start N+1 on a failed gate. Fallback if flight slips: scripted glide down + portal both ways. Conductor may apply that cut without a design meeting.

## 6. File ownership (collision map)

| Path / collection | Sole writer |
|---|---|
| `Docs/00_*` `Docs/01_*` | DES (AD on shotlist + bible) |
| `Docs/02_ART_BIBLE.md` | AD |
| `Docs/02_MATERIAL_SHEET.md` + `Lib/06_Materials_Master` | TA |
| `Lib/01_Homestead` `SM_IslandTop` `SM_Cliff` cabin modules | ENV-H |
| `Lib/02_Forest` planet meshes | ENV-P |
| `Lib/03_Gatherables` shrine, landing circle, planters, path tiles | PROP |
| `Lib/04_Beasts` `Lib/05_Spirits` family blockouts | CHA |
| `Lib/07_Night_SpiritLayer` lights, volume, moon, cameras | LIT |
| `Lib/08_Transit` glide spline crumbs after PROP circle exists | WLD + ENV-P |
| Gameplay / systems code | GP / SYS |
| Maps, export table | INT |
| `swarm/PHASE_BOARD.md` | CND |
| Defects `Docs/qa/` | QA |

If two packets name the same path, Conductor is wrong. Fix the packet. Do not let them “work it out.”

## 7. Spawn rules

1. Human pastes `WAVE_n` packet into Conductor.  
2. Conductor copies the matching `swarm/agents/{role}.md` into a new subagent (or Cursor custom agent).  
3. Worker prompt = agent file + **only** the inputs listed in the wave packet.  
4. Worker stops when outputs exist and handoff is written.  
5. Conductor updates `PHASE_BOARD.md`.  
6. Conductor presents the gate checklist + artifact paths to Human Lead. Lead types `APPROVE P{n}` or a fix list — **workers and Conductor do not self-approve**.

Max parallel in one wave: number of **non-overlapping owners**. Phase 3 max 3 (ENV-H, PROP, LIT). Phase 5 max 3 if CHA / GP / SYS own different trees.

**Thin worker context (required):** Worker prompt = role card (`swarm/agents/{role}.md`) + **only** canon slices and input paths listed in the wave packet + current `PHASE_BOARD` row. Conductor does **not** paste the full brief, prior worker chat, or UE automation docs into worker prompts.

## 8. Defect protocol

QA writes `Docs/qa/P{n}_{id}.md`:

- Canon clause violated
- Shot or verb that fails
- Expected vs found
- Owner to fix
- Blocker? (yes = phase cannot close)

Conductor assigns a **fix-only** task to the owner. No new scope on a fix ticket.

## 9. Token and context discipline

Worker context:

- Role card
- Canon slices listed in the packet (not the whole brief unless CND / DES / AD)
- Current phase board row
- Input artifact paths

Do not paste prior worker chat. Do not paste Unreal marketplace essays. Do not let workers renegotiate moon size, resource list, or map topology.

## 10. Multi-agent git safety

When several agents share one checkout (parallel subagents or sibling sessions):

- **One file, one owner** for the duration of a task (see collision map §6).
- **Stage explicit paths only** — `git add path/to/file …`. Never `git add -A` or `git add .` (picks up others' in-flight edits).
- **Do not commit** changes you did not make; **commit your own work promptly** in small coherent chunks.
- Prefer **worktrees** when two agents might touch the same `.blend` or tracked folder.
- Workers in a shared tree: **no push, no rebase** — Conductor or Lead coordinates what goes public.

Full rules: [.agents/skills/multi-agent-collaboration/SKILL.md](../.agents/skills/multi-agent-collaboration/SKILL.md).

## 11. Operational memory

Failures and impossibilities must survive the session — not live only in chat.

| Situation | Write to |
|---|---|
| Real local failure (build, tool, Blender MCP, export, test) | Append [docs/KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md) — symptom, cause, fix, date |
| Step that cannot be automated or scripted reliably | Append [docs/Automation/AUTOMATION_GAPS.md](../docs/Automation/AUTOMATION_GAPS.md) |
| Swarm handoff blocked by either | Reference the entry in handoff **Blockers**; Conductor reads before reassignment |

Do not record web/MCP assertions as KNOWN_ERRORS without a local repro. Do not copy untrusted fetched text into always-on files without a human Steer decision ([docs/human-use/OWNERSHIP.md](../docs/human-use/OWNERSHIP.md)).

## 12. Definition of a living swarm

The swarm is running correctly when:

- PHASE_BOARD has a current phase and named owners
- Every completed task has a handoff file with **artifact paths and evidence**
- No two open tasks share a write path
- QA has not been asked to “just approve”
- Human Lead only enters at gates and cut decisions (`APPROVE Pn`, `FALLBACK FLIGHT`, `FIX …`)
- Real failures are in KNOWN_ERRORS; automation impossibilities are in AUTOMATION_GAPS
- Git commits stage explicit paths only

## 13. Session resume (HS-B — debt #8)

Chat transcripts lag and refresh. **Durable continuity is files**, not chat.

**On every Conductor / swarm session start (required):**

1. Latest durable handoff: `Docs/handoffs/SESSION_HANDOFF_*.md` (pick newest by date in filename)
2. Rolling summary: [docs/SESSION_SUMMARY.md](../docs/SESSION_SUMMARY.md) — **append only**; do **not** rewrite all history
3. Live board: [PHASE_BOARD.md](PHASE_BOARD.md)

Resume from the handoff **resume_focus** / unfinished list. Do not reconstruct the day from chat alone.

Pointer also in [AGENTS.md](../AGENTS.md) § Session continuity.

## 14. Cloud Contents API fallback (HS-B — debt #4)

When cloud clone / workspace returns **ResourceExhausted** (or equivalent):

- **Sanctioned path:** GitHub **Contents API** via `gh api repos/<owner>/<repo>/contents/...` (read/write file, create branch, open PR) — **no local clone required**
- Encode use in handoff Evidence/Blockers as `ResourceExhausted → gh Contents API`
- Still: no `.uasset`/`.umap`; no DESKTOP Shell from cloud; exclusive ownership

Packet: [CLOUD_AGENT_PACKET.md](CLOUD_AGENT_PACKET.md).

## 15. Lead digests (HS-B — debt #6)

Prefer **phase-end digests** (one message: gate status + PR URL(s) + merge SHA(s) + next `APPROVE *` string) over per-CI / per-push spam. Stamp PRs for Lead gates remain valid; Conductor batches the Lead-facing narrative.

## 16. DESKTOP parent-only happy path (HS-B — debt #2)

Cross-link: [docs/Setup/WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) § Canonical Windows agent lane.

| Actor | DESKTOP Shell |
|-------|---------------|
| Conductor **parent** | **YES** |
| Task executor / worker | **NO** (FAIL) |
| Cloud Linux VM | **NO** |

Proof / failure modes: [Docs/handoffs/HR3_A_WINDOWS_EXEC.md](../Docs/handoffs/HR3_A_WINDOWS_EXEC.md).