#!/usr/bin/env node
/**
 * UE preflight (HR3-B) — fail loud before PIE / verb greps.
 * Repo-side checks run everywhere; MCP + on-disk assets on DESKTOP; deep checks via preflight_ue_editor.py.
 *
 * Usage:
 *   npm run preflight:ue                          # DESKTOP default (MCP + repo + disk assets + editor JSON)
 *   npm run preflight:ue -- --skip-mcp             # skip MCP port probe
 *   npm run preflight:ue -- --assets-only          # repo config only (cloud CI)
 *   HW_PREFLIGHT_SKIP_MCP=1 npm run preflight:ue # env alias for --skip-mcp
 *   npm run preflight:ue -- --require-editor       # fail if Saved/preflight_ue_editor.json missing/stale
 *   npm run preflight:ue -- --simulate-fail=MCP_UNREACHABLE  # dry-run fail (tests/docs)
 */
const fs = require('fs');
const net = require('net');
const path = require('path');

const projectRoot = path.resolve(__dirname, '..');
const configPath = path.join(projectRoot, 'config', 'preflight-ue.json');

const PREFIX = 'preflight:ue';

/** @typedef {{ code: string, message: string, detail?: string }} Blocker */

function loadConfig() {
  if (!fs.existsSync(configPath)) {
    console.error(`${PREFIX} — missing config: ${configPath}`);
    process.exit(2);
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

function parseArgs(argv) {
  const opts = {
    skipMcp: process.env.HW_PREFLIGHT_SKIP_MCP === '1',
    assetsOnly: false,
    requireEditor: false,
    simulateFail: null,
    help: false,
  };
  for (const arg of argv) {
    if (arg === '--help' || arg === '-h') opts.help = true;
    else if (arg === '--skip-mcp') opts.skipMcp = true;
    else if (arg === '--assets-only') opts.assetsOnly = true;
    else if (arg === '--require-editor') opts.requireEditor = true;
    else if (arg.startsWith('--simulate-fail=')) {
      opts.simulateFail = arg.slice('--simulate-fail='.length);
    } else {
      console.error(`${PREFIX} — unknown argument: ${arg}`);
      process.exit(2);
    }
  }
  return opts;
}

function printHelp() {
  console.log(`Usage: node scripts/preflight-ue.js [options]

Options:
  --skip-mcp              Skip UnrealMCP port ${55557} probe (cloud CI; or HW_PREFLIGHT_SKIP_MCP=1)
  --assets-only           Repo-side config/script checks only (no MCP, disk assets, or editor JSON)
  --require-editor        Fail when Saved/preflight_ue_editor.json is missing or reports blockers
  --simulate-fail=CODE    Inject a blocker for dry-run / unit tests (see config/preflight-ue.json blockerCodes)
  -h, --help              Show this help

Exit codes: 0 pass, 1 blocker(s), 2 misconfiguration`);
}

/**
 * /Game/HomeWorld/Foo/Bar -> Content/HomeWorld/Foo/Bar.{uasset,umap}
 * @returns {string[]}
 */
function gamePathToDiskCandidates(gamePath) {
  if (!gamePath || !gamePath.startsWith('/Game/')) return [];
  const rel = gamePath.replace(/^\/Game\//, 'Content/').replace(/^\//, '');
  const base = path.join(projectRoot, rel);
  const ext = gamePath.includes('/Maps/') ? '.umap' : '.uasset';
  return [base + ext, base + '.uasset', base + '.umap'];
}

function assetExistsOnDisk(gamePath) {
  return gamePathToDiskCandidates(gamePath).some((p) => fs.existsSync(p));
}

/**
 * @param {string} host
 * @param {number} port
 * @param {number} timeoutMs
 * @returns {Promise<boolean>}
 */
function probeTcp(host, port, timeoutMs) {
  return new Promise((resolve) => {
    const socket = new net.Socket();
    let settled = false;
    const finish = (ok) => {
      if (settled) return;
      settled = true;
      try {
        socket.destroy();
      } catch (_) {
        /* ignore */
      }
      resolve(ok);
    };
    socket.setTimeout(timeoutMs);
    socket.once('connect', () => finish(true));
    socket.once('timeout', () => finish(false));
    socket.once('error', () => finish(false));
    socket.connect(port, host);
  });
}

/** @returns {Blocker[]} */
function checkRepo(config) {
  /** @type {Blocker[]} */
  const blockers = [];
  const repo = config.repo || {};

  for (const rel of repo.requiredFiles || []) {
    const abs = path.join(projectRoot, rel);
    if (!fs.existsSync(abs)) {
      blockers.push({
        code: 'CONFIG_MISSING',
        message: config.blockerCodes?.CONFIG_MISSING || 'Required file missing',
        detail: rel,
      });
    }
  }

  const charCfgRel = repo.characterConfigPath;
  if (charCfgRel) {
    const charCfgAbs = path.join(projectRoot, charCfgRel);
    if (fs.existsSync(charCfgAbs)) {
      try {
        const charCfg = JSON.parse(fs.readFileSync(charCfgAbs, 'utf8'));
        for (const key of repo.requiredCharacterConfigKeys || []) {
          const val = (charCfg[key] || '').trim();
          if (!val) {
            blockers.push({
              code: 'CONFIG_EMPTY_PATH',
              message: config.blockerCodes?.CONFIG_EMPTY_PATH || 'Character config path empty',
              detail: `${charCfgRel} → ${key}`,
            });
          }
        }
      } catch (err) {
        blockers.push({
          code: 'CONFIG_MISSING',
          message: 'Invalid character_blueprint_config.json',
          detail: err.message,
        });
      }
    }
  }

  return blockers;
}

/** @returns {Blocker[]} */
function checkDiskAssets(config) {
  /** @type {Blocker[]} */
  const blockers = [];
  const content = config.content || {};
  const paths = [
    content.vsMvpMap,
    content.characterBlueprint,
    content.characterAnimBlueprint,
  ].filter(Boolean);

  if (content.skeletalMeshFromCharacterConfig) {
    const charCfgAbs = path.join(projectRoot, config.repo?.characterConfigPath || '');
    if (fs.existsSync(charCfgAbs)) {
      try {
        const charCfg = JSON.parse(fs.readFileSync(charCfgAbs, 'utf8'));
        if (charCfg.skeletal_mesh) paths.push(charCfg.skeletal_mesh);
      } catch (_) {
        /* covered by repo check */
      }
    }
  }

  for (const gamePath of paths) {
    if (!assetExistsOnDisk(gamePath)) {
      blockers.push({
        code: 'ASSET_MISSING_ON_DISK',
        message: config.blockerCodes?.ASSET_MISSING_ON_DISK || 'Asset missing on disk',
        detail: gamePath,
      });
    }
  }
  return blockers;
}

/** @returns {{ blockers: Blocker[], warnings: string[] }} */
function mergeEditorResults(config) {
  /** @type {Blocker[]} */
  const blockers = [];
  /** @type {string[]} */
  const warnings = [];
  const rel = config.editor?.resultFile || 'Saved/preflight_ue_editor.json';
  const abs = path.join(projectRoot, rel);

  if (!fs.existsSync(abs)) {
    return { blockers, warnings, missing: true };
  }

  try {
    const data = JSON.parse(fs.readFileSync(abs, 'utf8'));
    if (Array.isArray(data.blockers)) {
      for (const b of data.blockers) {
        if (b && b.code) blockers.push(b);
      }
    }
    if (data.ok === false && blockers.length === 0 && data.message) {
      blockers.push({ code: 'EDITOR_RESULTS_MISSING', message: data.message });
    }
    return { blockers, warnings, missing: false };
  } catch (err) {
    blockers.push({
      code: 'EDITOR_RESULTS_MISSING',
      message: 'Could not parse editor preflight results',
      detail: err.message,
    });
    return { blockers, warnings, missing: false };
  }
}

function describeBlocker(config, blocker) {
  const hint = config.blockerCodes?.[blocker.code];
  const parts = [`✗ [${blocker.code}] ${blocker.message}`];
  if (blocker.detail) parts.push(`    detail: ${blocker.detail}`);
  if (hint && hint !== blocker.message) parts.push(`    hint: ${hint}`);
  return parts.join('\n');
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    printHelp();
    process.exit(0);
  }

  const config = loadConfig();
  /** @type {Blocker[]} */
  const blockers = [];
  /** @type {string[]} */
  const warnings = [];

  console.log(`--- ${PREFIX} ---`);
  console.log(`mode: ${opts.assetsOnly ? 'assets-only (repo)' : opts.skipMcp ? 'repo+disk (skip MCP)' : 'full'}`);

  if (opts.simulateFail) {
    const msg = config.blockerCodes?.[opts.simulateFail] || `Simulated failure: ${opts.simulateFail}`;
    blockers.push({ code: opts.simulateFail, message: msg, detail: 'simulate-fail' });
  }

  blockers.push(...checkRepo(config));
  console.log(`repo checks: ${blockers.length ? 'FAIL' : 'PASS'}`);

  if (!opts.assetsOnly) {
    const mcp = config.mcp || {};
    if (!opts.skipMcp) {
      const reachable = await probeTcp(mcp.host || '127.0.0.1', mcp.port || 55557, mcp.timeoutMs || 3000);
      if (!reachable) {
        blockers.push({
          code: 'MCP_UNREACHABLE',
          message: config.blockerCodes?.MCP_UNREACHABLE || 'MCP unreachable',
          detail: `${mcp.host}:${mcp.port}`,
        });
        console.log('MCP probe: FAIL');
      } else {
        console.log('MCP probe: PASS');
      }
    } else {
      console.log('MCP probe: SKIPPED');
    }

    const diskBlockers = checkDiskAssets(config);
    blockers.push(...diskBlockers);
    console.log(`disk asset checks: ${diskBlockers.length ? 'FAIL' : 'PASS'}`);

    const editorMerge = mergeEditorResults(config);
    if (editorMerge.warnings.length) warnings.push(...editorMerge.warnings);
    if (editorMerge.missing) {
      const msg =
        'Editor deep-check results not found — run Content/Python/preflight_ue_editor.py via MCP on DESKTOP';
      if (opts.requireEditor) {
        blockers.push({
          code: 'EDITOR_RESULTS_MISSING',
          message: config.blockerCodes?.EDITOR_RESULTS_MISSING || msg,
          detail: config.editor?.resultFile,
        });
        console.log('editor JSON: FAIL (required, missing)');
      } else {
        warnings.push(msg);
        console.log('editor JSON: SKIP (optional — use --require-editor on DESKTOP before PIE)');
      }
    } else {
      blockers.push(...editorMerge.blockers);
      console.log(`editor JSON: ${editorMerge.blockers.length ? 'FAIL' : 'PASS'}`);
    }
  } else {
    console.log('MCP probe: SKIPPED (assets-only)');
    console.log('disk asset checks: SKIPPED (assets-only)');
    console.log('editor JSON: SKIPPED (assets-only)');
  }

  if (warnings.length) {
    console.log('');
    console.log('Warnings:');
    for (const w of warnings) console.log(`  ⚠ ${w}`);
  }

  console.log('');
  if (blockers.length === 0) {
    console.log(`${PREFIX} exit: 0 (PASS)`);
    process.exit(0);
  }

  console.log(`Blockers (${blockers.length}):`);
  for (const b of blockers) console.log(describeBlocker(config, b));
  console.log('');
  console.log(`${PREFIX} exit: 1 (FAIL — fix blockers before PIE / verb greps)`);
  process.exit(1);
}

main().catch((err) => {
  console.error(`${PREFIX} — unexpected error: ${err.message}`);
  process.exit(2);
});
