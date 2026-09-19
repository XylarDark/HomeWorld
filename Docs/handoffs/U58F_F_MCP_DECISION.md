# Docs/23 U58F-F — MCP landscape decision

| Field | Value |
|-------|-------|
| **Date** | 2026-09-19 |
| **Phase** | U58F-F · **WTR-B refresh** |
| **Decision** | **Keep UnrealMCP as primary** — do **not** enable Epic `ModelContextProtocol` alongside it |

---

## Compared (summary)

| | **UnrealMCP** (project) | **ModelContextProtocol** (Epic Experimental, UE 5.8.2) |
|--|-------------------------|------------------------------------------------------|
| Location | `Plugins/UnrealMCP/` (gitignored; Setup-MCP.bat) | Engine `Plugins/Experimental/ModelContextProtocol` |
| Port / bridge | Cursor MCP → **55557** (proven Docs/22) | Epic MCP server + **ToolsetRegistry** `AICallable` toolsets |
| HomeWorld automation | `execute_python_script`, actors, Blueprint/UMG helpers, PIE cheats | Broad Editor/PCG/UMG/plugin/config/test surface (see matrix) |
| Risk if dual-enabled | Port/tool collision; two transaction models (5.8.1/5.8.2 MCP crash fixes) | Experimental; tools/call framing + BP SCS fixes in hotfixes |

---

## WTR-B capability matrix (filesystem inventory — Epic **not** enabled)

Inventory method: read UE 5.8.2 plugin Source under `Engine/Plugins/Experimental/ModelContextProtocol` + `Engine/Plugins/Experimental/Toolsets/*` (`UFUNCTION(meta=(AICallable))`). **Did not** enable Epic MCP in `HomeWorld.uproject` (no dual-server).

### UnrealMCP tools (Conductor / Cursor namespace)

| Capability area | UnrealMCP tools |
|-----------------|-----------------|
| Level actors | `get_actors_in_level`, `find_actors_by_name`, `spawn_actor`, `delete_actor`, `set_actor_transform`, `get_actor_properties`, `set_actor_property`, `spawn_blueprint_actor` |
| Python / console | `execute_python_script`, `execute_console_command` |
| Blueprints | `create_blueprint`, `add_component_to_blueprint`, `set_*_properties`, `compile_blueprint`, `set_blueprint_property`, event/input/function nodes, `connect_blueprint_nodes`, variables, self refs, `find_blueprint_nodes` |
| Input | `create_input_mapping` |
| UMG | `create_umg_widget_blueprint`, `add_text_block_to_widget`, `add_button_to_widget`, `bind_widget_event`, `add_widget_to_viewport`, `set_text_block_binding` |

Primary HomeWorld path: **Python scripts via `execute_python_script`** (idempotent `Content/Python/*`).

### Epic Experimental toolsets (selected `AICallable` surface)

| Toolset | Representative tools | Overlap vs UnrealMCP |
|---------|----------------------|----------------------|
| **EditorAppToolset** | `SearchCVars`, `CaptureAssetImage` / `CaptureEditorImage` / `CaptureViewport`, `GetSelectedActors` / `SelectActors`, `GetCameraTransform` / `SetCameraTransform` / `FocusOnActors` / `GetVisibleActors`, screen↔world, Content Browser path/select/open, `StartPIE` / `StopPIE` / `IsPIERunning` | **Gap:** native viewport/asset capture + CVar search + selection/focus without custom Python |
| **LogsToolset** | `GetLogEntries`, `GetLogCategories`, `GetVerbosity` / `SetVerbosity` | **Gap:** structured log pull (we use Saved/Logs files today) |
| **PCGToolset** | `CreateGraph`, `GetGraphStructure`, `SetGraphParams`, `AddNode` / `UpdateNode` / `RemoveNode`, pin connect/disconnect, `SpawnGraphInstance` / `ExecuteGraphInstance`, `ListNativeNodes`, comments, `DrawSpline`, … | **Major gap:** first-class PCG graph edit (our Python still hits no-access mesh/By Tag) |
| **PCGSpatialToolset** | `RunPCGInstantGraph` | Gap: instant spatial graph run |
| **UMGToolSet** | Rich widget tree create/move/bind/compile (`CreateWidgetBlueprint`, `AddWidget`, `GetWidgetDescription`, …) | Partial overlap; Epic deeper than our UMG MCP helpers |
| **PluginToolset** | List/enable plugins, create plugin, descriptor edit | Gap: plugin enable from agent without uproject edit |
| **ConfigSettingsToolset** | List/get/set Project Settings sections | Gap: typed settings schema edits |
| **AutomationTestToolset** | `DiscoverTests`, `RunTests`, `GetTestResults`, … | Gap: MCP-native Automation Framework (we use Editor/CLI) |
| **LiveCodingToolset** | `CompileLiveCoding` | **Defer** — HomeWorld keeps Safe-Build |
| **NiagaraToolsets** | Asset discovery / BP wrappers | Out of MVP lookdev scope |
| Other shipped toolsets | AIModule, AnimationAssistant, ChaosCloth, Conversation, Dataflow, DataRegistry, GameFeatures, GameplayTags, GAS, MetaHumanGenerator, MVVM, Physics, SemanticSearch, SequencerAnimMixer, SlateInspector, StateTree, WorldConditions, … | Mostly **reject/defer** per product locks |

Epic also exposes MCP **resources / prompts / tools** capability structs (`ModelContextProtocolCapabilities`); tools are registered via **ToolsetRegistry** (legacy `UModelContextProtocolToolLibrary` deprecated).

### Decision: keep UnrealMCP — wrap later (optional)

**Confirm:** UnrealMCP remains the only MCP server for DESKTOP Conductor sessions.

Epic tools worth **wrapping into UnrealMCP or Python later** (not enabling Epic MCP now):

1. **PCGToolset** graph ops (`GetGraphStructure`, `AddNode`, `ConnectNodePins`, `SetGraphParams`) — closes AUTOMATION_GAPS around mesh list / By Tag where Epic already exposes AICallable.
2. **EditorAppToolset** `CaptureViewport` / `CaptureAssetImage` + `SetCameraTransform` — harden VNP/shot evidence without fragile Python viewport paths.
3. **LogsToolset** `GetLogEntries` — evidence-grep without scraping `Saved/Logs` only.

---

## Stamp

1. **Primary:** UnrealMCP remains the only MCP server HomeWorld automation depends on.
2. **Epic MCP:** Leave **disabled** in `HomeWorld.uproject`. Revisit only if Lead opens a dedicated track and UnrealMCP cannot cover a required tool surface.
3. **No dual servers** on DESKTOP-21CT3H0 — never run ModelContextProtocol + UnrealMCP together in Conductor sessions.
4. **WTR-B:** Capability matrix stamped 2026-09-19 from UE 5.8.2 filesystem inventory (plugin not enabled).

See [Docs/23_UE58_FEATURE_ADOPTION.md](../23_UE58_FEATURE_ADOPTION.md) · [Docs/25_WORKSPACE_TOOLING_REFINE.md](../25_WORKSPACE_TOOLING_REFINE.md) · [docs/Setup/MCP_SETUP.md](../../docs/Setup/MCP_SETUP.md).
