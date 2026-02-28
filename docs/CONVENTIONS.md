# HomeWorld – Conventions

## Programmatic by default

HomeWorld is developed **programmatically by default**: as much work as possible is done in C++ so that behavior is in code, versionable, and reviewable.

- **C++** is used for:
  - Gameplay systems (movement, input, camera, combat, building logic)
  - Core logic and reusable behavior
  - Anything that should be consistent across maps and Blueprint children

- **Blueprint** is used for:
  - Content (meshes, materials, level placement)
  - Designer-facing overrides and one-off behavior
  - Subclassing C++ classes to assign assets (e.g. character mesh, input assets)

When adding new features, prefer C++ for the core implementation; use Blueprint for data, overrides, and content integration.

**Debug instrumentation:** When implementing new features, add minimal debug instrumentation (entry/exit, key branches, critical values) by default so that when something goes wrong we can get runtime evidence quickly. See `.cursor/rules/16-feature-debug-instrumentation.mdc`.

---

## MCP-first when Editor is running

When the Unreal Editor is open and the MCP server is connected to Cursor:

1. **Use MCP tools first** for Editor tasks (spawning actors, setting properties, creating assets, configuring Blueprints).
2. **Save repeatable workflows** as Python scripts in `Content/Python/` alongside MCP usage, so operations can be re-run without MCP.
3. **Fall back to manual instructions** only when MCP and Python cannot accomplish the task (e.g. AnimGraph state machine editing).

See [MCP_SETUP.md](MCP_SETUP.md) for installation and `.cursor/rules/09-mcp-workflow.mdc` for full priority rules.

**Automation — variables with no access:** When adding automation for Editor/engine features (Python, MCP), follow the "variables no access" procedure: identify required settings from tutorials/docs, verify automation access, document no-access items and manual steps in KNOWN_ERRORS or a feature doc (e.g. [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md)). See `.cursor/rules/automation-standards.mdc`.

---

## Code-first checklist

- **New systems:** Implement in C++; expose designer-facing APIs with `UFUNCTION(BlueprintCallable)` or `BlueprintNativeEvent` where designers need to drive or extend behavior from Blueprint.
- **C++ systems (current):** Movement, input, camera, game mode, default pawn. GAS: `AHomeWorldCharacter` owns `UAbilitySystemComponent` and `UHomeWorldAttributeSet`; base ability class `UHomeWorldGameplayAbility`. New attributes go in `UHomeWorldAttributeSet` (or a second attribute set if needed).
- **Blueprint:** Content (meshes, materials, input assets), level layout, one-off logic, and Blueprint children of C++ classes for asset assignment (e.g. character mesh, IA_Move/IA_Look/IMC_Default).

---

## Input setup (Enhanced Input)

The default pawn is **AHomeWorldCharacter** (C++). Movement and look are driven by Enhanced Input.

**Automated setup:** Running `bootstrap_project.py` (via MCP or Editor Python console) creates all required input assets automatically:
- **IA_Move** (Value Type: Axis2D) — for WASD
- **IA_Look** (Value Type: Axis2D) — for mouse
- **IMC_Default** — maps W/S/A/D to Move and Mouse XY to Look

These are then assigned to the default pawn by `setup_character_blueprint.py` (called by the bootstrap).

**Manual creation (only if bootstrap hasn't run):** Create the assets above in the Editor and assign **MoveAction**, **LookAction**, and **DefaultMappingContext** on the default pawn (either on `AHomeWorldCharacter` class defaults or on a Blueprint child).

If these are not set, the character will spawn and the camera will work, but movement and look input will do nothing.

---

## Camera & controls

The default pawn uses a **third-person** setup:

- **Camera:** A spring arm and follow camera are attached to the character capsule. The camera orbits with the mouse (Look) and stays behind the character. Pitch is clamped so the camera does not flip.
- **Movement:** Movement is **camera-relative** — W moves toward where the camera looks, and the character orients to movement direction.
- **Input:** IA_Move, IA_Look, and IMC_Default are created by `bootstrap_project.py` and assigned to the default pawn. If running manually, see the Input setup section above. Camera settings (arm length, FOV, pitch limits, sensitivity) are exposed on the character for tuning.
