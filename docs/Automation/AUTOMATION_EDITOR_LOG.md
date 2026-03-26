# Editor Output Log: capture, filter, and safety rule

**Goal:** Use the Unreal Editor Output Log in the automation cycle. On failure we capture it, filter to development-relevant lines by default, and apply a **safety rule**: when the Fixer or Guardian cannot fix an issue, we instruct them to use the **unfiltered** log so the filter cannot hide the real error.

---

## Files

| File | Purpose |
|------|--------|
| **Saved/Logs/editor_output_full.txt** | Last N lines of Editor log (full, unfiltered). Written on each main-loop failure by the Watcher. Overwritten each capture. |
| **Saved/Logs/editor_output_filtered.txt** | Filtered subset: only lines that directly influence development (errors, warnings, project/PCG/script categories, signal keywords). Written by `Content/Python/filter_editor_log.py` after capture. |

Both files are produced on every failure (when the Watcher runs the capture step). We never write only the filtered view.

---

## When capture runs

- **When:** On **failure** of the main loop (Developer exits non-zero), **before** the Watcher starts the Fixer or invokes the Guardian.
- **Where:** The Watcher ([Tools/Watch-AutomationAndFix.ps1](../Tools/Watch-AutomationAndFix.ps1)) copies the last 3000 lines of `Saved/Logs/HomeWorld.log` (or the newest suitable `*.log` in `Saved/Logs/`) to `editor_output_full.txt`, then runs `Content/Python/filter_editor_log.py` to produce `editor_output_filtered.txt`.

---

## Filter (signal vs noise)

The filter script keeps lines that **directly influence development**:

- **Severity:** Lines containing `Error`, `Warning`, `Fatal`, `Assert`, `Exception` (case-insensitive).
- **Categories (allow-list):** LogPCG, LogScript, LogHomeWorld, LogOutputLog, LogPython, LogAutomation, LogTemp, LogLoad, LoadErrors, LogWindows, LogInit, LogExit, LogActor, LogGameMode, LogWorld, LogEngine, LogUnrealMCP.
- **Keywords:** error, failed, failure, exception, assert, not found, cannot, unable, missing, invalid, crash, fatal, traceback, "no surfaces found" (PCG).

High-volume categories (e.g. LogAssetRegistry, LogContentStreaming) are included only when the line also contains an error-like keyword. The allow-list and keywords can be tuned **without editing code** via `Content/Python/editor_log_filter_config.json` (allow_categories, signal_keywords, noise_categories_unless_signal, severity_pattern). If that file is missing, the script uses built-in defaults. If the filter is found to hide an important message, relax the rules in the config (or in the script defaults) and document the case in [KNOWN_ERRORS.md](KNOWN_ERRORS.md).

---

## Safety rule: if it cannot be fixed, use the full log

**Rule:** When the automation **cannot fix** the issue (Fixer tried and the same failure recurred, or Guardian is invoked), we **instruct the agent to read the unfiltered log** so the filter cannot hide the real error. We do not delete or disable the filter; we change which file the agent is told to use.

**Concrete behavior:**

1. **Fixer (first fix round):** Prompt says: read `editor_output_filtered.txt` for a development-relevant excerpt; if the cause is unclear, also read `editor_output_full.txt`.
2. **Fixer (later fix rounds, fixRound >= 1):** Prompt adds: *"Previous fix round(s) did not resolve the issue. Read the **unfiltered** Editor log: **Saved/Logs/editor_output_full.txt**. The filtered view may have hidden the relevant error; do not rely only on editor_output_filtered.txt."*
3. **Guardian:** Prompt always includes: read **Saved/Logs/editor_output_full.txt** (unfiltered Editor log) for full context.

So "stop filtering" is implemented as **switching the agent’s instructions to the full log**, not as removing the filtered file. The full log is always available for every capture.

---

## Verification

After a failure, confirm under `Saved/Logs/`:

- `editor_output_full.txt` exists and contains the tail of the Editor log.
- `editor_output_filtered.txt` exists and contains only development-relevant lines (and the one-line header pointing to the full log).

If the filter was found to hide an important message, add an entry to [KNOWN_ERRORS.md](KNOWN_ERRORS.md) and adjust the filter via `Content/Python/editor_log_filter_config.json` (or the defaults in `filter_editor_log.py`) so that class of message is included in future.
