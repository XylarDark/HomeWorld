@echo off
rem Build C# parts of the solution with the Engine's bundled .NET SDK, then build the game
rem with the Engine's Build.bat. The C++ project requires VS/Build.bat; dotnet msbuild cannot
rem build it. Run from the project root.

cd /d "%~dp0"
call "%~dp0scripts\SetEnv-BundledDotNet.bat"
if errorlevel 1 exit /B 1
if not exist "HomeWorld.sln" (
    echo HomeWorld.sln not found. Generate project files first - see docs\SETUP.md
    exit /B 1
)
echo Building C# projects in solution. Native project may show one error - that is expected.
dotnet msbuild HomeWorld.sln -p:Configuration="Development Editor" -p:Platform=Win64 -restore -t:Build %*
echo.
echo Building game module with Engine Build.bat...
call "%~dp0Build-HomeWorld.bat"
exit /B %ERRORLEVEL%
