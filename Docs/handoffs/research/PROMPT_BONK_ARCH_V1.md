# PROMPT BONK_ARCH_V1

Filed 2026-10-22 by Grok Bot for the research file protocol (Docs/handoffs/RESEARCH_PROMPT_CONTRACT.md). Sent to Cursor chat "Bonk system architecture review" (Ask, Grok 4.7 Extra High). The ASK section is the staged prompt file q2/bonkq.txt, verbatim. The other headings were added at filing time from tonight's dispatch; they are context, not part of the text that was sent.

## ROLE

Engineer advising Lead whether the bonk system needs an architecture pass.

## CONTEXT

HomeWorld repo on 2026-10-22, after the interaction-resolver stack, before fix/bonk-reentry-guard.

## CANON

HomeWorldBonkArc.h, HomeWorldBonkArcTests.cpp, the bonk code in HomeWorldCharacter.cpp, stress hooks (+5 per bonk, cap 100).

## ASK

Read-only question; don't edit anything. Lead wants to know whether the bonk system needs an architecture pass. Your earlier review judged BeginBonkReturn(Target) already the right shape. Look at HomeWorldBonkArc.h, HomeWorldBonkArcTests.cpp, the bonk code in HomeWorldCharacter.cpp, the stress hooks that bonks feed (+5 per bonk, cap 100), and anything else bonk touches (HUD, opening, wisp, guards).
Answer:
1. Is it worth a pass, yes or no, and why?
2. If yes, list concrete changes, each with the files touched, rough size, and what it saves in future implementation and testing (e.g. new bonk targets, guards, stress, camera).
3. What breaks or risks regressions if we change it?
4. If no, what's the one smallest improvement still worth doing, if any?
Keep it under 500 words.

## NON-GOALS

Read-only; do not edit anything.

## DONE-WHEN

Answer the four numbered questions in under 500 words.

## child Research needed?

N.
