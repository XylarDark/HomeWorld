"""
Validate docs/workflow/CURRENT_TASK_LIST.md for automation loop.
Checks: T1-T10 sections exist; each has goal, success_criteria, research_notes (or implementation_notes),
steps_or_doc, status; status in (pending, in_progress, completed, blocked).
Exit 0 if valid, 1 otherwise; print which task or field is missing.
Run from project root: python Content/Python/validate_task_list.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Resolve project root (parent of Content/)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
TASK_LIST_PATH = PROJECT_ROOT / "docs" / "workflow" / "CURRENT_TASK_LIST.md"

VALID_STATUSES = frozenset({"pending", "in_progress", "completed", "blocked"})
# Field names as they appear in the doc (success criteria has a space)
REQUIRED_FIELDS = ("goal", "success criteria", "steps_or_doc", "status")
# research_notes OR implementation_notes
NOTES_FIELDS = ("research_notes", "implementation_notes")
TASK_IDS = [f"T{i}" for i in range(1, 11)]


def _find_section_bounds(content: str) -> dict[str, tuple[int, int]]:
    """Return map of task id -> (start_line_0based, end_line_0based)."""
    lines = content.splitlines()
    section_starts: dict[str, int] = {}
    for i, line in enumerate(lines):
        m = re.match(r"^## (T\d+)\.", line.strip())
        if m:
            section_starts[m.group(1)] = i
    # End of section = start of next section or end of file
    result: dict[str, tuple[int, int]] = {}
    for j, tid in enumerate(TASK_IDS):
        if tid not in section_starts:
            continue
        start = section_starts[tid]
        if j + 1 < len(TASK_IDS) and TASK_IDS[j + 1] in section_starts:
            end = section_starts[TASK_IDS[j + 1]] - 1
        else:
            end = len(lines) - 1
        result[tid] = (start, end)
    return result


def _field_value(lines: list[str], start: int, end: int, field: str) -> str | None:
    """Extract value for '- **field:** value' in lines[start:end+1] (colon inside bold)."""
    pattern = re.compile(r"^-\s*\*\*" + re.escape(field) + r":\*\*\s*(.*)$")
    for i in range(start, min(end + 1, len(lines))):
        line = lines[i]
        m = pattern.match(line.strip())
        if m:
            return m.group(1).strip()
    return None


def validate(path: Path) -> list[str]:
    """Validate task list file. Return list of error messages (empty if valid)."""
    errors: list[str] = []
    if not path.exists():
        return [f"Task list not found: {path}"]
    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    bounds = _find_section_bounds(content)
    for tid in TASK_IDS:
        if tid not in bounds:
            errors.append(f"{tid}: section '## {tid}.' not found")
            continue
        start, end = bounds[tid]
        for field in REQUIRED_FIELDS:
            val = _field_value(lines, start, end, field)
            if val is None:
                errors.append(f"{tid}: missing '- **{field}:**'")
        # research_notes or implementation_notes
        has_notes = any(
            _field_value(lines, start, end, f) is not None for f in NOTES_FIELDS
        )
        if not has_notes:
            errors.append(
                f"{tid}: missing '- **research_notes:**' or '- **implementation_notes:**'"
            )
        status_val = _field_value(lines, start, end, "status")
        if status_val is not None and status_val.lower() not in VALID_STATUSES:
            errors.append(
                f"{tid}: invalid status '{status_val}' (must be one of {sorted(VALID_STATUSES)})"
            )
    if len(bounds) != 10:
        missing = set(TASK_IDS) - set(bounds.keys())
        if missing:
            errors.append(f"Missing sections: {sorted(missing)}")
    return errors


def main() -> int:
    errors = validate(TASK_LIST_PATH)
    if not errors:
        print("OK: CURRENT_TASK_LIST.md is valid (T1-T10, required fields, valid statuses).")
        return 0
    print("Validation failed:", file=sys.stderr)
    for e in errors:
        print(f"  {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
