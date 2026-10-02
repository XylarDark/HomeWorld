"""Mutation-verify the camp-night C++ automation tests.

A test suite that cannot fail is not evidence. Each mutation below breaks ONE law and
asserts the suite notices. The laws are refactor magnets: "eased AND asleep" looks
redundant, "converted is not calmed" looks like duplicate bookkeeping, and both are the
kind of thing a later pass "simplifies" while silently inverting the beat.

Usage (from repo root):

    python Content/Python/tests/_mutate_camp_night.py

Each round is a real C++ edit, a real Safe-Build, and a real headless automation run, so
this takes minutes. That is the point: a mutation test that does not actually rebuild
proves nothing about compiled code.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
UE = r"C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
UPROJECT = os.path.join(REPO, "HomeWorld.uproject")
LOG = os.path.join(tempfile.gettempdir(), "hw-mutate-automation.log")

STEALTH = os.path.join(REPO, "Source", "HomeWorld", "HomeWorldSpiritStealthComponent.cpp")
TYPES = os.path.join(REPO, "Source", "HomeWorld", "HomeWorldCampNightTypes.h")
#: GetSpiritTouchVerdict is DECLARED in the header and DEFINED in the .cpp. M2 first targeted
#: the header, matched nothing, and was reported SKIPPED rather than KILLED - so a mutation
#: that never applied was nearly recorded as a test weakness.
TYPES_CPP = os.path.join(REPO, "Source", "HomeWorld", "HomeWorldCampNightTypes.cpp")
#: The placed actors. Their self-tagging is what stops #14 soft-latching, and a break there is
#: invisible to every other test because they all hand-tag their own stand-ins.
CAMP_ACTOR = os.path.join(REPO, "Source", "HomeWorld", "HomeWorldCampActor.cpp")

# (name, file, pattern, replacement, test path fragment that MUST fail)
MUTATIONS = [
    (
        "M1: the freedom gate stops being consulted when freeing the captive",
        STEALTH,
        r"if \(!IsFreedomUnlocked\(\)\)",
        "if (false)",
        "HomeWorld.T0.M16.FreedomGate",
    ),
    (
        "M2: a spirit is allowed to touch an actor's BODY",
        TYPES_CPP,
        # Three tabs before the return, not two. The file is tab-indented one level deeper
        # than a naive reading of a GitHub diff suggests, and `\t\t\)` silently matched
        # nothing - the harness caught it as a HARNESS BUG rather than scoring it.
        r"(case EHomeWorldSpiritTouchTarget::ActorBody:\s*\n\t\tdefault:\s*\n\t\t\t)return EHomeWorldSpiritTouchVerdict::Refused;",
        r"\1return EHomeWorldSpiritTouchVerdict::Allowed;",
        "HomeWorld.T0.M15.SpiritTouchTable",
    ),
    (
        "M3: being eased stops being required - asleep alone opens the gate",
        TYPES,
        r"return bEased && bAsleep && !bKilled && !bConverted;",
        "return bAsleep && !bKilled && !bConverted;",
        "HomeWorld.T0.M16.CalmGateLaw",
    ),
    (
        "M4: a converted actor counts as calmed (conflating conversion with care)",
        TYPES,
        r"return bEased && bAsleep && !bKilled && !bConverted;",
        "return bEased && bAsleep && !bKilled;",
        "HomeWorld.T0.M16.CalmGateLaw",
    ),
    (
        "M5: easing the guard no longer puts them to sleep",
        STEALTH,
        r"(if \(Role == EHomeWorldCampRole::Guard\)\s*\n\t\{\s*\n)(.*?)(\n\t\tState->bAsleep = true;)",
        r"\1\2",
        "HomeWorld.T0.M14.EaseDirection",
    ),
    (
        # The first version of this was `return nullptr;` at the top of the function, which
        # is the obvious way to break it and CANNOT BE SCORED: it makes the rest of the body
        # unreachable, UE compiles C4702 as an error, build() raises, and a mutation that
        # never got as far as running gets filed under a crash instead of under a result.
        #
        # So it now breaks the SAME behaviour the honest way - the match never succeeds -
        # which compiles, runs, and is killed by a test for the right reason.
        "M6: the camp actor lookup silently fails again (soft latch everywhere)",
        STEALTH,
        r"return Actor->GetName\(\)\.Contains\(Label\.ToString\(\)\) \|\| Actor->ActorHasTag\(Label\);",
        "return false;",
        "HomeWorld.T0.M14.PlacedActorsAreDiscovered",
    ),
    # --- the placed actors must tag THEMSELVES, or #14 silently soft-latches again --------
    (
        "M7: a placed camp actor stops tagging itself (discovery breaks, nothing goes red)",
        CAMP_ACTOR,
        r"\tTags\.AddUnique\(Label\);",
        "\t// Tags.AddUnique(Label);",
        "HomeWorld.T0.M14.PlacedActorsAreDiscovered",
    ),
    (
        # An earlier version of this INSERTED a second `case EHomeWorldCampRole::Sleeper:`
        # rather than editing the existing one, and the build died with C2196 "case value
        # already used". A mutation that fails to compile is not scored - it never becomes
        # evidence either way - so it edits the real return instead.
        "M8: the label helper returns a role-blind constant (guard/sleeper/captive indistinguishable)",
        CAMP_ACTOR,
        r'(case EHomeWorldCampRole::Sleeper:\s*\n\t\t\treturn TEXT\("NODE_SLEEPER"\);)',
        r'case EHomeWorldCampRole::Sleeper:\n\t\t\treturn TEXT("NODE_GUARD");',
        "HomeWorld.T0.M14.PlacedActorsAreDiscovered",
    ),
    (
        # The editor-placement path. `OnConstruction` is what tags an actor a human dragged
        # into the level, and it is the path `t0_place_camp.py` leans on. Removing the
        # constructor's own call is not enough to catch this: the constructor already
        # tagged the DEFAULT role, so the actor keeps a plausible-looking but WRONG tag.
        "M9: OnConstruction stops re-tagging, so a role flip keeps the default role's tag",
        CAMP_ACTOR,
        r"(void AHomeWorldCampActor::OnConstruction\(const FTransform& Transform\)\s*\n\{\s*\n\tSuper::OnConstruction\(Transform\);)(.*?)(\n\tRefreshCampIdentity\(\);)",
        r"\1\2",
        "HomeWorld.T0.M14.PlacedActorsAreDiscovered",
    ),
]


#: Written while a mutation is applied. If the process dies mid-run, the next run finds this
#: and restores the tree before doing anything else.
INTERRUPT_MARKER = os.path.join(tempfile.gettempdir(), "hw-mutate-camp-night.inflight")


def _recover_if_interrupted():
    """Restore a tree left mutated by a killed run.

    An earlier run of this script was killed while a mutation was applied. The `finally`
    restore never ran, so the tree kept a bypassed freedom gate and the NEXT run's baseline
    correctly reported itself not green - for a reason that had nothing to do with the code
    under test.

    The lesson is the same one this session keeps arriving at: a guard that cleans up only
    on the happy path is a guard that leaves evidence behind when things go wrong. So the
    in-flight state is persisted to disk and repaired on the next start, rather than being
    trusted to a code path that a kill can skip.
    """
    if not os.path.exists(INTERRUPT_MARKER):
        return False
    with open(INTERRUPT_MARKER, "r", encoding="utf-8") as handle:
        state = json.load(handle)
    print(f"found an interrupted run; restoring {state['target']}")
    shutil.copyfile(state["backup"], state["target"])
    os.unlink(state["backup"])
    os.unlink(INTERRUPT_MARKER)
    print("restored\n")
    return True


def build():
    """Run Safe-Build. MUST actually invoke PowerShell.

    The first version of this used `shell=True` with a .ps1 path. On Windows that hands the
    script to cmd.exe, which does not execute PowerShell scripts - it returns exit code 0
    with EMPTY output and builds nothing. Every mutation then skipped its compile check and
    ran the tests against the unmutated binary, so all six reported "SURVIVED" for a reason
    that had nothing to do with the tests.

    That is the exact failure this project keeps meeting: a guard that silently does nothing
    and is mistaken for a result. Hence the assertion below, not just the invocation.
    """
    result = subprocess.run(
        [
            "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass",
            "-File", os.path.join(REPO, "Tools", "Safe-Build.ps1"),
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    output = (result.stdout or "") + (result.stderr or "")
    if "Build succeeded" not in output:
        raise RuntimeError(
            "Safe-Build did not report success. A mutation may only be scored after a real "
            "compile - otherwise the suite is testing the previous binary.\n" + output[-1500:]
        )
    return output


def run_tests():
    if os.path.exists(LOG):
        os.unlink(LOG)
    subprocess.run(
        [
            UE, UPROJECT,
            "-ExecCmds=Automation RunTests HomeWorld.T0; Quit",
            "-unattended", "-nopause", "-NullRHI", "-nosplash", "-stdout",
            "-abslog=" + LOG,
        ],
        cwd=REPO,
        capture_output=True,
        text=True,
        timeout=900,
    )
    if not os.path.exists(LOG):
        return None, {}
    with open(LOG, "r", encoding="utf-8", errors="replace") as handle:
        text = handle.read()
    results = {}
    for match in re.finditer(
        r"Test Completed\. Result=\{(\w+)\} Name=\{[^}]*\} Path=\{(HomeWorld[^}]*)\}", text
    ):
        results[match.group(2)] = match.group(1)
    errors = re.findall(r"LogAutomationController: Error: (Expected.*)", text)
    return results, errors


def main():
    _recover_if_interrupted()

    # Build BEFORE baselining. The first version of this script ran the baseline against
    # whatever DLL happened to be on disk, which silently assumed the binary matched the
    # source. After recovering an interrupted mutation the source was correct and the binary
    # was not, so the baseline reported a failure that had nothing to do with the code.
    #
    # The baseline is supposed to be the answer to "is the tree green right now?", and the
    # only honest way to ask that is to compile what is in the tree first.
    build()

    results, errors = run_tests()
    if results is None:
        print("BASELINE COULD NOT RUN - no automation log produced")
        return 1
    failed = [k for k, v in results.items() if v != "Success"]
    if failed:
        print("BASELINE IS NOT GREEN: " + ", ".join(failed))
        for err in errors[:10]:
            print("   " + err)
        return 1
    print(f"baseline green ({len(results)} T0 tests)\n", flush=True)

    survivors = []
    for name, path, pattern, replacement, expected in MUTATIONS:
        with open(path, "r", encoding="utf-8") as handle:
            original = handle.read()
        mutated, count = re.subn(pattern, replacement, original, flags=re.DOTALL)
        if count == 0:
            # This is a mistake in THIS harness, not a weakness in the tests: the mutation
            # never applied, so the run proves nothing either way. M2 did exactly this once by
            # targeting the declaration instead of the definition.
            print(
                f"  HARNESS BUG (pattern matched nothing, so nothing was proven) {name}",
                flush=True,
            )
            survivors.append(name)
            continue

        backup = tempfile.mktemp(suffix=(".h" if path.endswith(".h") else ".cpp"))
        shutil.copyfile(path, backup)
        # Persist the in-flight state BEFORE touching the source, so a kill from here on is
        # recoverable by the next run rather than poisoning it.
        with open(INTERRUPT_MARKER, "w", encoding="utf-8") as handle:
            json.dump({"target": path, "backup": backup, "mutation": name}, handle)
        try:
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(mutated)
            # build() raises rather than returning on a silent no-op, so an unbuilt
            # mutation can never be scored.
            build()
            res, _ = run_tests()
            outcome = res.get(expected, "MISSING")
            if outcome != "Success":
                print(f"  KILLED   {name}", flush=True)
            else:
                print(f"  SURVIVED {name}  <-- {expected} still passes", flush=True)
                survivors.append(name)
        finally:
            shutil.copyfile(backup, path)
            os.unlink(backup)
            if os.path.exists(INTERRUPT_MARKER):
                os.unlink(INTERRUPT_MARKER)

    # Leave the tree building and green again, not merely source-clean.
    build()
    final, _ = run_tests()
    if final is None:
        print("\nfinal verification could not run")
        return 1
    broken = [k for k, v in final.items() if v != "Success"]
    if broken:
        print(f"\nRESTORED TREE IS NOT GREEN: {broken}")
        return 1
    print(f"restored tree green ({len(final)} T0 tests)")

    if survivors:
        print(f"\n{len(survivors)} SURVIVOR(S) - the suite does not enforce these")
        return 1
    print("\nall mutations killed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())