# Docs/31 — Spirit Stealth feel (SS-B)

| Field | Value |
|-------|-------|
| **Status** | **SS-B STRATEGY APPROVED** · **SS-B IN PROGRESS** |
| **Date** | 2026-09-22 |
| **Author** | Cloud agent (HomeWorld) |
| **Prior track** | [25_SPIRIT_STEALTH_IMPL.md](25_SPIRIT_STEALTH_IMPL.md) **CLOSED / COMPLETE** (SS-A) |
| **Bible** | [SPIRIT_STEALTH_BIBLE.md](SPIRIT_STEALTH_BIBLE.md) · [SPIRIT_STEALTH_IMPL_PROMPT.md](SPIRIT_STEALTH_IMPL_PROMPT.md) |
| **Prefix** | **SS** — do not reuse MV / CD / DS gate strings |

---

## Gate

Lead **`APPROVE SS-B STRATEGY`**, 2026-09-21 ET — **GRANTED** (chat). Unlocks **SS-B** (readable stealth feel — not full NPC AI).

**SS-B close:** Lead **`APPROVE SS-B`** — **not stamped** in this PR (Lead closes later).

**Do not stamp SS-B APPROVED in a PR** — Lead types the gate string in chat.

---

## Goal (SS-B NOW)

Build on SS-A logs and volumes with **readable feel** only:

| Deliverable | Spec |
|-------------|------|
| Hidden cue | Spirit **unlit**: cool subtle point light + mesh tint (opacity/desat) + HUD `Spirit: hidden` |
| Revealed cue | **Lit** or alert rising: warm light + screen-edge pulse + HUD `Spirit: REVEALED` + alert bar 0→1 |
| Alert tick UI | On-screen bar while lit; `hw.Stealth.Status` prints `alert=0.00–1.00` |
| NPC torch | 1–2 **labeled** `AHomeWorldSpiritNpcTorchCarrier` on camp/den path (`NpcTorch` kind) |
| SS-A logs preserved | `STEALTH: LIT enter` · `STEALTH: ALERT` · `STEALTH: CLEAR` · optional `STEALTH: QUICK_WINDOW` |

**Forbidden:** crouch, kill-on-detect, body/spirit torch merge, spirit flight escape, homestead combat, breaking SS-A log tags, bulk `.uasset`.

---

## Tracks (Lead gates)

| Track | Name | Host | Status | Gate |
|-------|------|------|--------|------|
| **SS-B STRATEGY** | Feel polish policy | Lead | **APPROVED** | Lead **`APPROVE SS-B STRATEGY`**, 2026-09-21 ET |
| **SS-B** | Reveal VFX + alert tick + NPC torch | CLOUD+DESKTOP | **IN PROGRESS** | Pending Lead **`APPROVE SS-B`** — [handoffs/SS_B_STEALTH_FEEL.md](handoffs/SS_B_STEALTH_FEEL.md) |

---

## Code map

| Piece | Path |
|-------|------|
| Feel component | `HomeWorldSpiritStealthComponent.*` (hidden/revealed cues, alert 0–1) |
| NPC torch carrier | `HomeWorldSpiritNpcTorchCarrier.*` (extends lit volume, label + patrol optional) |
| HUD alert tick | `HomeWorldHUD.cpp` — bar + screen edge when spirit revealed |
| SS-A volumes | `HomeWorldSpiritLitVolume.*` (unchanged overlap logs) |
| Placement | [Content/Python/place_vs_mvp_ss_b_feel.py](../Content/Python/place_vs_mvp_ss_b_feel.py) (refreshes SS-A + carriers) |
| Cheats | `hw.Stealth.Status` (alert + feel), `hw.Stealth.ForceLit` |

---

## DONE-WHEN (SS-B)

- [ ] DESKTOP: `place_vs_mvp_ss_b_feel.py` after Safe-Build
- [ ] PIE spirit: unlit → readable **hidden** cue (HUD + cool feel light)
- [ ] Enter lit volume → **revealed** cue + alert bar rises; `STEALTH: LIT enter`
- [ ] Hold ~3s → `STEALTH: ALERT`; exit → `STEALTH: CLEAR` + hidden returns
- [ ] At least one `GP_SS_NpcTorch_*` labeled carrier on camp/den path
- [ ] Greps still include `STEALTH: LIT` / `STEALTH: ALERT` / `STEALTH: CLEAR`
- [ ] Lead **`APPROVE SS-B`** → track **CLOSED / COMPLETE**

**Grep:** `STEALTH:` in Output Log / `Saved/Logs/HomeWorld.log`

---

## Approval ladder

| Step | Lead action | Unlocks |
|------|-------------|---------|
| 0 | **`APPROVE SS-B STRATEGY`** | SS-B feel impl — **DONE** 2026-09-21 ET |
| 1 | **`APPROVE SS-B`** | Docs/31 track complete — pending |

```
Docs/25 Spirit Stealth (SS-A): CLOSED / COMPLETE — Lead APPROVE SS-A 2026-09-21 ET
Docs/31 Spirit Stealth feel (SS-B): IN PROGRESS — strategy approved; close pending APPROVE SS-B
```
