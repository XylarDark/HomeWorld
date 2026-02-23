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

### UnrealMCP plugin: ANY_PACKAGE removed in UE 5.7
- **Error:** `error C2065: 'ANY_PACKAGE': undeclared identifier` in UnrealMCPBlueprintCommands.cpp and UnrealMCPBlueprintNodeCommands.cpp (9 occurrences).
- **Cause:** `ANY_PACKAGE` macro was deprecated in UE 5.1 and fully removed in UE 5.7. The unreal-mcp plugin (chongdashu/unreal-mcp) targets UE 5.5.
- **Fix:** Replace all `ANY_PACKAGE` with `nullptr` in `FindObject<UClass>()` calls.
- **Context:** 2026-02, UnrealMCP plugin build, UE 5.7 migration.

### UnrealMCP plugin: CompressImageArray deprecated in UE 5.7
- **Error:** `error C2664: cannot convert argument 4 from 'TArray<uint8>' to 'TArray<uint8, FDefaultAllocator64>&'` in UnrealMCPEditorCommands.cpp.
- **Cause:** `FImageUtils::CompressImageArray` deprecated; replaced by `PNGCompressImageArray` which requires `TArray64<uint8>`.
- **Fix:** Replace `CompressImageArray` with `PNGCompressImageArray` and change `TArray<uint8>` to `TArray64<uint8>`.
- **Context:** 2026-02, UnrealMCP plugin build, UE 5.7 migration.

### UnrealMCP plugin: BufferSize name collision in UE 5.7
- **Error:** `error C4459: declaration of 'BufferSize' hides global declaration` in MCPServerRunnable.cpp (treated as error in UE 5.7).
- **Cause:** Global `const int32 BufferSize = 8192` in plugin code shadows a local in UE's `StringConv.h` header.
- **Fix:** Rename to `static constexpr int32 MCPRecvBufferSize = 8192`.
- **Context:** 2026-02, UnrealMCP plugin build, UE 5.7 migration.
