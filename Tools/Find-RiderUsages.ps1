# Find-RiderUsages.ps1 - List the files that reference a C++ member, without any way to delete one.
# Run from project root:
#   .\Tools\Find-RiderUsages.ps1 -FilePath Source/HomeWorld/HomeWorldCharacter.h -SymbolName bCloudDescentActive
#
# This is the sanctioned path for Rider's safe_delete. safe_delete deletes when preview is omitted,
# and the MCP whitelist cannot constrain a tool by parameter, so this wrapper is the only caller
# here: it always sends --preview true and refuses the result if anything was touched.
#
# Requires the Rider MCP server: .\Tools\Start-RiderMcp.ps1 (stop it with -Stop).

param(
    [Parameter(Mandatory = $true)]
    [string]$FilePath,

    [Parameter(Mandatory = $true)]
    [string]$SymbolName,

    [int]$Port = 64342
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Uri = "http://127.0.0.1:$Port/stream"

# Rider wants forward slashes and a path it can resolve from the project root.
$Path = $FilePath.Replace('\', '/').Trim()
if ($Path -notmatch '^[A-Za-z]:' -and $Path -notmatch '^/') {
    $Path = "$Root/".Replace('\', '/') + $Path
}

if (-not (Test-NetConnection -ComputerName 127.0.0.1 -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue)) {
    Write-Error "No Rider MCP server on 127.0.0.1:$Port. Start it with .\Tools\Start-RiderMcp.ps1, then re-run."
    exit 1
}

function Invoke-McpPost {
    param([string]$Body, [string]$SessionId)
    $Headers = @{ 'Accept' = 'application/json, text/event-stream' }
    if ($SessionId) { $Headers['mcp-session-id'] = $SessionId }
    Invoke-WebRequest -Uri $Uri -Method Post -Headers $Headers -Body $Body `
        -ContentType 'application/json' -UseBasicParsing
}

function ConvertFrom-McpPayload {
    # Rider may answer plain JSON or SSE. SSE frames the payload on a "data:" line.
    param([string]$Raw)
    $Text = $Raw
    $DataLines = @($Raw -split "`n" | Where-Object { $_ -match '^\s*data:' })
    if ($DataLines.Count -gt 0) {
        $Text = ($DataLines | ForEach-Object { $_ -replace '^\s*data:\s?', '' }) -join ''
    }
    $Text.Trim().TrimEnd("`r")
}

$Init = @{ jsonrpc = '2.0'; id = 1; method = 'initialize'
           params = @{ protocolVersion = '2024-11-05'
                       capabilities = @{}
                       clientInfo = @{ name = 'Find-RiderUsages.ps1'; version = '1.0' } } }
$InitResp = Invoke-McpPost -Body ($Init | ConvertTo-Json -Depth 8)
$SessionId = $InitResp.Headers['mcp-session-id'] | Select-Object -First 1
if (-not $SessionId) { Write-Error "Rider MCP did not return a session id on $Uri."; exit 1 }

# preview is hardcoded below. Do not add a switch that removes it.
$Command = "safe_delete --filePath $Path --symbolName $SymbolName --preview true"
$Call = @{ jsonrpc = '2.0'; id = 2; method = 'tools/call'
           params = @{ name = 'execute_tool'
                       arguments = @{ command = $Command; rootFolder = $Root.Replace('\', '/') } } }
$CallResp = Invoke-McpPost -Body ($Call | ConvertTo-Json -Depth 8) -SessionId $SessionId
$PayloadText = ConvertFrom-McpPayload -Raw $CallResp.Content

try {
    $Envelope = $PayloadText | ConvertFrom-Json
} catch {
    Write-Error "Could not parse the Rider reply:`n$PayloadText"
    exit 1
}

# execute_tool returns the tool payload as JSON inside its text content.
$Inner = $PayloadText
if ($Envelope.result.content) {
    $Inner = ($Envelope.result.content | ForEach-Object { $_.text }) -join ''
    try { $Inner = $Inner | ConvertFrom-Json } catch { }
}

$Applied = $false
$Deleted = @()
$Conflicts = @()
if ($Inner -is [string]) {
    try { $Inner = $Inner | ConvertFrom-Json } catch { }
}
if ($Inner -and $Inner -isnot [string]) {
    if ($null -ne $Inner.applied) { $Applied = [bool]$Inner.applied }
    if ($Inner.deleted) { $Deleted = @($Inner.deleted) }
    if ($Inner.conflicts) { $Conflicts = @($Inner.conflicts) }
}

if ($Applied -or $Deleted.Count -gt 0) {
    # preview must never write. If it did, say so loudly and fail the run.
    Write-Host "!! preview reported a write (applied=$Applied, deleted=$($Deleted.Count)). This is a bug in the tool, not in your arguments. Restore from git and report it."
    if ($Deleted.Count -gt 0) { $Deleted | ForEach-Object { "   deleted: $_" } }
    exit 2
}

$Files = @()
foreach ($c in $Conflicts) {
    if ($c -is [string]) { $Files += $c }
    elseif ($c.file) { $Files += $c.file }
    elseif ($c.path) { $Files += $c.path }
    else { $Files += ($c | ConvertTo-Json -Compress -Depth 4) }
}
$Files = @($Files | Where-Object { $_ } | Sort-Object -Unique)

"References to '$SymbolName' in '$Path': $($Files.Count) file(s)"
foreach ($f in $Files) { "  $f" }
if ($Files.Count -eq 0) { "  (no conflicts reported: either nothing references it, or the symbol did not resolve)" }
"Preview only. Nothing was written."
exit 0
