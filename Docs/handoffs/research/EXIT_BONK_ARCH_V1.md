# EXIT BONK_ARCH_V1

Filed 2026-10-22 by Grok Bot. Prompt: Docs/handoffs/research/PROMPT_BONK_ARCH_V1.md. Source: the answer in Cursor chat "Bonk system architecture review" (Ask, Grok 4.7 Extra High), copied with the message copy button to q2/bonk_answer.md. The answer below is verbatim; it predates this filing and was not written to the EXIT section shape (Diagnosis / Do bites / Accept checklist), so fitness grep B is not expected to pass. Not an ACCEPTed EXIT.

---

Mode: solo · State: agent. The bonk flight is already the shape a new caller should use, so it does not need an architecture pass.

The arc is one pure header (`HomeWorldBonkArc.h`) with one test (`HomeWorld.Opening.BonkArc`). `BeginBonkReturn` is the only flight: inset landing, slope-capped swoop, input lock, flying mode, party end, then `TickBonkReturn`. The opening detector is the only caller, and the one-shot flag is what stopped the retrigger loop. Stress is a separate ledger: `NotifyBonk` adds 5 and `Add` clamps at 100, and only a late paradox in `HomeWorldStrokeReportComponent.cpp` calls it, then `StartGlideHome`. The opening fall does not. That matches the passed bonk (step and shoulder light unchanged). The HUD never reads a bonk. The shoulder wisp is attached to the capsule, so it rides the teleport. Guards spend tries and glide home on the stroke path. They never enter the arc.

Changing it risks the flight that is still waiting on a human play (one `opening_bonk: return to`, then one `landed`).

- Retuning `MakeArc` or the 500 cm inset breaks `HomeWorldBonkArcTests.cpp` and the inland landing from the 18 Oct pass.
- Calling `NotifyBonk` from `BeginBonkReturn` puts stress on the island fall. The passed row says the step and the light stay the same.
- Routing the pad swoop through `StartGlideHome`, or the ease bonk through the arc, crosses two returns. Crumb eject covers day camp, night boot, and beast charge. The pad arc is the local swoop that replaced the teleport loop.
- The six visibility traces inside `BeginBonkReturn` are what shove the landing off clutter. Moving them moves the landing the playtest asked for.
- `EndPartyOuting(Bonk)` is inside the flight. A caller that only wanted the arc would send the family home.
- `TickBonkReturn` runs only from `UpdateOpeningBonk`, and that runs only on SizeTest. Hoisting the tick while leaving the old call double-steps the swoop. Dropping it without a hoist leaves the pawn in flying with move input ignored.

The one small fix still worth doing: at the top of `BeginBonkReturn` in `HomeWorldCharacter.cpp`, return if `bOpeningBonkReturning` is already set. That is about four lines. The detector already bails, so today's fall does not change. A later guard or second pad cannot restart the arc mid-flight and bring the retrigger loop back. Do that after the swoop play, not as a pass.
