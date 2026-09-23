# HOST_PULSE — External tool-agnostic heartbeat

| Field | Value |
|-------|-------|
| **ID** | PDF_DESIGN_HOST_PULSE |
| **Slug** | HOST_PULSE_AGNOSTIC |
| **Mode** | HYBRID — Design docs → Implement tools → Conductor routine consumes |
| **Status** | DESIGN READY — pending Implement packet |
| **Date** | 2026-09-22 ET |
| **Owner** | HomeWorld Design |
| **Next** | Conductor opens Implement packet |

## Intent

External **tool-agnostic** heartbeat so Conductor detects stalls early when waiting on any external app/console (not UE-only).

**Default stall threshold:** `300` seconds (5 minutes) of inactivity **or** explicit failed state.

**Stall floor:** `300` seconds everywhere — per-target `stall_threshold_sec` must not be set below **300**.

**No new product phase. No `APPROVE *` gate.** Pulse is a Conductor signal, not a Lead product gate.

## States

| Status | Meaning | Notify? |
|--------|---------|---------|
| `healthy` | Last check OK within `stall_threshold_sec` | **Quiet** (no chat spam) |
| `blocked` | Host/tool down or no OK within threshold **during a pending Act** | Yes — transition only |
| `failed` | Explicit fail signal from check or helper | Yes — transition only |

**Product scores** (`soft_fail` / `closed_fail` on PS-C etc.) remain on Test’s sheet and apply **only after Arrange+map OK and Act actually ran**. Host/MCP/tool down = **`blocked`**, never product closed_fail.

## Constraints (Lead)

1. Grok Bot cron **cannot** fire faster than **5 minutes**.
2. **Primary path (MVP):** Conductor routine polls watched targets **at 5m cadence** (aligned with bot limit) and applies the **300s stall floor**. Conductor may **re-check targets directly** — no sub-5m local watcher is a **hard Design requirement**.
3. **Optional (nice-to-have):** A DESKTOP **multi-target pulse helper** may poll on the same cadence (≥5m) or less frequently, and write `Saved/host_pulse.json` for Conductor to **read** instead of duplicating checks. Helper is **not mandatory for MVP**; Implement defers `Tools/host_pulse` unless Conductor scopes it in the Implement packet.

## Target record (schema)

Each watched target:

| Field | Type | Notes |
|-------|------|-------|
| `id` | string | Stable id, e.g. `ue-editor`, `mcp-55557`, `ps-c-act` |
| `kind` | enum | `process` \| `tcp_port` \| `log_mtime` \| `http` |
| `check` | object | Kind-specific params (see below) |
| `stall_threshold_sec` | int | Default **300**; minimum **300**; overridable per target only upward |
| `last_ok_iso` | string \| null | ISO-8601 last successful check |
| `last_status` | enum | `healthy` \| `blocked` \| `failed` |

### `check` by kind

| kind | Required params | Pass when |
|------|-----------------|-----------|
| `process` | `name` or `image` (e.g. `UnrealEditor`) | Process exists and not OS “Not Responding” when detectable |
| `tcp_port` | `host` (default `127.0.0.1`), `port` (e.g. `55557`) | TCP connect succeeds |
| `log_mtime` | `path`, optional `max_age_sec` (default = stall threshold, floor 300) | File mtime within max age |
| `http` | `url`, optional `timeout_sec` (default 5) | HTTP 2xx/3xx within timeout |

## Optional output file: `Saved/host_pulse.json`

When a helper is deployed, it writes this file; Conductor may **read** it instead of re-running the same checks. **KEEP-LOCAL** — do not commit `Saved/` artifacts. **Not required for MVP** if Conductor performs direct 5m checks.

```json
{
  "schema": "host_pulse/v1",
  "updated_iso": "2026-09-22T21:00:00-04:00",
  "pending_act": true,
  "targets": [
    {
      "id": "ue-editor",
      "kind": "process",
      "check": { "image": "UnrealEditor" },
      "stall_threshold_sec": 300,
      "last_ok_iso": "2026-09-22T20:59:30-04:00",
      "last_status": "healthy"
    },
    {
      "id": "mcp-55557",
      "kind": "tcp_port",
      "check": { "host": "127.0.0.1", "port": 55557 },
      "stall_threshold_sec": 300,
      "last_ok_iso": null,
      "last_status": "blocked"
    }
  ],
  "aggregate": "blocked"
}
```

**`aggregate`:** `failed` if any target `failed`; else `blocked` if any `blocked` **and** `pending_act` is true; else `healthy`. If `pending_act` is false, down targets may stay recorded but Conductor stays quiet (no pending wait).

## DONE-WHEN (Design)

- [x] Spec stamped in this handoff
- [x] Pointer § in `swarm/PDF_CYCLE.md`
- [ ] Conductor opens Implement packet with write paths below

## DONE-WHEN (Implement — for Conductor packet)

**Primary (MVP):** Conductor **5m pulse** — direct target re-checks at ≥5m cadence; stall floor **300s**; notify only on transition while `pending_act`.

**Optional / deferred unless packet scopes it:**

| Artifact | Path (suggested) | Notes |
|----------|------------------|-------|
| Pulse helper | `Tools/host_pulse/` (or `Tools/host_pulse.py` + README) | Optional multi-target writer; ≥5m poll OK; write `Saved/host_pulse.json`; kinds above; default stall 300s |
| Example config | `Tools/host_pulse/targets.example.json` | Sample UE + MCP 55557 targets; no secrets |
| Docs stamp | This file § Implement notes + link from `swarm/PDF_CYCLE.md` | Only if Design already listed |

**Out of scope for Implement:** product phases, `APPROVE *`, uasset, DESKTOP MCP prove of PS-C. Grok routine wiring remains **Conductor-owned** as part of the primary 5m path.

### Implement prove checklist (for Test / Conductor)

1. Conductor 5m pulse runs; stall logic uses **300s** floor; valid target state transitions.
2. Kill/stop a watched process or close port → within ≤**300s** (and next 5m tick as applicable) `last_status` becomes `blocked` or `failed` when `pending_act: true`.
3. Recovery → `healthy`; Conductor notify is **transition-only** (no spam while healthy).
4. If helper is in scope: helper produces valid `host_pulse/v1` JSON; Conductor can read file OR direct-check (one source of truth per target, no double-notify).

## Conductor routine — Design requirements only

- Cadence: **5m** (bot limit); **primary** implementation re-checks targets directly at this cadence.
- May **read** optional `Saved/host_pulse.json` (DESKTOP project root) when helper is present; must not depend on sub-5m polling.
- Notify only on **transition** into `blocked` / `failed` while a pending Act is set.
- Quiet when `aggregate=healthy`.

## What Design did not invent

- [x] No new product phase / Docs/34 track
- [x] No `APPROVE *` gate string
- [x] No Tools/ code in this PR (Implement owns code)
- [x] No PS-C score-sheet changes (Test owns; blocked ≠ closed_fail already locked)
- [x] No mandatory sub-5m DESKTOP watcher

## Risks for Implement

- Windows process “Not Responding” detection may be best-effort; document limitation in KNOWN_ERRORS if unavailable.
- Path to optional `Saved/host_pulse.json` must match DESKTOP project root Conductor uses.
- Do not commit live `Saved/host_pulse.json`.
- 5m poll + 300s stall: first `blocked` detection may occur on the first Conductor tick after threshold elapsed — document expected latency.

## Evidence (Design)

- This file: `Docs/handoffs/HOST_PULSE.md`
- Pointer: `swarm/PDF_CYCLE.md` § Host Pulse
