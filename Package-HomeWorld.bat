@echo off
rem Package HomeWorld for Windows (64-bit) Shipping via RunUAT BuildCookRun.
rem Run from the project root. Close the Editor before running.
rem Output: Saved\StagedBuilds (or see log). Log: Package-HomeWorld.log

set "PROJECT_ROOT=%~dp0"
set "UPROJECT=%PROJECT_ROOT%HomeWorld.uproject"
set "RUNUAT=C:\Program Files\Epic Games\UE_5.7\Engine\Build\BatchFiles\RunUAT.bat"
set "LOGFILE=%PROJECT_ROOT%Package-HomeWorld.log"

if not exist "%UPROJECT%" (
    echo ERROR: HomeWorld.uproject not found. Run this script from the project root.
    exit /B 1
)

if not exist "C:\Program Files\Epic Games\UE_5.7\Engine\Build\BatchFiles\RunUAT.bat" (
    echo ERROR: RunUAT.bat not found. Adjust UE_5.7 path in this script if the engine is installed elsewhere.
    exit /B 1
)

set "ARCHIVE=%PROJECT_ROOT%Saved\StagedBuilds"
echo Packaging HomeWorld Win64 Shipping... Output: %ARCHIVE%
echo [%date% %time%] RunUAT BuildCookRun ... > "%LOGFILE%"
"%RUNUAT%" BuildCookRun -project="%UPROJECT%" -platform=Win64 -clientconfig=Shipping -cook -stage -pak -archive -archivedirectory="%ARCHIVE%" -skipeditorcontent >> "%LOGFILE%" 2>&1
set PACK_EXIT=%ERRORLEVEL%
echo [%date% %time%] Exit code: %PACK_EXIT% >> "%LOGFILE%"
if %PACK_EXIT% neq 0 echo Package failed. See %LOGFILE%
exit /B %PACK_EXIT%
