# MCP Server Setup: Cursor-to-Unreal Editor Bridge

Connect Cursor IDE to the running Unreal Editor so the AI agent can create assets, spawn actors, configure Blueprints, and manipulate the Editor in real time.

## Installed configuration

| Component | Location |
|-----------|----------|
| Python MCP server | `C:\tools\unreal-mcp\Python\unreal_mcp_server.py` |
| UE plugin (UnrealMCP) | `Plugins\UnrealMCP\` (gitignored; copied from the cloned repo) |
| Cursor config | `.cursor\mcp.json` |
| Cursor rule | `.cursor\rules\09-mcp-workflow.mdc` |

The plugin auto-starts a TCP listener on **port 55557** when the Editor opens. Cursor launches the Python MCP server via the `uv run` command defined in `.cursor/mcp.json`.

---

## Quick start (one command)

From the project root, run:

```
Setup-MCP.bat
```

This handles everything: installs `uv`, clones the MCP server, installs Python dependencies, copies the UE plugin, and creates `.cursor/mcp.json`. After it finishes, build the project (`Build-HomeWorld.bat`), open the Editor, and restart Cursor.

---

## Manual setup from scratch

Follow these steps if the batch script fails or you need to customize the installation.

### 1. Install prerequisites

```powershell
# Install uv (Astral package manager)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Add to current session PATH
$env:Path = "C:\Users\$env:USERNAME\.local\bin;$env:Path"

# Verify
uv --version        # expects 0.10+
python --version     # expects 3.10+
```

### 2. Clone and install the Python server

```powershell
git clone https://github.com/chongdashu/unreal-mcp.git C:\tools\unreal-mcp
cd C:\tools\unreal-mcp\Python
uv sync
```

Verify the module loads:

```powershell
uv --directory C:\tools\unreal-mcp\Python run python -c "import unreal_mcp_server; print('OK')"
```

### 3. Install the UE plugin

Copy the plugin into the project:

```powershell
Copy-Item -Path "C:\tools\unreal-mcp\MCPGameProject\Plugins\UnrealMCP" `
          -Destination "c:\dev\HomeWorld\Plugins\UnrealMCP" -Recurse -Force
```

The plugin is already listed in `HomeWorld.uproject`:

```json
{"Name": "UnrealMCP", "Enabled": true}
```

Restart the Editor. The plugin compiles on first launch and starts the TCP listener on port 55557. Check Output Log for `UnrealMCP: Server started`.

### 4. Cursor configuration

`.cursor/mcp.json` (already in the repo):

```json
{
  "mcpServers": {
    "unrealMCP": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\tools\\unreal-mcp\\Python",
        "run",
        "unreal_mcp_server.py"
      ]
    }
  }
}
```

After creating or modifying this file, **restart Cursor completely**.

### 5. Verify

1. Open the HomeWorld project in Unreal Editor (plugin starts automatically).
2. In Cursor, go to **Settings > Tools & MCP**. Look for a green dot next to **unrealMCP**.
3. Test by asking Cursor to "list all actors in the current level" or "spawn a cube at origin".

---

## Fallback: UnrealMCPBridge

If UnrealMCP fails to compile against UE 5.7, use `appleweed/UnrealMCPBridge` instead. It proxies to UE's built-in Python API via a socket bridge with no C++ plugin compilation required.

### Install

Available on the [Fab marketplace](https://www.fab.com/listings/0167ac03-47b5-4a08-b68f-5d54ab7b208e) or from GitHub:

```powershell
git clone https://github.com/appleweed/UnrealMCPBridge.git C:\tools\UnrealMCPBridge
pip install mcp
```

### Configure Cursor

Update `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "unrealMCP": {
      "command": "python",
      "args": ["C:\\tools\\UnrealMCPBridge\\MCPClient\\unreal_mcp_client.py"]
    }
  }
}
```

In the Editor, click **Start MCP Bridge** in the toolbar (port 9000).

---

## Capabilities

| Capability | UnrealMCP | UnrealMCPBridge |
|---|---|---|
| Actor CRUD (create, transform, delete) | Yes | Yes |
| Blueprint creation and component setup | Yes | Yes |
| Blueprint node graph wiring | Yes | No |
| Any `unreal.*` Python call | No (curated tools) | Yes |
| PCG graph manipulation | Via Python | Via Python |
| Viewport control | Yes | No |
| AnimGraph editing | No | No |

## MCP-first workflow

When connected, the AI agent follows `.cursor/rules/09-mcp-workflow.mdc`:

1. **MCP tools first** for live Editor manipulation
2. **Python scripts** for batch/repeatable operations (saved in `Content/Python/`)
3. **Manual instructions** only when MCP and Python cannot accomplish the task

## Troubleshooting

| Issue | Fix |
|---|---|
| MCP tools don't appear in Cursor | Restart Cursor after adding/changing `.cursor/mcp.json`; ensure `uv` is on PATH |
| "Connection refused" | Ensure the Editor is open with the UnrealMCP plugin enabled; check Output Log for errors |
| Python version error | Requires Python 3.10+; check with `python --version` |
| Plugin compilation failure on UE 5.7 | Switch to UnrealMCPBridge fallback (see above) |
| `uv` not found | Run the install script or add `C:\Users\<user>\.local\bin` to PATH |
