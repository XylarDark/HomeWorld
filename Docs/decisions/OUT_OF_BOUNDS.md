# Out-of-bounds problems

Problems that are **not** the harness's fault, recorded once so the next
occurrence is visible instead of rediscovered. **A repeated problem here earns a
written response, never a new gate** - a gate is the thing that got deleted.

This file is not a task list. If it passes 40 lines the response is not working.

| First seen | Signature | Count | Response |
|---|---|---|---|
| 2026-10-02 | `json-blob-in-diff` | 1 | Merged a large machine-generated JSON blob into a commit. Fix is bounded diffs; no gate will ever catch this and none should be built. |
| 2026-10-02 | `ue-editor-lock-contention` | 2 | Two agents each opened the UE Editor. Fix is one writer at a time (npm run editor:lock); the harness cannot enforce it from inside the Editor. |
