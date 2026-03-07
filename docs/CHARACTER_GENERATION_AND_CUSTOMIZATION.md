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

Then in the Editor:

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

### 3. Character creation/customization screen (WBP_CharacterCreate)

Create a second Widget Blueprint `WBP_CharacterCreate` in `/Game/HomeWorld/UI` (Parent Class: **HomeWorldCharacterCustomizeWidget**):

- Placeholder **Upload / Scan** button (and optional URL field).
- Placeholder **Face sliders** (or â€œFace customizationâ€ area).
- **Confirm** button.

Open this widget from the main menu **Character** button (in WBP_MainMenu, in **OnCharacterClicked** create and add WBP_CharacterCreate to viewport, or call a subsystem that does so). Backend for â€œimage â†’ characterâ€ and face params is Phase C/E.

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
| `Content/Python/ensure_main_menu_map.py` | Idempotent create MainMenu map. |
| `Content/Python/ensure_ui_folders.py` | Idempotent create /Game/HomeWorld/UI. |

**In-game customization (Phase F):** From pause menu or hub, call `GetGameInstance<UHomeWorldGameInstance>()->OpenCharacterScreen()` to show the same WBP_CharacterCreate. Set input mode to UI when the widget is shown; when the widget closes (OnBackClicked or OnConfirmClicked), restore game input (e.g. SetInputModeGameOnly in the widget or in the pause menu). Optionally set the customization target to the current pawn's mesh when opening from in-game (e.g. in the widget's NativeConstruct, get the local pawn and call the customization subsystem's SetCustomizationTarget(Pawn->GetMesh())).

---

**See also:** [MILADY_IMPORT_ROADMAP.md](tasks/MILADY_IMPORT_ROADMAP.md), [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md), [EDITOR_POLISH_TUTORIAL.md](EDITOR_POLISH_TUTORIAL.md).
