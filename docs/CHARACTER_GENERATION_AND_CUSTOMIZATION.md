# Character generation and customization

**Purpose:** How generated and static characters coexist, how to run the main menu and character flow, and how to enable the main menu as the game start.

---

## Generated vs static characters

- **Static:** Default pawn (BP_HomeWorldCharacter), family/NPCs. Mesh and skeleton from project content; same C++ pawn class.
- **Generated:** Player-supplied art (NFT or any image) â†’ pipeline (e.g. Meshy 2Dâ†’3D, VRM4U) â†’ rigged mesh â†’ same pawn class with different Skeletal Mesh. Body types are standardized (one target skeleton); face/head varies. See [MILADY_IMPORT_ROADMAP.md](tasks/MILADY_IMPORT_ROADMAP.md) for the stylized pipeline.

**In game:** Character source is `Static` or `Generated`. Spawn uses the same pawn class; for generated players the mesh (and optional material) come from the generated asset. Store which generated character is selected in SaveGame or profile.

---

## Main menu and character screen (setup)

### 1. Create MainMenu map

Run in Editor: **Tools â†’ Execute Python Script** â†’ `Content/Python/ensure_main_menu_map.py`.

- If a template is set in `Content/Python/main_menu_config.json` (`template_level_path`), the script creates `/Game/HomeWorld/Maps/MainMenu` from it.
- Otherwise, create manually: **File â†’ New Level â†’ Empty Level** (or Basic), then **Save As** â†’ `Content/HomeWorld/Maps/MainMenu`.

### 2. Create UI folder and widgets

Run: `Content/Python/ensure_ui_folders.py` (creates `/Game/HomeWorld/UI`).

Both scripts are idempotent: they check before create and log "already exists" or skip when the map/folder is present.

**Create-if-missing: WBP_MainMenu** — Run **Tools → Execute Python Script** → `Content/Python/ensure_wbp_main_menu.py` (or via MCP `execute_python_script("ensure_wbp_main_menu.py")`). The script is idempotent: it creates the widget in `/Game/HomeWorld/UI` with parent **HomeWorldMainMenuWidget** if the Editor provides a Widget Blueprint factory; otherwise it logs and you create manually. If the widget was created, open it and add a **Canvas Panel**, **Vertical Box**, and four **Buttons** (Play, Character, Options, Quit); bind each **On Clicked** to **OnPlayClicked**, **OnCharacterClicked**, **OnOptionsClicked**, **OnQuitClicked**. If the script did not create the asset: in **Content Browser** go to `/Game/HomeWorld/UI` → right‑click → **User Interface → Widget Blueprint**, name it `WBP_MainMenu`, then **Class Settings** → Parent Class: **HomeWorldMainMenuWidget**, and add the four buttons and bindings as above. Set `MainMenuWidgetClassPath` in DefaultGame.ini (step 2 below). MCP create_umg_widget_blueprint and add_button_to_widget currently fail (parameter naming); see [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md).

Then in the Editor (full steps):

1. **WBP_MainMenu**  
   - **Content Browser** â†’ Rightâ€‘click in `/Game/HomeWorld/UI` â†’ **User Interface â†’ Widget Blueprint**.  
   - Name it `WBP_MainMenu`.  
   - Open it â†’ **Class Settings** â†’ Parent Class: **HomeWorldMainMenuWidget**.  
   - In the Designer: add a **Canvas Panel**, then a **Vertical Box** with four **Buttons**: Play, Character, Options, Quit.  
   - For each button, in **On Clicked** call the matching C++ method: **OnPlayClicked**, **OnCharacterClicked**, **OnOptionsClicked**, **OnQuitClicked**.

2. **Widget class in config**  
   In `Config/DefaultGame.ini`, under `[/Script/HomeWorld.HomeWorldGameInstance]`, set:
   ```ini
   MainMenuWidgetClassPath=/Game/HomeWorld/UI/WBP_MainMenu.WBP_MainMenu_C
   ```
   (This is already set if you use the default path.)

3. **Start game on main menu**  
   In `Config/DefaultEngine.ini`, under `[/Script/EngineSettings.GameMapsSettings]`:
   - Set `GameDefaultMap=/Game/HomeWorld/Maps/MainMenu.MainMenu` (uncomment the MainMenu line and comment or remove the Homestead line).
   - Ensure `GameInstanceClass=/Script/HomeWorld.HomeWorldGameInstance` is set.

After this, launching the game opens the MainMenu map and the main menu widget (Play, Character, Options, Quit). **Play** loads the game map (default: DemoMap).

**First-launch flow (List 55 — how to verify):** (1) **Ensure MainMenu map exists** — Run `Content/Python/ensure_main_menu_map.py` in Editor (Tools → Execute Python Script or MCP `execute_python_script("ensure_main_menu_map.py")`). The script is idempotent; it creates `/Game/HomeWorld/Maps/MainMenu` from the template in `Content/Python/main_menu_config.json` (default template: Homestead) if the map is missing. If the map is missing and you launch the game, the engine may fail to open. (2) **Config** — `Config/DefaultEngine.ini` under `[/Script/EngineSettings.GameMapsSettings]` has `GameDefaultMap=/Game/HomeWorld/Maps/MainMenu.MainMenu` and `EditorStartupMap` set to MainMenu so the game (and Editor) start on the main menu. (3) **Verify:** Launch the game (packaged exe or PIE). You should see the main menu widget (Play, Character, Options, Quit). Click **Play**; the playable level (DemoMap) should load. Success = MainMenu → Play → DemoMap.

**Play → game map (code path):** WBP_MainMenu Play button **On Clicked** → `UHomeWorldMainMenuWidget::OnPlayClicked()` → `GetHomeWorldGameInstance()` → `UHomeWorldGameInstance::OpenGameMap()`. The map loaded is `GameMapPath` (default in C++: `/Game/HomeWorld/Maps/DemoMap.DemoMap` if not set); overridable in Blueprint (BP_GameInstance) or config. Success: launching from MainMenu and clicking Play opens the playable level (DemoMap or the configured map).

**Character → character screen (code path):** WBP_MainMenu Character button **On Clicked** → `UHomeWorldMainMenuWidget::OnCharacterClicked()` → `GetHomeWorldGameInstance()` → `UHomeWorldGameInstance::OpenCharacterScreen()`. The game instance creates the widget from `CharacterScreenWidgetClassPath` (default in `Config/DefaultGame.ini`: `/Game/HomeWorld/UI/WBP_CharacterCreate.WBP_CharacterCreate_C`) and adds it to the viewport. For the screen to appear, **WBP_CharacterCreate** must exist in `/Game/HomeWorld/UI` with Parent Class **HomeWorldCharacterCustomizeWidget** (see §3 below). Success: clicking Character on the main menu opens the character customization screen.

**Options and Quit (code path):** **Options** — `UHomeWorldMainMenuWidget::OnOptionsClicked()` is a stub (logs to Output Log; override in Blueprint to show an options panel). **Quit** — `OnQuitClicked()` runs the engine console command `quit`, which requests application exit. WBP_MainMenu Options and Quit buttons should be bound to **OnOptionsClicked** and **OnQuitClicked** respectively.

**Pre-demo verification entry point (one doc):** [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md) § Pre-demo verification is the single doc that links (1) the step-by-step run sequence [VERTICAL_SLICE_CHECKLIST §3](workflow/VERTICAL_SLICE_CHECKLIST.md) and (2) the `hw.*` command reference (same doc). Open CONSOLE_COMMANDS for both.

### Main menu flow checklist

Use this checklist to verify the main menu flow (List 55 / MVP full scope) without re-reading the full doc:

1. **Game starts on MainMenu** — Launch the game (or PIE with MainMenu as start map). Confirm the main menu widget appears (Play, Character, Options, Quit).
2. **Play loads game map** — Click **Play**. The playable level (default: DemoMap) should load.
3. **Character opens character screen** — From the main menu, click **Character**. The character customization screen (WBP_CharacterCreate) should open.
4. **Confirm (character screen)** — On the character screen, click **Confirm**. Profile is saved (e.g. to Saved/CharacterCustomization.json) and the character screen closes; main menu remains.
5. **Back from character screen** — On the character screen, click **Back**. The character screen closes and the main menu is shown again.
6. **Options** — Click **Options**. Stub: log in Output Log; no panel yet (override in Blueprint for options screen).
7. **Quit** — Click **Quit**. The game (or PIE) should exit.

**Optional PIE verification:** Run from Editor: **Play** (PIE). If the game is configured to start on MainMenu (GameDefaultMap in DefaultEngine.ini), the same steps apply. For the full pre-demo run and console commands, see [VERTICAL_SLICE_CHECKLIST §3](workflow/VERTICAL_SLICE_CHECKLIST.md) and [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md).

### 3. Character creation/customization screen (WBP_CharacterCreate)

Create a second Widget Blueprint `WBP_CharacterCreate` in `/Game/HomeWorld/UI` (Parent Class: **HomeWorldCharacterCustomizeWidget**):

- Placeholder **Upload / Scan** button (and optional URL field).
- Placeholder **Face sliders** (or â€œFace customizationâ€ area).
- **Confirm** button.
- **Back** button.

**Confirm button (stub):** In WBP_CharacterCreate, bind the Confirm button **On Clicked** to **OnConfirmClicked**. The C++ implementation logs to Output Log (`HomeWorld: Character Confirm clicked; saving profile and closing.`), calls `UHomeWorldCharacterCustomizationSubsystem::SaveCustomizationToProfile()` if the subsystem is present (writes to `Saved/CharacterCustomization.json`), then removes the widget. The flow is testable without the full Phase C/E generation pipeline: Main menu → Character → Confirm closes the screen and optionally persists current morph values; full "image → character" and face-param backend is deferred.

**Back button:** Bind the Back button **On Clicked** to **OnBackClicked**. The C++ implementation removes the character screen widget (no save); the main menu remains visible underneath.

The main menu **Character** button is wired in C++: **OnCharacterClicked** calls `GetHomeWorldGameInstance()->OpenCharacterScreen()`, which creates the widget from `CharacterScreenWidgetClassPath` (see DefaultGame.ini) and adds it to the viewport. Ensure WBP_MainMenu Character button **On Clicked** is bound to **OnCharacterClicked** (no Blueprint graph needed if using the C++ base class). If WBP_CharacterCreate does not exist yet: in Content Browser under `/Game/HomeWorld/UI`, create **User Interface → Widget Blueprint**, name it `WBP_CharacterCreate`, then set **Class Settings → Parent Class** to **HomeWorldCharacterCustomizeWidget**. Backend for â€œimage â†’ characterâ€ and face params is Phase C/E.

---

## Face generation (stylized pipeline)

- **Input:** Any artwork (upload/URL or NFT metadata image). Reuse `DownloadMiladyPNG` or add generic `DownloadImageForCharacter(URL Or Path)`.
- **Body standardized:** One target skeleton; all generated characters retargeted to it so only head/face geometry differs. Optionally use a â€œface onlyâ€ generation step and attach to a standard body.
- **Face quality:** Use a face-forward crop as Meshy input, or a portraitâ†’3D face service, then composite in UE. Define a standard head topology and morph targets for consistency.

See [MILADY_IMPORT_ROADMAP.md](tasks/MILADY_IMPORT_ROADMAP.md) Phases 3â€“5 (PNG â†’ Meshy â†’ VRM4U).

---

## Standardized body and face

**Body:** Use a **single target skeleton** (e.g. VRM4Uâ€™s standard or a project â€œstylizedâ€ skeleton) so all generated characters share one rig and one animation set. Meshy (or similar) can output a consistent pose/rig; otherwise add a **conform step** (retarget to the project skeleton) so body proportions are fixed and only head/face geometry varies.

**Option A (full character):** Meshy â€œcharacterâ€ preset outputs consistent body proportions; retarget all imports to the project skeleton so only the head/face mesh differs.

**Option B (face only):** Separate â€œbody templateâ€ (one GLB with standard body) and â€œface onlyâ€ generation: run Meshy (or a face API) on a cropped face/portrait, then in UE attach or blend the generated face to the body (face submesh + material, or morph targets on a standard head). More work but strict body consistency.

**Face consistency:** Define a **standard head/face topology** (e.g. one base head mesh with blend shapes). Post-process Meshy output to project face vertices to this topology or drive morphs from a small set of parameters (width, nose, eyes) so all faces share the same rig and animation.

**API:** `UHomeWorldMiladyImportSubsystem::StartCharacterFromImage(ImageURLOrPath)` starts the flow (download if URL, then Meshy/VRM4U stubs). `LastGeneratedCharacterMeshPath` holds the resulting mesh asset path once VRM4U is integrated. `UHomeWorldNFTSubsystem::DownloadImageForCharacter(ImageURL)` downloads any image to `Saved/CharacterCache/character.png`.

---

## Post-generation face customization

- **Morph targets:** If the generated mesh has morph targets, expose them in the character customization UI; store values in SaveGame and apply at load.
- **Parametric preset:** Define 5â€“10 parameters (e.g. face roundness, eye size); blend pre-made heads or drive morphs from these params; persist in SaveGame.
- **Technical:** `UHomeWorldCharacterCustomizationSubsystem`: call `SetCustomizationTarget(Pawn->GetMesh())` when opening the screen, then `GetMorphTargetNames()`, `SetMorphTargetValue(Name, Value)`, `SaveCustomizationToProfile()`, `LoadCustomizationFromProfile()`. Profile is saved to `Saved/CharacterCustomization.json`. On Confirm, the widget calls `SaveCustomizationToProfile()` then removes itself.

---

## Files and content paths

| Path | Purpose |
|------|--------|
| `/Game/HomeWorld/Maps/MainMenu` | Main menu level; game can start here when GameDefaultMap is set. |
| `/Game/HomeWorld/UI/` | WBP_MainMenu, WBP_CharacterCreate. |
| `Source/HomeWorld/HomeWorldGameInstance` | Game instance; OpenGameMap(), IsMainMenuMap(), MainMenuWidgetClass. |
| `Source/HomeWorld/HomeWorldMainMenuWidget` | Base class for WBP_MainMenu; OnPlayClicked, OnCharacterClicked, OnOptionsClicked, OnQuitClicked. |
| `Source/HomeWorld/HomeWorldCharacterCustomizeWidget` | Base class for WBP_CharacterCreate; OnConfirmClicked (saves profile), OnBackClicked. |
| `Source/HomeWorld/HomeWorldCharacterCustomizationSubsystem` | SetCustomizationTarget, GetMorphTargetNames, SetMorphTargetValue, Save/LoadCustomizationFromProfile, ApplyMorphValues. |
| `Source/HomeWorld/HomeWorldPlayerController` | Shows main menu widget when on MainMenu map; SetInputMode UI. |
| `Config/DefaultGame.ini` | `[/Script/HomeWorld.HomeWorldGameInstance]` MainMenuWidgetClassPath. |
| `Content/Python/ensure_main_menu_map.py` | Idempotent: check before create; log skip if exists. |
| `Content/Python/ensure_ui_folders.py` | Idempotent: check before create; log skip if exists. |

**In-game customization (Phase F):** From pause menu or hub, call `GetGameInstance<UHomeWorldGameInstance>()->OpenCharacterScreen()` to show the same WBP_CharacterCreate. Set input mode to UI when the widget is shown; when the widget closes (OnBackClicked or OnConfirmClicked), restore game input (e.g. SetInputModeGameOnly in the widget or in the pause menu). Optionally set the customization target to the current pawn's mesh when opening from in-game (e.g. in the widget's NativeConstruct, get the local pawn and call the customization subsystem's SetCustomizationTarget(Pawn->GetMesh())).

---

**See also:** [MILADY_IMPORT_ROADMAP.md](tasks/MILADY_IMPORT_ROADMAP.md), [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md), [EDITOR_POLISH_TUTORIAL.md](EDITOR_POLISH_TUTORIAL.md).
