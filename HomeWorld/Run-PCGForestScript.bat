@echo off
REM Optional: run PCG forest setup script when opening the Editor.
REM Set UE_EDITOR to your UnrealEditor.exe path (e.g. "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe")
set UE_EDITOR=
if "%UE_EDITOR%"=="" (
    echo Set UE_EDITOR in this batch file to your UnrealEditor.exe path.
    exit /b 1
)
set PROJECT=%~dp0HomeWorld.uproject
"%UE_EDITOR%" "%PROJECT%" -ExecutePythonScript="Content/Python/create_pcg_forest.py" %*
pause
