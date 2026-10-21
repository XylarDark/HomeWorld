# Companion party play-confirm

Desk sign-off for #319 (`1e9b0e00`) and #325 (`307b949c`). The rules stay in [`Docs/41_COMPANION_PARTY_DESIGN.md`](../41_COMPANION_PARTY_DESIGN.md). This file does not change them.

Automation is `HomeWorld.Party` via `.\Tools\RunTests.ps1 -Filter HomeWorld.Party`. A green run is not the desk pass. Lead fills the result line after seeing the step.

The invite exists only after the captive is freed this session. Before that, the press falls through to the opening partner beat. Home is any loaded map whose name does not contain `Field`. `L_SizeTest` is home. `L_Field` is away. The press is the existing interact. There is no new key and no widget.

## 1. Before the rescue

**Setup.** Day, body, on `L_SizeTest`. The captive has not been freed.

**Action.** Aim at the partner and press the existing interact.

**Expected.** They do not come with you. The opening lead-inside beat still runs. Both flags stay home.

**Covers.** `HomeWorld.Party.RecordDefaults` and `HomeWorld.Party.HomeInteract` (the refuse). The opening beat still running is human only.

## 2. Invite at home

**Setup.** The captive has been freed. Day, body, on `L_SizeTest`. Aim at the partner or the child.

**Action.** Press the existing interact once.

**Expected.** That person is out. The line is `party: partner comes` or `party: child comes`. The other person stays home if you did not press them.

**Covers.** `HomeWorld.Party.HomeInteract` (invited). The on-screen line is human only.

## 3. Second press sends them home

**Setup.** Step 2, still at home, by day, in the body. One of them is out.

**Action.** Press the existing interact on that same person again.

**Expected.** Only that person goes home, back where they stood when invited. The line is `party: partner stays` or `party: child stays`. The other person, if out, stays out.

**Covers.** `HomeWorld.Party.HomeInteract` (sent home, and the child press leaves the partner out).

## 4. Refusals

**Setup.** The captive has been freed. Try one of: night or dusk, spirit form, or `L_Field`.

**Action.** Press the existing interact on the partner or the child.

**Expected.** The flags do not change. If they were already out, they stay out. The line is `party: stays home`.

**Covers.** `HomeWorld.Party.HomeInteract` (night, spirit, and away). The line is human only.

## 5. Follow

**Setup.** Step 2, then walk on the homestead by day in the body.

**Expected.** That person walks to a point 160 cm behind you and stops. You stay the possessed pawn. They do not gather, draw, or finish an ease.

**Covers.** `HomeWorld.Party.FollowLeash` (160 cm goal, no possess). Seeing the gap and that gather is unchanged is human only.

## 6. Outing clear

**Setup.** Someone is out.

**Action.** Bonk, sleep at the bed on a spirit-capable phase, enter dusk or night, start a stroke, or reach the camp or the cave.

**Expected.** Both flags clear. Anyone who was out is back where they stood. They do not ride the bonk glide.

**Covers.** `HomeWorld.Party.OutingClear`.

## 7. Night teleport

**Setup.** Defend night starts while someone is marked out.

**Expected.** The outing ends first, so the defend teleport can still move family who are home. A family actor the record still marks out is not moved onto a defend or dawn marker. The teleport still runs once.

**Covers.** `HomeWorld.Party.NightTeleport`.

## 8. Save and load

**Setup.** A day after the rescue, with someone out. Save. Load that slot on a day, in the body, with the rescue still complete. Then load a night slot, or a slot from before the rescue.

**Expected.** The day load keeps who is out, with no saved position. An old save, a night load, or a spirit load is solo, and anyone who was out is placed on the home spot remembered at the invite.

**Covers.** `HomeWorld.Party.SaveRoundTrip` and `HomeWorld.Party.LoadSendsHome`.

## Result

| Step | Lead | Date | Sentence |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
