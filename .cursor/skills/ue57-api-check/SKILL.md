---
name: ue57-api-check
description: Before adding or changing C++ or Python that uses UE 5.7–sensitive APIs (FindObject, FPaths, image utils, collision profiles, get_actor_bounds, AnimBP factory, AssetRegistry). Check pitfalls table and KNOWN_ERRORS, use replacements, then build/test.
---

# UE 5.7 API check

Use when adding or modifying code that touches APIs that changed or were removed in UE 5.7. Avoid repeating documented pitfalls.

## When to use

- Adding or changing **C++** that uses: `FindObject`, `ANY_PACKAGE`, `FPaths::IsRelativePath` / `IsRelative`, `UCollisionProfile::` constants, `FImageUtils::CompressImageArray`, `SCENE_QUERY_STAT`, or global names that might collide with engine headers (e.g. `BufferSize`).
- Adding or changing **Python** Editor scripts that use: `get_actor_bounds`, AnimBP factory lookup, `FAssetRegistryModule`, or other Unreal Python APIs noted in KNOWN_ERRORS.

## Instructions

1. **Check the pitfalls table** — Open [.cursor/rules/unreal-cpp.mdc](../../.cursor/rules/unreal-cpp.mdc) and read the "UE 5.7 API pitfalls" table. Use the replacement column (e.g. `nullptr` instead of `ANY_PACKAGE`, `FPaths::IsRelative(...)` instead of `IsRelativePath(...)`).

2. **Check KNOWN_ERRORS** — Open [docs/KNOWN_ERRORS.md](../../docs/KNOWN_ERRORS.md) and search for the API or area (e.g. "get_actor_bounds", "AnimBlueprintFactory", "PCGComponent", "UCollisionProfile"). Apply the documented fix.

3. **Apply replacements** — In C++, use `FName("Pawn")` or `FName("OverlapAllDynamic")` instead of removed `UCollisionProfile::` constants; in Python, use `origin, extent = actor.get_actor_bounds(False)` (tuple return). For AnimBP factory, try multiple names: `AnimBlueprintFactory`, `AnimationBlueprintFactory`, `AnimBlueprint_Factory`.

4. **Build and verify** — Run `Build-HomeWorld.bat`, check `Build-HomeWorld.log`. For Python changes, run the script in the Editor or via MCP and confirm no TypeError or missing-attribute errors.

## References

- [docs/UE57_TECH.md](../../docs/UE57_TECH.md) — UE 5.7 tech entry point, canonical examples, upgrade path
- [.cursor/rules/unreal-cpp.mdc](../../.cursor/rules/unreal-cpp.mdc) — pitfalls table
- [docs/KNOWN_ERRORS.md](../../docs/KNOWN_ERRORS.md) — full list of recorded errors and fixes
- [.cursor/rules/12-python.mdc](../../.cursor/rules/12-python.mdc) — UE 5.7 Python API changes
