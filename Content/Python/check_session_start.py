#!/usr/bin/env python3
"""Fail if the session door drifts from the contract it is supposed to be.

Does not load the pack. Does not start a session. A broken door exits 1.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOOR = ROOT / "Docs" / "context" / "SESSION_START.md"
PACK = ROOT / "Docs" / "handoffs" / "CONTEXT_PACK_V1.md"

READS = ("Docs/context/ROUTE_INDEX.md",)
# The full state rule. The door carries the short form inline; this file opens on demand.
STATE_RULE = "UserHarness/docs/human-use/route-context.md"
STATE_RULE_MUST_SAY = (
    "first match wins",
    "`decide`",
    "`do`",
    "`agent`",
    "Never a fourth state",
)
# Files whose backtick and markdown-link paths must match the case git records.
CASE_CHECKED = ("Docs/context/SESSION_START.md", "AGENTS.md")
_LINK = re.compile(r"\]\(([^)\s]+)\)")
_TICK = re.compile(r"`([^`\s]+)`")
_NOT_A_PATH = set("<>*{}$|")
NAMED = (
    "Docs/WORLD_METRICS.md",
    "Docs/level/L_VS_MVP_Markers_manifest.json",
    "Docs/COMMANDS_AND_LOG_TAGS.md",
)
MUST_SAY = (
    "counts.actors",
    "completeness.verdict",
    "That file is the actor scan",
    "Name only the active task (Co: the active bite)",
    "Do not wait on a UserHarness SHA",
    "do not copy them here",
)
MUST_NOT = (
    "103 actors",
    "afdcb0f",
    "5caf7be",
    "does not name a bite",
    "Name only the active bite.",
    "Main SHA the session last pulled",
    "A placeable actor needs a scene root",
)
QUESTION_GATE = ("one typed clarifier",)
NAMED_ON_DEMAND = (
    "Docs/context/HANDBACK.md",
    "Docs/context/LEVEL_RULES.md",
    "Docs/context/T0_INTERVIEW_LOCK.md",
)


def tracked_paths(root: Path) -> set[str] | None:
    """Every path git tracks under root, plus each parent directory. None without git."""
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            capture_output=True, check=True,
        ).stdout.decode("utf-8", "replace")
    except (OSError, subprocess.CalledProcessError):
        return None
    files = [f for f in out.split("\0") if f]
    tracked = set(files)
    for f in files:
        parts = f.split("/")
        for i in range(1, len(parts)):
            tracked.add("/".join(parts[:i]))
    return tracked


def _candidates(text: str, rel_dir: str):
    """(kind, path as written, repo-relative path) for each link and backtick path."""
    for m in _LINK.finditer(text):
        raw = m.group(1).split("#", 1)[0]
        if not raw or re.match(r"^[a-z][a-z0-9+.-]*:", raw, re.I) or _NOT_A_PATH & set(raw):
            continue
        rel = os.path.normpath(os.path.join(rel_dir, raw)).replace(os.sep, "/")
        if rel.startswith(".."):
            continue
        yield "link", m.group(1), rel
    for m in _TICK.finditer(text):
        raw = m.group(1).replace("\\", "/")
        if raw.startswith("./"):
            raw = raw[2:]
        if "/" not in raw or _NOT_A_PATH & set(raw) or raw.startswith(("/", "http")):
            continue
        yield "path", m.group(1), raw.rstrip("/")


def path_case_problems(name: str, text: str, tracked: set[str]) -> list[str]:
    """A path that git records under another case, or a link to nothing, is a broken path."""
    lower = {}
    for p in tracked:
        lower.setdefault(p.lower(), p)
    problems = []
    rel_dir = os.path.dirname(name)
    for kind, written, rel in _candidates(text, rel_dir):
        if rel in tracked:
            continue
        # A path inside a submodule (a tracked gitlink) is not in this index.
        parts = rel.split("/")
        prefixes = ("/".join(parts[:i]) for i in range(1, len(parts)))
        if any(pre in tracked and _is_gitlink(pre, tracked) for pre in prefixes):
            continue
        if rel.lower() in lower:
            problems.append(f"{name}: {kind} `{written}` is `{lower[rel.lower()]}` in git (case)")
        elif kind == "link":
            problems.append(f"{name}: link `{written}` resolves to `{rel}`, which git does not track")
    return problems


def _is_gitlink(prefix: str, tracked: set[str]) -> bool:
    """A tracked entry with nothing tracked beneath it is a file or a submodule gitlink."""
    return not any(p.startswith(prefix + "/") for p in tracked)


def state_rule_problems(text: str) -> list[str]:
    problems = []
    for phrase in STATE_RULE_MUST_SAY:
        if phrase not in text:
            problems.append(f"door lost the inline state rule: {phrase}")
    if STATE_RULE not in text:
        problems.append(f"door does not name the full state rule: {STATE_RULE}")
    if re.search(r"^\d+\. `?UserHarness/docs/human-use/route-context\.md", text, re.M):
        problems.append("route-context is a numbered start read again; it opens on demand")
    for line in text.splitlines():
        if "Transition" in line and "PHASES.md" in line and "Look room" not in line:
            problems.append("the Transition header reads PHASES.md outside the Look room")
    return problems


def main() -> int:
    problems: list[str] = []
    if not DOOR.is_file():
        problems.append(f"missing {DOOR.relative_to(ROOT)}")
        text = ""
    else:
        text = DOOR.read_text(encoding="utf-8")
        if not text.strip():
            problems.append("SESSION_START.md is empty")
    for rel in READS + NAMED:
        if not (ROOT / rel).is_file():
            problems.append(f"named path missing: {rel}")
        elif rel in READS and Path(rel).name not in text and rel not in text:
            problems.append(f"read path not named in the door: {rel}")
    if "HOMEWORLD_ROUTE.md" not in text:
        problems.append("door does not name the full route for descent, gather, or fertilizer")
    problems.extend(state_rule_problems(text))
    if not (ROOT / STATE_RULE).is_file():
        print(f"WARN  {STATE_RULE} is not on disk; run git submodule update --init UserHarness")
    if "wins on the close order" not in text or "The state file wins" in text:
        problems.append("door does not keep the close order")
    rules = (ROOT / "Docs/context/DOOR_RULES.md").read_text(encoding="utf-8") if (ROOT / "Docs/context/DOOR_RULES.md").is_file() else ""
    if "DOOR_RULES.md" not in text:
        problems.append("door does not name DOOR_RULES.md")
    held = text + "\n" + rules
    for phrase in MUST_SAY:
        if phrase not in held:
            problems.append(f"door missing required phrase: {phrase}")
    if len(text.splitlines()) > 100:
        problems.append(f"door is over 100 lines ({len(text.splitlines())})")
    if re.search(r"^\d+\. .*WORLD_METRICS\.md", text, re.M):
        problems.append("metrics sheet is in the start read")
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8") if (ROOT / "CLAUDE.md").is_file() else ""
    if "@AGENTS.md" not in claude:
        problems.append("CLAUDE.md does not import AGENTS.md")
    for phrase in QUESTION_GATE:
        if phrase not in text:
            problems.append(f"door lost the question-before-discovery gate: {phrase}")
    for phrase in MUST_NOT:
        if phrase in text:
            problems.append(f"door still copies a stale phrase: {phrase}")
    for rel in NAMED_ON_DEMAND:
        if rel not in text:
            problems.append(f"door does not name on-demand file: {rel}")
        path = ROOT / rel
        if not path.is_file():
            problems.append(f"on-demand file missing: {rel}")
        elif rel.endswith("HANDBACK.md") and "Main SHA the session last pulled" not in path.read_text(encoding="utf-8"):
            problems.append("HANDBACK.md lost the field list")
        elif rel.endswith("LEVEL_RULES.md") and "A placeable actor needs a scene root" not in path.read_text(encoding="utf-8"):
            problems.append("LEVEL_RULES.md lost the placeable rule")
    if re.search(r"\(\d+ actors", text):
        problems.append("door copies an actor count")
    for stub in ("Docs/context/DISCOVERY_START.md", "Docs/context/ROUTE_START.md"):
        if (ROOT / stub).exists():
            problems.append(f"retired door still exists: {stub}")
    if "DISCOVERY_START.md" in text or "ROUTE_START.md" in text:
        problems.append("door still names a retired start file")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8") if (ROOT / "AGENTS.md").is_file() else ""
    if "Docs/context/SESSION_START.md" not in agents:
        problems.append("AGENTS.md does not point at the door")
    pack = PACK.read_text(encoding="utf-8") if PACK.is_file() else ""
    if "Until the manifest exists, wait" in pack and "old instruction" not in pack:
        problems.append("CONTEXT_PACK still gives the old manifest wait as current")
    if "skip a path not on main" in pack:
        problems.append("CONTEXT_PACK still describes the old skip-if-missing read")
    index = (ROOT / "Docs/context/ROUTE_INDEX.md").read_text(encoding="utf-8") if (ROOT / "Docs/context/ROUTE_INDEX.md").is_file() else ""
    if re.search(r"\d+\s*m\b", index) or re.search(r"\d+\s*s\b", index):
        problems.append("ROUTE_INDEX.md copies a number; the sheet owns numbers")
    for cited in re.findall(r"`([^`]+\.md)`", text):
        if cited in ("route-context.md", "Docs/qa/HUMAN_TUTORIAL.md"):
            continue
        if cited.startswith("Docs/") or cited.startswith("docs/") or cited.startswith("swarm/") or cited == "START_HERE.md":
            if not (ROOT / cited).is_file():
                problems.append(f"door names a missing file: {cited}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
    if "UE 5.7" in readme:
        problems.append("README.md still says UE 5.7")
    vision = (ROOT / "VisionBoard/README.md").read_text(encoding="utf-8") if (ROOT / "VisionBoard/README.md").is_file() else ""
    if "not product canon" not in vision.lower():
        problems.append("VisionBoard/README.md does not say it is not product canon")
    console = (ROOT / "docs/CONSOLE_COMMANDS.md").read_text(encoding="utf-8") if (ROOT / "docs/CONSOLE_COMMANDS.md").is_file() else ""
    if "COMMANDS_AND_LOG_TAGS.md" not in console:
        problems.append("console index does not point at the generated list")
    known = (ROOT / "docs/KNOWN_ERRORS.md").read_text(encoding="utf-8") if (ROOT / "docs/KNOWN_ERRORS.md").is_file() else ""
    if "Do not load this file whole" not in known:
        problems.append("KNOWN_ERRORS.md does not forbid a full read")
    tasks = (ROOT / "docs/TaskLists/CURRENT_TASK_LIST.md").read_text(encoding="utf-8") if (ROOT / "docs/TaskLists/CURRENT_TASK_LIST.md").is_file() else ""
    if "chat task wins" not in tasks:
        problems.append("task list does not say a chat task wins")
    tracked = tracked_paths(ROOT)
    if tracked is None:
        print("WARN  git is not available; the path-case check did not run")
    else:
        for rel in CASE_CHECKED:
            path = ROOT / rel
            if path.is_file():
                problems.extend(path_case_problems(rel, path.read_text(encoding="utf-8"), tracked))
    if problems:
        for p in problems:
            print(f"FAIL  {p}")
        return 1
    print("SESSION_START door check: pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
