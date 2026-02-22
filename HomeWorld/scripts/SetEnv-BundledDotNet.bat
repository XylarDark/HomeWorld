@echo off
rem Set DOTNET_ROOT and PATH to UE 5.7 bundled .NET 8 SDK so MSBuild can find Microsoft.NET.Sdk.
rem Source this before building the solution (e.g. "call scripts\SetEnv-BundledDotNet.bat").
rem Engine path; change if UE 5.7 is installed elsewhere.
set "UE_ENGINE=C:\Program Files\Epic Games\UE_5.7"
set "UE_DOTNET=%UE_ENGINE%\Engine\Binaries\ThirdParty\DotNet\8.0.412\win-x64"
if not exist "%UE_DOTNET%\dotnet.exe" (
    echo ERROR: Bundled dotnet not found at %UE_DOTNET%
    exit /B 1
)
set "DOTNET_ROOT=%UE_DOTNET%"
set "PATH=%UE_DOTNET%;%PATH%"
set "DOTNET_MULTILEVEL_LOOKUP=0"
echo DOTNET_ROOT and PATH set to bundled SDK: %UE_DOTNET%
