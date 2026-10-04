"""Which phase of a task is this, and may anyone say it is approved?

WHY THIS EXISTS. The Lead set the task format on 2026-10-04:

    research -> design -> questions -> design refinement / approval
             -> implementation -> implementation questions / refinement / approval
             -> testing -> task approval / refinement

Written as guidance it drifts within a week, because the agent that benefits
from skipping the middle is the agent writing the checklist. So the ladder lives
in code, and the whole module exists to enforce ONE invariant that prose cannot:

    **Approval is never self-granted.**

Everything else here is bookkeeping. That one is the load-bearing part. A phase
marked `approved` without a named human who is not the agent is the exact defect
class this project has spent three sessions closing - a seeded record that reads
as done. An agent that can approve its own design has not implemented a process,
it has implemented a rubber stamp that costs a reviewer's attention and returns
nothing.

Read [docs/human-use/CYCLE.md](../../../docs/human-use/CYCLE.md) for the ladder
and who owns each step. This module is the machine-checkable part, not the
process.

WHAT THIS WILL NOT DO. It does not decide whether a task is *good*, whether the
design is right, or whether the phase order suits a particular job. It checks
that the record is honest about who did what and in what order. Taste is not
machine-checkable and this does not pretend otherwise.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

#: The ladder, in order. Names are the ones the Lead used, lowercased and
#: underscored so they are stable identifiers rather than prose.
#:
#: Owner per phase:
#:   research      agent      - read the repo, measure, do not guess
#:   design        agent      - propose, with alternatives
#:   questions     both       - agent asks; human answers what only they know
#:   design_approval human    - the design is agreed before it is built
#:   implementation agent     - build it
#:   implementation_review both - questions, refinement, approval of what was built
#:   testing       agent      - prove it, including proving the guard
#:   task_approval human      - accept, refine, or reject the whole task
#:
#: Why approval sits AFTER implementation as well as before: the Lead's format
#: has it in both places deliberately. Pre-approval stops the agent building the
#: wrong thing; post-approval is where the agent surfaces "here is what I did
#: not verify", which is the one thing a reviewer cannot reconstruct later.
PHASES = [
    ("research", "agent"),
    ("design", "agent"),
    ("questions", "both"),
    ("design_approval", "human"),
    ("implementation", "agent"),
    ("implementation_review", "both"),
    ("testing", "agent"),
    ("task_approval", "human"),
]
PHASE_ORDER = [p for p, _ in PHASES]
OWNER = dict(PHASES)

#: The two phases whose whole point is that a human said yes.
APPROVAL_PHASES = ("design_approval", "task_approval")

#: Legal values for a phase's `state`.
#:
#: `skipped` exists because the Lead said "where it makes sense". A task with no
#: design question must be able to say so without running an empty phase - but it
#: must say WHY, or "skipped" becomes the default for every phase and the ladder
#: records nothing. That is the opposite failure and it is caught below.
STATES = ("pending", "done", "skipped", "approved", "needs_revision")

#: Who may not approve anything. Spelled several ways because the temptation is
#: to write "agent" in one record and "AI" in another and neither trips a check.
NON_HUMAN = {"agent", "ai", "assistant", "model", "codex", "claude", "gpt",
             "bot", "automation", "self", "me"}


def phase_problems(record: dict[str, Any]) -> list[str]:
    """Everything wrong with a task record. Empty means it is trustworthy.

    Read `record` rather than a file so the rules are testable without disk, and
    so the same function serves the CLI, the gate, and the tests.
    """
    problems: list[str] = []

    raw = record.get("phases")
    if not isinstance(raw, list) or not raw:
        return ["no `phases` list - the record says nothing about this task"]

    seen: list[str] = []
    for i, entry in enumerate(raw):
        where = f"phases[{i}]"
        if not isinstance(entry, dict):
            problems.append(f"{where}: not an object")
            continue
        name = entry.get("phase")
        if name not in PHASE_ORDER:
            problems.append(
                f"{where}: phase {name!r} is not one of the ladder: "
                + ", ".join(PHASE_ORDER))
            continue
        if name in seen:
            problems.append(f"{where}: phase {name!r} appears twice")
            continue
        seen.append(name)

        state = entry.get("state")
        if state not in STATES:
            problems.append(f"{where} ({name}): state {state!r} not one of "
                            + ", ".join(STATES))
            continue

        if state == "skipped" and not str(entry.get("reason") or "").strip():
            problems.append(
                f"{where} ({name}): skipped with no reason. A skip without a "
                f"reason is how every phase becomes optional and the ladder "
                f"records nothing.")
        if state == "done" and not str(entry.get("evidence") or "").strip():
            problems.append(
                f"{where} ({name}): done with no evidence. 'Done' is the "
                f"assertion that makes this process worth running; without a "
                f"path, a command, or a measurement it is a claim.")
        if state == "needs_revision" and not str(entry.get("reason") or "").strip():
            problems.append(
                f"{where} ({name}): needs_revision with no reason - nobody can "
                f"act on a revision nobody described.")

        # THE INVARIANT. Approval is the one thing an agent may not grant itself.
        if state == "approved":
            if name not in APPROVAL_PHASES:
                problems.append(
                    f"{where} ({name}): marked approved, but this is not an "
                    f"approval phase (only {', '.join(APPROVAL_PHASES)} are). "
                    f"Use `done` - claiming approval on a non-approval phase "
                    f"inflates the ladder into a scoreboard.")
                continue
            by = str(entry.get("by") or "").strip()
            if not by:
                problems.append(
                    f"{where} ({name}): approved with nobody named. This is the "
                    f"fail-open this module exists to close - a record that can "
                    f"say approved without saying who approved it.")
            elif by.lower() in NON_HUMAN:
                problems.append(
                    f"{where} ({name}): approved by {by!r}. Approval is never "
                    f"self-granted; the agent cannot approve its own work.")

    # Ordering. A later phase cannot be done while an earlier one is still
    # pending, because that is the shape of skipping the middle and calling it
    # progress.
    idx = {p: i for i, p in enumerate(PHASE_ORDER)}
    last_unresolved: tuple[int, str] | None = None
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        name = entry.get("phase")
        if name not in idx:
            continue
        state = entry.get("state")
        if state in ("pending", "needs_revision"):
            last_unresolved = (idx[name], name)
        elif last_unresolved is not None and idx[name] > last_unresolved[0]:
            problems.append(
                f"phases[{name}]: is {state} while `{last_unresolved[1]}` is "
                f"{'pending' if last_unresolved[1] else 'unresolved'}. Later "
                f"phases cannot be finished ahead of an earlier one.")

    # A task with no approval phase at all has not been through the process.
    for ap in APPROVAL_PHASES:
        if ap not in seen:
            problems.append(
                f"phase {ap!r} is absent entirely. Record it as skipped with a "
                f"reason if it genuinely does not apply - absence is not the "
                f"same as 'not needed'.")
    return problems


def load(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return {}


def render(record: dict[str, Any]) -> str:
    L: list[str] = []
    A = L.append
    task = record.get("task") or "(unnamed task)"
    A(f"# Task phase: {task}")
    A("")
    problems = phase_problems(record)
    if problems:
        A("## This record is not trustworthy")
        A("")
        A("Fix these before reading the ladder as progress:")
        A("")
        for p in problems:
            A(f"- {p}")
        A("")
    A("| Phase | Owner | State | Evidence / by |")
    A("|---|---|---|---|")
    raw = record.get("phases") or []
    by_name = {e.get("phase"): e for e in raw if isinstance(e, dict)}
    for name in PHASE_ORDER:
        e = by_name.get(name)
        if e is None:
            A(f"| `{name}` | {OWNER[name]} | **absent** | — |")
            continue
        detail = e.get("evidence") or e.get("by") or e.get("reason") or ""
        state = e.get("state", "?")
        if state == "approved":
            detail = f"approved by {e.get('by', 'NOBODY')}"
        A(f"| `{name}` | {OWNER[name]} | **{state}** | {detail} |")
    A("")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Report which phase a task is in, and whether that is honest.")
    ap.add_argument("record", help="path to the task record JSON")
    args = ap.parse_args(argv)

    path = Path(args.record)
    if not path.is_file():
        print(f"no task record at {path}", file=sys.stderr)
        return 2
    record = load(path)
    problems = phase_problems(record)
    if "--json" in (argv or sys.argv):
        print(json.dumps({"task": record.get("task"),
                          "problems": problems,
                          "phases": record.get("phases")}, indent=2))
        return 1 if problems else 0
    print(render(record))
    # 1 for a dishonest record, 0 for a clean one. This IS a gate - unlike
    # session_close, whose job is to always have something to ask.
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())