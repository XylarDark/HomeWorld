---
name: navigating-code
description: Use when finding callers or implementations of a C++ symbol in Rider. Do not use for plain text or file names.
allowed-tools: execute_tool
metadata:
  author: JetBrains
---

# Navigating Code

Rider answers "who uses this?" and "who implements this?" from its reference index. One call replaces a grep-and-read loop, and it skips same-name symbols, comments and strings that grep returns.

## Pick the tool

| Question | Tool | Required flags |
|---|---|---|
| Where is a symbol declared? | `search_symbol` | `--q` |
| Who uses / calls / reads / writes this symbol? | `find_usages` | `--filePath` + `--symbolName` or `--line` |
| Which .NET classes implement this interface or derive from this class? | `find_implementations` | `--filePath` + `--symbolName` or `--line` |
| Which .NET members override or implement this virtual, abstract or interface member? | `find_implementations` | `--filePath` + `--symbolName` or `--line` |
| Where does this text occur (strings, comments, config)? | `search_text` / `search_regex` | `--q` |

Call through `execute_tool`: the first token is the tool name, then `--flag value` pairs.

```
execute_tool(command="find_usages --filePath API/Services/OrderService.cs --symbolName OrderService.Submit")
execute_tool(command="find_implementations --filePath Domain/IPaymentGateway.cs --symbolName IPaymentGateway")
```

If your client lists the Rider tools directly, call `find_usages` and `find_implementations` by name with the same arguments.

## This build (HomeWorld) — read before using the table

**`find_usages` and `find_implementations` do not exist in this build.** Verified 2026-10-15 by
listing every tool the server can expose with its tool whitelist disabled: the maximum surface is
86 tools and neither name is among them. Waiting, retrying, or re-reading this file will not make
them appear.

Use instead:

| You want | Use here |
|---|---|
| Where is a symbol declared? | `search_symbol --q <Name>` (works; returns the file paths) |
| Where is a symbol used? | `search_symbol` for the declaration, then `search_text`/`search_regex` for the identifier. The IDE reference index is not reachable, so this is a text answer - say so. |
| Every reference to a symbol, resolving aliases/macros (C++) | Run `.\Tools\Find-RiderUsages.ps1 -FilePath <header> -SymbolName <Member>` — it wraps the only tool that answers this and always sends `--preview true`, so it cannot delete. Under it: `safe_delete --filePath <header> --symbolName <Member> --preview true` on the default whitelist. Preview writes nothing (`applied: false`, `deleted: []`) and `conflicts[]` names the files that reference the member. Verified: `bCloudDescentActive` returned 7 conflicts in the `.h` and `.cpp` in 0.9 s. It does not return line numbers. **Never call `safe_delete` without `--preview true`** — without it this tool deletes. The richer report is `rename_refactoring --preview true` (`affects.files` / `affects.callSites`), and that tool exists only when the whitelist is disabled (`-AllowedTools '*'`); see `Tools/Start-RiderMcp.ps1`. |
| Which Blueprints inherit a C++ class? | `get_class_hierarchy --baseClass <CppClass>`. Verified: `AHomeWorldCharacter` returned `BP_HomeWorldCharacter_C`. Or `search_assets --baseClass <CppClass>`. **Asset inheritance, not a C++ subclass tree** - for C++ subclasses, grep `: public <Type>`. |

Verified working on this project: `search_symbol`, `search_file` (its `q` is a **glob**),
`search_text`, `search_regex`, `get_class_hierarchy`, `search_assets`, `get_file_problems`,
`get_project_problems`, `lint_files` (~14s for one header, so batch deliberately). `search_assets
--query BP_` matched nothing while `--baseClass` worked, so prefer `--baseClass`. The Unreal Editor
bridge tools (`ue_status`, `ue_health`, `ue_get_logs`) answer `{"connected":false}` unless the
editor is running with RiderLink. Every call needs `rootFolder=C:/dev/HomeWorld`.

Canonical reference for this build: `docs/tools/Rider_MCP_for_UE_Games.md`.

## Identify the symbol

- **You know the declaring file:** pass `--filePath` and `--symbolName` as `Name` or `Type.Member`.
- **You do not know the file:** call `search_symbol` first, then pass its `filePath`.
- **Overloads, or a symbol you see at a call site:** pass `--filePath` and `--line` of that declaration or usage, plus `--symbolName` (or `--column`) to pick the symbol on the line. This works in any file that mentions the symbol.
- **C++:** pass `--line` together with `--symbolName` as `Type::Member`. The qualifier picks the member on the line, such as the constructor in `AMyActor::AMyActor()`. Without `--line`, a qualified C++ name does not resolve. `find_implementations` does not support C++ yet, so it returns an error for a C++ symbol.

## Read the result

- `find_usages` returns `{symbol, declarations, files: [{file, usages: [{line, column, text, kinds, member}]}], total, more, note}`.
  `text` is the source line, so do not open the file only to see the call. `kinds` tells how the symbol is used (for example `Invocation`, `Read`, `Write`). `member` names the caller.
- `find_implementations` returns `{symbol, declarations, implementations: [{symbol, file, line, column}], total, more, note}`. The list is recursive: it holds indirect inheritors and overrides too.
- A `note` means that the IDE is still indexing, so the list can be incomplete. Say so, or retry later.
- `more=true` means that `--limit` (default 100) cut the list. Narrow with `--paths '["src/Api/**"]'` before you raise the limit.

## Rules

1. **Prefer these tools to grep for identifiers.** Grep finds text, not references: it misses usages through aliases, `nameof`, XAML/Razor bindings and C++ macros, and it adds same-name symbols.
2. **Fix the input, then retry.** "not declared in" means the file does not declare the symbol: pass the declaring file from `search_symbol`, or pass `--line`. "has N overloads" lists the line of each overload: pass `--line` of the one you mean. Do not retry with the same arguments.
3. **Fall back to text search only when the tool cannot answer.** The cases are a timeout (the tools stop after 60 seconds), a file outside the solution, a language that Rider does not parse, and `find_implementations` on a C++ symbol. Then say that the result comes from text search.
4. **Ask about several symbols at once.** When you need the usages or implementations of several symbols, issue all the calls in one turn, not one call per turn.
5. **Use the counts.** `total` answers "how many callers?" without reading the files. Read a usage only when you need the code around it.
