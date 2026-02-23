@echo off
rem One-click MCP setup: installs the Cursor-to-Unreal bridge so AI can control the Editor.
rem Run from the project root (folder containing HomeWorld.uproject).
rem Requires: Python 3.10+, internet access, git on PATH.

setlocal enabledelayedexpansion

set "TOOLS_DIR=C:\tools\unreal-mcp"
set "PLUGIN_SRC=%TOOLS_DIR%\MCPGameProject\Plugins\UnrealMCP"
set "PLUGIN_DST=%~dp0Plugins\UnrealMCP"
set "MCP_JSON=%~dp0.cursor\mcp.json"
set "UV_BIN=%USERPROFILE%\.local\bin\uv.exe"

echo ============================================
echo   HomeWorld MCP Setup
echo ============================================
echo.

rem --- Step 1: Check Python ---
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found on PATH. Install Python 3.10 or newer and try again.
    exit /B 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Python %PYVER%

rem --- Step 2: Install uv if missing ---
if exist "%UV_BIN%" (
    echo [OK] uv already installed
) else (
    echo Installing uv package manager...
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    if not exist "%UV_BIN%" (
        echo ERROR: uv installation failed. Visit https://docs.astral.sh/uv/ to install manually.
        exit /B 1
    )
    echo [OK] uv installed
)
set "Path=%USERPROFILE%\.local\bin;%Path%"

rem --- Step 3: Clone unreal-mcp if missing ---
if exist "%TOOLS_DIR%\Python\unreal_mcp_server.py" (
    echo [OK] unreal-mcp already cloned at %TOOLS_DIR%
) else (
    echo Cloning chongdashu/unreal-mcp...
    git clone https://github.com/chongdashu/unreal-mcp.git "%TOOLS_DIR%"
    if %ERRORLEVEL% neq 0 (
        echo ERROR: git clone failed. Check internet and git installation.
        exit /B 1
    )
    echo [OK] Cloned to %TOOLS_DIR%
)

rem --- Step 4: Install Python dependencies ---
echo Installing Python dependencies...
"%UV_BIN%" --directory "%TOOLS_DIR%\Python" sync
if %ERRORLEVEL% neq 0 (
    echo ERROR: uv sync failed. Python 3.10 or newer is required.
    exit /B 1
)
echo [OK] Python dependencies installed

rem --- Step 5: Copy UE plugin ---
if exist "%PLUGIN_DST%\UnrealMCP.uplugin" (
    echo [OK] UnrealMCP plugin already in Plugins/
) else (
    if not exist "%PLUGIN_SRC%\UnrealMCP.uplugin" (
        echo ERROR: Plugin source not found at %PLUGIN_SRC%
        exit /B 1
    )
    echo Copying UnrealMCP plugin to project...
    if not exist "%~dp0Plugins" mkdir "%~dp0Plugins"
    xcopy "%PLUGIN_SRC%" "%PLUGIN_DST%" /E /I /Q
    echo [OK] Plugin copied to Plugins\UnrealMCP
)

rem --- Step 6: Create .cursor/mcp.json if missing ---
if exist "%MCP_JSON%" (
    echo [OK] .cursor/mcp.json already exists
) else (
    echo Creating .cursor/mcp.json...
    if not exist "%~dp0.cursor" mkdir "%~dp0.cursor"
    (
        echo {
        echo   "mcpServers": {
        echo     "unrealMCP": {
        echo       "command": "uv",
        echo       "args": [
        echo         "--directory",
        echo         "C:\\tools\\unreal-mcp\\Python",
        echo         "run",
        echo         "unreal_mcp_server.py"
        echo       ]
        echo     }
        echo   }
        echo }
    ) > "%MCP_JSON%"
    echo [OK] Created .cursor/mcp.json
)

echo.
echo ============================================
echo   MCP Setup Complete
echo ============================================
echo.
echo Next steps:
echo   1. Build the project:  Build-HomeWorld.bat
echo   2. Open HomeWorld.uproject in the Editor
echo      (the UnrealMCP plugin compiles on first launch)
echo   3. Restart Cursor so it picks up .cursor/mcp.json
echo   4. Check Cursor: Settings ^> Tools ^& MCP for green dot
echo.
echo If the plugin fails to compile against UE 5.7,
echo see docs/MCP_SETUP.md for the UnrealMCPBridge fallback.
echo.
