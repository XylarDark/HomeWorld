# quest_preflight.py
# Host-only quest preflight. Called by run_quest_tests_host.py --check and
# Tools/RunTests.ps1 -QuestCheck. The Lead picked this (host-only preflight
# first): opening the Editor is expensive, and a manifest/beat mismatch is
# invisible until a PIE run wastes 15 minutes or goes inconclusive for a
# reason the manifest could have been told statically.
#
# Reads text only:
#   Source/HomeWorld/HomeWorldCharacter.cpp  (beat names, stop words, skip
#                                             steps, state JSON keys, the
#                                             documented beats line)
#   Content/Python/quest_test_manifest.py    (loaded as a module)
#   Content/Python/quest_test_runner.py      (_build_snapshot keys, map path)
#   Content/HomeWorld/Maps/SizeTest/L_SizeTest.umap  (existence only)
#
# It never starts PIE, never loads a map, never builds, and never writes
# anything except nothing. Exit codes: 0 clean (warnings allowed), 2 a real
# mismatch. A parse that cannot be answered is a warning ("unsure"), never a
# failure, so the check only bites when it understood both sides.

import importlib.util
import glob
import os
import re
import socket
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import quest_test_contract as contract  # noqa: E402  host-safe, no unreal

PROJECT_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))

CHARACTER_REL = os.path.join("Source", "HomeWorld", "HomeWorldCharacter.cpp")
MANIFEST_REL = os.path.join("Content", "Python", "quest_test_manifest.py")
RUNNER_REL = os.path.join("Content", "Python", "quest_test_runner.py")
COVERAGE_REL = os.path.join("Content", "Python", "quest_test_coverage.py")

MCP_HOST, MCP_PORT = "127.0.0.1", 55557

# The documented actors.* allowlist. `_build_snapshot` emits exactly these
# actor keys, so a manifest path outside this set is inconclusive at runtime
# even though the contract calls it well-shaped. The runner is also parsed for
# the first-level keys it actually writes; see _check_snapshot_paths.
ACTOR_KEYS = {
    "pawn": {"location"},
    "reveal": {"location", "spirit_visible", "partner_waiting", "partner_stand"},
    "partner": {"location"},
    "counter": {"location", "east_face", "west_face"},
    "dog": {"location", "tamed"},
    "wisps": {"count"},
}


# ---------------------------------------------------------------------------
# Small parsing ground rules: every parser returns (value, ""). When the
# structure is not found it returns (None, reason) and the caller warns.
# ---------------------------------------------------------------------------


def _read(rel, root):
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        return None, path
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return handle.read(), path


def _region(text, start_marker, end_marker):
    """The body of one C++ function, or None when the marker is missing."""
    start = text.find(start_marker)
    if start < 0:
        return None
    end = text.find(end_marker, start + len(start_marker))
    if end < 0:
        return None
    return text[start:end]


def _parse_beat_names(text):
    region = _region(text, "const TCHAR* PlaytestBeatName(int32 Beat)", "\n\t}")
    if region is None:
        return None, "PlaytestBeatName function not found"
    names = dict(re.findall(
        r'case\s+(PlaytestBeat\w+)\s*:\s*return\s+TEXT\("([a-z_]+)"\)\s*;', region))
    if not names:
        return None, "PlaytestBeatName has no `case PlaytestBeat*: return TEXT(...);` entries"
    return names, ""


def _parse_skip_steps(text):
    region = _region(text, "int32 PlaytestSkipStep(int32 Beat)", "\n\t}")
    if region is None:
        return None, "PlaytestSkipStep function not found"
    steps = {
        const: int(num)
        for const, num in re.findall(r"case\s+(PlaytestBeat\w+)\s*:\s*return\s+(\d+)\s*;", region)
    }
    if not steps:
        return None, "PlaytestSkipStep has no `case PlaytestBeat*: return n;` entries"
    return steps, ""


def _parse_keyword_rules(text):
    """Ordered (constant, [word, ...]) rules from PlaytestBeatFromText.

    The last state of a stop word is the rule order, so the parse keeps the
    source order. Returns ((rules, empty_default), "") or (None, reason).
    """
    region = _region(text, "int32 PlaytestBeatFromText(const FString& Text)", "\n\t}")
    if region is None:
        return None, "PlaytestBeatFromText function not found"
    rules = []
    for line in region.split("\n"):
        keywords = re.findall(r'Key\.Contains\(TEXT\("([a-z_]+)"\)\)', line)
        if not keywords:
            continue
        match = re.search(r"return\s+(PlaytestBeat\w+)\s*;", line)
        if not match:
            return None, "a Contains line without a matching return, order is unreadable"
        rules.append((match.group(1), keywords))
    if not rules:
        return None, "no `Key.Contains(TEXT(...))` rules found"
    empty = re.search(r"IsEmpty\(\)\)\s*\{?\s*return\s+(PlaytestBeat\w+)\s*;", region)
    return (rules, empty.group(1) if empty else None), ""


def _parse_documented_beats(text):
    match = re.search(r"playtest_ff: beats:\s*([a-z_,\s]+)", text)
    if match is None:
        return None, "no `playtest_ff: beats:` line"
    ids = [item.strip() for item in match.group(1).split(",") if item.strip()]
    if not ids:
        return None, "the beats log line is empty"
    return ids, ""


def _parse_state_keys(text):
    """Keys emitted by GetPlaytestStateJson, from its Printf format literals."""
    region = _region(text, "FString AHomeWorldCharacter::GetPlaytestStateJson() const", "\n}")
    if region is None:
        return None, "GetPlaytestStateJson function not found"
    keys = set()
    for literal in re.findall(r'TEXT\("(.+?)"\)', region, re.S):
        unescaped = literal.replace('\\"', '"')
        keys.update(re.findall(r'"([a-z_]+)":', unescaped))
    if not keys:
        return None, "GetPlaytestStateJson format literals carry no `\"key\":` entries"
    return keys, ""


def _parse_popped_keys(runner_text):
    """Keys _build_snapshot moves from quest.* to beat.* (quest.pop)."""
    keys = set(re.findall(r'quest\.pop\("([a-z_]+)"', runner_text))
    if not keys:
        return None, "_build_snapshot has no quest.pop(...) lines"
    return keys, ""


def _parse_runner_actor_keys(runner_text):
    keys = set(re.findall(r'actors\["(\w+)"\]', runner_text))
    keys.update(re.findall(r'actors = \{"(\w+)"', runner_text))
    if not keys:
        return None, "_build_snapshot has no actors[...] writes"
    return keys, ""


def _parse_level_path(runner_text):
    match = re.search(r'LEVEL_PATH\s*=\s*"(/Game/[\w/.-]+)"', runner_text)
    if match is None:
        return None, "LEVEL_PATH not found"
    return match.group(1), ""


def _parse_automation_test_names(source_dir):
    """Every automation test name in Source/HomeWorld/*.cpp.

    Handles both `IMPLEMENT_SIMPLE_AUTOMATION_TEST(FType, "Name", ...)` and
    the Custom forms (`IMPLEMENT_CUSTOM_SIMPLE_AUTOMATION_TEST(FType, "Name", ...)`):
    the name is the first string literal after the opening paren's optional
    type argument. Returns the set or (None, reason).
    """
    if not os.path.isdir(source_dir):
        return None, "%s does not exist" % source_dir
    names = set()
    for base, _dirs, files in os.walk(source_dir):
        for name in files:
            if not name.endswith(".cpp"):
                continue
            with open(os.path.join(base, name), "r", encoding="utf-8", errors="replace") as handle:
                names.update(re.findall(
                    r'IMPLEMENT_\w+_AUTOMATION_TEST\(\s*(?:\w+\s*,\s*)?"([^"]+)"',
                    handle.read()))
    if not names:
        return None, "no IMPLEMENT_*_AUTOMATION_TEST names found under Source/HomeWorld"
    return names, ""


def _resolve_stop(stop, keyword_state):
    """C++ semantics of PlaytestBeatFromText: lowercase, _, fold-out, first hit.

    Returns the matched PlaytestBeat* constant, or None for an unknown stop.
    An empty stop is the IsEmpty default (None when that line did not parse).
    """
    rules, empty_default = keyword_state
    key = stop.lower().replace("_", "").replace(" ", "")
    if not key:
        return empty_default
    for target, keywords in rules:
        if any(word in key for word in keywords):
            return target
    return None


def _load_quests(manifest_path):
    """QUESTS from a manifest file path. Returns (quests, error)."""
    try:
        spec = importlib.util.spec_from_file_location("quest_preflight_manifest", manifest_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as exc:  # a broken manifest must name itself, not implode
        return None, "manifest does not import: %s" % exc
    quests = getattr(module, "QUESTS", None)
    if not isinstance(quests, list):
        return None, "manifest has no QUESTS list"
    return quests, ""


# ---------------------------------------------------------------------------
# Warnings that cost nothing and bite nobody (the optional half).
# ---------------------------------------------------------------------------


def _mcp_warning():
    """The preflight is host-only; say so when the Editor is not there."""
    try:
        with socket.create_connection((MCP_HOST, MCP_PORT), timeout=0.5):
            return None
    except OSError:
        return ("UnrealMCP is not listening on %d; the preflight checked host data only "
                "- open the Editor for the real sweep" % MCP_PORT)


def _stale_dll_warning(root):
    """No build, no pie - but a stale editor DLL is tonight's red herring."""
    binary_glob = os.path.join(root, "Binaries", "Win64", "UnrealEditor-HomeWorld*.dll")
    dlls = glob.glob(binary_glob)
    if not dlls:
        return ("no UnrealEditor-HomeWorld DLL under Binaries/Win64 yet - "
                "run .\\Tools\\Safe-Build.ps1 before the sweep")
    newest_dll = max(os.path.getmtime(path) for path in dlls)
    newest_src = 0.0
    source_dir = os.path.join(root, "Source", "HomeWorld")
    for base, _dirs, names in os.walk(source_dir):
        for name in names:
            if name.endswith((".cpp", ".h")):
                newest_src = max(newest_src, os.path.getmtime(os.path.join(base, name)))
    if newest_src > newest_dll:
        return ("the editor DLL is older than Source/HomeWorld changes - "
                "rebuild with .\\Tools\\Safe-Build.ps1 or the sweep may refuse GetPlaytestStateJson")
    return None


# ---------------------------------------------------------------------------
# The preflight itself.
# ---------------------------------------------------------------------------


def _problem(rel, symbol, detail):
    return {"file": rel, "symbol": symbol, "detail": detail}


def _warn_unsure(warnings, rel, symbol, reason):
    warnings.append("unsure: %s :: %s: %s (warned, not failed)" % (rel, symbol, reason))


def run_preflight(root=None):
    """Return (problems, warnings). A problem is a real, file+named mismatch."""
    root = os.path.abspath(root or PROJECT_ROOT)
    problems = []
    warnings = []
    manifest_rel = MANIFEST_REL.replace(os.sep, "/")

    character_rel = CHARACTER_REL.replace(os.sep, "/")
    runner_rel = RUNNER_REL.replace(os.sep, "/")
    character_text, _character_path = _read(CHARACTER_REL, root)
    runner_text, _runner_path = _read(RUNNER_REL, root)
    if character_text is None:
        problems.append(_problem(character_rel, "file", "missing: the preflight reads it for beat names, stop words, and state keys"))
        return problems, warnings
    if runner_text is None:
        problems.append(_problem(runner_rel, "file", "missing: the preflight reads it for _build_snapshot keys"))
        return problems, warnings

    # --- manifest + contract --------------------------------------------
    quests, load_error = _load_quests(os.path.join(root, MANIFEST_REL))
    if quests is None:
        problems.append(_problem(manifest_rel, "QUESTS", load_error))
        return problems, warnings

    contract_errors = contract.validate_manifest(quests)
    for error in contract_errors:
        problems.append(_problem(manifest_rel, error.split(" ")[0], error))
    ids = [quest.get("id") for quest in quests if isinstance(quest, dict)]
    if not ids:
        problems.append(_problem(manifest_rel, "QUESTS", "no readable beat ids"))
        return problems, warnings

    # --- C++ parses: unsure is a warning, never a failure ----------------
    names, reason = _parse_beat_names(character_text)
    if names is None:
        _warn_unsure(warnings, character_rel, "PlaytestBeatName", reason)

    keyword_state, reason = _parse_keyword_rules(character_text)
    if keyword_state is None:
        _warn_unsure(warnings, character_rel, "PlaytestBeatFromText", reason)

    skip_steps, reason = _parse_skip_steps(character_text)
    if skip_steps is None:
        _warn_unsure(warnings, character_rel, "PlaytestSkipStep", reason)

    documented, reason = _parse_documented_beats(character_text)
    if documented is None:
        _warn_unsure(warnings, character_rel, "DebugFastForwardOpening", reason)

    state_keys, reason = _parse_state_keys(character_text)
    if state_keys is None:
        _warn_unsure(warnings, character_rel, "GetPlaytestStateJson", reason)

    popped, reason = _parse_popped_keys(runner_text)
    if popped is None:
        _warn_unsure(warnings, runner_rel, "_build_snapshot", reason)

    snapshot_actors, reason = _parse_runner_actor_keys(runner_text)
    if snapshot_actors is None:
        _warn_unsure(warnings, runner_rel, "_build_snapshot", reason)

    level_path, reason = _parse_level_path(runner_text)
    if level_path is None:
        _warn_unsure(warnings, runner_rel, "LEVEL_PATH", reason)

    # --- documented beats vs manifest ids --------------------------------
    if documented is not None and documented != ids:
        problems.append(_problem(
            character_rel, "DebugFastForwardOpening",
            "the `playtest_ff: beats:` line lists %s but the manifest is %s"
            % (", ".join(documented), ", ".join(ids))))

    # --- ids vs the name switch -------------------------------------------
    if names is not None:
        for beat_id in ids:
            if beat_id not in names.values():
                problems.append(_problem(
                    character_rel, "PlaytestBeatName",
                    "manifest beat '%s' has no `return TEXT(\"%s\");` case" % (beat_id, beat_id)))
        extra = sorted({name for name in names.values()} - set(ids))
        if extra:
            problems.append(_problem(
                manifest_rel, "QUESTS ids",
                "PlaytestBeatName knows beat(s) %s that the manifest does not declare" % ", ".join(extra)))

    # --- skip steps: every skipped beat must be a manifest beat -----------
    if skip_steps is not None and names is not None:
        for const, _step in sorted(skip_steps.items()):
            beat_name = names.get(const)
            if beat_name is None:
                problems.append(_problem(
                    character_rel, "PlaytestSkipStep",
                    "%s has a skip case but no name in PlaytestBeatName" % const))
            elif beat_name not in ids:
                problems.append(_problem(
                    character_rel, "PlaytestSkipStep",
                    "beat '%s' skips the player step but is not a manifest beat" % beat_name))

    # --- stop words: manifest stops must resolve to their own beat --------
    if keyword_state is not None and names is not None:
        rules, empty_default = keyword_state
        for quest in quests:
            beat_id = quest.get("id")
            stop = quest.get("stop") or ""
            constant = _resolve_stop(stop, keyword_state)
            if constant is None:
                if not stop and empty_default is None:
                    warnings.append("unsure: no IsEmpty default in PlaytestBeatFromText; '%s' stop not checked" % beat_id)
                    continue
                problems.append(_problem(
                    character_rel, "PlaytestBeatFromText",
                    "stop %r (beat '%s') matches no keyword rule; hw.Playtest.FastForward would log 'beat unknown'"
                    % (stop or "(empty)", beat_id)))
                continue
            resolved_name = names.get(constant)
            if resolved_name is None:
                problems.append(_problem(
                    character_rel, "PlaytestBeatName",
                    "a stop rule returns %s, which PlaytestBeatName does not name" % constant))
            elif resolved_name != beat_id:
                problems.append(_problem(
                    character_rel, "PlaytestBeatFromText",
                    "stop %r resolves to beat '%s' but the manifest beat is '%s'"
                    % (stop or "(empty)", resolved_name, beat_id)))

    # --- snapshot paths ----------------------------------------------------
    for quest in quests:
        beat_id = quest.get("id")
        manifest_where = "%s (beat '%s')" % (manifest_rel, beat_id)
        for check in (quest.get("checks") if isinstance(quest, dict) else None) or []:
            if not isinstance(check, dict):
                continue
            for field in ("path", "a", "b"):
                path = check.get(field)
                if not isinstance(path, str) or path.count(".") == 0:
                    continue
                parts = path.split(".")
                if parts[0] == "quest" and state_keys is not None and parts[1:]:
                    if popped is not None and parts[1] in popped:
                        problems.append(_problem(
                            manifest_where, "GetPlaytestStateJson",
                            "quest.%s is moved into beat.* by _build_snapshot; check beat.%s" % (parts[1], parts[1])))
                    elif parts[1] not in state_keys:
                        problems.append(_problem(
                            manifest_where, "GetPlaytestStateJson",
                            "quest.%s is not a GetPlaytestStateJson key (would be inconclusive)" % parts[1]))
                elif parts[0] == "beat" and popped is not None and parts[1:]:
                    if parts[1] not in popped:
                        problems.append(_problem(
                            manifest_where, "_build_snapshot",
                            "beat.%s is not a snapshot beat key (pop only handles %s)"
                            % (parts[1], ", ".join(sorted(popped)))))
                elif parts[0] == "actors" and parts[1:]:
                    group = parts[1]
                    if snapshot_actors is not None and group not in snapshot_actors:
                        problems.append(_problem(
                            manifest_where, "_build_snapshot",
                            "actors.%s is never written by _build_snapshot (would be inconclusive)" % group))
                    elif group in ACTOR_KEYS:
                        if len(parts) > 2 and parts[2] not in ACTOR_KEYS[group]:
                            problems.append(_problem(
                                manifest_where, "ACTOR_KEYS",
                                "actors.%s.%s is not a documented snapshot key (allowlist has %s)"
                                % (group, parts[2], ", ".join(sorted(ACTOR_KEYS[group])))))
                    elif snapshot_actors is not None:
                        warnings.append(
                            "stale allowlist: _build_snapshot writes actors.%s but ACTOR_KEYS does not list it "
                            "(sub-keys cannot be checked)" % group)
                    else:
                        problems.append(_problem(
                            manifest_where, "ACTOR_KEYS",
                            "actors.%s is in neither the actors allowlist nor _build_snapshot" % group))

    if snapshot_actors is not None:
        stale = sorted(snapshot_actors - set(ACTOR_KEYS))
        if stale:
            warnings.append(
                "stale allowlist: _build_snapshot emits actors.%s, not in ACTOR_KEYS" % ", ".join(stale))

    # --- the map the sweep loads -------------------------------------------
    if level_path is not None:
        # /Game/HomeWorld/Maps/SizeTest/L_SizeTest -> Content/HomeWorld/Maps/SizeTest/L_SizeTest.umap
        rel_parts = ["Content"] + level_path.strip("/").split("/")[1:]
        umap_rel = "/".join(rel_parts) + ".umap"
        if not os.path.isfile(os.path.join(root, *rel_parts) + ".umap"):
            problems.append(_problem(
                umap_rel, "LEVEL_PATH",
                "the map the sweep loads does not exist (%s, expected %s); every beat would end inconclusive"
                % (level_path, umap_rel)))

    # --- optional warnings: reachability of the sweep, never failures ------
    for warning in (_mcp_warning(), _stale_dll_warning(root)):
        if warning:
            warnings.append(warning)

    # --- declared coverage: warn-only sidecar checks -----------------------
    # Inverted too far to be a mismatch: the coverage matrix is documentation.
    # But a declared test name that does not exist, or a row for a beat the
    # manifest dropped, is drift someone must see early.
    try:
        import quest_coverage
    except Exception as exc:  # pragma: no cover - a broken sibling warns loudly once
        warnings.append("unsure: quest_coverage could not import (%s)" % exc)
    else:
        warnings.extend(quest_coverage.declared_warnings(root))
    return problems, warnings


def main(root=None):
    problems, warnings = run_preflight(root)
    for warning in warnings:
        print("quest_preflight: warn: %s" % warning)
    if problems:
        print("quest_preflight: FAIL - %d real mismatch(es)" % len(problems))
        for problem in problems:
            print("  %s :: %s" % (problem["file"], problem["symbol"]))
            print("      %s" % problem["detail"])
        return 2
    print("quest_preflight: PASS - manifest ids, stop words, skip steps, snapshot paths, and the map agree")
    return 0
