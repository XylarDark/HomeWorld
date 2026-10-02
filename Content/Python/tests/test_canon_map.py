"""Contract tests for Docs/CANON_MAP.md - the pointer surface.

Written 2026-10-02, immediately after the consolidation failure that motivated it.

THE FAILURE THESE TESTS PIN

While implementing T0 I recorded this into the canonical must list:

    #17 Spirit-stealth - Found: **Nothing.** No stealth state, no awareness, no detection

That was false. Spirit-stealth was LOCKED on 2026-09-21, implemented across
HomeWorldSpiritStealthComponent.{h,cpp} + HomeWorldSpiritLitVolume.h + a 414-line
.cpp, and CLOSED with a Lead stamp (``APPROVE SS-A``) with every DONE-WHEN box
ticked. I wrote "Nothing" because no document in the T0 track pointed at
Docs/25_SPIRIT_STEALTH_IMPL.md.

This is the SAME failure class as the broken shrine: the shrines were in no spec, so
a lintel sitting on the ground survived every gate. There, a geometry check had
nothing to measure. Here, an index had nothing to point at. Both are "nothing
referenced it".

A map nobody checks goes stale, so the map is a test subject. These tests exist to
make CANON_MAP.md fail loudly rather than quietly rot.

Runs without Blender or Unreal: pure-Python, like test_homeworld_graybox_spec.py.
"""

import os
import re
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

from homeworld_graybox_spec import MASTER_NAMES  # noqa: E402

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CANON_MAP = os.path.join(REPO_ROOT, "Docs", "CANON_MAP.md")
MUST_LIST = os.path.join(REPO_ROOT, "Docs", "handoffs", "T0_MECHANIC_INVENTORIES_V1.md")

#: The canon six. Compost/dung yields RES_SEED, which is why this stays six.
CANON_RESOURCES = {
    "RES_HERB",
    "RES_SEED",
    "RES_WOOD",
    "RES_BERRY",
    "RES_FIBER",
    "RES_STONE",
}

#: Only backticked tokens that start at a known tree root are treated as paths.
#: Bare names like ``DAYNIGHT_`` in the bible row are deliberately NOT paths.
_PATH_ROOTS = ("Docs/", "docs/", "Lib/", "Maps/", "Content/", "Source/", "VisionBoard/", "swarm/")
_PATH_RE = re.compile(r"`((?:Docs|docs|Lib|Maps|Content|Source|VisionBoard|swarm)/[^`]+)`")


def _read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read()


def _section(text, heading):
    """Return the body of a '## N. heading' section, up to the next '## '."""
    start = text.find(heading)
    if start == -1:
        return ""
    rest = text[start + len(heading):]
    end = rest.find("\n## ")
    return rest if end == -1 else rest[:end]


def _exists_as_given(relative):
    """Resolve a map path on disk, expanding * globs. Directories count."""
    absolute = os.path.join(REPO_ROOT, relative.replace("/", os.sep))
    if "*" in relative:
        import glob

        return bool(glob.glob(absolute))
    return os.path.exists(absolute)


def test_canon_map_exists_and_is_substantial():
    assert os.path.exists(CANON_MAP), "Docs/CANON_MAP.md is the pointer surface; it must exist"
    text = _read(CANON_MAP)
    for required in ("## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6.", "## 7."):
        assert required in text, f"CANON_MAP.md is missing section {required!r}"
    assert len(text) > 4000, (
        f"CANON_MAP.md is only {len(text)} chars - a stub index cannot replace "
        "441 files of scattering, so a stub must not be allowed to pass"
    )


def test_every_path_named_in_the_lookup_table_resolves():
    """A path that does not resolve is worse than no path: it is a confident wrong answer.

    This is the test that would have caught the Docs/docs collision being described
    as a real split, and any future doc renamed without the map being updated.
    """
    text = _read(CANON_MAP)
    section = _section(text, "## 2.")
    assert section, "the 'If you need X, read Y' lookup table is the map's whole job"

    paths = _PATH_RE.findall(section)
    assert len(paths) >= 20, f"only {len(paths)} paths found in the lookup table - regex too strict?"

    missing = [p for p in paths if not _exists_as_given(p)]
    assert not missing, (
        "CANON_MAP.md lookup table names paths that do not resolve: "
        f"{missing}. Fix the map or restore the file - do not relax the test."
    )


def test_lookup_table_names_only_canon_masters_and_resources():
    """Guards the same way test_zone_specs_name_only_canon_masters guards specs.

    Four invented masters (M_GrassField, M_FurBeast, M_LeafHerb, M_BarkPine) and a
    pair of invented ones (M_FamilySilhouette, M_ValleyNight) already got caught in
    this project. The map is read more often than any spec, so it gets the same guard.
    """
    text = _read(CANON_MAP)
    named = set(re.findall(r"\bM_[A-Za-z0-9_]+\b", text))
    invented = {n for n in named if n not in MASTER_NAMES}
    assert not invented, (
        f"CANON_MAP.md names non-canon master materials: {sorted(invented)}. "
        f"Canon masters are {sorted(MASTER_NAMES)}"
    )

    resources = set(re.findall(r"\bRES_[A-Za-z0-9_]+\b", text))
    stray = resources - CANON_RESOURCES
    assert not stray, f"CANON_MAP.md names resources outside the canon six: {sorted(stray)}"


def test_must_numbering_agrees_between_map_and_canonical_must_list():
    """Both files number the musts. A silent renumber in one is a trap."""
    map_text = _read(CANON_MAP)
    must_text = _read(MUST_LIST)

    table = _section(map_text, "## 3.")
    assert table, "section 3 is the verified Found table"

    for number in range(1, 18):
        tag = f"#{number}"
        assert re.search(rf"^\| \*?\*?{re.escape(tag)}", table, re.MULTILINE) or (
            tag in table
        ), f"{tag} does not appear in the CANON_MAP found table"
        assert tag in must_text, f"{tag} does not appear in the canonical must list"


def test_m17_stealth_is_never_recorded_as_absent():
    """THE anti-regression test for the error that motivated this file.

    #17 was written up as "Found: **Nothing.** No stealth state, no awareness, no
    detection" while the mechanic was LOCKED, implemented, and CLOSED with a Lead
    stamp. If this ever reads N again, the index has failed and the failure is
    exactly the one this file was written to prevent.
    """
    map_text = _read(CANON_MAP)
    must_text = _read(MUST_LIST)

    row = [ln for ln in map_text.splitlines() if ln.strip().startswith("| **#17")]
    assert row, "the #17 row is missing from the found table"
    assert "APPROVE" in row[0], (
        f"#17 must cite its closing stamp so it cannot be misread as absent. Row: {row[0]!r}"
    )

    heading = [ln for ln in must_text.splitlines() if ln.startswith("### ") and "#17" in ln]
    assert heading, "#17 heading missing from the must list"
    assert "CLOSED" in heading[0].upper(), (
        "#17 must be recorded as CLOSED in the canonical must list. It was LOCKED "
        "2026-09-21 and stamped APPROVE SS-A. Heading reads: " f"{heading[0]!r}"
    )
    assert "Nothing" not in heading[0], (
        "#17 must not claim absence - it is implemented and closed. Heading: " f"{heading[0]!r}"
    )


def test_soft_latch_is_documented_as_a_defect_not_a_feature():
    """The map records the fail-open. A fail-open nobody named is the whole problem.

    Asserted on CODE IDENTIFIERS, not prose. An earlier version of this test matched
    the words "soft-latch" OR "soft latch" and was proven vacuous by mutation M6:
    renaming one spelling left the other, so the assertion still passed. Matching
    `bSoftLatch` and `SOFT_LATCH_ONLY` cannot be satisfied by prose drift - they are
    the field and the log tag the fix actually depends on.
    """
    text = _read(CANON_MAP)
    section = _section(text, "## 4.")
    assert section, "section 4 documents the one real code defect the consolidation found"

    assert "bSoftLatch" in section, (
        "the map must name FHomeWorldCampActorCalm::bSoftLatch - it is the field that "
        "distinguishes a count granted without a real actor from one granted with"
    )
    assert "SOFT_LATCH_ONLY" in section, (
        "the map must name the SOFT_LATCH_ONLY log tag, so the fail-open is visible in "
        "the log rather than hidden in a return value"
    )
    assert "SatisfiesFreedomGateStrict" in section, (
        "the map must name the strict counterpart that excludes soft latches, so a "
        "reader knows which half is the evidence and which half is the courtesy"
    )