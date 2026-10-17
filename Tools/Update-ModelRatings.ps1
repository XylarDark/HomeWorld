# Refreshes Docs/context/MODEL_RANKINGS.{json,md} for the use-case model routing.
# Rating basis: Artificial Analysis Intelligence Index (AA), page-pulled per model.
# Read-only: it never edits configs or the registry.
#
# Usage (repo root):
#   powershell -ExecutionPolicy Bypass -File Tools\Update-ModelRatings.ps1
#   powershell -ExecutionPolicy Bypass -File Tools\Update-ModelRatings.ps1 -Probe
#
# Sources
#   - AA model pages. The page payload embeds scoreboards for MANY models, so every
#     metric is anchored on the model's own gated token: \"slug\":\"<slug>\", and the
#     first anchor slice containing the metric wins. Verified live 2026-10-17 on all
#     seven AA-covered models (DeepSeek needed the richer third anchor block).
#     nemotron-3-ultra has NO AA page (all slug variants 404, re-checked each run).
#   - models.dev api.json "opencode" provider: gateway-enforced context + modalities.
#   - `opencode models`: catalog availability; picker-disabled ids subtracted via the
#     user's global config (%USERPROFILE%\.config\opencode\opencode.json).
#   - Vals Index v2.1 and SWE-Atlas / Recruitly numbers are static snapshots from the
#     2026-10 research session, recorded in $catalog and labelled static.

param(
  [switch]$Probe,
  [int]$FreshnessWarnDays = 7
)

$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

Set-Location (Join-Path $PSScriptRoot '..')
$root = (Get-Location).Path
$outJson = Join-Path $root 'Docs\context\MODEL_RANKINGS.json'
$outMd   = Join-Path $root 'Docs\context\MODEL_RANKINGS.md'

$aaBase = 'https://artificialanalysis.ai/models'

# ---------------------------------------------------------------------------
# Catalog: picker id -> static facts + AA slug.
# tie = explicit rank inside the bucket when AA is null (kept identical to the
# picker's artificial releaseDate ordering in the user's global config).
# ---------------------------------------------------------------------------
$catalog = [ordered]@{
  'code/glm-5.3-flash-free'            = @{ bucket='code'; tie=1; name='GLM-5.3-Flash';        aaSlug='glm-5-3-flash';           vals=44.58; notes=@('Vals v2.1 snapshot 44.58% = #41/49; AA is the basis.') }
  'code/deepseek-v4.1-flash-free'      = @{ bucket='code'; tie=2; name='DeepSeek V4.1 Flash';  aaSlug='deepseek-v4-1-flash';     vals=51.32; notes=@('Vals v2.1 snapshot 51.32% = #26/49; AA is the basis.') }
  'code/big-pickle'                    = @{ bucket='code'; tie=3; name='Big Pickle';           aaSlug=$null;                     vals=$null; notes=@('No AA page. SWE-Atlas Codebase QnA 50.8% (63/124) is the only code-specific number; static snapshot.') }
  'plan/beam-free'                     = @{ bucket='plan'; tie=1; name='Beam 1.0';             aaSlug='reflection-beam';         vals=$null; notes=@('TB4.0 3%, so not a terminal coder; long-context reasoning role.') }
  'plan/nemotron-3-ultra-free'         = @{ bucket='plan'; tie=2; name='Nemotron 3 Ultra';     aaSlug='nemotron-3-ultra';        vals=$null; notes=@('AA model page 404s on every slug variant tried. AA 23 comes from AAs own X post; ranked n/r until a page exists.') }
  'plan/longcat-2.5-preview-free'      = @{ bucket='plan'; tie=3; name='LongCat 2.5 Preview';  aaSlug=$null;                     vals=$null; notes=@('No AA page. Meituan preview; image input per provider docs.') }
  'art/mimo-v2.6-flash-free'           = @{ bucket='art';  tie=1; name='MiMo-V2.6-Flash';      aaSlug='mimo-v2-6-flash';         vals=53.23; notes=@('Vals v2.1 snapshot 53.23% = #20/49; AA is the basis.') }
  'art/nemotron-3.5-super-vl-free'     = @{ bucket='art';  tie=2; name='Nemotron 3.5 Super VL'; aaSlug='nemotron-3-5-super-vl';  vals=$null; notes=@() }
  'art/space-bunny-free'               = @{ bucket='art';  tie=3; name='Space Bunny';          aaSlug=$null;                     vals=$null; notes=@('No AA page. Recruitly 73/100 (static); #1 usage on the OpenRouter free tier.') }
  'bulk/nemotron-3.5-lightning-free'   = @{ bucket='bulk'; tie=1; name='Nemotron 3.5 Lightning'; aaSlug='nemotron-3-5-lightning'; vals=$null; notes=@('Cheapest throughput pick; TB4.0 0.5%.') }
  'cloudflare/glm-4.7-flash'           = @{ bucket='fallback'; tie=1; name='GLM-4.7-Flash';    aaSlug='glm-4-7-flash';           vals=$null; notes=@('AA page is the (Reasoning) variant. Cloudflare is its own provider; it cannot ride the opencode canonical groups.') }
}

$bucketMeta = [ordered]@{
  'code'     = @{ label='Code dev (UE C++)';            note='Proxied by Terminal-Bench 4.0 (agentic terminal coding) and SciCode.' }
  'plan'     = @{ label='Architecture & game design';   note='No public benchmark tests game design; this group is long-context systems reasoning as the closest measurable proxy.' }
  'art'      = @{ label='Art design & assets';          note='Image-input models only; ranked by AA.' }
  'bulk'     = @{ label='Fast / bulk';                  note='High-throughput drafting; last resort for code or vision work.' }
  'fallback' = @{ label='Cloudflare bulk (fallback)';   note='Separate provider, kept outside the use-case buckets.' }
}

# ---------------------------------------------------------------------------
# AA scrape (slug-anchored)
# ---------------------------------------------------------------------------
function Get-AAScores {
  param([string]$Slug)
  $c = (Invoke-WebRequest -Uri "$aaBase/$Slug" -UseBasicParsing -TimeoutSec 30).Content
  $anchors = [regex]::Matches($c, [regex]::Escape('\"slug\":\"' + $Slug))
  $fallback = $null
  foreach ($m in $anchors) {
    $len = [Math]::Min(5000, $c.Length - $m.Index)
    $slice = $c.Substring($m.Index, $len)
    $intS = [regex]::Match($slice, 'intelligenceIndex["\:\\:]*([0-9.]+)').Groups[1].Value
    if (-not $intS) { continue }
    $rec = @{
      int = [double]$intS
      tb  = $null; sci = $null; ctx = $null
    }
    $tbS  = [regex]::Match($slice, 'terminalBench40["\:\\:]*([0-9.]+|null)').Groups[1].Value
    $sciS = [regex]::Match($slice, 'scicode["\:\\:]*([0-9.]+|null)').Groups[1].Value
    $ctxS = [regex]::Match($slice, 'contextWindowTokens["\:\\:]*([0-9]+)').Groups[1].Value
    if ($rec.int -eq 0) { continue }
    if ($tbS -and $tbS -ne 'null') { $rec.tb = [math]::Round([double]$tbS * 100, 1) }
    if ($sciS -and $sciS -ne 'null') { $rec.sci = [math]::Round([double]$sciS * 100, 1) }
    if ($ctxS) { $rec.ctx = [int64]$ctxS }
    if ($tbS) { return $rec }              # first anchor that carries the scoreboard
    if (-not $fallback) { $fallback = $rec }
  }
  return $fallback
}

$aaData = @{}
foreach ($slug in @($catalog.Values | Where-Object { $_.aaSlug } | ForEach-Object { $_.aaSlug } | Select-Object -Unique)) {
  try {
    $d = Get-AAScores -Slug $slug
    if ($d) { $aaData[$slug] = $d }
    else { $aaData[$slug] = $null; Write-Host ("AA anchors empty for {0}" -f $slug) }
  } catch {
    Write-Host ("AA fetch failed for {0}: {1}" -f $slug, $_.Exception.Message)
    $aaData[$slug] = $null
  }
  Start-Sleep -Milliseconds 400
}

# nemotron-3-ultra: re-check the known-404 pages each run so the report reflects today
$nemNote = 'AA model page 404s on every slug variant tried. AA 23 comes from AAs own X post; ranked n/r until a page exists.'
$nemVariants = @('nemotron-3-ultra','nemotron-3-ultra-550b','nemotron-3-ultra-550b-a55b')
foreach ($v in $nemVariants) {
  try {
    $d = Get-AAScores -Slug $v
    if ($d) {
      $catalog['plan/nemotron-3-ultra-free'].aaSlug = $v
      $catalog['plan/nemotron-3-ultra-free'].notes = @('AA page now live at slug ' + $v)
      $nemNote = $null
      break
    }
  } catch { }
}

# ---------------------------------------------------------------------------
# models.dev (gateway context + modalities)
# ---------------------------------------------------------------------------
$mdDev = @{}
try {
  $api = Invoke-RestMethod -Uri 'https://models.dev/api.json' -TimeoutSec 40
  foreach ($id in $catalog.Keys) {
    $mid = ($id -split '/')[1]
    $dev = $api.'opencode'.models.$mid
    if ($dev) {
      $mods = ''
      if ($dev.modalities -and $dev.modalities.input) {
        $mods = (@($dev.modalities.input) | Where-Object { $_ -ne 'text' }) -join '+'
        if (-not $mods) { $mods = 'text' }
      }
      $mdDev[$mid] = @{
        ctx = if ($dev.limit -and $dev.limit.context) { [int64]$dev.limit.context } else { $null }
        mods = $mods
        toolCall = [bool]$dev.tool_call
      }
    }
  }
} catch {
  Write-Host ("models.dev fetch failed: {0}" -f $_.Exception.Message)
}

# ---------------------------------------------------------------------------
# Availability: `opencode models` minus picker-disabled ids from global config
# ---------------------------------------------------------------------------
$discIds = @()
try {
  $discRaw = & opencode models 2>$null
  $discIds = @($discRaw | ForEach-Object { ($_ -split '\s+')[0] } | Where-Object { $_ -match '^[A-Za-z0-9._-]+/[A-Za-z0-9@._-]+$' })
} catch {
  Write-Host "opencode models failed; availability will show unknown"
}

$disabled = @{}
$cfgPath = Join-Path $env:USERPROFILE '.config\opencode\opencode.json'
if (Test-Path $cfgPath) {
  try {
    $gcfg = Get-Content $cfgPath -Raw | ConvertFrom-Json
    foreach ($p in $gcfg.providers.PSObject.Properties) {
      if ($p.Value.models) {
        foreach ($mm in $p.Value.models.PSObject.Properties) {
          if ($mm.Value.disabled) { $disabled[($p.Name + '/' + $mm.Name)] = $true }
        }
      }
    }
  } catch { Write-Host "global config parse failed; disabled-set skipped" }
}
$visibleSet = @{}
foreach ($i in $discIds) { if (-not $disabled.ContainsKey($i)) { $visibleSet[$i] = $true } }

# ---------------------------------------------------------------------------
# Optional probe: `opencode run` a trivial prompt per visible model
# ---------------------------------------------------------------------------
$probes = @{}
if ($Probe) {
  foreach ($id in $catalog.Keys) {
    if (-not $visibleSet.ContainsKey($id)) { continue }
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    $ok = $false
    try {
      $r = & opencode run --model $id 'Reply with exactly: OK' 2>$null
      $ok = (($r -join ' ') -match '\bOK\b')
    } catch { $ok = $false }
    $sw.Stop()
    $probes[$id] = @{ ok = $ok; seconds = [math]::Round($sw.Elapsed.TotalSeconds, 1) }
    Write-Host ("probe {0,-40} ok={1} {2}s" -f $id, $ok, $sw.Elapsed.TotalSeconds)
  }
}

# ---------------------------------------------------------------------------
# Build records
# ---------------------------------------------------------------------------
$records = @()
foreach ($id in $catalog.Keys) {
  $e = $catalog[$id]
  $mid = ($id -split '/')[1]
  $aa = $null; $tb = $null; $sci = $null; $ctxAa = $null; $prov = $null
  if ($e.aaSlug -and $aaData.ContainsKey($e.aaSlug) -and $aaData[$e.aaSlug]) {
    $d = $aaData[$e.aaSlug]
    $aa = [math]::Round($d.int, 1); $tb = $d.tb; $sci = $d.sci; $ctxAa = $d.ctx
    $prov = 'AA model page (slug-anchored)'
  }
  if ($id -eq 'plan/nemotron-3-ultra-free' -and $nemNote) { $prov = $nemNote }
  $dev = if ($mdDev.ContainsKey($mid)) { $mdDev[$mid] } else { $null }

  $mods = if ($dev) { $dev.mods } else { $null }
  if ($id -eq 'plan/longcat-2.5-preview-free' -and -not $mods) { $mods = 'image (provider docs)' }

  $records += [pscustomobject]@{
    id = $id; bucket = $e.bucket; name = $e.name
    aa = $aa
    tb40Pct = $tb
    scicodePct = $sci
    vals = $e.vals
    aaProvenance = $prov
    contextSpec = $ctxAa
    contextGateway = if ($dev) { $dev.ctx } else { $null }
    modalities = $mods
    toolCall = if ($dev) { $dev.toolCall } else { $null }
    available = [bool]$visibleSet.ContainsKey($id)
    probe = if ($probes.ContainsKey($id)) { $probes[$id] } else { $null }
    notes = @($e.notes)
  }
}

$unmappedVisible = @($visibleSet.Keys | Where-Object {
  $i = $_; -not ($catalog.Contains($i)) -and ($_ -like '*-free' -or $_ -like 'opencode/*')
} | Sort-Object)

# bucket ordering: aa desc (nulls last), then explicit tie rank, then original order
$i = 0
$records = foreach ($r in $records) {
  Add-Member -InputObject $r -NotePropertyName seq -NotePropertyValue ([int]$i) -Force
  Add-Member -InputObject $r -NotePropertyName tie -NotePropertyValue ([int]$catalog[$r.id].tie) -Force
  $i++
  $r
}
$records = @($records | Sort-Object -Property bucket, `
  @{Expression={ if ($null -ne $_.aa) { $_.aa } else { -999999 } }; Descending=$true }, `
  @{Expression={ [int]$_.tie } }, `
  @{Expression={ [int]$_.seq } })
$clean = @($records | Select-Object id, bucket, name, aa, tb40Pct, scicodePct, vals, aaProvenance, contextSpec, contextGateway, modalities, toolCall, available, probe, notes)

# recommendations
$rec = [ordered]@{}
foreach ($b in $bucketMeta.Keys) {
  $list = @($records | Where-Object { $_.bucket -eq $b } | Select-Object -ExpandProperty id)
  if ($list.Count) {
    $rec[$b] = [pscustomobject]@{ firstWave = $list[0]; crossReference = @($list | Select-Object -Skip 1) }
  }
}

$now = [DateTime]::UtcNow
$stamp = $now.ToString('yyyy-MM-dd HH:mm') + 'Z'

# ---------------------------------------------------------------------------
# Write JSON
# ---------------------------------------------------------------------------
$jsonObj = [pscustomobject]@{
  generatedAt = $now.ToString('yyyy-MM-ddTHH:mm:ssZ')
  generatedBy = 'Tools/Update-ModelRatings.ps1 - do not hand-edit; re-run instead'
  ratingBasis = 'Artificial Analysis Intelligence Index (AA); models without an AA page rank n/r and sit last in their bucket'
  staleness = @{ warnAfterDays = $FreshnessWarnDays; warnIfOlderThan = $now.AddDays(-$FreshnessWarnDays).ToString('yyyy-MM-ddTHH:mm:ssZ') }
  protocol = 'First task of a feature starts on the bucket first-wave pick; later passes cross-reference the remaining models in listed order. Switch models via /models only; agents suggest, never switch.'
  sources = [pscustomobject]@{
    aa = "$aaBase/<slug> (slug-anchored: intelligenceIndex, terminalBench40, scicode, contextWindowTokens)"
    gatewayFacts = 'https://models.dev/api.json, opencode provider (context coverage + input modalities the gateway actually serves)'
    availability = 'opencode models, minus ids the user disabled in the picker config'
    staticSnapshots = 'Vals Index v2.1; SWE-Atlas (big-pickle 50.8%); Recruitly (Space Bunny 73/100)'
  }
  buckets = $bucketMeta
  recommended = $rec
  models = $clean
  unmappedVisibleModels = $unmappedVisible
  probes = if ($Probe) { $probes } else { 'not run this pass (-Probe to enable)' }
}

$jsonText = ($jsonObj | ConvertTo-Json -Depth 8)
[System.IO.File]::WriteAllText($outJson, $jsonText, (New-Object System.Text.UTF8Encoding($false)))

# ---------------------------------------------------------------------------
# Write Markdown (NOTE: -f expressions are built into $line first; -f with a
# comma list directly inside a method call mis-compiles on Windows PowerShell 5.1)
# ---------------------------------------------------------------------------
$md = New-Object System.Collections.Generic.List[string]
$md.Add('# MODEL_RANKINGS - free OpenCode models for HomeWorld')
$md.Add('')
$md.Add(('Generated: {0}. Stale after {1} days. Rating basis: **Artificial Analysis Intelligence Index**.' -f $stamp, $FreshnessWarnDays))
$md.Add('Generated by Tools/Update-ModelRatings.ps1. Do not hand-edit; re-run instead.')
$md.Add('')
$md.Add('## Protocol')
$md.Add('')
$md.Add('First task on a feature starts on the bucket **first wave** pick. Later passes cross-reference the remaining models of the same bucket, in listed order, and **agents recommend rather than switch** - the human changes model via /models.')
$md.Add('')
$md.Add('## Legend')
$md.Add('')
$md.Add('AA = Intelligence Index (0-100) | TB40 = Terminal-Bench 4.0 % | Sci = SciCode % | Vals = Vals Index v2.1 (static) | Ctx = AA model spec / opencode gateway limit (tokens) | Mods = input modalities the gateway serves (models.dev) | Live = visible in `opencode models` minus picker-disabled ids.')
$md.Add('Picker labels round AA to one decimal and TB40 to whole percent; this file keeps one decimal everywhere.')
$md.Add('')
foreach ($b in $bucketMeta.Keys) {
  $list = @($records | Where-Object { $_.bucket -eq $b })
  if (-not $list.Count) { continue }
  $first = $list[0]
  $md.Add(('## {0}' -f $bucketMeta[$b].label))
  $md.Add('')
  if ($first.available) {
    $aaS = $(if ($null -ne $first.aa) { $first.aa } else { 'n/r' })
    $md.Add(('**First wave: `{0}`** ({1}, AA {2})' -f $first.id, $first.name, $aaS))
  } else {
    $md.Add(('**First wave would be `{0}` but it is not currently visible in the catalog; fall through in order.**' -f $first.id))
    $alt = @($list | Where-Object { $_.available } | Select-Object -First 1)
    if ($alt.Count) { $md.Add(('Next live: `{0}`' -f $alt[0].id)) }
  }
  $cross = @($list | Select-Object -Skip 1 | ForEach-Object { ('`{0}`' -f $_.id) })
  if ($cross.Count) { $md.Add(('Cross-reference order: {0}' -f ($cross -join ' -> '))) }
  $md.Add('')
  $md.Add($bucketMeta[$b].note)
  $md.Add('')
  $md.Add('| Model | id | AA | TB40 | Sci | Vals | Ctx spec/serve | Mods | Live |')
  $md.Add('|---|---|---|---|---|---|---|---|---|')
  foreach ($r in $list) {
    $aaS = $(if ($null -ne $r.aa) { $r.aa } else { 'n/r' })
    $tbS = $(if ($null -ne $r.tb40Pct) { ('{0}%' -f $r.tb40Pct) } else { '-' })
    $scS = $(if ($null -ne $r.scicodePct) { ('{0}%' -f $r.scicodePct) } else { '-' })
    $vS  = $(if ($null -ne $r.vals) { $r.vals } else { '-' })
    $ctxS = $(if ($r.contextSpec) { $r.contextSpec } else { '-' })
    $cgS  = $(if ($r.contextGateway) { $r.contextGateway } else { '-' })
    $cS = ('{0} / {1}' -f $ctxS, $cgS)
    $mS = $(if ($r.modalities) { $r.modalities } else { '-' })
    $lS = $(if ($r.available) { 'yes' } else { 'NO' })
    $line = ('| {0} | `{1}` | {2} | {3} | {4} | {5} | {6} | {7} | {8} |' -f $r.name, $r.id, $aaS, $tbS, $scS, $vS, $cS, $mS, $lS)
    $md.Add($line)
  }
  $md.Add('')
}
$md.Add('## Caveats and provenance')
$md.Add('')
foreach ($r in $records) {
  foreach ($n in $r.notes) {
    $line = ('- **{0}**: {1}' -f $r.name, $n)
    $md.Add($line)
  }
}
$md.Add('- **Game design**: no public benchmark tests it (AA GDPval axes: finance, strategy, legal, healthcare, engineering, economics; Vals: finance, coding, legal, tax). It rides the Architecture bucket as the closest measurable proxy.')
$md.Add('- **Vals dissent**: on covered models Vals v2.1 ranks MiMo 53.23 (#20/49) > DeepSeek 51.32 (#26/49) > GLM-5.3-Flash 44.58 (#41/49). The chosen basis is AA.')
$md.Add('- **Picker order**: the /models order comes from artificial `releaseDate` keys in `%USERPROFILE%\.config\opencode\opencode.json` (releaseDate is the pickers sort key and is never displayed). This script does not edit that file; re-key by hand or ask the agent after material rating shifts.')
$md.Add('')
if ($unmappedVisible.Count) {
  $md.Add('## Unmapped visible models (free-ish ids not in this routing)')
  $md.Add('')
  foreach ($u in $unmappedVisible) { $md.Add(('`{0}`' -f $u)) }
  $md.Add('')
}
$mdText = ($md -join "`r`n")
[System.IO.File]::WriteAllText($outMd, $mdText, (New-Object System.Text.UTF8Encoding($false)))

# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------
Write-Host ''
Write-Host ('Wrote {0}' -f $outJson)
Write-Host ('Wrote {0}' -f $outMd)
foreach ($b in $bucketMeta.Keys) {
  if ($rec.Contains($b) -and $rec[$b]) { Write-Host ('  {0,-10} first wave: {1}' -f $b, $rec[$b].firstWave) }
}
if ($unmappedVisible.Count) { Write-Host ('  unmapped visible ids: ' + ($unmappedVisible -join ', ')) }
