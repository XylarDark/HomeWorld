# Discovery context acceptance

This record defines a repeatable acceptance check for the pre-built discovery
context. It is provider-, model-, IDE-, and runner-agnostic. Run it in the
conversation being used for the work; a particular app window or a fresh chat
is not part of the contract.

## Acceptance sequence

Start from `Docs/context/SESSION_START.md`. Read exactly one file per step,
waiting for each read to finish before beginning the next:

1. `UserHarness/docs/human-use/route-context.md` — identify the state and its
   decision rule.
2. `Docs/context/HOMEWORLD_ROUTE.md` — read project route facts.
3. `UserHarness/docs/context/menu.md` — identify the available next questions.

Only after all three reads, ask one concise discovery question. It must not ask
the developer to name a bite or invite the agent to choose one. The developer
names any additional files. If an unrelated second task appears, alert and stop.
If evidence shows route context is needed, use the transition question below;
do not open a second context before the developer confirms.

The state file and route facts may be inspected through the current environment's
normal file-reading interface. Do not claim a read happened if it did not. If
that interface cannot enforce sequential reads, issue separate read operations
and wait for each result before the next.

## Context transition acceptance

The one start door may offer another context only after identifying evidence that
it is needed. The offer must state that evidence, ask whether to
switch, and wait. No files from the other sequence are read before a yes. A no
keeps the session in the current context or ends it at that boundary. Topic
keywords alone are not a trigger. Test both directions separately. An unrelated
second task still triggers an alert and stop.

## Result record

Record the tested provider/model and interface as test metadata only; these are
not workflow requirements. Mark each ordered read observed or failed, note the
question asked, and report pass or fail. A response that merely paraphrases the
files without executing this sequence is not a pass. This is a procedural check,
not evidence that a later development task or cloud/glider implementation is
ready.

## ChatGPT trial — 2026-10-05

Interface: ChatGPT conversation with repository shell access. All three ordered
reads returned in separate completed operations. The route facts were read
after the state rules and before the menu. No fourth state or new route fact was
invented. Discovery did not open the route start. Result: **pass** for the
procedural acceptance check. The provider is test metadata only; this does not
validate other interfaces or implementation readiness.

## Codex trial — 2026-10-05

Interface: Codex conversation with repository shell access. The discovery
sequence and route-start reads were each completed one file at a time. The
developer directly named the current steered cloud descent before the route
handoff rule was added, so the evidence-question transition was not exercised.
Result: discovery and route sequences observed; bidirectional offer-and-wait
criterion **not yet tested**. This does not validate the cloud/glider
implementation.
