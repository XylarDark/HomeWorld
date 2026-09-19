# Taste Profiler

Maintain the durable taste profile and session candidates. Bootstrap → stage → promote (Lead-gated). Never invent product feel.

**Canon:** [Docs/29_TASTE_PROFILER.md](../../../Docs/29_TASTE_PROFILER.md) · [taste-profile.md](../../../docs/human-use/taste-profile.md) · [taste-profiler.md](../../../docs/human-use/taste-profiler.md)

## When to load

- First-time or empty profile sections that need Lead bootstrap
- After a Taste Gate answer that should become durable
- Explicit Lead ask to update process prefs
- Prove / dry-run promote path

**Do not load** to invent feel, replace the art bible, or auto-consolidate chat into the profile.

## Procedures

### Bootstrap (max 2 Q/turn)

1. Read [taste-profile.md](../../../docs/human-use/taste-profile.md).
2. Ask at most **2** questions (Docs/26-style A/B/Skip).
3. Put drafts in the OWNERSHIP alert; scribe only after confirm.
4. Seed canon pointers and do-not from existing Docs/00–02 / Docs/26 — do not invent new product targets.

### Stage candidate

Append or update `Saved/taste_profile_session.json`:

```json
{
  "candidates": [
    {
      "id": "TP-CAND-001",
      "created": "YYYY-MM-DD",
      "source": "taste-gate|chat|APPROVE",
      "text": "one-line candidate",
      "status": "staged"
    }
  ]
}
```

Idempotent on `id`. Status: `staged` | `rejected` | `promoted`.

### Promote (Lead-gated)

Only after Lead/AD confirm, explicit “promote”, or `APPROVE *` that implies the decision:

1. Write the confirmed line into the right section of `taste-profile.md` (prefs, locked decisions, gaps, or do-not).
2. Set candidate `status` to `promoted` (or `rejected` if Lead declines).
3. Update **Last promoted** date on the profile.

### Refuse

- Auto-promote from logs or Memories
- Duplicate palette chips from the art bible
- Open a product Docs track without Lead name or Taste Gate

## With Taste Gates

When [taste-gate](../taste-gate/SKILL.md) fires, stage a candidate stub for the fork. After Lead answers, run **Promote** (or reject) before resuming agent work named in `After you pick`.
