# Homestead plateau spawn — ref images for GUI automation (optional)

Used by [homestead_plateau_from_ui.py](../../homestead_plateau_from_ui.py) to set the Player Start (or spawn actor) **Location** in the Details panel from config. **Preferred:** Use the config-driven script [place_homestead_spawn.py](../../place_homestead_spawn.py) (runs in Editor, no ref images); it places or moves the Player Start at coordinates from `homestead_spawn_config.json` (or `planetoid_map_config.json`). Use the GUI script only when you want to set position via the Details panel (e.g. when Python cannot set actor transform).

## Capture

From project root with the **planetoid level** open and **Player Start** selected in the Outliner:

1. In Details, expand **Transform** and ensure **Location** (X, Y, Z) is visible.
2. Run: `py Content/Python/gui_automation/capture_homestead_refs.py`
3. Capture the **Location** field (one ref that includes the X field or the whole Transform section). Save to `refs/homestead/`.
4. Crop to the Location X field (or the first numeric field) for typing coordinates.

See [docs/REF_IMAGES_SETUP_TUTORIAL.md](../../../../docs/REF_IMAGES_SETUP_TUTORIAL.md) §4.8 and [MANUAL_EDITOR_TUTORIAL.md](../../../../docs/MANUAL_EDITOR_TUTORIAL.md) §9.
