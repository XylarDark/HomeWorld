@echo off
rem mixar-mcp.cmd - MCP client entry point for Mixar.
rem
rem Mixar is a Blender 4.2.2 fork (mixar.exe --version says so; bpy.app.version returns a
rem spoofed (5, 2, 0) that exists only so extensions requiring >=5.1 install). Mixar is now
rem the default 3D tool, and bpy plus the FBX/GLTF exporters work unchanged.
rem
rem blender-mcp resolves the application executable from the BLENDER_PATH environment
rem variable and falls back to "blender" on PATH, so setting it here is what makes the
rem background/CLI code path target Mixar. The socket path does not need this, but a
rem fallback that quietly opened vanilla Blender would be worse than no fallback.
rem
rem The add-on serves the socket from a running Mixar. Start it with:
rem   .\Tools\Start-MixarMcp.ps1

set "BLENDER_PATH=C:\Program Files\Mixar\mixar.exe"
"C:\Users\User\.local\bin\blender-mcp.exe" %*