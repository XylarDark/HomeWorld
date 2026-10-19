---
name: refactoring-code
description: Use when a Rider refactor must update declarations and usages, such as rename, move, extract, or a signature change.
allowed-tools: execute_tool
metadata:
  author: JetBrains
---

# Code Refactoring

Rider/ReSharper semantic refactorings on a solution open in Rider. Each tool resolves the target through the IDE index and rewrites **every** reference — `nameof`, `<see cref>`, XAML/Razor bindings, C++/Unreal — in one call. Always prefer the tool over a text edit: grep-and-replace *looks* done but silently misses these and leaves the solution broken.

## Invoke a tool

Call through `execute_tool` — the first token is the exact tool name, then `--flag value` pairs. Map each refactor to exactly one tool and issue it directly; the required flags are below, so no lookup is needed first.

```
execute_tool(command="rename_refactoring --filePath API/Services/OrderService.cs --symbolName OrderService --newName OrderProcessor")
```

| Refactor | Tool | Required flags |
|---|---|---|
| Rename a symbol + all usages | `rename_refactoring` | `--filePath --symbolName --newName` |
| Change a method signature (add/remove/reorder params) | `change_api_signature` | `--filePath --methodName --parameters` |
| Move a type to another namespace | `move_type_to_namespace` | `--filePath --typeName --targetNamespace` |
| Sync namespaces to folders | `reorganize_namespaces` | `--scope` |
| Delete a symbol only if unused | `safe_delete` | `--filePath --symbolName` |
| Extract an interface | `extract_interface` | `--filePath --typeName --interfaceName --members` |
| Extract a base class | `extract_base_class` | `--filePath --typeName --baseClassName --members` |
| Extract a method (C# only) | `extract_method` | `--filePath --startLine --endLine --methodName` |

**HomeWorld: only two rows in this table are callable.** The default whitelist exposes `safe_delete`, and `rename_refactoring` registers only under `-AllowedTools '*'`. Every other tool here was dropped from the default whitelist on 2026-10-15 (DEC-0050) and answers `Tool '<x>' not found` — that is the tool being absent, not a wrong name, so the table is not a list to copy from. See the block below.

## This project's Rider build (HomeWorld)

Before the first Rider call, follow the AGENTS.md sentence: start Rider once only when a C++ symbol, diagnostic, or refactor needs it and port 64342 is down.

Verified 2026-10-15 by reading the live tool surface two independent ways (`tools/list`, and the
router's own `Tool 'x' not found. Available tools: ...` reply):

- **`rename_refactoring` is not exposed by default.** It registers only when the MCP server was
  started with its tool whitelist **disabled** (`-AllowedTools '*'`). Under a `--allowed-tools`
  value - *including one that names it* - it never registers, at any point after startup. Where it
  is exposed it works on C++: a preview rename of `AHomeWorldCharacter` resolved 37 files and 327
  call sites. See `Tools/Start-RiderMcp.ps1` for the mode and its trade-off.
- **Of the other seven refactorings, only `safe_delete` is still exposed.** DEC-0050 (2026-10-15)
  removed `change_api_signature`, `move_type_to_namespace`, `reorganize_namespaces`,
  `extract_interface`, `extract_base_class`, and `extract_method` from the default whitelist: each
  now answers `Tool '<x>' not found` before any argument can reach it. The results below were
  measured while they were still exposed, and stand for when they are exposed again (under
  `-AllowedTools '*'`, or a later build), all with `--preview true` except where noted:
  - `safe_delete` **does** resolve C++. `--preview true` on `bCloudDescentActive` returned
    `applied: false`, `deleted: []`, and 7 `conflicts` naming the `.h` and `.cpp`. Use that preview
    when you need the files that reference a member. **Never omit `--preview true`** — without it
    the tool deletes.
  - `change_api_signature`, `move_type_to_namespace`, `extract_interface`, and `extract_base_class`
    answered "not found" for `AHomeWorldCharacter` / `BeginPlay`. They are not C++ refactors here.
    Do not retry them on C++.
  - `extract_method` accepted `HomeWorldCharacter.cpp` and then rejected a real statement block
    inside `BeginPlay` (lines 228–233): "The line range does not cover a complete sequence of
    statements inside one member." Do not use it to extract C++.
  - `reorganize_namespaces` rejected a file path ("expected a project name or a folder path").
    Not a file-scoped C++ edit.
- `execute_tool` is exposed in the default (`direct`) mode as well, so the call style above works,
  and calling a tool by name reaches the same surface.
- Every call needs `rootFolder=C:/dev/HomeWorld`, or the server answers *"Unable to determine the
  target project for the current MCP tool call."*

Canonical reference for this build: `docs/tools/Rider_MCP_for_UE_Games.md`.

- `--symbolName`/`--typeName` accept `Name` or `Type.Member`. Every **exposed** tool also takes `--preview true` (analysis only, no writes) — add it first for public-API or many-call-site changes, then re-issue without it to apply.
- The next three bullets are parameter detail for tools that are **not** on this project's default whitelist (see above). They still hold wherever those tools are exposed — `-AllowedTools '*'` — and are kept so the guidance is not lost:
- `change_api_signature`: **always** pass a **bare** `--methodName` (a qualified `Type.Member` can report "not found") **and** `--declaringType <FullyQualifiedType>` on the very first call — don't wait for an `ambiguous_method` error; the method is usually on an interface/impl pair, and `--declaringType` is harmless when it isn't. `--parameters` is a single-quoted JSON array = the **complete** new parameter list in order: an existing name is kept/moved, an omitted one is removed, a new name needs `type` (and optional `defaultValue` inserted at call sites). Disambiguate remaining overloads with `--currentSignature '["int","string"]'` (the CURRENT parameter types).
- `extract_interface`/`extract_base_class` `--members` is a single-quoted JSON array of member names, e.g. `'["IsMatch","Merge"]'` — not a comma-separated list.
- A multi-part request ("rename `X` **and** move it to `Y`") is one tool per step, in sequence — never folded into one call.
- Only for a tool not in the table, or a genuinely unclear parameter, read `reference/tools/<tool>.md` once (index: `reference/tools.md`). There is no `--describe`.

## Rules

1. **Use the tool; never hand-edit or fall back before a real call has run.** `Missing required parameters: …` (add them from the table), `Tool '<x>' not found` (wrong name — copy from the table), and conflict/ambiguous responses are all **fixable input mistakes** — correct the argument and retry. Fall back to a text edit only if `execute_tool` isn't in your toolset, or a call actually ran and failed in a way no input change can fix. **In this project, do not retry these:** `rename_refactoring` is not exposed by the default whitelist — no argument change reaches it. Hand-edit (`search_symbol` + `search_text` for the call sites), use `safe_delete --preview true` when you only need the files that reference a C++ member, or ask the user whether to restart as `Tools\Start-RiderMcp.ps1 -AllowedTools '*'`, which exposes rename (and also shell and file-write tools, so it is the user's call). `change_api_signature`, `move_type_to_namespace`, `reorganize_namespaces`, `extract_interface`, `extract_base_class`, and `extract_method` are **not on the default whitelist at all** since DEC-0050, so `Tool '<x>' not found` is expected and never becomes a call — hand-edit, or ask the user whether to restart as `Tools\Start-RiderMcp.ps1 -AllowedTools '*'` (which also exposes shell and file-write tools). Where they are exposed they still fail on this C++ (type or method not found, or the line range rejected). Retrying them is not a fix.
2. **Trust the success signal — never verify, never build.** On success the response's `touched`/`affects`/`files` counts **are** the confirmation. Do **not** re-read files, re-run `grep`/`rg`, diff the tree, or run the build/tests "to catch fallout" — a build never changes an already-applied refactor, it only burns tokens. Build or test **only** if the user explicitly asked. The one thing worth surfacing: a count of **1** for a type/method/property/field/namespace (declaration only, no callers).
3. **Don't retry blindly** — change an argument between calls. Flags are camelCase; pass real values or omit optional ones (no `""`/`"/"`/fake-path placeholders), and copy paths and names verbatim from `search_*`. (`get_symbol_info` returns empty documentation for C++ here, so it is not a source of names.)
4. **Library / external symbols can't be refactored** — surface to the user; the change must be made upstream.

## Conflicts, ambiguity, limits

A non-empty `conflicts` list means **no files changed** (except `reorganize_namespaces`, whose conflicts are advisory and still apply). An `ambiguous`/`candidates` list means the name matched several symbols — narrow it (`Type.Member`, or the current overload types). Full conflict-kind handling, escalation thresholds, and known gaps (strings/comments, `<see cref>`, file-not-moved, call-site reflow) are in [reference/conflicts.md](reference/conflicts.md) — read it only when a response actually contains conflicts.
