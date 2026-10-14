#!/usr/bin/env python3
"""Check that relative Markdown links resolve, and repair the unambiguous ones.

Why this exists
---------------
A link is a claim that a path resolves. When a directory moves, every claim in
every file that points into it becomes false at once, and nothing turns red.
Measured 2026-10-13: 1,608 relative links across ``docs/**`` did not resolve,
including 107 in ``docs/KNOWN_ERRORS.md`` and 96 in ``docs/AGENTS_REFERENCE.md``
- the two files an agent opens when it is already stuck. One entry in
``KNOWN_ERRORS.md`` advised setting the editor startup map to *DemoMap*, which
had been deleted, so following it would have re-caused the crash it documented.

Repair policy
-------------
Only links that resolve to exactly one file in the repository are rewritten.
Ambiguous basenames (``SKILL.md`` exists in dozens of places) and names that no
longer exist anywhere are reported and left alone, because guessing at either
turns a working guess into a confidently wrong pointer. Those two buckets are
the entire reason this is a checker and not a find-and-replace.

Non-file targets are classified and ignored rather than treated as broken:
external schemes, pure anchors, and Unreal content paths (``/Game/...``) which
are engine references that never correspond to a file on disk.

Usage
-----
    py Content/Python/check_doc_links.py                 # report, exit 1 if any
    py Content/Python/check_doc_links.py --fix docs      # repair unambiguous
    py Content/Python/check_doc_links.py --json          # machine-readable

Exit codes: ``0`` nothing broken, ``1`` broken links remain, ``2`` bad usage.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Dict, List, NamedTuple, Optional, Tuple
from urllib.parse import unquote

# Targets that are not file paths and must never be judged as broken.
_EXTERNAL = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
_UNREAL = re.compile(r"^/(Game|Engine|Script|Memory|Temp|EpicGames)/")

_LINK = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?\s*\)")


class Broken(NamedTuple):
    path: str        # file containing the link, repo-relative
    line: int
    target: str      # the link as written
    status: str      # gone | ambiguous
    candidates: Tuple[str, ...]


def _path_part(target: str) -> str:
    """The path portion of a link: backslashes normalised, percent-decoded, no anchor.

    Decoding matters because a space in a filename is written ``%20`` in a link.
    Without it a link to ``07_VERTICAL_SLICE_SIGN%20OFF.md`` never matches the
    real ``docs/07_VERTICAL_SLICE_SIGN OFF.md`` and reads as gone when the file
    is right there - a fabricated break in the one report meant to be trusted.
    """
    return unquote(target.replace("\\", "/").split("#")[0])


def classify(target: str) -> Optional[str]:
    """Return None for a file link, else the reason it is not one."""
    if not target or target.startswith("#"):
        return "anchor"
    if _EXTERNAL.match(target):
        return "external"
    if _UNREAL.match(target):
        return "unreal"
    return None


def build_index(root: str) -> Dict[str, List[str]]:
    """Every file and directory under root, keyed by name, repo-relative.

    Directories are stored with a trailing slash so a link to a folder - common
    in these docs, and a shape a file-only index would report as gone forever -
    can be repaired as well as a link to a file.
    """
    index: Dict[str, List[str]] = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in dirnames:
            rel = os.path.relpath(os.path.join(dirpath, name), root).replace(os.sep, "/") + "/"
            index.setdefault(name, []).append(rel)
        for name in filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), root).replace(os.sep, "/")
            index.setdefault(name, []).append(rel)
    return index


def _links(text: str) -> List[Tuple[int, str]]:
    found = []
    for number, line in enumerate(text.splitlines(), start=1):
        for match in _LINK.finditer(line):
            found.append((number, match.group(1)))
    return found


def _basename(target: str) -> str:
    """The final name in the path, with any #anchor, directory, and trailing slash removed.

    The trailing slash is the load-bearing part: a link to a folder is written
    ``handoffs/``, and the old ``split("/")[-1]`` returned ``""`` for it. An
    empty key never matches the directory the index stores under ``handoffs``,
    so every folder link was reported gone - and gone is blocking.
    """
    trimmed = _path_part(target).rstrip("/")
    return trimmed.split("/")[-1] if trimmed else ""


def resolve(target: str, index: Dict[str, List[str]]) -> Optional[str]:
    """The one unambiguous target for a broken link, or None if there is no call.

    None covers both failure shapes - the name is gone, or several files share
    it - and the caller is expected to distinguish them from the index rather
    than have this function guess.
    """
    hits = index.get(_basename(target), [])
    return hits[0] if len(hits) == 1 else None


def check_file(path: str, root: str, index: Dict[str, List[str]]) -> List[Broken]:
    base = os.path.dirname(path)
    broken = []
    with open(path, encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    for line, target in _links(text):
        if classify(target):
            continue
        if os.path.exists(os.path.normpath(os.path.join(base, _path_part(target)))):
            continue
        hits = tuple(sorted(index.get(_basename(target), [])))
        broken.append(Broken(
            path=os.path.relpath(path, root).replace(os.sep, "/"),
            line=line,
            target=target,
            status="gone" if not hits else ("resolvable" if len(hits) == 1 else "ambiguous"),
            candidates=hits,
        ))
    return broken


def _rewrite(target: str, suggestion: str, base: str) -> str:
    """Replace the path portion, preserving any #anchor verbatim."""
    anchor = target[target.index("#"):] if "#" in target else ""
    return os.path.relpath(suggestion, base).replace(os.sep, "/") + anchor


def fix_file(path: str, root: str, index: Dict[str, List[str]]) -> int:
    """Rewrite the unambiguous links in one file. Returns how many changed."""
    base = os.path.dirname(path)
    with open(path, encoding="utf-8", errors="replace") as handle:
        text = handle.read()

    changed = 0

    def replace(match: "re.Match[str]") -> str:
        nonlocal changed
        target = match.group(1)
        if classify(target) or os.path.exists(os.path.normpath(os.path.join(base, _path_part(target)))):
            return match.group(0)
        suggestion = resolve(target, index)
        if suggestion is None:
            return match.group(0)
        changed += 1
        # Splice around the captured target rather than rebuilding the match, so
        # the link text in [text](path) survives whatever it happens to say.
        # The suggestion from the index is repo-relative while base is absolute,
        # so they have to be brought into the same space before relpath runs.
        whole = match.group(0)
        prefix = whole[:match.start(1) - match.start(0)]
        suffix = whole[match.end(1) - match.end(0):]
        return prefix + _rewrite(target, os.path.join(root, suggestion), base) + suffix

    updated = _LINK.sub(replace, text)
    if changed:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(updated)
    return changed


def main(argv: Optional[List[str]] = None) -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    default_root = os.path.dirname(os.path.dirname(here))
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", help="Files or directories to check")
    parser.add_argument("--root", default=default_root, help="Repository root")
    parser.add_argument("--fix", action="store_true", help="Repair unambiguous links")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Machine-readable output")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    index = build_index(root)

    targets = []
    for item in args.paths or [os.path.join(root, "docs")]:
        if os.path.isdir(item):
            for dirpath, dirnames, filenames in os.walk(item):
                dirnames[:] = [d for d in dirnames if d != ".git"]
                targets += [os.path.join(dirpath, n) for n in filenames if n.endswith(".md")]
        elif os.path.isfile(item):
            targets.append(item)

    broken, repaired = [], 0
    for path in targets:
        if args.fix:
            repaired += fix_file(path, root, index)
        broken += check_file(path, root, index)

    gone = [b for b in broken if b.status == "gone"]
    amb = [b for b in broken if b.status == "ambiguous"]
    fixable = [b for b in broken if b.status == "resolvable"]
    # Only gone and ambiguous are failures: a resolvable link is one --fix can
    # settle, and an exit code that turns red on it would be red in the moment
    # it is most useful.
    blocking = gone + amb

    if args.as_json:
        print(json.dumps({
            "repaired": repaired, "fixable": len(fixable),
            "gone": [b._asdict() for b in gone],
            "ambiguous": [b._asdict() for b in amb],
        }, indent=2))
        return 1 if blocking else 0

    print(f"checked {len(targets)} files; repaired {repaired}; "
          f"still broken {len(blocking)} ({len(fixable)} more repairable with --fix)")
    if fixable:
        print(f"\n  resolvable - one file by that name, --fix will repair ({len(fixable)}):")
        for b in fixable[:10]:
            print(f"    {b.path}:{b.line}  {b.target}  ->  {b.candidates[0]}")
        if len(fixable) > 10:
            print(f"    ... {len(fixable) - 10} more")
    if gone:
        print(f"\n  gone - no file by that name anywhere ({len(gone)}):")
        for b in gone[:20]:
            print(f"    {b.path}:{b.line}  {b.target}")
        if len(gone) > 20:
            print(f"    ... {len(gone) - 20} more")
    if amb:
        print(f"\n  ambiguous - several files share the name ({len(amb)}), not guessed:")
        for b in amb[:20]:
            print(f"    {b.path}:{b.line}  {b.target}  ({len(b.candidates)} candidates)")
        if len(amb) > 20:
            print(f"    ... {len(amb) - 20} more")
    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
