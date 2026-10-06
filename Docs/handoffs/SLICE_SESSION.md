# Slice session (model-agnostic)

Any agent that reads `AGENTS.md` follows this. Do not depend on Cursor rules or `CLAUDE.md`.

Sessions start at `Docs/context/SESSION_START.md`. Use this file only once Luke names a slice job (steer, taste, or test).

## Start

The door has already been read. Do not read it again, and do not reopen ownership or cycle from here.

1. Read the latest `Docs/handoffs/SESSION_HANDOFF_*.md` if one exists for this slice. Do not read the full session log.
2. Canon for product scope: `Docs/VISION_BOARD.md`, then `Docs/01_GDD_MVP.md` and `Docs/02_ART_BIBLE.md`.
3. Name the job (steer, taste, or test). Draft the contract from the human's words. Ask with numbered options, then stop. Do not edit until the scenarios are confirmed.
4. Build with `Tools/Safe-Build.ps1`. A clean log is not done. The human plays the slice and explains it in one minute. Disclose what you wrote and what you did not verify.

Shaping does not waive Steer or Test.

## When to open a new chat

Open a new chat when the slice changes, or when this chat is past the dumb zone (about 60k tokens — instruction-following degrades). Do not open a new chat for a one-line follow-up on the same slice.

Before you leave, write `Docs/handoffs/SESSION_HANDOFF_<slice>.md` from the template below and append one line to `docs/SESSION_SUMMARY.md`. The next chat starts from that file, not from this transcript.

## Handoff template

```
# SESSION_HANDOFF_<slice>

Slice:
Canon checked:
Job confirmed: steer | taste | test
Scenarios the human accepted:
Changed paths:
Evidence: command, count, pass | fail | inconclusive
Human play: what they saw, one-minute explanation (or not yet)
Disclosed / not verified:
Do not redo:
Next action:
```
