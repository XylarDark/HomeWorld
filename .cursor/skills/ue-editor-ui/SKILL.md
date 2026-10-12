---
name: ue-editor-ui
description: Drive Unreal Editor panels that have no Python API. Use when a log or result contains editor_ui: NEED_SLATE, when LevelToOpen could not be set, when a State Tree graph must be edited, or when a PCG Details field (Get Landscape Data By Tag, or a Static Mesh Spawner mesh list) cannot be written. Prefer UnrealMCP and Editor Python first.
---

# Unreal editor UI

Epic's Slate inspector clicks a widget by its ref. It does not move the mouse. The server is `http://127.0.0.1:8000/mcp`. Project UnrealMCP stays on port 55557 for actors, Blueprints, and Python.

The token `editor_ui: NEED_SLATE` names the panel. `portal-level` is the LevelToOpen field. `state-tree` is the State Tree graph. `pcg-details` is Get Landscape Data By Tag, or a Static Mesh Spawner mesh list. Snapshot that panel.

## Order

1. If Editor Python or UnrealMCP can do the change, use that. Do not call this server while `execute_python_script` is still running.
2. Describe `SlateInspectorToolset` once per session. Later clicks reuse that schema.
3. Call `Observe` on the panel before a deep snapshot. A snapshot of the main window alone stops at the splitter.
4. Click, type, or press a key by the ref from that snapshot. One Epic tool call at a time. Epic runs tools on the game thread.

## Stop

Stop on a password, a purchase, or a delete confirmation. Do not use this for landscape sculpt or for placing something by taste. Do not import an asset through MCP. `AssetImportTask` on that path hits the TaskGraph recursion guard and crashes the editor.

## If it is empty

A server with no tools means `ToolsetRegistry` or `SlateInspectorToolset` is disabled. Port 8000 is the default. A taken port uses `-ModelContextProtocolPort` and the same number in Cursor's `unrealEditorUi` URL.

## Measure

`python Content/Python/count_mcp_editor_ui.py` prints three counts from `Saved/Logs/HomeWorld.log`: `NEED_SLATE`, Slate `Click`, and MCP hang lines. A token with no click means the inspector was not used. Clicks that leave the panel unchanged mean the snapshot ref was too shallow.
