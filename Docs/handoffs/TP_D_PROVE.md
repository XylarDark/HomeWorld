# TP-D — Taste Profiler dry-run prove

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / CLOSED** — Lead **`APPROVE TP-D`**, 2026-09-19 ET |
| **Date** | 2026-09-19 |
| **Track** | [Docs/29_TASTE_PROFILER.md](../29_TASTE_PROFILER.md) |
| **Fake fork** | Heuristic **6** — next product track TBD; would invent without reading profile |

---

## Scenario

Agent would invent the next Docs product track. Instead: read [taste-profile.md](../../docs/human-use/taste-profile.md) → open gap / do-not invent → Taste Gate → stage candidate → stop.

## Alert (OWNERSHIP shape)

```
Owner: human — next product direction (profile open gap)
Job: taste
You are here: Docs/29 prove / taste-profile open gaps / shaping
Why now: inventing a track contradicts profile do-not and Docs/28 heuristics
I will not: open a new Docs product track or invent feel targets
Recommend: Skip product this session OR name the next track in chat
Need from you:
  1. Name next track in chat (when you know)
  2. Start Docs/26-style taste interview (2 Q/turn)
  3. Skip — harness-only / no product (recommended for this prove)
After you pick: promote/reject session candidate; update taste-profile open gaps; resume only agent-owned work
```

## Queue / session evidence

- Gate handoff stub: [TASTE_GATE_TP_DRY_NEXT.md](TASTE_GATE_TP_DRY_NEXT.md)
- Session: `Saved/taste_profile_session.json` — candidate `TP-CAND-DRY-NEXT` status `staged`
- Profile read: do-not invent next track; process pref Lead-named or Taste Gate

## Spike paths verified

| Artifact | Path |
|----------|------|
| Docs/29 | `Docs/29_TASTE_PROFILER.md` |
| Profile | `docs/human-use/taste-profile.md` |
| Skills | `.cursor/skills/taste-profiler/` · taste-gate step 0 |
| Human-use | `docs/human-use/taste-profiler.md` |

## Lead gates

| Phrase | Effect |
|--------|--------|
| **`APPROVE TP-D`** | Accept prove; mark TP-D DONE |
| **`APPROVE TP-E`** | Close Docs/29 |
