# Known Errors

Record errors and their fixes here so they are not repeated. See `.cursor/rules/07-ai-agent-behavior.mdc` (Error recurrence prevention) and `05-error-handling.mdc` (Learning from errors).

## Entry format

For each entry use:

- **Error** – What failed (command, file, or step).
- **Cause** – Likely reason.
- **Fix** – What was done to resolve it.
- **Context** – Optional: area (e.g. build, API, refactor) or date.

---

## Entries

<!-- Example:
### Build failure: missing include
- **Error:** Unreal build fails with "undefined symbol" in GameMode.
- **Cause:** New C++ module not added to .Build.cs or wrong include path.
- **Fix:** Add module dependency in MyProject.Build.cs; use correct path to shared headers.
- **Context:** 2025-02, C++ modules.
-->
