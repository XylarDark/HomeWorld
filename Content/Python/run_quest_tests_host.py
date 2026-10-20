# run_quest_tests_host.py
# Host launcher for the in-editor opening quest sweep.
#
# Usage (from the repo root, with the Editor open):
#   python Content/Python/run_quest_tests_host.py
#   python Content/Python/run_quest_tests_host.py --only night,collect,heal
#   python Content/Python/run_quest_tests_host.py --list
#   .\Tools\RunTests.ps1 -Quest
#
# The script sends execute_python_script("quest_tests.py") over the Editor's
# raw TCP command port, then polls Saved/quest_tests.json. The suite runs on
# the Editor tick, so this process never blocks the game thread.
#
# Exit codes: 0 all selected beats passed; 1 a beat failed or was
# inconclusive; 2 the Editor, request, or run could not be reached; 3 a run is
# already active.

import argparse
import json
import os
import socket
import sys
import time

HOST = "127.0.0.1"
PORT = 55557
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONTENT_PYTHON = os.path.join(PROJECT_ROOT, "Content", "Python")
SAVED = os.path.join(PROJECT_ROOT, "Saved")
RESULTS = os.path.join(SAVED, "quest_tests.json")
STATUS = os.path.join(SAVED, "quest_tests_status.json")
REQUEST = os.path.join(SAVED, "quest_tests_request.json")

sys.path.insert(0, CONTENT_PYTHON)
try:
    import quest_test_contract as contract
    import quest_test_manifest as manifest
except Exception as exc:  # pragma: no cover - host setup failure
    print("quest_tests: cannot import the quest suite contract: %s" % exc)
    sys.exit(2)


def _read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, ValueError):
        return None


def _write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
    os.replace(tmp, path)


def _send(command, params):
    payload = json.dumps({"type": command, "params": params}).encode("utf-8")
    with socket.create_connection((HOST, PORT), timeout=5) as sock:
        sock.sendall(payload)
        chunks = b""
        while True:
            chunk = sock.recv(65536)
            if not chunk:
                break
            chunks += chunk
            try:
                return json.loads(chunks.decode("utf-8"))
            except ValueError:
                continue
    if chunks:
        return json.loads(chunks.decode("utf-8"))
    raise RuntimeError("no response from the Editor")


def _only_list(raw):
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def _print_manifest():
    print("quest_tests: %d beats in chain order" % len(manifest.QUESTS))
    for index, quest in enumerate(manifest.QUESTS, 1):
        stop = quest.get("stop") or "(no argument)"
        print("  %2d. %-8s %-22s stop=%s" % (
            index, quest.get("id"), quest.get("section", ""), stop))


def _first_problem(beat):
    for assertion in beat.get("assertions", []):
        if assertion.get("status") != "passed":
            return assertion
    return None


def _report(data):
    beats = data.get("beats", [])
    selected = data.get("selected", [])
    run_ok = contract.all_passed(selected, beats)

    print("")
    print("quest_tests: %s" % ("PASS" if run_ok else "FAIL"))
    for beat in beats:
        print("  %-8s %-12s %5.1fs" % (
            beat.get("id", "?"), beat.get("status", "?"),
            float(beat.get("duration_s") or 0.0)))
        problem = _first_problem(beat)
        if problem is not None:
            print("      %s: %s" % (problem.get("status"), problem.get("check")))
            print("      expected %s  actual %s" % (
                problem.get("expected"), problem.get("actual")))
            if problem.get("detail"):
                print("      %s" % problem.get("detail"))
        if beat.get("error"):
            print("      error: %s" % beat.get("error"))

    print("quest_tests: %d/%d passed, %d failed, %d inconclusive" % (
        data.get("passed", 0), data.get("beats_run", 0),
        data.get("failed", 0), data.get("inconclusive", 0)))
    stalls = data.get("stalls") or []
    if stalls:
        print("quest_tests: warning: %d Editor stall(s), longest %.1fs; test deadlines were extended" % (
            len(stalls), max(float(item.get("seconds") or 0.0) for item in stalls)))
    if data.get("error"):
        print("quest_tests: error: %s" % data.get("error"))
    print("quest_tests: results %s" % RESULTS)
    return 0 if run_ok else 1


def main():
    parser = argparse.ArgumentParser(description="Run the opening quest sweep in the open Unreal Editor.")
    parser.add_argument("--only", help="comma-separated beat ids (default: every beat)")
    parser.add_argument("--list", action="store_true", help="print the beats and exit")
    parser.add_argument("--no-load-level", action="store_true", help="refuse to load L_SizeTest")
    parser.add_argument("--timeout", type=int, default=1800, help="poll timeout in seconds (default 1800)")
    args = parser.parse_args()

    contract_errors = contract.validate_manifest(manifest.QUESTS)
    if contract_errors:
        print("quest_tests: manifest contract failed:")
        for error in contract_errors:
            print("  " + error)
        return 2

    if args.list:
        _print_manifest()
        return 0

    only = _only_list(args.only)
    unknown = [item for item in only if manifest.by_id(item) is None]
    if unknown:
        print("quest_tests: unknown beat id(s): %s" % ", ".join(unknown))
        return 2

    status = _read_json(STATUS)
    if status and status.get("active") and time.time() - float(status.get("updated_at") or 0) < 60:
        print("quest_tests: a sweep is already active (beat %s, phase %s)." % (
            status.get("beat"), status.get("phase")))
        print("quest_tests: wait for it to finish; results are in %s" % RESULTS)
        return 3

    run_id = "%s-%d" % (time.strftime("%Y%m%d-%H%M%S"), os.getpid())
    request = {
        "run_id": run_id,
        "only": only,
        "load_level": not args.no_load_level,
    }
    _write_json(REQUEST, request)

    selected = [quest["id"] for quest in manifest.QUESTS if not only or quest["id"] in set(only)]
    print("quest_tests: starting %d beat(s): %s" % (len(selected), ", ".join(selected)))
    print("quest_tests: the Editor will load L_SizeTest if needed and end PIE when the sweep finishes.")

    try:
        response = _send("execute_python_script", {"script_path": "quest_tests.py"})
    except Exception as exc:
        try:
            os.remove(REQUEST)
        except OSError:
            pass
        print("quest_tests: cannot reach the Editor on %s:%d (%s)." % (HOST, PORT, exc))
        print("quest_tests: open the Editor, wait for UnrealMCP, then retry.")
        return 2

    if not response or response.get("status") == "error" or response.get("success") is False:
        detail = ""
        if response:
            detail = response.get("error") or response.get("message") or ""
        print("quest_tests: the Editor refused quest_tests.py: %s" % detail)
        try:
            os.remove(REQUEST)
        except OSError:
            pass
        return 2

    deadline = time.time() + args.timeout
    last_status = None
    while time.time() < deadline:
        data = _read_json(RESULTS)
        if data and data.get("run_id") == run_id and data.get("done"):
            return _report(data)

        current = _read_json(STATUS)
        if current and current.get("run_id") == run_id:
            key = (
                current.get("index"), current.get("total"),
                current.get("beat"), current.get("phase"),
            )
            if key != last_status:
                last_status = key
                if current.get("beat"):
                    print("quest_tests: [%s/%s] %s - %s" % (
                        current.get("index"), current.get("total"),
                        current.get("beat"), current.get("phase")))
                else:
                    print("quest_tests: %s" % current.get("phase"))
        time.sleep(0.5)

    data = _read_json(RESULTS)
    if data and data.get("run_id") == run_id:
        print("quest_tests: timed out waiting for the sweep to finish; last result is below.")
        return _report(data)
    print("quest_tests: timed out after %ds with no result for run %s." % (args.timeout, run_id))
    print("quest_tests: check the Editor Output Log for quest_tests: lines and %s" % STATUS)
    return 2


if __name__ == "__main__":
    sys.exit(main())
