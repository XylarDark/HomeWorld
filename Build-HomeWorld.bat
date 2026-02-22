@echo off
rem Build HomeWorld using the Engine's Build.bat (avoids MSBuild .NET SDK issues).
rem Run from the project root (folder containing HomeWorld.uproject).

set UPROJECT=%~dp0HomeWorld.uproject
set ENGINE_BAT="C:\Program Files\Epic Games\UE_5.7\Engine\Build\BatchFiles\Build.bat"

if not exist %UPROJECT% (
    echo ERROR: HomeWorld.uproject not found. Run this script from the project root.
    exit /B 1
)

if not exist %ENGINE_BAT% (
    echo ERROR: Engine Build.bat not found at %ENGINE_BAT%
    echo Adjust the path in this script if UE 5.7 is installed elsewhere.
    exit /B 1
)

echo Building HomeWorldEditor Win64 Development...
%ENGINE_BAT% HomeWorldEditor Win64 Development -Project=%UPROJECT% %*
exit /B %ERRORLEVEL%
