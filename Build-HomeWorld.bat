@echo off
rem Build HomeWorld using the Engine's Build.bat (avoids MSBuild .NET SDK issues).
rem Run from the project root (folder containing HomeWorld.uproject).
rem Build output is logged to Build-HomeWorld.log in the project directory.

set UPROJECT=%~dp0HomeWorld.uproject
set ENGINE_BAT="C:\Program Files\Epic Games\UE_5.7\Engine\Build\BatchFiles\Build.bat"
set "LOGFILE=%~dp0Build-HomeWorld.log"

if not exist %UPROJECT% (
    echo ERROR: HomeWorld.uproject not found. Run this script from the project root.
    exit /B 1
)

if not exist %ENGINE_BAT% (
    echo ERROR: Engine Build.bat not found at %ENGINE_BAT%
    echo Adjust the path in this script if UE 5.7 is installed elsewhere.
    exit /B 1
)

echo Building HomeWorldEditor Win64 Development... Log: %LOGFILE%
echo [%date% %time%] %ENGINE_BAT% HomeWorldEditor Win64 Development -Project=%UPROJECT% %* > "%LOGFILE%"
%ENGINE_BAT% HomeWorldEditor Win64 Development -Project=%UPROJECT% %* >> "%LOGFILE%" 2>&1
set BUILD_EXIT=%ERRORLEVEL%
echo. >> "%LOGFILE%"
echo [%date% %time%] Exit code: %BUILD_EXIT% >> "%LOGFILE%"
if %BUILD_EXIT% neq 0 echo Build failed. See %LOGFILE%
exit /B %BUILD_EXIT%
