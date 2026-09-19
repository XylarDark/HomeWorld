# Taste Gate

When the agent hits a **human taste limit**, stop inventing. Detect → alert → queue → stop. After the human answers, scribe and resume agent-owned work.

**Canon:** [Docs/28_TASTE_GATES.md](../../../Docs/28_TASTE_GATES.md) · [taste-gates.md](../../../docs/human-use/taste-gates.md) · [taste-profile.md](../../../docs/human-use/taste-profile.md) · [OWNERSHIP.md](../../../docs/human-use/OWNERSHIP.md)

## When to load

Load this skill when any **taste-limit heuristic** from Docs/28 is true and undecided for this task (vision/GDD/art bible/shot invent; next Docs track feel; architecture `(fill in)`; AD still verdict; reopen CLOSED feel; PHASE_BOARD next TBD but agent would start product work).

**Do not load** for typo/one-line, flesh-out of locked taste, or work after an explicit Lead `APPROVE *` unlock for that phase.

## Procedure

### 0. Read profile

Open [taste-profile.md](../../../docs/human-use/taste-profile.md).

- If the fork is **already covered** (locked decision, do-not, or clear process pref) and this task is flesh-out only → do **not** invent; follow the profile and continue agent work (or stop if profile says park).
- If the fork **conflicts** with the profile or is an **open gap** / missing pref → continue with Detect → Alert → Queue; also **stage** a candidate stub via [taste-profiler](../taste-profiler/SKILL.md) (`Saved/taste_profile_session.json`).

### 1. Detect

Name the heuristic id (1–6 from Docs/28) and the fork in one sentence.

### 2. Alert (OWNERSHIP shape)

Emit exactly this shape (Job: **taste** unless Steer/Test applies):

```
Owner: human — <this decision>
Job: taste
You are here: <task / path / shaping|settled>
Why now: <what goes wrong if we skip or guess>
I will not: <the feel/purpose/shape I must not invent>
Recommend: <one option grounded in repo evidence, or "no evidence — skip">
Need from you: <numbered options; recommended first; skip last>
After you pick: <what I do next; next human fork if any>
```

**Question budget:** max **2** questions per turn (Docs/26-style). Prefer A/B choices over open essays.

### 3. Queue

1. Write or update durable handoff: `Docs/handoffs/TASTE_GATE_<SHORT_ID>.md` (gate id, heuristic, alert paste, status `PENDING`).
2. Write machine queue (gitignored): `Saved/taste_gates_pending.json` — array of objects:

```json
{
  "id": "TG-DRY-NEXT-TRACK",
  "created": "YYYY-MM-DD",
  "heuristic": 6,
  "status": "pending",
  "handoff": "Docs/handoffs/TASTE_GATE_DRY_NEXT_TRACK.md",
  "summary": "one-line fork"
}
```

Idempotent: same `id` updates in place; do not duplicate.

### 4. Stop

Do **not** invent taste, open a new product Docs track, or keep coding past the fork. End the turn after the alert + queue.

### 5. Scribe and resume (after human answer)

When Lead/AD answers (chat pick, `APPROVE *`, or dictate):

1. Scribe confirmed taste into the gate file named in the alert (or Docs track).
2. Set queue entry `status` to `resolved`; note resolution in handoff.
3. **Promote or reject** the staged profile candidate ([taste-profiler](../taste-profiler/SKILL.md)) — do not leave durable profile stale.
4. Resume only **agent-owned** work named in `After you pick`.

## Gate template (Docs/26-style)

Round N (max 2 Q):

| Q | Prompt | Options |
|---|--------|---------|
| 1 | What should we decide now? | A / B / Skip |
| 2 | If A: which intensity? | Low / Mid / High / Skip |

Do not start Round N+1 until Round N is answered or skipped.

## Non-goals

- Auto-approve or invent product feel
- Resurrect `Start-AllAgents*` / agent-company loop (WAVE F)
- Preference-model training from Lead chat
- Building cursor-cannot products
