# quest_test_contract.py
# The host-runnable contract for the opening quest sweep.
#
# This module owns the manifest shape and the declarative check vocabulary. It
# deliberately does not import unreal: pytest imports it on the host, without an
# Editor. quest_test_runner.py calls the same functions inside PIE.
#
# A check has two jobs, and the statuses keep them apart:
#   passed       the check measured its subject and matched
#   failed       the check measured its subject and did not match
#   inconclusive the check could not measure (missing path, wrong type, bad kind)
#
# A suite is green only when every selected beat produced a result, in chain
# order, and every result passed. Zero selected beats is never green.

import math

CHECK_KINDS = ("eq", "ne", "le", "ge", "between", "near", "present", "count_tag")
SNAPSHOT_ROOTS = ("quest", "beat", "actors", "tag_counts")


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def _is_path(value):
    if not isinstance(value, str) or not value:
        return False
    return all(part for part in value.split("."))


def _is_snapshot_path(value):
    if not _is_path(value):
        return False
    return value.split(".")[0] in SNAPSHOT_ROOTS


def _require_path(check, field, where, errors):
    path = check.get(field)
    if not _is_snapshot_path(path):
        errors.append(
            "%s.%s must be a dotted snapshot path rooted at %s"
            % (where, field, ", ".join(SNAPSHOT_ROOTS))
        )


def validate_check(check, where="check"):
    """Return a list of contract errors for one declarative check."""
    errors = []
    if not isinstance(check, dict):
        return ["%s must be a dict" % where]

    kind = check.get("kind")
    if kind not in CHECK_KINDS:
        return ["%s has unknown check kind %r" % (where, kind)]

    if kind in ("eq", "ne", "le", "ge", "between"):
        _require_path(check, "path", where, errors)

    if kind in ("eq", "ne") and "value" not in check:
        errors.append("%s.%s needs a value" % (where, kind))

    if kind in ("le", "ge"):
        if not _is_number(check.get("value")):
            errors.append("%s.%s value must be a number" % (where, kind))

    if kind == "between":
        low = check.get("low")
        high = check.get("high")
        if not _is_number(low) or not _is_number(high):
            errors.append("%s.between low and high must be numbers" % where)
        elif low > high:
            errors.append("%s.between low must be <= high" % where)

    if kind == "near":
        _require_path(check, "a", where, errors)
        _require_path(check, "b", where, errors)
        cm = check.get("cm")
        if not _is_number(cm) or cm <= 0:
            errors.append("%s.near cm must be a positive number" % where)

    if kind == "present":
        _require_path(check, "path", where, errors)

    if kind == "count_tag":
        tag = check.get("tag")
        if not isinstance(tag, str) or not tag:
            errors.append("%s.count_tag needs a non-empty tag" % where)
        count = check.get("value")
        if not _is_int(count) or count < 0:
            errors.append("%s.count_tag value must be a non-negative integer" % where)

    return errors


def validate_manifest(quests):
    """Return every contract error in the manifest. An empty list means valid."""
    if not isinstance(quests, list) or not quests:
        return ["QUESTS must be a non-empty list"]

    errors = []
    seen = set()
    for index, quest in enumerate(quests):
        where = "QUESTS[%d]" % index
        if not isinstance(quest, dict):
            errors.append("%s must be a dict" % where)
            continue

        quest_id = quest.get("id")
        if not isinstance(quest_id, str) or not quest_id:
            errors.append("%s.id must be a non-empty string" % where)
        elif quest_id in seen:
            errors.append("%s.id duplicates %r" % (where, quest_id))
        else:
            seen.add(quest_id)

        if not isinstance(quest.get("stop"), str):
            errors.append("%s.stop must be a string (empty means no argument)" % where)
        if not isinstance(quest.get("section"), str) or not quest.get("section"):
            errors.append("%s.section must be a non-empty string" % where)
        if not isinstance(quest.get("note"), str) or not quest.get("note"):
            errors.append("%s.note must be a non-empty string" % where)

        checks = quest.get("checks")
        if not isinstance(checks, list) or not checks:
            errors.append("%s.checks must be a non-empty list" % where)
            continue
        for check_index, check in enumerate(checks):
            errors.extend(validate_check(
                check, "%s.checks[%d]" % (where, check_index)))

    return errors


def describe(check):
    if not isinstance(check, dict):
        return str(check)
    kind = check.get("kind")
    if kind in ("eq", "ne", "le", "ge"):
        symbols = {"eq": "==", "ne": "!=", "le": "<=", "ge": ">="}
        return "%s %s %s" % (check.get("path"), symbols[kind], check.get("value"))
    if kind == "between":
        return "%s in [%s, %s]" % (check.get("path"), check.get("low"), check.get("high"))
    if kind == "near":
        return "2D(%s, %s) <= %s cm" % (check.get("a"), check.get("b"), check.get("cm"))
    if kind == "present":
        return "%s present" % check.get("path")
    if kind == "count_tag":
        return "tag %s count == %s" % (check.get("tag"), check.get("value"))
    return str(check)


def _resolve(data, path):
    if not isinstance(path, str):
        return False, None
    current = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return False, None
        current = current[part]
    return True, current


def _xy(point):
    if isinstance(point, dict):
        point = point.get("location")
    if isinstance(point, (list, tuple)) and len(point) >= 2:
        try:
            return float(point[0]), float(point[1])
        except (TypeError, ValueError):
            return None
    if hasattr(point, "x") and hasattr(point, "y"):
        try:
            return float(point.x), float(point.y)
        except (TypeError, ValueError):
            return None
    return None


def _dist2d(a, b):
    pa = _xy(a)
    pb = _xy(b)
    if pa is None or pb is None:
        return None
    return math.hypot(pa[0] - pb[0], pa[1] - pb[1])


def _inconclusive(description, detail):
    return {
        "check": description,
        "status": "inconclusive",
        "detail": detail,
    }


def run_check(check, snapshot):
    """Evaluate one check against a snapshot. Never raises for bad data."""
    if not isinstance(check, dict):
        return _inconclusive(str(check), "check must be a dict")
    check_errors = validate_check(check)
    if check_errors:
        return _inconclusive(describe(check), "; ".join(check_errors))
    if not isinstance(snapshot, dict):
        snapshot = {}
    kind = check.get("kind")
    description = describe(check)

    if kind in ("eq", "ne", "le", "ge", "between"):
        found, value = _resolve(snapshot, check.get("path", ""))
        if not found or value is None:
            return _inconclusive(description, "path missing: " + check.get("path", ""))
        expected = check.get("value", [check.get("low"), check.get("high")])
        try:
            if kind == "eq":
                passed = value == check.get("value")
            elif kind == "ne":
                passed = value != check.get("value")
            elif kind == "le":
                passed = value <= check.get("value")
            elif kind == "ge":
                passed = value >= check.get("value")
            else:
                passed = check.get("low") <= value <= check.get("high")
        except TypeError as exc:
            return _inconclusive(description, "cannot compare: " + str(exc))
        return {
            "check": description,
            "status": "passed" if passed else "failed",
            "expected": expected,
            "actual": value,
        }

    if kind == "present":
        found, value = _resolve(snapshot, check.get("path", ""))
        passed = found and value is not None
        return {
            "check": description,
            "status": "passed" if passed else "failed",
            "expected": "present",
            "actual": value,
        }

    if kind == "near":
        found_a, a = _resolve(snapshot, check.get("a", ""))
        found_b, b = _resolve(snapshot, check.get("b", ""))
        if not found_a or not found_b or a is None or b is None:
            return _inconclusive(description, "one or both points missing")
        distance = _dist2d(a, b)
        if distance is None:
            return _inconclusive(description, "points are not locations")
        return {
            "check": description,
            "status": "passed" if distance <= check.get("cm", 0) else "failed",
            "expected": "<= %s cm" % check.get("cm"),
            "actual": round(distance, 1),
        }

    if kind == "count_tag":
        count = snapshot.get("tag_counts", {}).get(check.get("tag"), 0)
        return {
            "check": description,
            "status": "passed" if count == check.get("value") else "failed",
            "expected": check.get("value"),
            "actual": count,
        }

    return _inconclusive(description, "unknown check kind: " + str(kind))


def evaluate_checks(checks, snapshot):
    """Return (assertions, status) with failed taking precedence over inconclusive."""
    if not isinstance(checks, (list, tuple)) or not checks:
        checks = []
    if not checks:
        return ([{
            "check": "beat declares at least one check",
            "status": "inconclusive",
            "detail": "checks list is empty",
        }], "inconclusive")

    assertions = [run_check(check, snapshot) for check in checks]
    if any(item.get("status") == "failed" for item in assertions):
        status = "failed"
    elif any(item.get("status") == "inconclusive" for item in assertions):
        status = "inconclusive"
    else:
        status = "passed"
    return assertions, status


def counts(results):
    """Count result statuses without letting an unknown status read as a pass."""
    counted = {"passed": 0, "failed": 0, "inconclusive": 0, "other": 0}
    for result in results:
        if not isinstance(result, dict):
            counted["other"] += 1
            continue
        status = result.get("status")
        if status in counted:
            counted[status] += 1
        else:
            counted["other"] += 1
    return counted


def all_passed(selected_ids, results):
    """True only for every selected beat, in chain order, with a passed result."""
    selected = list(selected_ids)
    results = list(results)
    if not selected or len(results) != len(selected):
        return False
    for expected_id, result in zip(selected, results):
        if not isinstance(result, dict):
            return False
        if result.get("id") != expected_id:
            return False
        if result.get("status") != "passed":
            return False
    return True
