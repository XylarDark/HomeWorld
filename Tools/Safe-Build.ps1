# Safe-Build.ps1 - Build with Editor-build protocol: close Editor if running, build, retry once on Editor-related failure.
# Use this instead of Build-HomeWorld.bat when running autonomously so build never stalls on "Editor is open."
#
# Usage: From project root, .\Tools\Safe-Build.ps1 [optional: -LaunchEditorAfter]
#   -LaunchEditorAfter: After a successful build, if Editor was closed by this script, launch it and wait for MCP port 55557 (requires UE_EDITOR set).
#
# Exit code: 0 = build succeeded; non-zero = build failed (see Build-HomeWorld.log).

param(
    [switch]$LaunchEditorAfter
)

$ErrorActionPreference = "Stop"
$ProjectRoot = $null
if ($env:HOMEWORLD_PROJECT -and (Test-Path -LiteralPath $env:HOMEWORLD_PROJECT)) {
    $ProjectRoot = $env:HOMEWORLD_PROJECT.TrimEnd("\", "/")
}
if (-not $ProjectRoot) {
    $ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}
$BuildLog = Join-Path $ProjectRoot "Build-HomeWorld.log"
$BuildBat = Join-Path $ProjectRoot "Build-HomeWorld.bat"

function Write-SafeLog { param([string]$Msg) Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Safe-Build: $Msg" }

function Test-EditorRunning {
    $out = & tasklist /FI "IMAGENAME eq UnrealEditor.exe" /NH 2>$null
    return ($out -match "UnrealEditor\.exe")
}

function Wait-ForEditorExit {
    param([int]$TimeoutSeconds = 90)
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if (-not (Test-EditorRunning)) { return $true }
        Start-Sleep -Seconds 2
    }
    return $false
}

function Close-EditorGracefully {
    if (-not (Test-EditorRunning)) { return $true }
    Write-SafeLog "Closing Editor (graceful taskkill)..."
    & taskkill /im UnrealEditor.exe 2>$null
    return (Wait-ForEditorExit)
}

function Close-EditorForce {
    if (-not (Test-EditorRunning)) { return $true }
    Write-SafeLog "Force-closing Editor (taskkill /f)..."
    & taskkill /f /im UnrealEditor.exe 2>$null
    return (Wait-ForEditorExit)
}

function Test-BuildFailureEditorRelated {
    if (-not (Test-Path -LiteralPath $BuildLog)) { return $false }
    $content = Get-Content -Path $BuildLog -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if (-not $content) { return $false }
    $c = $content.ToLowerInvariant()
    if ($content -match "Exit code:\s*6\b") { return $true }
    if ($c -match "live coding" -or $c -match "unable to build while") { return $true }
    if ($c -match "editor" -and ($c -match "lock" -or $c -match "in use")) { return $true }
    return $false
}

# Ensure we're in project root
Push-Location $ProjectRoot
try {
    if (-not (Test-Path -LiteralPath $BuildBat)) {
        Write-SafeLog "Build-HomeWorld.bat not found."
        exit 1
    }

    $editorWasRunning = Test-EditorRunning
    if ($editorWasRunning) {
        Write-SafeLog "Editor is running; closing before build (Editor-build protocol)."
        if (-not (Close-EditorGracefully)) {
            Write-SafeLog "Editor did not exit in time."
            exit 1
        }
    }

    Write-SafeLog "Running build..."
    & $BuildBat
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0 -and (Test-BuildFailureEditorRelated)) {
        Write-SafeLog "Build failed; log suggests Editor was in use. Force-closing and retrying once."
        Close-EditorForce | Out-Null
        Write-SafeLog "Retrying build..."
        & $BuildBat
        $exitCode = $LASTEXITCODE
    }

    if ($exitCode -eq 0) {
        Write-SafeLog "Build succeeded."
        if ($LaunchEditorAfter -and $editorWasRunning) {
            Write-SafeLog "Launching Editor and waiting for MCP (port 55557)..."
            $cycleScript = Join-Path $ProjectRoot "Content\Python\run_automation_cycle.py"
            if ((Test-Path -LiteralPath $cycleScript) -and $env:UE_EDITOR) {
                & python $cycleScript --no-build --launch-and-wait
                if ($LASTEXITCODE -ne 0) { Write-SafeLog "Editor launch/wait failed (non-fatal)." }
            } else {
                Write-SafeLog "Skipping LaunchEditorAfter (run_automation_cycle.py or UE_EDITOR missing)."
            }
        }
    } else {
        Write-SafeLog "Build failed (exit $exitCode). See Build-HomeWorld.log"
    }
    exit $exitCode
} finally {
    Pop-Location
}
