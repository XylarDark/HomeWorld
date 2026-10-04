"""End a session by handing the next one a question, not a silence.

WHY THIS EXISTS. The Lead's stated need, 2026-10-04: after a session ends the
developer should be prompted with a question that advances to the next session,
because a session that simply stops leaves them disengaged and off the critical
path. Keeping that engagement is the whole job here. The question is the
mechanism.

So this script answers one question - what is the critical path right now, and
what single thing is next - and prints it. It is not a summary tool. A summary
is what you already have: POLISH_READINESS.md. This exists to end with a
question.

THE CRITICAL PATH IS DERIVED, NOT ASSERTED. `polish_readiness.py` already
encodes the one rule the industry is consistent about: a gate cannot open while
the gate beneath it is red. That is a real dependency chain, G-ENV -> G-ASSET ->
G-FEEL, and it means the furthest-back red gate is the critical path. Not the
row with the most problems, and not whatever was worked on last. The gate whose
blockers delay every later gate.

WHAT THIS WILL NOT DO. It does not choose feel, does not rank which of your open
questions matters most, and does not decide whether a red row should be waived.
It orders what is already ordered, then asks. Where the honest answer is "you
pick", it says that rather than inventing a preference - a recommendation about
art is exactly the thing this repo forbids an agent from producing.

Three question shapes, chosen by what is actually on the path:

  agent work available    the path is clear enough that the agent should be
                          working. Says so, and points at the row.
  human labour            the path runs through work only you can do. Prints
                          the steps, in order, resumable.
  needs your judgment     the path runs through a decision. Asks it, with the
                          options and a recommendation if one is recorded.

Run with --json for the machine-readable form. Exit code is 0 whenever a
question was asked, including "the agent has work" - this is not a gate and
must not fail a build over a red row.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import polish_readiness as pr

#: Gate order, earliest first. Mirrors the `_upstream` chain in
#: polish_readiness: G-ASSET declares dep on G-ENV, G-FEEL declares dep on
#: G-ASSET, so this is read off the code rather than chosen.
GATE_ORDER = ("G-ENV", "G-ASSET", "G-FEEL")

#: Which human-use job each question belongs to, from
#: docs/human-use/OWNERSHIP.md. Printed so the reader knows whether they are
#: being asked for a judgment, a piece of labour, or a steer ruling.
JOB_FOR_KIND = {
    pr.DECIDE: "steer/taste - yours",
    pr.DO: "test - your hands",
    pr.ENV: "environment - nobody's move",
    pr.AGENT: "agent-owned",
    pr.HELD: "decided - not a question",
}

#: Kinds that do NOT become the closing question, and why.
#:
#: HELD is excluded because its answer is already on file. Offering the Lead a
#: red row whose own note says "the correct action right now is none" invites
#: either a re-answer to a settled question or the false conclusion that the
#: agent is blocked on him. The script's first draft did exactly that, which is
#: why this is a named exclusion rather than a lucky ordering.
#:
#: ENV is excluded for the opposite reason and needs care. An environment block
#: is real work with a real owner - you - so it is not skipped by default; it is
#: only reached when no decision and no labour is on the path. Waiting is correct
#: for nobody to be blamed, but it is still a thing that has to be unblocked, and
#: silence about it is how a stale editor assumption outlives the session.
NEVER_ASK = (pr.HELD,)


#: Phrases that mean "this row is not awaiting an answer", found in the rows
#: whose next_action was written to say so. Kept narrow on purpose: this is not
#: prose-sniffing in general, it recognises the one explicit signal the gate
#: itself uses to park a row until a later pass.
_HELD_MARKERS = (
    "correct action right now is none",
    "stays red until",
)


def _is_held(c: pr.Check) -> bool:
    """True when a row's own text says it is not awaiting a decision.

    A decide-classified row whose action names no next step is not deciding
    anything. Demoting it is the difference between asking the Lead to re-answer
    a question the repo already answers, and asking the one that is actually
    open - which on 2026-10-04 is the severity ladder in the queue.
    """
    text = f"{c.next_action} {c.note}".lower()
    if any(m in text for m in _HELD_MARKERS):
        return True
    return not (c.next_action or "").strip()


def _blocked(checks: list[pr.Check]) -> list[pr.Check]:
    return [c for c in checks
            if c.state in (pr.FAIL, pr.MISSING, pr.STALE)
            and not c.id.startswith("dep.")]


def critical_gate(gates: dict[str, pr.Gate]) -> str | None:
    """The furthest-back red gate: the one delaying everything after it.

    Walking GATE_ORDER from the front and returning the first non-GREEN gate is
    the definition. If G-ENV is red, nothing in G-ASSET or G-FEEL can be
    entered, so G-ENV is the path regardless of how much work G-FEEL needs.

    A gate that is GREEN does not block, so it is skipped - which means a fully
    green G-ENV correctly exposes G-ASSET as the path.
    """
    for gid in GATE_ORDER:
        g = gates.get(gid)
        if g is None:
            return None
        if g.state != pr.GREEN:
            return gid
    return None


def path_rows(gates: dict[str, pr.Gate], gate_id: str) -> list[pr.Check]:
    """Blocked rows inside the critical gate, hardest-first within the gate.

    Ordering within the gate is by kind, not by row id: the point of the
    classification is that labour the developer owes is what unblocks a session,
    and a decision is what unblocks a session sooner. AGENT rows come last
    because they are not blocking anyone.
    """
    g = gates.get(gate_id)
    if g is None:
        return []
    rank = {pr.DECIDE: 0, pr.DO: 1, pr.ENV: 2, pr.AGENT: 3, pr.HELD: 4}
    return sorted(_blocked(g.checks),
                  key=lambda c: (rank.get(c.action_kind, 9), c.id))


def next_question(gates: dict[str, pr.Gate],
                  queue: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """The one question to end on. Never None, never silent.

    Priority is deliberate and follows the dependency chain rather than
    convenience:

      1. A decision on the critical path. A judgment blocks everything behind
         it and costs the developer one sentence, so it goes first.
      2. Labour on the critical path. Expensive in human time but it is the
         session's actual work.
      3. Agent work. If the path is clear of humans, say so - that is a real
         state, not an absence of one, and a session that ends "nothing to do"
         is the failure this script exists to prevent.

    A queued decision is promoted above a gate row when the gate has no DECIDE
    row, because a queued question is the only kind the developer can answer
    from a terminal without opening the editor.
    """
    queue = queue if queue is not None else pr.load_queue()
    open_qs = [d for d in queue if d.get("state") == "open"]
    gid = critical_gate(gates)

    if gid is None:
        return {
            "kind": "none_blocked",
            "gate": None,
            "question": (
                "Nothing is blocked: every gate is GREEN. Do we open the next "
                "stage, or is one of these three gates measuring the wrong "
                "thing?"),
            "job": "taste",
            "options": [
                "Open the next stage - the gates say we may",
                "A gate is measuring the wrong thing - name which",
                "Hold - something is not being measured at all",
            ],
            "recommendation": (
                "Before opening a stage, check whether a green gate means the "
                "right thing was measured. Every gate here has been RED for "
                "days, and a gate that has never been green has never been "
                "tested against a real pass."),
            "critical_path": [],
        }

    rows = path_rows(gates, gid)
    # A HELD row is not a decide, so it cannot lead - but a row *classified*
    # DECIDE whose own action says the correct action is none IS a held row that
    # was mislabelled. Detect that from the row's own text rather than trusting
    # the classification, because the whole failure here was trusting it.
    #
    # WHY TEXT AND NOT A FLAG. The signal is the row contradicting itself: a
    # decide-row that names no next step, or that says waiting is correct, is not
    # awaiting a decision whatever its kind says. That is checkable without
    # trusting prose in general - the test is narrow (an explicit marker), and it
    # only ever demotes, never promotes. A false positive costs a skipped
    # question; a false negative costs the Lead a session spent re-answering a
    # settled question.
    gate_decides = [c for c in rows
                    if c.action_kind == pr.DECIDE and not _is_held(c)]
    mislabelled = [c.id for c in rows
                   if c.action_kind == pr.DECIDE and _is_held(c)]
    gate_labour = [c for c in rows if c.action_kind == pr.DO]
    gate_env = [c for c in rows if c.action_kind == pr.ENV]
    gate_agent = [c for c in rows if c.action_kind == pr.AGENT]
    # Held rows are reported on the path but never become the question. They are
    # red on purpose, so the Lead re-answering one wastes a session on a settled
    # question and learns nothing about what is actually blocking.
    gate_held = [c for c in rows
                 if c.action_kind in NEVER_ASK or _is_held(c)]
    held_red = sorted({c.id for c in gate_held})

    # 1. A decision, from the gate or the queue.
    if gate_decides:
        c = gate_decides[0]
        return {
            "kind": pr.DECIDE,
            "gate": gid,
            "row": c.id,
            "question": (
                f"{gid} cannot advance past `{c.id}` until you decide: "
                f"{c.requirement}"),
            "job": JOB_FOR_KIND[pr.DECIDE],
            "detail": c.note,
            "action": c.next_action,
            "measured": c.measured,
            "also_waiting": [x.id for x in gate_decides[1:]],
            "held_red": held_red,
            "options": None,
            "recommendation": None,
            "critical_path": [x.id for x in rows],
        }
    if open_qs:
        q = open_qs[0]
        return {
            "kind": pr.DECIDE,
            "gate": gid,
            "row": None,
            "question": q.get("question", ""),
            "job": f"{q.get('job', '?')} - yours",
            "queued_id": q.get("id"),
            "blocks": q.get("blocks", []),
            "options": q.get("options"),
            "recommendation": q.get("recommendation"),
            "measured": None,
            # Reported even on the queued branch. A queue decision is chosen
            # precisely because it is the question to ask, and the rows it is
            # chosen over - including the ones deliberately held red - are the
            # context that makes it answerable.
            "held_red": held_red,
            "critical_path": [x.id for x in rows],
        }

    # 2. Labour.
    if gate_labour:
        c = gate_labour[0]
        return {
            "kind": pr.DO,
            "gate": gid,
            "row": c.id,
            "question": (
                f"{gid} is blocked on work only you can do. `{c.id}` is next "
                f"- open it now, or say which of the "
                f"{len(gate_labour)} labour rows you would rather do first?"),
            "job": JOB_FOR_KIND[pr.DO],
            "detail": c.note,
            "action": c.next_action,
            "measured": c.measured,
            "also_waiting": [x.id for x in gate_labour[1:]],
            "held_red": held_red,
            "options": None,
            "recommendation": (
                f"Start with `{c.id}` and work the rows in this order: "
                + ", ".join(x.id for x in gate_labour)),
            "held_red": held_red,
            "critical_path": [x.id for x in rows],
        }

    # 3. Environment - nobody owes anything, and saying so is the honest answer.
    if gate_env:
        c = gate_env[0]
        return {
            "kind": pr.ENV,
            "gate": gid,
            "row": c.id,
            "question": (
                f"{gid} is blocked on the environment, not on a person. "
                f"`{c.id}` needs: {c.next_action} - can you make that available, "
                f"or should we treat it as not blocking?"),
            "job": JOB_FOR_KIND[pr.ENV],
            "detail": c.note,
            "action": c.next_action,
            "measured": c.measured,
            "also_waiting": [x.id for x in gate_env[1:]],
            "held_red": held_red,
            "options": None,
            "recommendation": None,
            "critical_path": [x.id for x in rows],
        }

    # 4. The agent's own work. A real state, stated as one.
    if gate_agent:
        c = gate_agent[0]
        return {
            "kind": pr.AGENT,
            "gate": gid,
            "row": c.id,
            "question": (
                f"Nothing on {gid} is waiting on you. The agent can act on "
                f"`{c.id}` now - start it, or tell me to stop and hand back?"),
            "job": JOB_FOR_KIND[pr.AGENT],
            "detail": c.note,
            "action": c.next_action,
            "measured": c.measured,
            "also_waiting": [x.id for x in gate_agent[1:]],
            "held_red": held_red,
            "options": None,
            "recommendation": None,
            "held_red": held_red,
            "critical_path": [x.id for x in rows],
        }

    # The critical gate is red but every row is a dep rollup we filtered out.
    # Reaching here means the gate's redness comes from rows with no action
    # recorded - which the gate's own test forbids, so it is a bug, and saying
    # so is better than inventing a question.
    return {
        "kind": "unclassified",
        "gate": gid,
        "question": (
            f"{gid} is RED but no blocked row says who owes the next move. That "
            f"is a bug in the gate rather than a question for you - should I "
            f"fix it?"),
        "job": "agent-owned",
        "options": None,
        "recommendation": None,
        "critical_path": [],
    }


def _bullets(rows: list[pr.Check]) -> list[str]:
    out = []
    for c in rows:
        mark = f"**{c.id}** ({c.state}, {JOB_FOR_KIND.get(c.action_kind, '?')})"
        out.append(f"- {mark}")
        if c.note:
            out.append(f"  - {c.note}")
        if c.next_action:
            out.append(f"  - next: {c.next_action}")
    return out


def render(q: dict[str, Any], gates: dict[str, pr.Gate]) -> str:
    L: list[str] = []
    A = L.append
    A("# Closing this session")
    A("")
    A("Generated by `Content/Python/session_close.py`. Read-only.")
    A("")
    A("## The critical path")
    A("")
    if q["gate"] is None:
        A("Nothing is blocked. All three gates are GREEN.")
    else:
        A(f"**{q['gate']}** is the furthest-back red gate, so it is the path.")
        A("")
        A("The chain is real, not a ranking: a gate cannot open while the gate")
        A("beneath it is red, so everything after this one is waiting regardless")
        A("of how much work it needs.")
        A("")
        for gid in GATE_ORDER:
            g = gates.get(gid)
            if g is None:
                continue
            mark = "**<- here**" if gid == q["gate"] else ("blocked" if g.state != pr.GREEN else "green")
            A(f"- `{gid}` {g.state} — {mark}")
    A("")
    A("## Ask this")
    A("")
    A(f"> **{q['question']}**")
    A("")
    A(f"_Job: {q['job']}_")
    A("")
    if q.get("options"):
        A("Options:")
        A("")
        for i, o in enumerate(q["options"], 1):
            A(f"{i}. {o}")
        A("")
    if q.get("recommendation"):
        A(f"**Recommend:** {q['recommendation']}")
        A("")
    if q.get("measured"):
        A(f"Measured: `{q['measured']}`")
        A("")
    if q.get("detail"):
        A(q["detail"])
        A("")
    if q.get("action"):
        A(f"**To advance it:** {q['action']}")
        A("")
    if q.get("also_waiting"):
        A("Also waiting behind it: " + ", ".join(f"`{i}`" for i in q["also_waiting"]))
        A("")
    if q.get("critical_path"):
        gid = q["gate"]
        rows = path_rows(gates, gid) if gid else []
        if rows:
            A("Everything blocking that gate:")
            A("")
            L.extend(_bullets(rows))
            A("")
    if q.get("held_red"):
        A("Red on purpose, and not what I asked about: "
          + ", ".join(f"`{i}`" for i in q["held_red"])
          + ". Those are decided - the ruling says they stay red until the art"
            " pass, so there is no question for you in them.")
        A("")
    if q.get("queued_id"):
        A(f"Recorded in `Docs/qa/POLISH_QUEUE.json` as {q['queued_id']}.")
        A("")
    A("## Not asked, and why")
    A("")
    A("Nothing in this output picks art, picks a number, or decides which red")
    A("row matters most. Where the answer is genuinely yours, it says so and")
    A("stops.")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Print the question that ends this session.")
    ap.add_argument("--json", action="store_true",
                    help="machine-readable form")
    args = ap.parse_args(argv)

    gates = pr.build()
    queue = pr.load_queue()
    problems = pr.queue_problems(queue)
    q = next_question(gates, queue)

    if args.json:
        payload = dict(q)
        payload["queue_problems"] = problems
        payload["gate_states"] = {g: gates[g].state for g in GATE_ORDER if g in gates}
        print(json.dumps(payload, indent=2))
        return 0

    print(render(q, gates))
    if problems:
        print("\nThe decision queue is not trustworthy - fix "
              "Docs/qa/POLISH_QUEUE.json before relying on the options above:")
        for p in problems:
            print(f"  - {p}")

    # Deliberately always 0. A red gate is the normal state of this project and
    # is not a failure of this script. Returning non-zero here would make a
    # session close look like a broken build.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())