#!/usr/bin/env python3
"""Fail if the session door drifts from the contract it is supposed to be.

Does not load the pack. Does not start a session. A broken door exits 1.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOOR = ROOT / "Docs" / "context" / "SESSION_START.md"
PACK = ROOT / "Docs" / "handoffs" / "CONTEXT_PACK_V1.md"

READS = (
    "UserHarness/docs/human-use/route-context.md",
    "Docs/context/ROUTE_INDEX.md",
)
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
NAMED_ON_DEMAND = (
    "Docs/context/HANDBACK.md",
    "Docs/context/LEVEL_RULES.md",
)


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
    if "Stop before `## Session close`" not in text:
        problems.append("door does not stop the state read before the close section")
    for phrase in MUST_SAY:
        if phrase not in text:
            problems.append(f"door missing required phrase: {phrase}")
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
    if problems:
        for p in problems:
            print(f"FAIL  {p}")
        return 1
    print("SESSION_START door check: pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
