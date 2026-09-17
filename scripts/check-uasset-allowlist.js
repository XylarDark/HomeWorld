#!/usr/bin/env node
/**
 * Warn when allowlisted UE assets (Docs/20) are missing on disk.
 * Does not fail CI by default — use --strict for exit 1.
 *
 * Usage:
 *   npm run check:uasset-allowlist
 *   npm run check:uasset-allowlist -- --strict
 */
const fs = require('fs');
const path = require('path');

const projectRoot = path.resolve(__dirname, '..');
const configPath = path.join(projectRoot, 'config', 'uasset-allowlist.json');
const PREFIX = 'check:uasset-allowlist';

function parseArgs(argv) {
  return { strict: argv.includes('--strict'), help: argv.includes('--help') || argv.includes('-h') };
}

function printHelp() {
  console.log(`Usage: node scripts/check-uasset-allowlist.js [--strict]

  Warns when required allowlisted assets from config/uasset-allowlist.json are absent.
  --strict  Exit 1 if any required asset is missing (default: exit 0 with warnings)`);
}

function loadConfig() {
  if (!fs.existsSync(configPath)) {
    console.error(`${PREFIX} — missing ${configPath}`);
    process.exit(2);
  }
  return JSON.parse(fs.readFileSync(configPath, 'utf8'));
}

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

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    printHelp();
    process.exit(0);
  }

  const config = loadConfig();
  const missing = [];

  for (const entry of config.requiredOnDisk || []) {
    if (!assetExistsOnDisk(entry.gamePath)) {
      missing.push(entry);
    }
  }

  if (missing.length === 0) {
    console.log(`${PREFIX} — OK: all ${(config.requiredOnDisk || []).length} required allowlisted asset(s) present on disk`);
    console.log(`${PREFIX} — policy: ${config.policyDoc} (gate: ${config.gateString})`);
    process.exit(0);
  }

  console.warn(`${PREFIX} — ${missing.length} required allowlisted asset(s) missing on disk:`);
  for (const m of missing) {
    const candidates = gamePathToDiskCandidates(m.gamePath);
    console.warn(`  - ${m.label}: ${m.gamePath}`);
    console.warn(`    expected one of: ${candidates.join(', ')}`);
  }
  console.warn(`${PREFIX} — run \`${config.gitLfsInstallHint}\` or DESKTOP bootstrap (see ${config.policyDoc})`);

  process.exit(opts.strict ? 1 : 0);
}

main();
