---
name: ue58-api-check
description: Before adding or changing C++ or Python that uses UE 5.8–sensitive APIs (FindObject, FPaths, image utils, collision profiles, get_actor_bounds, AnimBP factory, AssetRegistry, Mass plugins). Check pitfalls table and KNOWN_ERRORS, use replacements, then Safe-Build/test.
---

# UE 5.8 API check

Use when adding or modifying code that touches APIs that changed across UE 5.7→5.8 or that were already sensitive in 5.7. Avoid repeating documented pitfalls.

## When to use

- Adding or changing **C++** that uses: `FindObject`, `ANY_PACKAGE`, `FPaths::IsRelativePath` / `IsRelative`, `UCollisionProfile::` constants, `FImageUtils::CompressImageArray`, `SCENE_QUERY_STAT`, or global names that might collide with engine headers (e.g. `BufferSize`).
- Adding or changing **Python** Editor scripts that use: `get_actor_bounds`, AnimBP factory lookup, `FAssetRegistryModule`, or other Unreal Python APIs noted in KNOWN_ERRORS.
- Enabling **Mass** plugins — do **not** list `MassEntity` in `.uproject` on 5.8 (plugin removed; use MassGameplay / MassAI).

## Instructions

1. **Check the pitfalls table** — Open [.cursor/rules/unreal-cpp.mdc](../../.cursor/rules/unreal-cpp.mdc) and read the API pitfalls table (5.7 rows remain relevant; add 5.8 notes from KNOWN_ERRORS).
2. **Check KNOWN_ERRORS** — Open [docs/KNOWN_ERRORS.md](../../docs/KNOWN_ERRORS.md) and search for the API or “UE 5.8”.
3. **Apply replacements** — Same 5.7 replacements unless a 5.8 entry says otherwise.
4. **Build and verify** — Run `.\Tools\Safe-Build.ps1` (engine default `UE_5.8`). For Python, run via MCP `execute_python_script` and confirm no TypeError.

## References

- [docs/UE/UE58_TECH.md](../../docs/UE/UE58_TECH.md) — UE 5.8 tech entry point
- [Docs/22_UE58_UPGRADE.md](../../Docs/22_UE58_UPGRADE.md) — upgrade track
- [.cursor/rules/unreal-cpp.mdc](../../.cursor/rules/unreal-cpp.mdc)
- [docs/KNOWN_ERRORS.md](../../docs/KNOWN_ERRORS.md)
- Legacy skill: [ue57-api-check](../ue57-api-check/SKILL.md)
