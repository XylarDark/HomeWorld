# HomeWorld – Conventions

## Programmatic by default

HomeWorld is developed **programmatically by default**: maximize C++ (and Python automation); minimize Blueprint logic so behavior is in code, versionable, and reviewable.

- **C++** is used for:
  - Gameplay systems (movement, input, camera, combat, building logic)
  - **Abilities and GAS logic** — implement in C++ ability subclasses (e.g. `UHomeWorldInteractAbility`); reparent GA_* Blueprints to these classes so no Blueprint graph wiring is needed (use `reparent_ga_*_to_cpp.py`-style scripts where applicable)
  - Core logic and reusable behavior
  - Anything that should be consistent across maps and Blueprint children

- **Blueprint** is used for:
  - Content (meshes, materials, level placement)
  - Designer-facing overrides and one-off data (e.g. asset references on C++ class defaults)
  - Subclassing C++ classes **only to assign assets** (e.g. character mesh, input assets); avoid adding logic in the Blueprint graph when a C++ subclass can do it

**Default for new abilities:** Implement the ability in C++ (subclass of `UHomeWorldGameplayAbility` or a dedicated C++ ability class). Create or reparent the corresponding GA_* Blueprint to that C++ class so the Blueprint remains data-only (no Event Graph logic). Use Blueprint graph wiring only when C++ or reparenting is not feasible.

When adding new features, prefer C++ for the core implementation; use Blueprint for data and content integration, not for control flow or gameplay logic.

**Debug instrumentation and log-driven validation:** When implementing new features, add minimal debug instrumentation (entry/exit, key branches, critical values, and for user-triggered actions: trigger + outcome) by default. Every feature must be **validatable from logs** (Output Log, log files, or test output) so you can confirm it works without prompting for logging. See `.cursor/rules/16-feature-debug-instrumentation.mdc`.

---

## MCP-first when Editor is running

When the Unreal Editor is open and the MCP server is connected to Cursor:

1. **Use MCP tools first** for Editor tasks (spawning actors, setting properties, creating assets, configuring Blueprints).
2. **Save repeatable workflows** as Python scripts in `Content/Python/` alongside MCP usage, so operations can be re-run without MCP.
3. When MCP and Python cannot accomplish a step, **log it to [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md)** with a suggested approach for future automation; do not document manual steps for the user (project is fully autonomous). See `.cursor/rules/20-full-automation-no-manual-steps.mdc`.

See [MCP_SETUP.md](MCP_SETUP.md) for installation and `.cursor/rules/09-mcp-workflow.mdc` for full priority rules. For PIE pre-demo validation and vertical slice checks, see [VERTICAL_SLICE_CHECKLIST](workflow/VERTICAL_SLICE_CHECKLIST.md) §3. Current cycle status: [CURRENT_TASK_LIST](workflow/CURRENT_TASK_LIST.md) and [KNOWN_ERRORS.md](KNOWN_ERRORS.md) (next priority / freshness).

**Automation — variables with no access:** When adding automation for Editor/engine features (Python, MCP), follow the "variables no access" procedure: identify required settings from tutorials/docs, verify automation access, document no-access items and manual steps in KNOWN_ERRORS or a feature doc (e.g. [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md)). See `.cursor/rules/automation-standards.mdc`.

---

## Code-first checklist

- **New systems:** Implement in C++; expose designer-facing APIs with `UFUNCTION(BlueprintCallable)` or `BlueprintNativeEvent` where designers need to drive or extend behavior from Blueprint.
- **New abilities:** Implement in a C++ ability class (e.g. `UHomeWorldInteractAbility`); reparent the GA_* Blueprint to that class so the Blueprint has no graph logic. Do not default to "wire it in the Blueprint graph."
- **C++ systems (current):** Movement, input, camera, game mode, default pawn. GAS: `AHomeWorldCharacter` owns `UAbilitySystemComponent` and `UHomeWorldAttributeSet`; base `UHomeWorldGameplayAbility`; dedicated C++ abilities (e.g. `UHomeWorldInteractAbility`) for Interact. New attributes go in `UHomeWorldAttributeSet` (or a second attribute set if needed).
- **Blueprint:** Content (meshes, materials, input assets), level layout, and Blueprint children of C++ classes for **asset assignment only** (e.g. character mesh, IA_Move/IA_Look/IMC_Default). Avoid adding gameplay logic in Blueprint when it can live in C++.

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

---

## Design rules (day/night, death)

- **No death during the day:** There are no mechanics to die during the day; the day phase is safe in that sense. Death mechanics apply to night (astral) combat and to succession (permanent death when no heirs). See [PROTOTYPE_SCOPE](workflow/PROTOTYPE_SCOPE.md) § Day/night and astral (MVP scope) and [VISION](workflow/VISION.md) § Day and night: physical and spiritual worlds.

### Physical vs spiritual goods (T7)

Per [VISION](workflow/VISION.md) **Day and night: physical and spiritual worlds**:

- **Physical goods:** Materials, food, and supplies collected **by day** (harvest, resource piles, yield nodes). Stored in `UHomeWorldInventorySubsystem` (resource types and counts). Day harvest → physical; use `hw.Goods` or harvest in PIE to see physical total.
- **Spiritual (artefacts/power):** Collected **at night** (Phase 2) via overlap on spiritual collectibles or night-only interactions. Stored in `AHomeWorldPlayerState::SpiritualPowerCollected`. Night collect → spiritual; use `hw.Goods` or `hw.SpiritualPower` to see spiritual total.
- **Rule:** One counter per realm: physical = inventory total (sum of all resource amounts); spiritual = `GetSpiritualPowerCollected()`. Both observable in PIE via console command `hw.Goods`.
