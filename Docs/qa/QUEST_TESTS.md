# In-editor quest tests

The opening sweep runs the real `hw.Playtest.FastForward` stops in PIE and checks the read-only state at each stop. It is the developer check. It does not fill, replace, or grade the human pass tables in [`TUTORIAL_PLAYTEST_QUEUE.md`](TUTORIAL_PLAYTEST_QUEUE.md).

## Run

With the Editor open and UnrealMCP listening on 55557:

```powershell
.\Tools\RunTests.ps1 -Quest
.\Tools\RunTests.ps1 -Quest -QuestOnly night,collect,heal
.\Tools\RunTests.ps1 -Quest -QuestList
```

- `-Quest` loads `L_SizeTest` if needed, ends any PIE, then starts one fresh PIE per selected stop.
- The suite ends PIE when it finishes and leaves the Editor on `L_SizeTest`.
- Save unrelated Editor work first; loading `L_SizeTest` can discard unsaved map changes.
- Run the sweep alone. A scene-placement script or another MCP editor command during a beat is reported as `inconclusive`, not a pass. Long Editor stalls pause the phase clock and are listed under `stalls` in the result.
- Results: `Saved/quest_tests.json`. Progress: `Saved/quest_tests_status.json`.
- Exit code `0` means every selected beat ran and passed. `1` means a beat failed or was inconclusive. `2` means the Editor, request, or run was unreachable. `3` means a sweep was already active.

A direct MCP call works too:

```text
execute_python_script("quest_tests.py")
```

That call arms the suite and returns. Poll the status file; do not call `time.sleep` in the suite.

## Preflight

Before anyone opens the Editor, the host-only preflight proves the manifest still matches the C++ fast-forward:

```powershell
.\Tools\RunTests.ps1 -QuestCheck   # python Content/Python/run_quest_tests_host.py --check
```

No Editor, no PIE, no map load, no build. It reuses `quest_test_contract.validate_manifest`, then checks:

- beat ids against `PlaytestBeatName`, `PlaytestSkipStep`, and the documented `playtest_ff: beats:` line in `HomeWorldCharacter.cpp`;
- every beat's `stop` word against the `PlaytestBeatFromText` keyword table, resolved the way C++ resolves it (first hit wins);
- `quest.*` / `beat.*` paths against `GetPlaytestStateJson` keys and `_build_snapshot`'s `quest.pop`;
- `actors.*` paths against what `_build_snapshot` actually writes, plus the documented allowlist `ACTOR_KEYS` in `Content/Python/quest_preflight.py`;
- that the `L_SizeTest.umap` the sweep loads exists (existence only; an LFS pointer file counts).

Exit `0` clean, `2` on a real mismatch, printed as `file :: symbol`. A parse the preflight cannot answer is a warning ("unsure"), never a failure; UnrealMCP reachability and a stale editor DLL are warnings too. `Content/Python/tests/test_quest_preflight.py` plants every mismatch class into a disposable copy of the tree and proves each one exits 2.

## What a beat checks

Every beat starts from the manifest's `stop`, waits for `playtest_ff: ready for <id>`, then evaluates declarative checks against one snapshot:

```json
{
  "quest": { "spirit_claimed": false, "herbs_gathered": 0, "...": "..." },
  "beat": { "ready_for": "herbs", "ready_distance": 252.0, "fast_forward_step": 0 },
  "actors": {
    "reveal": { "partner_waiting": false, "partner_stand": [760, 0, 0] },
    "counter": { "east_face": 985.0 },
    "dog": { "tamed": false },
    "wisps": { "count": 3 }
  },
  "tag_counts": { "NODE_OPENING_WISP": 3 }
}
```

Statuses are distinct:

- `passed`: every check measured its subject and matched.
- `failed`: a check measured its subject and did not match, or the fast-forward timed out.
- `inconclusive`: the check could not measure (missing getter, actor, or path). This is not a pass, and it makes the suite exit non-zero.

Green requires `beats_run == selected`, `beats_run > 0`, and zero failed or inconclusive beats. A run that executes zero beats is never green.

## Add a quest

1. Add the stop and its ready line to `DebugFastForwardOpening` in `Source/HomeWorld/HomeWorldCharacter.cpp`.
2. Add any new flags, counts, or positions to `AHomeWorldCharacter::GetPlaytestStateJson()`, or expose a read-only getter on the actor that owns them.
3. Add an entry to `Content/Python/quest_test_manifest.py` in chain order. Do not edit the runner for a data-only quest.
4. Run `.\Tools\RunTests.ps1 -Quest -QuestOnly <id>` and check `Saved/quest_tests.json`.

The manifest is `Content/Python/quest_test_manifest.py`; the engine is `Content/Python/quest_test_runner.py`; the executable check contract is `Content/Python/quest_test_contract.py`. The split is deliberate: the manifest is data, the runner drives PIE, and the contract module owns validation and check evaluation so host pytest can prove both without an Editor. A malformed manifest is refused before a sweep starts.

### Manifest shape

```python
{
    "id": "night",
    "stop": "",                 # argument to hw.Playtest.FastForward; "" means no argument
    "section": "Night on the island",
    "note": "night is on, the bed is behind you",
    "checks": [
        eq("beat.ready_for", "night"),
        eq("quest.night_spirit", True),
        count_tag("NODE_OPENING_WISP", 3),
        le("beat.ready_distance", 260),
        near("actors.partner.location", "actors.reveal.partner_stand", 80),
    ],
}
```

### Check vocabulary

| Helper | Meaning |
|---|---|
| `eq(path, value)` / `ne(path, value)` | Exact equality / inequality. |
| `le(path, value)` / `ge(path, value)` | Numeric bound. |
| `between(path, low, high)` | Inclusive numeric range. |
| `near(a, b, cm)` | 2D distance between two locations is at most `cm`. |
| `present(path)` | Path exists and is not null. |
| `count_tag(tag, value)` | Actor tag count equals `value`. |

Paths are dotted lookups into the snapshot and must start with `quest`, `beat`, `actors`, or `tag_counts`. A missing path in a value check is `inconclusive`; a present value that is wrong is `failed`. `present` is the exception: a missing path is `failed`, because absence is what that check measures.

## Stop semantics

The stop is **before** the named action, so the checks are preconditions, not completions. For example, `kettle` has the partner waiting and the armor gift, but `kettle_brewed` is false. `night` runs the whole chain and checks night plus the three tagged wisps. See the manifest for the full list.

Every fast-forward starts on the day body: it resets the time-of-day phase to Day and syncs the form before step 1. A PIE copied from a night Editor therefore still brews and gathers. `night`, `collect`, and `heal` reach Night at step 9.

## Boundaries

- **Not the queue pass.** Human judgement (feel, sightline, hover, wording) stays in `TUTORIAL_PLAYTEST_QUEUE.md`.
- **No second beat script.** The suite drives `hw.Playtest.FastForward`; it is not a parallel situation tool.
- **No queue writes.** The suite writes only `Saved/quest_tests.json` and `Saved/quest_tests_status.json`.
