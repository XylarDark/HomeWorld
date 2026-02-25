@echo off
rem Open HomeWorld.sln in Visual Studio with DOTNET_ROOT set to the Engine's bundled .NET SDK,
rem so building the solution in VS does not fail with "Microsoft.NET.Sdk specified could not be found".
rem Run from the project root (folder containing HomeWorld.uproject).

cd /d "%~dp0"
call "%~dp0SetEnv-BundledDotNet.bat"
if errorlevel 1 exit /B 1
if not exist "HomeWorld.sln" (
    echo HomeWorld.sln not found. Generate project files first - see docs\SETUP.md
    exit /B 1
)
start "" "HomeWorld.sln"
exit /B 0
