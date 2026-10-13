"""Every "see <Section> in AGENTS.md" pointer must name a section that exists.

WHY THIS IS A GATE

A pointer to a section that does not exist is worse than no pointer. The
reader trusts it, opens the file, does not find the section, and then either
guesses or re-derives the rule the pointer was supposed to supply. That is a
silent failure of exactly the kind this repo keeps rediscovering: CI stays
green because nothing measures the claim.

Four of these were live when this test was written. The always-on file had
been slimmed - `AGENTS.md` holds `Canon`, `Lock`, `Steer gate`, `Session`,
`Build`, `Do not re-litigate`, and delegates everything else to
`docs/AGENTS_REFERENCE.md` - but the pointers were never moved with the
content. So `create-pr` sent readers to an "Code style" section, `review-changes`
to a "Boundaries" section, and rule 20 asserted three times that its invariant
was "already stated in AGENTS.md". It was not, and rule 20 had been
glob-scoped on the strength of that belief.

The sibling gate `scripts/harness-paths.test.js` checks that referenced FILES
exist. Nothing checked that referenced SECTIONS do. This is the other half.

WHAT IT DELIBERATELY DOES NOT DO

It does not attempt to prove a pointer is *useful*, only that it resolves.
And it is deliberately biased toward silence: a candidate must look like a
title (capitalised, long enough) before it is judged, because prose ending in
"...in AGENTS.md" is overwhelmingly a sentence, not a section reference. A
gate that cries wolf gets disabled, which is worse than no gate.
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

AGENTS = os.path.join(REPO_ROOT, "AGENTS.md")
AGENTS_REFERENCE = os.path.join(REPO_ROOT, "docs", "AGENTS_REFERENCE.md")

#: Surfaces an agent actually follows when doing work. Docs/ audit records are
#: excluded on purpose: they describe the file as it stood when written, so
#: holding them to today's headings would fail on history rather than on drift.
SCAN_ROOTS = (
    os.path.join(REPO_ROOT, ".cursor", "commands"),
    os.path.join(REPO_ROOT, ".cursor", "rules"),
    os.path.join(REPO_ROOT, ".agents", "skills"),
    os.path.join(REPO_ROOT, ".cursor", "skills"),
    os.path.join(REPO_ROOT, "docs", "human-use"),
    os.path.join(REPO_ROOT, "docs", "Setup"),
)

FILE_ALT = r"(AGENTS(?:_REFERENCE)?\.md)"
LINK = r"(?:\]\([^)]*\))?"          # consumes `](../../docs/AGENTS_REFERENCE.md)`
SECTION = r"([A-Z][A-Za-z0-9 \-/&]{2,40})"

#: Literals, not \xNN escapes - in a raw string `r"\xe2\x86\x92"` matches six
#: backslash-prefixed characters rather than the arrow, which silently disabled
#: the arrow alternative in the first draft.
CLAIM_PATTERNS = [
    re.compile(FILE_ALT + LINK + r"\s*(?:->|\u2192|\()\s*\**" + SECTION),
    re.compile(FILE_ALT + LINK + r"\s*\u00a7\s*\**" + SECTION),
    re.compile(r"\**" + SECTION + r"\**\s+in\s+\[?`?" + FILE_ALT),
    re.compile(r"(?:section|\u00a7)\s+\**" + SECTION + r"\**\s+of\s+\[?`?" + FILE_ALT),
    # "AGENTS.md Boundaries" - a capitalised word straight after the filename.
    # This shape escaped the first draft of the audit entirely.
    re.compile(FILE_ALT + LINK + r"\s+" + SECTION),
]


def _headings(path: str) -> set[str]:
    """ATX headings plus bold lead-ins, normalised for loose comparison."""
    if not os.path.exists(path):
        return set()
    text = open(path, encoding="utf-8", errors="replace").read()
    out: set[str] = set()
    for m in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.M):
        out.add(_norm(m.group(1)))
    for m in re.finditer(r"^\*\*(.+?)\*\*", text, re.M):
        out.add(_norm(m.group(1)))
    return {h for h in out if h}


def _norm(s: str) -> str:
    """Lower-case and strip punctuation so `Code style` matches `Code-style`."""
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def _claims(text: str):
    """Yield (section, filename) for every pointer-shaped claim in text.

    Runs against both the original and a newlines-flattened copy. Wrapped
    pointers - a section name on one line and its filename on the next - are
    real, and the first version of this check missed one it had itself just
    introduced.
    """
    seen = set()
    for body in (text, re.sub(r"\s*\n\s*", " ", text)):
        for pat in CLAIM_PATTERNS:
            for m in pat.finditer(body):
                g1, g2 = m.group(1), m.group(2)
                fname, section = (g1, g2) if g1.endswith(".md") else (g2, g1)
                key = (section.strip().lower(), fname)
                if key in seen:
                    continue
                seen.add(key)
                yield section.strip(), fname


def _resolves(section: str, fname: str, pools: dict[str, set[str]]) -> bool:
    cand = _norm(section)
    if not cand:
        return True
    key = "REFERENCE" if "REFERENCE" in fname.upper() else "AGENTS"
    own = pools[key]
    for h in own:
        if h == cand or h.startswith(cand) or cand.startswith(h):
            return True
        ht, ct = set(h.split()), set(cand.split())
        if ht & ct and len(ht & ct) >= min(len(ht), len(ct)):
            return True
    return False


def _iter_files():
    for root in SCAN_ROOTS:
        if not os.path.isdir(root):
            continue
        for dp, _, fns in os.walk(root):
            for fn in fns:
                if fn.endswith((".md", ".mdc")):
                    yield os.path.join(dp, fn)


def test_every_section_pointer_resolves():
    """The gate. Reports every unresolved pointer at once, not just the first."""
    pools = {
        "AGENTS": _headings(AGENTS),
        "REFERENCE": _headings(AGENTS_REFERENCE),
    }
    assert pools["AGENTS"], "AGENTS.md yielded no headings; the parser is broken"
    assert pools["REFERENCE"], "AGENTS_REFERENCE.md yielded no headings"

    broken = []
    for path in _iter_files():
        rel = os.path.relpath(path, REPO_ROOT)
        text = open(path, encoding="utf-8", errors="replace").read()
        for section, fname in _claims(text):
            if not _resolves(section, fname, pools):
                broken.append(f"{rel}: claims {section!r} in {fname}")

    assert not broken, (
        "pointers name sections that do not exist. A reader who follows these "
        "finds nothing and either guesses or re-derives the rule:\n  "
        + "\n  ".join(broken)
    )


def test_the_patterns_still_match_every_known_pointer_shape():
    """Tripwire for a silently dead regex.

    The first draft of this gate asserted a *count* of live pointers instead,
    which fails when someone legitimately deletes a pointer - punishing correct
    content and training the next maintainer to delete the gate. Shapes are
    fixed, so shapes are what get pinned.
    """
    probes = {
        # plain file, then arrow
        "commits (AGENTS.md -> Code style)": ("Code style", "AGENTS.md"),
        # markdown link between filename and arrow (the shape that broke the
        # first version of this check)
        "commits ([AGENTS_REFERENCE.md](../x.md) \u2192 Code style)":
            ("Code style", "AGENTS_REFERENCE.md"),
        # "X in AGENTS.md"
        "see **Boundaries** in [AGENTS.md](../AGENTS.md)": ("Boundaries", "AGENTS.md"),
        # plain space + capitalised word - the shape the original audit missed
        "team decision (AGENTS.md Lock).": ("Lock", "AGENTS.md"),
        # wrapped pointer: section name on one line, filename on the next.
        # Flattening is what makes this resolvable at all - without it the
        # first version of this gate missed a pointer it had just introduced.
        "the **Boundaries** in\n[AGENTS.md](../AGENTS.md)":
            ("Boundaries", "AGENTS.md"),
    }
    for text, expected in probes.items():
        got = list(_claims(text))
        assert expected in got, (
            f"pattern no longer recognises {text!r}; got {got}. Pointers of "
            "this shape would be skipped entirely."
        )


def test_the_gate_reports_a_pointer_it_cannot_resolve():
    """Self-check the resolver on synthetic input, not on the live corpus."""
    pools = {"AGENTS": {"canon", "lock", "session"}, "REFERENCE": {"code style"}}
    assert _resolves("Lock", "AGENTS.md", pools)
    assert not _resolves("Ghosts", "AGENTS.md", pools), (
        "the resolver accepted a section that exists in neither file - the "
        "gate would never fire"
    )


def test_the_two_context_files_actually_have_sections():
    """Guard the parser's own precondition: if headings ever stop parsing,
    every pointer would be 'broken' and the failure message would lie."""
    assert _headings(AGENTS) >= {"canon", "lock", "session", "build"}
    assert "code style" in _headings(AGENTS_REFERENCE)
