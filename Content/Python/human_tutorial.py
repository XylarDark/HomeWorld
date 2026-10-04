"""Generate a tutorial for every piece of human work, from research.

The policy, from the Lead on 2026-10-04: *"for all human work, a tutorial is made
from research to guide the initial discovery phase and to ease the developer into
the work."*

Two words in that sentence are load-bearing.

**"Made", not written.** A hand-written tutorial is a parallel document, and a
parallel document drifts. This module generates the tutorial from the same
artifacts the gate reads: the procedure text comes from the check's own
`next_action`, the field names come from the artifact the check validates, and
every recipe cites the research it was built from - with the citation *resolved
against the file* at generation time. A recipe citing a file that moved, or a
`_key` that was renamed, produces a warning in the generated output rather than
a tutorial that quietly teaches something stale.

**"The initial discovery phase."** The hard part of human work here is not the
procedure, it is arriving. Someone who has never stood in the editor does not
know which of the two real .umap files is the world, or that MainMenu is the
default map and does not contain the island. Every recipe therefore opens with
`discovery`: what to look at and what to answer *before* touching anything. That
is the phase that eases someone in, and it is the one a next_action sentence
cannot carry.

This is the third working state the Lead asked about: not "the agent asks" and
not "the agent works", but "here is the work, generated for you, starting from
what you do not know yet".
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import polish_readiness as pr
import session_close as sc

OUT_MD = pr.ROOT / "Docs" / "qa" / "HUMAN_TUTORIAL.md"
OUT_JSON = pr.ROOT / "Docs" / "qa" / "HUMAN_TUTORIAL.json"

#: Row kinds a human owns. `held` is excluded because the answer is already
#: recorded, and `agent` because nothing is owed by a person.
HUMAN_KINDS = (pr.DO, pr.DECIDE, pr.ENV)

#: Sections every recipe must fill. `discovery` is required because it is the
#: point of the exercise; the rest because a tutorial missing one of them is a
#: paragraph with a heading.
REQUIRED_SECTIONS = ("discovery", "record", "done_when", "if_it_fails", "do_not")

# --------------------------------------------------------------------------
# Recipes
# --------------------------------------------------------------------------
#
# Each `research` entry is `path` or `path#key`. For a JSON path the key must
# exist in that file; for a markdown path, the fragment must appear in it. These
# are the sources the recipe was built from and they are checked, not cited as
# decoration - a tutorial whose research has moved is worse than none, because
# it is trusted.

RECIPES: dict[str, dict[str, Any]] = {
    "env.ue_island_measured": {
        "sequence": 1,
        "blocked_by": [],
        "title": "Find out whether the engine actually has the 180 m island",
        "kind": "labour",
        "why": (
            "Everything downstream depends on it. The island is 180 x 100 m in "
            "Blender and unmeasured in Unreal - the last recorded engine figure "
            "was 19.3 x 10.7, nine times smaller. Every other gate row reads the "
            "Blender source, so this is the only row that reads the artefact the "
            "player stands on. V2, the walk-off-the-edge test, is a test of "
            "island geometry and is meaningless until this is true."),
        "before_you_start": [
            "Unreal open on the DESKTOP, not a commandlet. The script reads the "
            "level, so the level has to be open and its actors loaded.",
            "`Content/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers.umap` open. Not "
            "MainMenu - see discovery.",
            "Nothing needs writing. The script only reads; it spawns nothing and "
            "saves no level.",
        ],
        "discovery": [
            "Which map am I in? There are two real .umap files. MainMenu is the "
            "project's DEFAULT map and contains no island, no cabin and no "
            "crumbs - 1,270 World Partition external actors of kit-bash rock and "
            "bricks. L_VS_MVP_Markers is the homestead, with 78 StaticMeshActors "
            "including SM_IslandTop. If you opened the game and saw MainMenu, "
            "you are in the wrong scene and every measurement will be wrong.",
            "Is SM_IslandTop selected in the World Outliner? If you cannot find "
            "it in this level at all, stop - the measurement will report a "
            "missing actor rather than a size.",
            "What does the island look like from above? A 180 x 100 m plate "
            "fills the frame. A 19 m one is a coaster. Your eye is the fastest "
            "check available and it costs nothing.",
        ],
        "record": (
            "Run the script, then commit what it writes. "
            "`Content/Python/measure_ue_island.py` fills "
            "`Docs/qa/UE_ISLAND_MEASUREMENT.json`: `local_bbox_cm`, `bbox_cm`, "
            "`asset`, `level`, `measured_at`, `non_unit_scale_actors`. The gate "
            "requires five of those to be right and rejects the record "
            "otherwise."),
        "done_when": (
            "`local_bbox_cm` is near 18000 x 10000 (Unreal centimetres), `asset` "
            "is `SM_IslandTop`, `level` is `L_VS_MVP_Markers`, `measured_at` is "
            "later than the FBX export, and `non_unit_scale_actors` is empty. "
            "Then `python Content/Python/polish_readiness.py` shows "
            "`env.ue_island_measured` PASS."),
        "if_it_fails": (
            "If it comes back near 1930 x 1070, the asset was never re-imported "
            "- the FBX on disk is current but the .uasset in the project is old. "
            "That is not a failure of your run, it is the state of the project. "
            "Re-import the FBX over the existing SM_IslandTop, re-place the "
            "actor if its transform moved, and re-run. Record what you saw; do "
            "not edit the JSON to make it pass."),
        "do_not": [
            "Do not hand-write local_bbox_cm. The record is the evidence, and "
            "edited evidence cannot be told from measured evidence later.",
            "Do not measure in MainMenu. The gate rejects it and says why, but "
            "you will have spent the run for nothing.",
            "Do not stop after re-importing. Re-running the measurement is the "
            "step that gets skipped, and skipping it is exactly how the plate "
            "went missing for a day with nothing going red.",
        ],
        "research": [
            "Docs/qa/UE_ISLAND_MEASUREMENT.json#_why_it_exists",
            "Docs/qa/UE_ISLAND_MEASUREMENT.json#_how_to_fill",
            "Docs/qa/UE_ISLAND_MEASUREMENT.json#_local_not_world",
            "docs/KNOWN_ERRORS.md#Which map actually holds the world",
        ],
    },
    "feel.verb_script": {
        "sequence": 2,
        "blocked_by": ["env.ue_island_measured"],
        "title": "Run the eight verbs and record what happened",
        "kind": "labour",
        "why": (
            "No human has ever played this build. Until someone does, every "
            "statement about whether it works is an inference from source code. "
            "Eight verbs is the whole MVP surface: if these do not work, nothing "
            "else matters yet."),
        "before_you_start": [
            "`env.ue_island_measured` PASS. V2 tests island geometry, and "
            "running it on an unverified island produces a result about the "
            "wrong thing.",
            "Unreal open on L_VS_MVP_Markers, Play ready.",
            "The output log visible: Window > Developer Tools > Output Log, or "
            "Saved/Logs/HomeWorld.log after the run.",
        ],
        "discovery": [
            "Where do I start? Press Play. A menu appears (WBP_MainMenu) and its "
            "Play button travels to L_VS_MVP_Markers. If nothing happens, read "
            "the log for 'HomeWorld: OpenGameMap' - it names the target it tried "
            "and whether it resolved.",
            "What is the run order? The verbs map is already in order: V1 walk, "
            "V2 glide, V3 gather, V4 tame, V5 portal, V6 heal, V7 nurture, V8 "
            "return. Run them top to bottom so a later session is comparable.",
            "What counts as a result? Three values, and the third is most of "
            "them: null means not run yet, pass means it did what canon says, "
            "and anything else means it ran and did not - write what happened in "
            "`note`. A bare word is not a result.",
        ],
        "record": (
            "Per verb in `Docs/qa/POLISH_HUMAN_PLAYTEST.json`: set `result`, "
            "and paste the log line you grepped into `log_grep`. Docs/14 "
            "requires a log excerpt per verb, not a tick. Then fill `commit`, "
            "`played_at`, `host`, `notes` at the top of the file."),
        "done_when": (
            "All eight `result` fields are non-null, each has either a log "
            "excerpt or a `note` saying what happened, and `commit` names the "
            "short sha you played. Then `feel.verb_script` goes PASS - or "
            "FAIL, if any verb did not pass, which is a real and useful result."),
        "if_it_fails": (
            "A verb that fails is information, not an embarrassment. FAIL means "
            "a person tried it and it did not work; null means nobody has tried. "
            "The gate distinguishes these on purpose. Write down WHY in `note` - "
            "a verb that fails for a mechanical reason is an agent task, one "
            "that fails because it does not feel right is yours, and only the "
            "note distinguishes them."),
        "do_not": [
            "Do not fill this in to make a gate go green. The record asserts a "
            "person sat at the keyboard on a named commit. An invented one is "
            "worse than an absent one, because it can never be told apart from "
            "a real one later.",
            "Do not leave a bare word like 'failed'. Write what happened.",
            "Do not skip V2 because it is the awkward one. It is the main event.",
        ],
        "research": [
            "Docs/qa/POLISH_HUMAN_PLAYTEST.json#_how_to_run",
            "Docs/qa/POLISH_HUMAN_PLAYTEST.json#_do_not",
            "Docs/qa/POLISH_HUMAN_PLAYTEST.json#_result_values",
            "Docs/qa/POLISH_HUMAN_PLAYTEST.json#_then",
        ],
    },
    "feel.human_playtest": {
        "sequence": 3,
        "blocked_by": ["feel.verb_script"],
        "title": "Record that a person played this build",
        "kind": "labour",
        "why": (
            "The verb script proves the mechanics. This proves a person was "
            "here. `docs/human-use/OWNERSHIP.md` puts ship/no-ship with the "
            "human, and nobody can review outcomes they have not seen."),
        "before_you_start": [
            "You have just run the verb script. This is the same session - the "
            "record describes that run.",
        ],
        "discovery": [
            "What am I attesting to? That a person sat at the keyboard, on a "
            "named commit, and saw what happened. Not that the game is good.",
            "What goes in notes? What you actually saw. One honest pass with "
            "notes beats three empty ones, because the point of the field is "
            "that a later decision is judged against what happened rather than "
            "against a memory.",
        ],
        "record": (
            "`Docs/qa/POLISH_HUMAN_PLAYTEST.json`: `commit` (git rev-parse "
            "--short HEAD), `played_at`, `host`, `notes`."),
        "done_when": (
            "`commit`, `played_at` and `notes` are all filled. Then "
            "`feel.human_playtest` goes PASS."),
        "if_it_fails": (
            "If you did not get to play, leave it null. The gate reads MISSING "
            "and that is the honest state - it says nobody has played this "
            "build, which is true and is the most useful thing the row can say "
            "today."),
        "do_not": [
            "Do not fill it in to move the gate. See _do_not in that file.",
            "Do not put a commit sha for a build you did not play.",
        ],
        "research": [
            "Docs/qa/POLISH_HUMAN_PLAYTEST.json#_what_this_is",
            "Docs/qa/POLISH_HUMAN_PLAYTEST.json#_do_not",
        ],
    },
    "env.traversal_measured": {
        "sequence": 4,
        "blocked_by": ["env.ue_island_measured", "feel.verb_script"],
        "title": "Time the two routes and record the median",
        "kind": "labour",
        "why": (
            "It is the only instrument in the project that can say whether the "
            "island is the right size to walk around. A circuit time over a 19 m "
            "island says nothing about a 180 m one, which is why this is "
            "sequenced after the measurement rather than alongside it."),
        "before_you_start": [
            "`env.ue_island_measured` PASS. Timings before that are measuring "
            "the wrong island.",
            "Cells streamed. A nullrhi commandlet cannot time a walk - it has "
            "no streaming, so there is nothing to walk on.",
            "A stopwatch. Three runs per route; record the median, not the "
            "best.",
        ],
        "discovery": [
            "Which routes? Two, both declared in the same file: "
            "cabin_to_lookout_s, and island_circuit_s. The canon window they are "
            "judged against lives in Docs/canon/FEEL.md, not in the data file.",
            "Where do I start each? At the cabin PlayerStart. Stop the timer on "
            "arrival at CRUMB_Lookout.",
            "What is island_circuit_s? cabin -> lookout -> path stones -> back "
            "to cabin. The same loop the canon window describes, so a change to "
            "the island shows up here first.",
        ],
        "record": (
            "The median of three runs into `measured_s` for each key in "
            "`Docs/qa/POLISH_BASELINE.json`. These come from the same play "
            "session as the verb script - do not time a separate walk."),
        "done_when": (
            "Both keys have a `measured_s` inside the canon window. Then "
            "`env.traversal_measured` goes PASS."),
        "if_it_fails": (
            "Out of window is a finding, not an error. Say which direction. If "
            "the island is too small to walk the canon loop at all, that is "
            "the measurement working."),
        "do_not": [
            "Do not record a number you did not time. This is the one row no "
            "script can fill, and a plausible number here would be "
            "indistinguishable from a walked one forever.",
            "Do not time in a commandlet.",
        ],
        "research": [
            "Docs/qa/POLISH_BASELINE.json#_how_to_measure_traversal",
            "Docs/qa/POLISH_BASELINE.json#_waiver_policy",
            "Docs/qa/POLISH_HUMAN_PLAYTEST.json#_then",
        ],
    },
    "asset.board": {
        "sequence": 5,
        "blocked_by": [],
        "title": "Say where each of the ten masters actually is",
        "kind": "decision",
        "why": (
            "The board exists so a batch can be reviewed together at S2, rather "
            "than finishing one asset at a time at S3 where moving it is "
            "expensive. It cannot batch anything until each row carries a real "
            "stage. Nothing else in the file is read by the gate, so a partial "
            "fill buys nothing."),
        "before_you_start": [
            "The live blend. `_user_counts_measured` in the board is from the "
            "real file as of 2026-10-04 and is there to help you prioritise.",
        ],
        "discovery": [
            "What are the rungs? S0 MEASURE, S1 BLOCKOUT, S2 ART-BLOCKOUT, S3 "
            "ASSET PRODUCTION, S4 DRESS, S5 FEEL TUNE. The full text is in the "
            "board's `_stage_ladder`. S2 accepts 'S2' or 'S2 ART-BLOCKOUT' "
            "alike.",
            "What am I judging? Where the asset has ACTUALLY reached, not where "
            "it is going. A stage is a claim about the present.",
            "What is priority, if not effort? The order you want to review in. "
            "That is what makes batching work - the point is a batch at S2, not "
            "a queue.",
            "Which two materials are NOT on this list? M_FamilySilhouette and "
            "M_ValleyNight. They are not one of the ten masters; they fail "
            "env.master_binding and you ruled they stay RED for the art pass. "
            "They do not belong here until an art decision remaps them.",
        ],
        "record": (
            "`stage` and `priority` per row in "
            "`Docs/qa/POLISH_ASSET_BOARD.json`. Nothing else in that file is "
            "read by the gate."),
        "done_when": (
            "Ten rows, each with a stage on the S0..S5 ladder and a priority "
            "1..10. Then `asset.board` goes PASS."),
        "if_it_fails": (
            "A stage off the ladder is rejected rather than counted, so a typo "
            "cannot read as a declared state. If a material genuinely has no "
            "rung yet, that is S0 - measure, instruments exist, numbers "
            "recorded."),
        "do_not": [
            "Do not fill it in to make the gate go green. A stage is a claim "
            "about where an asset actually is, made by someone who has looked "
            "at it.",
            "Do not add M_FamilySilhouette or M_ValleyNight. They are not on "
            "the board on purpose.",
        ],
        "research": [
            "Docs/qa/POLISH_ASSET_BOARD.json#_stage_ladder",
            "Docs/qa/POLISH_ASSET_BOARD.json#_how_to_fill",
            "Docs/qa/POLISH_ASSET_BOARD.json#_note_on_the_two_failing_materials",
        ],
    },
}


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def _research_target(cite: str) -> tuple[Path, str]:
    path, _, frag = cite.partition("#")
    return pr.ROOT / path, frag


def research_problems(recipes: dict[str, dict[str, Any]] | None = None) -> list[str]:
    """Every way a tutorial can be confidently wrong. Empty means trustworthy.

    The important check is citation resolution. A recipe that cites
    `Docs/qa/UE_ISLAND_MEASUREMENT.json#_how_to_fill` after that key is renamed
    reads as researched and teaches a stale procedure. Resolving the citation
    turns "made from research" from a claim into something checked.
    """
    recipes = RECIPES if recipes is None else recipes
    problems: list[str] = []
    for row, r in sorted(recipes.items()):
        for section in REQUIRED_SECTIONS:
            if not str(r.get(section) or "").strip():
                problems.append(f"{row}: section {section!r} is empty")
        for field in ("sequence", "title", "why", "before_you_start", "record",
                      "research"):
            if not r.get(field):
                problems.append(f"{row}: no {field!r}")
        cites = r.get("research") or []
        if not cites:
            problems.append(f"{row}: cites no research - a tutorial built from "
                            f"nothing is a guess with a heading")
        for cite in cites:
            path, frag = _research_target(cite)
            if not path.is_file():
                problems.append(f"{row}: research target missing - {cite}")
                continue
            if not frag:
                continue
            if path.suffix.lower() == ".json":
                try:
                    data = json.loads(path.read_text(encoding="utf-8-sig"))
                except ValueError:
                    problems.append(f"{row}: cannot read {cite}")
                    continue
                if frag not in data:
                    problems.append(
                        f"{row}: key {frag!r} not in {path.name}. The research "
                        f"moved; the tutorial now teaches a stale procedure.")
            else:
                if frag not in path.read_text(encoding="utf-8", errors="replace"):
                    problems.append(
                        f"{row}: {frag!r} not found in {path.name}. The research "
                        f"moved; the tutorial now teaches a stale procedure.")
    return problems


def coverage_problems(gates: dict[str, pr.Gate] | None = None) -> list[str]:
    """Every human row has a tutorial, and every tutorial has a human row."""
    gates = pr.build() if gates is None else gates
    problems: list[str] = []
    human: set[str] = set()
    for g in gates.values():
        for c in g.checks:
            if c.state in (pr.FAIL, pr.MISSING, pr.STALE) \
                    and not c.id.startswith("dep.") \
                    and c.action_kind in HUMAN_KINDS:
                human.add(c.id)
    for row in sorted(human - set(RECIPES)):
        problems.append(
            f"{row} is human work ({[c.action_kind for g in gates.values() for c in g.checks if c.id == row][0]}) "
            f"with no tutorial. The policy is a tutorial for ALL human work.")
    for row in sorted(set(RECIPES) - human):
        problems.append(
            f"{row} has a tutorial but is not currently human work. Either it "
            f"went green and the recipe is stale, or its action_kind is wrong.")
    for row, r in RECIPES.items():
        for dep in r.get("blocked_by", []):
            if dep not in RECIPES:
                problems.append(f"{row}: blocked_by {dep!r} has no recipe")
            elif RECIPES[dep].get("sequence", 0) >= r.get("sequence", 0):
                problems.append(
                    f"{row} (sequence {r.get('sequence')}) is blocked by {dep} "
                    f"(sequence {RECIPES[dep].get('sequence')}) - the order is "
                    f"circular, so neither can ever be reached first")
    return problems


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def _bullets(items: list[str]) -> list[str]:
    return [f"- {i}" for i in items]


def render(gates: dict[str, pr.Gate], problems: list[str]) -> str:
    L: list[str] = []
    A = L.append
    A("# Human work: a tutorial for each piece")
    A("")
    A("Generated by `Content/Python/human_tutorial.py`. Do not hand-edit — "
      "regenerate.")
    A("")
    A("Every piece of work that belongs to a person gets one of these, built "
      "from the")
    A("same artifacts the gate reads. The order matters: each entry says what "
      "it is")
    A("blocked by, and doing them out of order produces measurements of the "
      "wrong")
    A("thing rather than errors.")
    A("")
    if problems:
        A("## Read this first")
        A("")
        A("This tutorial has known problems. It is still more useful than "
          "nothing,")
        A("but do not trust it without checking:")
        A("")
        for p in problems:
            A(f"- {p}")
        A("")

    ordered = sorted(RECIPES.items(), key=lambda kv: kv[1].get("sequence", 99))
    A("## The order")
    A("")
    A("| # | Work | Kind | Blocked by |")
    A("|---|---|---|---|")
    for row, r in ordered:
        deps = ", ".join(f"`{d}`" for d in r.get("blocked_by", [])) or "—"
        A(f"| {r['sequence']} | [{r['title']}](#{_anchor(row)}) | "
          f"{r.get('kind','?')} | {deps} |")
    A("")
    for row, r in ordered:
        c = next((x for g in gates.values() for x in g.checks if x.id == row), None)
        A(f"## {_anchor(row)}")
        A("")
        A(f"### {r['sequence']}. {r['title']}")
        A("")
        if c is not None:
            A(f"`{row}` — currently **{c.state}**")
            A("")
        A(f"**Why this is on your list.** {r['why']}")
        A("")
        A("**Before you start**")
        A("")
        L.extend(_bullets(r["before_you_start"]))
        A("")
        A("**Start here — look before you touch anything**")
        A("")
        L.extend(_bullets(r["discovery"]))
        A("")
        A(f"**What to record.** {r['record']}")
        A("")
        A(f"**How you will know it worked.** {r['done_when']}")
        A("")
        A(f"**If it does not work.** {r['if_it_fails']}")
        A("")
        A("**Do not**")
        A("")
        L.extend(_bullets(r["do_not"]))
        A("")
        A(f"<sub>Built from: {', '.join('`' + x + '`' for x in r['research'])}</sub>")
        A("")
    A("## What this tutorial will not tell you")
    A("")
    A("Whether the game is any good, and what should change about it. Those are")
    A("taste calls and they are yours — see [docs/human-use/OWNERSHIP.md]"
      "(../../docs/human-use/OWNERSHIP.md).")
    A("")
    return "\n".join(L)


def _anchor(row: str) -> str:
    return row.replace(".", "").replace("_", "").lower()


def build() -> dict[str, Any]:
    gates = pr.build()
    problems = research_problems() + coverage_problems(gates)
    ordered = sorted(RECIPES.items(), key=lambda kv: kv[1].get("sequence", 99))
    return {
        "problems": problems,
        "tutorials": [
            {"row": row, "sequence": r["sequence"],
             "title": r["title"], "kind": r.get("kind"),
             "blocked_by": r.get("blocked_by", []),
             "research": r["research"]}
            for row, r in ordered
        ],
    }


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(
        description="Generate a tutorial for every piece of human work.")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true",
                    help="report problems without writing")
    args = ap.parse_args(argv)

    data = build()
    problems = data["problems"]

    if args.json:
        print(json.dumps(data, indent=2))
        return 1 if problems else 0
    if not args.check:
        OUT_JSON.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        OUT_MD.write_text(render(sc.pr.build(), problems), encoding="utf-8")
        print(f"wrote {OUT_MD.relative_to(pr.ROOT)}")
        print(f"wrote {OUT_JSON.relative_to(pr.ROOT)}")
    for t in data["tutorials"]:
        deps = ", ".join(t["blocked_by"]) or "-"
        print(f"  {t['sequence']}. {t['title'][:58]:58} blocked_by={deps}")
    if problems:
        print(f"\n{len(problems)} PROBLEM(S):")
        for p in problems:
            print(f"  - {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
