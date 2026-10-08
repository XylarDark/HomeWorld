# Hand-back

Open this file when the session is Co and the message says hand back. The door keeps the trigger. `mode: co — hand back` is that message. This file is the payload.

The session switches to Co mode if it is not already, says `mode: co (hand back)`, and writes one message that starts with `HANDBACK to HomeWorld Co`. Lead pastes that message into the room. It holds, in this order:

1. Main SHA the session last pulled.
2. Each PR: number, head SHA, merged or open, and what it waits for (Test score or Lead's yes).
3. Each item from the handoff: expected vs found, one line each. An item not started says `not started`.
4. Desk checks, only if Lead ran them: expected vs found.
5. Open questions for Lead, one per line, with no answer guessed.
6. Anything left uncommitted or unpushed, by path.

No transcripts, full logs, or gate JSON. Paths and SHAs only.
