# 38 — What UE developers actually do with AI agents

**Status:** RESEARCH. Read-only; this document changes no gate and no code.
**Date:** 2026-10-03. Requested by the Lead: *"research on what other UE
developers are doing to accomplish this with AI."*

Confidence tags are load-bearing. A reader must be able to tell a measured
result from a forum post without opening every link.

| Tag | Meaning |
|---|---|
| **[A]** | Primary source read directly — paper abstract, official docs, official repo. |
| **[B]** | Secondary: commentary, vendor marketing, forum snippets. |
| **[C]** | Our inference. Not a sourced claim. |

---

## 1. The finding that should change how we work

**CraftBench-UE** (Wu, Calderone, Tsen; arXiv 2609.23142, Sep 2026) **[A]**
evaluated agents on 70 real Unreal tasks with deterministic build, asset and
runtime checks and **no LLM judge**. Two results matter to us:

- C++ completion exceeded Blueprint by **30.0 and 42.9 percentage points**
  across two editor configurations, on paired tasks with identical runtime tests.
- Among on-time Blueprint submissions that **passed the asset checks, 42.2%
  and 50.0% failed explicit runtime assertions.**

That is the core risk of this project stated as a number: **Blueprint work
that looks fine, opens fine, and is asset-valid is wrong about half the time.**
Our own positive control already found the UE-specific version of this — the
editor's Python runner *imports* each module and never executes a single
assertion, so a green UE automation run proves the module parses, nothing
more. Two independent sources, same shape of failure.

**Consequence for us [C]:** keep agent work in text (C++, Markdown specs,
Python that runs under host pytest). Treat Blueprint and `.uasset` as
human-wired. Never let a UE automation green stand in for a behavioural claim.

## 2. What is real in UE tooling

**Epic shipped a first-party MCP server in UE 5.8** **[A]** —
[Unreal MCP docs](https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor).
Facts that will save us time:

- The plugin identifier is **`ModelContextProtocol`**, not "Unreal MCP".
  It exposes no tools alone; **`AllToolsets`** must also be enabled.
- HTTP/SSE only, **loopback only, no auth**. Epic: "not safe to expose beyond
  the local machine." Tool calls are serialised onto the game thread.
- `ModelContextProtocol.StartServer [port]`, `.RefreshTools`,
  `.GenerateClientConfig <Client>`; CLI flags exist for headless use.
- **Adding a new `UFUNCTION` does not propagate through Live Coding** — full
  restart required. Changing a *body* is fine, but then refresh and reconnect.
- Its `unreal-mcp` toolset already covers a **Testing** domain: discover, run
  and inspect C++ automation tests.

**Epic also publishes an official Claude Code plugin** **[A]** —
`EpicGames/unreal-engine-skills-for-claude-code-plugin`, MIT, in Anthropic's
official marketplace. Ships an `unreal-mcp` skill plus a `create-toolset`
scaffold, and a `SessionStart` hook that detects a UE repo.

> "Installing this plugin gives Claude broad, live access to the running
> Unreal Editor. Treat that access the same way you would treat running
> arbitrary code from an assistant, because in practice it is."
> — Epic's own README **[A]**

Its two most useful warnings, verbatim **[A]**: *"Localhost is not a trust
boundary"*, and *"Save and commit (or shelve) before any long MCP-driven
session so the working copy is recoverable."*

**Third-party:** `IvanMurzak/Unreal-MCP` (Apache-2.0, C++ plugin, 61 tools,
per-tool enable/disable enforced at the execution boundary, plus an
in-game runtime mode). `StraySpark` is $129 commercial; treat its blog as
marketing **[B]**.

## 3. Guardrails that are enforceable today, not aspirational

**Epic's Data Validation plugin** **[A]** ships enabled and is CI-callable:
`UnrealEditor-Cmd.exe <proj> -run=DataValidation`. Custom rulesets exist for
exactly our guardrails — *"Checking that assets meet name conventions /
enforcing space and performance budgets / catching non-cyclic dependencies"* —
and rules may be written in **C++, Blueprint or Python** via
`UEditorValidatorBase`. Our `master_binding` criterion is hand-rolled; this is
the supported mechanism and belongs in the same gate.

**Naming** **[A]**: Epic's official prefix table (`M_`, `MI_`, `T_`, `SM_`,
`SK_`, `BP_`, `ABP_`, `WBP_`, `PHYS_`, `FXE_`, `LS_`, …), the community
[ue5-style-guide](https://github.com/Allar/ue5-style-guide) pattern
`Prefix_BaseAssetName_Variant_Suffix`, and a machine-readable 180-convention
reference at [unrealdirective.com](https://unrealdirective.com/resources/project-standards/asset-naming/).

## 4. The quality-gate design worth copying

**Yurukusa**, *Why Your AI Agent Needs a Quality Gate (Not Just Tests)* **[A]** —
a first-person account of the exact failure mode we live with:

> "My AI agent would make a change, run the tests, see green checkmarks,
> commit, and move on. The tests passed. The code compiled. The game launched.
> And the game was *unplayable*. Zero damage taken in 60 seconds."

His claim: **"Tests verify correctness. Quality Gates verify value."** Three
tiers, thresholds externalised to JSON so an agent can retune them without
touching gate logic:

1. **Stability — hard gate.** Did it run at all (`total_fires >= 1`)? Zero
   fires means the player could not use the ability. *"That's not a balance
   issue — that's a broken game."*
2. **Balance band — soft, 3-of-4 majority.** One hard veto: dying in the
   first 60 s is NO-GO regardless.
3. **Regression vs saved baseline.** Warn >25% delta, NO-GO >50%.

Result over 26 runs: 18 GO, 4 CONDITIONAL, 4 NO-GO — *"it catches the bottom
15%, and that alone is worth the ~220 lines."*

His own stated limitations are the useful part **[A]**: the gate cannot
evaluate *feel*; a bot that happens to dodge everything can mask real problems;
**baseline drift** (many small negative changes, each under threshold);
**outlier contamination** (a spawn bug produced `peak_enemies: 153`, which
became the baseline and made every normal run look like a catastrophic
regression).

> "When a human developer ships code, there's an implicit quality gate running
> in their head. They play the game... When an AI agent ships code at 3 AM
> while you're asleep, that implicit gate doesn't exist. You need to make it
> explicit."

**Mapping to us [C]:** we already have the tier-1 half — `polish_readiness.py`
with exit 2 for "could not measure at all" and MISSING never passing. We do
**not** have tier 3 (baseline regression) or an externalised threshold file.
Those are the two gaps worth closing, and the 15% claim is a reason to expect
it pays.

## 5. Two measurements that reframe the cost

**METR RCT** (arXiv 2507.09089) **[A]**: 16 experienced developers, 246 real
tasks in repos they knew well, per-task randomisation, screen recordings.
**AI-allowed tasks took 19% longer** (CI +2% to +39%), while developers
**believed they were ~20% faster** — a ~40-point perception gap. Two honest
caveats: METR has said (Feb 2026) it is revising the design, and the figure is
specific to early-2025 tools; the population is mature large C++ OSS, arguably
our hardest case.

**GameDevBench** (arXiv 2602.11103) **[A]**: best agent+method solves 53.8% of
333 game-dev tasks; success drops from 51.4% (gameplay) to 33.0% (2D
graphics) — difficulty tracks *multimodal* complexity, not code complexity.
Its actionable result: simple image/video feedback lifted GPT-5.4 from **41.1%
to 52.0%**.

> **Consequence [C]:** give agents eyes. We already have
> `capture_shotlist_viewport.py`; wiring a screenshot into the loop is
> cheap and measured. And measure agent ROI with a clock, because self-report
> lies in exactly the direction that costs us the most.

## 6. The failure pattern to watch for

Kirsch's metroidvania post-mortem **[A]** (Godot, Apr 2026) is the most
detailed first-person account available. The decisive test: he asked the agent
to refactor a state machine out of a long player script. It reported success.

> "The state machine was basically a global variable the player script would
> check. **None of the logic or functionality made it into the state
> machine.** It was all still in the player script."

That is an **AI facade of a refactor**: structure cosmetically present,
behaviour absent — the same pathology CraftBench-UE measured at 42–50%.

**What caught it:** he asked the agent to *adversarially review its own work*.
His generalised conclusion, and ours to adopt **[C]**: *"the agents can't
handle more than 2-3 scripts at a time."*

## 7. Division of labor — three independent lines agree

Feel, pacing, tuning numbers and art direction stay human. Evidence **[A]**:

1. CraftBench-UE — compiling and asset-validating ≠ implementing intent.
2. GameDevBench — vision-facing work is the weak axis.
3. Yurukusa — *"the gap between numerically balanced and fun is still a human
   judgment."* And of his own gate: *"the gate said GO on builds that a human
   player would flag in 30 seconds."*

Plus arXiv 2603.27249, *"An Endless Stream of AI Slop"* **[A]** — 1,154
Reddit/HN posts coded, framed as a tragedy of the commons: *"individual
productivity gains externalize costs onto reviewers."* On a 1-human team the
reviewer *is* you and there is no second signature.

## 8. What we could NOT find — stated, not padded

1. **No primary account of Gauntlet used to verify AI-generated UE changes.**
   Gauntlet is real and documented; the AI-safety framing appears repeated
   without a source. Do not cite it as precedent.
2. **No credible practitioner spec for AI-driven Blender→UE environment
   blockout guardrails** — master-material enforcement, collision-proxy
   conventions, LOD budgets. The material is vendor tutorials or undetailed
   forum posts. §3 is the real, sourced answer and it is sufficient to start.
3. **No verified productivity number for AI-assisted UE5 development.** The
   widely repeated "38% reduction" traces to a page with content-farm
   artefacts and is unsourced. NVIDIA's post is vendor marketing.
4. **No longitudinal study** of UE agent adoption. Everything is a 2025–2026
   snapshot; nobody has published what happened after 12 months.
5. Reddit, Medium and blog.luden.io blocked automated fetching; those quotes
   are snippet-level **[B]** and approximate.

---

## 9. What we change, concretely

Ranked by measured payoff **[C]**, from the evidence above.

| # | Action | Grounded in |
|---|---|---|
| 1 | **Adversarial self-review as a standard step.** Before any commit touching mechanics, make a fresh agent try to break it and report what it cannot prove. | Kirsch's FSM facade was caught only this way **[A]**; our own positive control proved UE Python runs assert nothing **[A]** |
| 2 | **Add a baseline-regression tier** (tier 3) to `polish_readiness.py`, plus externalise thresholds to JSON. Guard specifically against baseline drift and outlier contamination. | Yurukusa hit both failure modes and documented them **[A]** |
| 3 | **Run `-run=DataValidation`** alongside our own checker, and port `master_binding` to a supported validator. | Epic Data Validation **[A]** |
| 4 | **Feed screenshots into the loop** for any environment or camera change. | GameDevBench: +11 points for trivial visual feedback **[A]** |
| 5 | **Enable Epic's `ModelContextProtocol` + `AllToolsets`** and use its Testing toolset rather than growing another runner. Commit before any long MCP session. | Epic 5.8 docs + README warnings **[A]** |
| 6 | **Keep agent work in C++ / Markdown / host-pytest.** Blueprint and `.uasset` are human-wired. | CraftBench-UE 30–43 pp C++/Blueprint gap **[A]** |
| 7 | **Measure agent ROI with a clock.** | METR: 19% slower, believed 20% faster **[A]** |

Not adopted, deliberately:

- **Gauntlet as an AI gate** — no primary source (§8.1).
- **Anything from a vendor selling an MCP server** — treat tool counts as
  marketing until audited (§8.3).
- **Autonomous end-to-end playtesting.** The one practitioner report **[B]**
  says they built it and it was "too slow and unstable to rely on"; what
  worked instead was making the agent *write its own documentation of the
  game systems first*. That part is worth stealing.

## 10. The one-line version

The industry evidence and our own session failures agree on the same shape:
**compiling, opening, and passing asset checks are not evidence that anything
works** — the measured rate for the latter is around half. Our differentiator
is not generating more code; it is refusing to call anything done that we
cannot demonstrate, and keeping feel in human hands. The gate work in
`Docs/37_POLISH_PASS_PROCESS.md` is the right shape. Tier 3 is the missing
piece.

---

## 11. Round two — studio practice, not papers (2026-10-04)

The first round asked what UE developers do with agents. This round asked a
different question: **is the way we divide work between the Lead and the agent
normal, and what does the industry do about the specific gaps we have?** Same
confidence tags.

### 11.1 Our AI/human split is the industry norm, not a doctrine we invented

**GDC 2026 State of the Game Industry** **[A]**, ~2,300 professionals: AI is
used for research/brainstorming **81%**, admin 47%, prototyping 35%, testing and
debugging 22%, asset generation 19% — and **player-facing features only 5%**.

Adoption by profession **[A]**: analytics 97%, art/design 43%, QA 37%.

Two readings, and both matter for us:

- The highest adoption is in analytical and back-office work; the lowest is
  anything a player experiences. That is precisely the split
  `docs/human-use/OWNERSHIP.md` already encodes — the agent does measurement,
  refactoring and process; the Lead keeps design, taste and feel.
- Negative sentiment toward generative AI rose **18% (2024) → 30% (2025) → 52%
  (2026)** **[A]**. The tooling is not the exposure. **Shipping AI-looking output
  to players is.** See §11.2.

So the vision in `docs/human-use/OWNERSHIP.md` is not a contrarian position
**[C]**. It is the mainstream shape, and the sentiment trend says it is also the
defensible one.

### 11.2 The commercial constraint, which until now existed only in chat

**Valve's January 2026 Steam content policy update** **[A]** requires disclosure
for **AI content that is shipped to, and consumed by, players**. Using AI for
tooling, workflow, or internal efficiency **requires no disclosure**.

The risk is therefore **not** that we use agents. It is **placeholders reaching
players** — and the reference cases are exactly that **[A]**:
*Clair Obscur: Expedition 33* (a painted-over programmer's face in an early
build) and *The Alters*. Both are placeholder incidents, not tooling incidents.

This is now written into `Docs/20_UASSET_AI_POLICY.md` §4A so it stops being
knowledge that only exists in a chat log.

### 11.3 We are behind on one thing: gates have a severity ladder

Automated content validation is standard studio tooling **[A]**, and the mature
implementations do not have a binary pass/fail. They ship a new rule as a
**warning**, promote it to an **error** once it has been clean for a while, and
only then let it block **[A]**. Our `polish_readiness.py` is binary.

We are **not** applying that unilaterally, and the reason is worth recording: on
2026-10-04 the Lead ruled that `master_binding` and `family_distinct` stay RED in
G-ENV. Adding a WARN tier and marking those two rows WARN would have quietly
undone that ruling by another name. The capability is recorded here as an option
and left for a decision.

One point is already satisfied **[C]**: separating "the check failed" from "the
check could not run at all" is the substance of a severity ladder, and we have it
— MISSING never passes, and `--selftest` exercises the fail-open paths directly.

### 11.4 Open question, deliberately not answered here

**"Polish" is the wrong name for this stage.** Industry usage defines polish as
the **alpha → beta** transition **[A]**. This project has not reached alpha: there
is no human playtest record, the engine has not been measured, and the asset board
is 0/10 declared. Calling pre-production work "polish" sets an expectation the
build cannot meet, and it is why `Docs/qa/POLISH_*` reads as though the game is
nearly done when it is at a vertical slice.

This is a scope-and-vocabulary call for the Lead. It is **recorded, not decided** —
renaming a stage would touch every gate row id, both `Docs/qa/POLISH_*` files and
four canon docs, and that is not a change to make unasked.

### 11.5 Traversal should be telemetry, not a stopwatch

**IO Interactive's *Kane & Lynch* pace-of-movement work** **[A]** treats
traversal as recorded telemetry analysed in aggregate, not a stopwatch on one
walk. That is a better instrument for `env.traversal_measured` than the single
median-of-three the baseline file currently describes: repeated samples plus a
distribution answer "is this island walkable?" far better than one number answers
"is this walk 60 seconds?".

The Lead deferred `traversal_measured` to the polish pass on 2026-10-04, so this
is recorded as the instrument to reach for when the time comes, not as work
started.

### 11.6 §9 item 1 is done, and it paid for itself immediately

The highest-ranked action in §9 was adversarial self-review before commit. It was
run on the two gate rows added the same evening **[A]**, and found **six ways to
turn them green without measuring anything** — including a `max(off_x, off_y)`
that silently discarded a NaN in the Y slot and reported PASS, and a comparison of
Blender's object-space box against Unreal's world AABB, which would have failed
on any rotated island.

Both were written by an agent minutes earlier and both were confidently
documented, with comments explaining why they were correct. That is the most
useful data point in this document: **a reviewer finds what the author's own
reasoning cannot**, and the cost was one background agent.