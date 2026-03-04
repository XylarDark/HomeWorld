# filter_editor_log.py - Filter Unreal Editor log to development-relevant lines only.
# Used by Watch-AutomationAndFix.ps1: reads editor_output_full.txt, writes editor_output_filtered.txt.
# Include: severity (Error/Warning/Fatal/Exception), project categories (LogPCG, LogScript, etc.), keywords.
# Exclude: high-volume noise unless line also matches error-like keywords.
# See docs/AUTOMATION_EDITOR_LOG.md for the safety rule (when unfixable, use full log).
#
# Config: Optional Content/Python/editor_log_filter_config.json (allow_categories, signal_keywords,
# noise_categories_unless_signal, severity_pattern). If missing, built-in defaults are used.
#
# Usage (from project root): python Content/Python/filter_editor_log.py [input_path] [output_path]
# Default: input = Saved/Logs/editor_output_full.txt, output = Saved/Logs/editor_output_filtered.txt

import json
import os
import re
import sys
from typing import FrozenSet, List, Optional, Tuple

# #region agent log
PREFIX = "filter_editor_log: "
# #endregion

# Built-in defaults (used when config file is missing)
_DEFAULT_ALLOW_CATEGORIES = frozenset({
    "LogPCG", "LogScript", "LogHomeWorld", "LogOutputLog", "LogPython", "LogAutomation",
    "LogTemp", "LogLoad", "LoadErrors", "LogWindows", "LogInit", "LogExit", "LogActor",
    "LogGameMode", "LogWorld", "LogEngine", "LogUnrealMCP",
})
_DEFAULT_SIGNAL_KEYWORDS = [
    "error", "failed", "failure", "exception", "assert", "not found", "cannot",
    "unable", "missing", "invalid", "crash", "fatal", "traceback",
    "no surfaces found",
]
_DEFAULT_NOISE_CATEGORIES = frozenset({
    "LogAssetRegistry", "LogContentStreaming", "LogAssetManager",
})
_DEFAULT_SEVERITY_PATTERN = r"\b(Error|Warning|Fatal|Assert|Exception)\b"


def _config_path(script_dir: str) -> str:
    return os.path.join(script_dir, "editor_log_filter_config.json")


def _load_config(script_dir: str) -> Tuple[FrozenSet[str], List[str], FrozenSet[str], re.Pattern]:
    path = _config_path(script_dir)
    if not os.path.isfile(path):
        allow = _DEFAULT_ALLOW_CATEGORIES
        keywords = _DEFAULT_SIGNAL_KEYWORDS
        noise = _DEFAULT_NOISE_CATEGORIES
        severity_re = re.compile(_DEFAULT_SEVERITY_PATTERN, re.IGNORECASE)
        return allow, keywords, noise, severity_re
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        allow = frozenset(data.get("allow_categories", list(_DEFAULT_ALLOW_CATEGORIES)))
        keywords = data.get("signal_keywords", _DEFAULT_SIGNAL_KEYWORDS)
        noise = frozenset(data.get("noise_categories_unless_signal", list(_DEFAULT_NOISE_CATEGORIES)))
        pat = data.get("severity_pattern", _DEFAULT_SEVERITY_PATTERN)
        severity_re = re.compile(pat, re.IGNORECASE)
        return allow, keywords, noise, severity_re
    except (json.JSONDecodeError, OSError):
        return (
            _DEFAULT_ALLOW_CATEGORIES,
            _DEFAULT_SIGNAL_KEYWORDS,
            _DEFAULT_NOISE_CATEGORIES,
            re.compile(_DEFAULT_SEVERITY_PATTERN, re.IGNORECASE),
        )


_script_dir = os.path.dirname(os.path.abspath(__file__))
ALLOW_CATEGORIES, SIGNAL_KEYWORDS, NOISE_CATEGORIES_UNLESS_SIGNAL, SEVERITY_PATTERNS = _load_config(_script_dir)
_KEYWORD_RE = re.compile("|".join(re.escape(k) for k in SIGNAL_KEYWORDS), re.IGNORECASE)


def _has_signal_keyword(line: str) -> bool:
    return bool(_KEYWORD_RE.search(line))


def _has_severity(line: str) -> bool:
    return bool(SEVERITY_PATTERNS.search(line))


def _category_from_line(line: str) -> Optional[str]:
    # Common UE log format: "LogCategory: message" or "[timestamp] LogCategory: message"
    m = re.search(r"(?:^\[[^\]]+\]\s+)?(Log[A-Za-z0-9]+|LoadErrors)\b", line)
    return m.group(1) if m else None


def should_include_line(line: str) -> bool:
    if not line.strip():
        return False
    # Severity always include
    if _has_severity(line):
        return True
    # Any signal keyword
    if _has_signal_keyword(line):
        return True
    cat = _category_from_line(line)
    if cat and cat in ALLOW_CATEGORIES:
        return True
    # Noise category: include only if line has signal keyword
    if cat and cat in NOISE_CATEGORIES_UNLESS_SIGNAL:
        return _has_signal_keyword(line)
    return False


def filter_log(input_path: str, output_path: str) -> None:
    if not os.path.isfile(input_path):
        with open(output_path, "w", encoding="utf-8", errors="replace") as f:
            f.write("# No Editor log captured (input file missing). Unfiltered: Saved/Logs/editor_output_full.txt\n")
        return
    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    kept = [line.rstrip("\n\r") for line in lines if should_include_line(line)]
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8", errors="replace") as f:
        f.write("# Filtered Editor log (development-relevant only). Unfiltered: Saved/Logs/editor_output_full.txt\n")
        for line in kept:
            f.write(line + "\n")


def main() -> int:
    project_root = os.environ.get("HOMEWORLD_PROJECT") or os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    saved_logs = os.path.join(project_root, "Saved", "Logs")
    default_input = os.path.join(saved_logs, "editor_output_full.txt")
    default_output = os.path.join(saved_logs, "editor_output_filtered.txt")
    input_path = sys.argv[1] if len(sys.argv) > 1 else default_input
    output_path = sys.argv[2] if len(sys.argv) > 2 else default_output
    filter_log(input_path, output_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
