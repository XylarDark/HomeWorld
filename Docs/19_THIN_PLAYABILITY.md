# Docs/19 — Thin Playability (D19)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED** — Lead **`APPROVE D19 STRATEGY`**, 2026-09-17 ET |
| **Date** | 2026-09-17 |
| **Author** | Conductor (HomeWorld) |
| **Baseline main** | `aa6472e` — VP2 CLOSED; HS-G APPROVED |
| **Prior track** | [18_VERIFY_PROVE.md](18_VERIFY_PROVE.md) **CLOSED** — Lead **`APPROVE VP2-C STOP`**, 2026-09-17 ET |

---

## Goal

Gather **without cheats** where possible, plus a **seed grant cheat** so N1_Crop nurture success-path is unblocked, and **evidence scoring** that prefers success-path log lines over soft-fail / `component ready` diagnostics.

**Success:** DESKTOP can re-prove verb greps with real pile harvest + `hw.Gather.Seed` for nurture, scored via `evidence:grep --success-path`.

---

## Non-goals

| Out | Why |
|-----|-----|
| Art / lookdev / AnimGraph | Out of D19 scope |
| Combat / free-flight | Placeholder policy unchanged |
| `.uasset`/`.umap` commits | Hard rule; KEEP-LOCAL save only |
| Reopening VP2 | CLOSED at Lead gate |
| Branch protection | DEFERRED |
| Inventing tracks beyond D19-A/B/C | Lead gate required |

---

## Tracks (Lead gates)

Naming: **D19-A … D19-C**. Do **not** reuse VP2 or PL gate strings.

| Track | Name | Host | Status | Gate |
|-------|------|------|--------|------|
| **D19-A** | Gather piles that stick | CLOUD+DESKTOP | **IN PROGRESS** | Lead **`APPROVE D19-A`** after DESKTOP pile harvest |
| **D19-B** | Seed cheat (`hw.Gather.Seed`) | CLOUD | **IN PROGRESS** | Lead **`APPROVE D19-B`** after PIE grant log |
| **D19-C** | Success-path evidence filter | CLOUD | **IN PROGRESS** | Lead **`APPROVE D19-C`** after tests green |

**Lead strategy gate:** **`APPROVE D19 STRATEGY`** — **APPROVED** 2026-09-17 ET.

---

### D19-A — Gather piles that stick

**Goal:** Idempotent `place_vs_mvp_resource_piles.py` places stable `GP_Gather_WOOD` / `GP_Gather_HERB` / `GP_Gather_BERRY` actors; safe to re-run; labels + tags survive editor session until Conductor saves level locally.

| Item | Spec |
|------|------|
| **Script** | `Content/Python/place_vs_mvp_resource_piles.py` |
| **Labels** | `GP_Gather_WOOD`, `GP_Gather_HERB`, `GP_Gather_BERRY` |
| **Tags** | Same FName tags on actor for PIE lookup fallback |
| **Level** | `L_VS_MVP_Markers` — **KEEP-LOCAL** save after run (not in git) |
| **Prereq** | `place_vs_mvp_markers.py` + Safe-Build |

**Runbook (DESKTOP, before PIE gather prove):**

```text
place_vs_mvp_markers.py
place_vs_mvp_gp.py
place_vs_mvp_resource_piles.py
# Conductor: File → Save Current Level (KEEP-LOCAL)
```

**Expected gather success-path:** `GATHER: RES_WOOD +N` and/or `GATHER: harvest ok` (face pile ~280 cm, day/body, Interact or `try_harvest_in_front()`).

**Gate:** Lead **`APPROVE D19-A`**

---

### D19-B — Seed cheat

**Goal:** Console command grants `RES_SEED` like Ore→STONE / Flowers→HERB so N1_Crop nurture is cheat-unblocked.

| Item | Spec |
|------|------|
| **Command** | `hw.Gather.Seed [amount]` — default **1** |
| **Log** | `HomeWorld: hw.Gather.Seed granted RES_SEED +N` |
| **Mirror** | `CmdGatherOre` / `CmdGatherFlowers` in `HomeWorld.cpp` |
| **Use** | PIE: `hw.Gather.Seed 1` then night/spirit at `GP_N1_Crop` → `NURTURE: success N1_Crop M_Nurtured=1` |

**Gate:** Lead **`APPROVE D19-B`**

---

### D19-C — Success-path evidence filter

**Goal:** `scripts/evidence-grep.js` optional **`--success-path`** mode counts success lines only; does not PASS on `component ready` / soft-fail-only.

| Prefix | Success-path substring |
|--------|------------------------|
| `STORE:` | `STORE: deposit` |
| `HEAL:` | `HEAL: success` |
| `NURTURE:` | `NURTURE: success` |
| `TAME:` | `TAME: offer accepted` |
| `GATHER:` | `GATHER: RES_` |
| `DAWN:` | `DAWN: persisted` |
| `INVENTORY:` | `INVENTORY: dump begin` |
| `FORM:` / `FALLBACK:` | Any line with prefix (unchanged) |

**Usage:**

```powershell
npm run evidence:grep -- --log Saved/Logs/HomeWorld.log --success-path --strict
```

Default (no flag) remains backward-compatible for existing tables.

**Gate:** Lead **`APPROVE D19-C`**

---

## Evidence checklist (DESKTOP)

1. `git pull`; `.\Tools\Safe-Build.ps1`
2. Run marker + pile scripts (D19-A runbook); save level locally
3. PIE on `L_VS_MVP_Markers`; `log LogTemp Log`
4. Day/body: harvest `GP_Gather_WOOD` → `GATHER: RES_WOOD`
5. `hw.Gather.Seed 1` → grant log; night: `GP_N1_Crop` → `NURTURE: success`
6. Score: `node scripts/evidence-grep.js --log Saved/Logs/HomeWorld.log --success-path --json Saved/d19_evidence.json`

---

## Board

See [swarm/PHASE_BOARD.md](../swarm/PHASE_BOARD.md) — **Docs/19 IN PROGRESS / APPROVED strategy**. VP2 remains **CLOSED**.

---

*APPROVED — Lead **`APPROVE D19 STRATEGY`**, 2026-09-17 ET.*
