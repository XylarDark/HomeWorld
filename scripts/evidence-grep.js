#!/usr/bin/env node
/**
 * HS-D / D19-C — Host-side verb evidence grep (no UE required).
 * Scores a Saved log (or any text file) for canonical gameplay prefixes.
 * Does not invent greps; MISSING means zero matches in the file.
 *
 * Usage:
 *   npm run evidence:grep -- --log Saved/Logs/HomeWorld.log
 *   npm run evidence:grep -- --log path/to.log --json Saved/hs_d_evidence_grep.json
 *   npm run evidence:grep -- --log path/to.log --strict   # exit 1 if any required MISSING
 *   npm run evidence:grep -- --log path/to.log --success-path  # D19-C success-path rows only
 *   npm run evidence:grep -- --stdin < path/to.log
 *
 * Exit: 0 report ok (or all PASS under --strict), 1 missing log / strict fail, 2 bad CLI
 */
const fs = require('fs');
const path = require('path');

const PREFIX = 'evidence:grep';

/** Canonical HS-D / VP-A / PL prefixes (order stable for tables). */
const DEFAULT_PREFIXES = [
  'FORM:',
  'FALLBACK:',
  'HEAL:',
  'NURTURE:',
  'DAWN:',
  'TAME:',
  'GATHER:',
  'STORE:',
  'INVENTORY:',
];

/**
 * D19-C — success-path substrings per prefix (--success-path mode).
 * FORM:/FALLBACK: use default prefix match (any line containing prefix).
 */
const SUCCESS_PATH_SUBSTRINGS = {
  'STORE:': 'STORE: deposit',
  'HEAL:': 'HEAL: success',
  'NURTURE:': 'NURTURE: success',
  'TAME:': 'TAME: offer accepted',
  'GATHER:': 'GATHER: RES_',
  'DAWN:': 'DAWN: persisted',
  'INVENTORY:': 'INVENTORY: dump begin',
};

/** Diagnostic-only markers — never PASS alone under --success-path. */
const SOFT_FAIL_MARKERS = [
  'component ready',
  'soft fail',
  'soft-reject',
  'blocked —',
  'offer blocked',
  'offer skipped',
  'deposit fail',
  'fail inventory',
  'fail stack',
  'need RES_',
  'pile empty',
  'reject unknown',
];

function parseArgs(argv) {
  const opts = {
    log: null,
    json: null,
    stdin: false,
    strict: false,
    successPath: false,
    prefixes: [...DEFAULT_PREFIXES],
    help: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') opts.help = true;
    else if (arg === '--stdin') opts.stdin = true;
    else if (arg === '--strict') opts.strict = true;
    else if (arg === '--success-path') opts.successPath = true;
    else if (arg === '--log') {
      opts.log = argv[++i];
      if (!opts.log) {
        console.error(`${PREFIX} — --log requires a path`);
        process.exit(2);
      }
    } else if (arg.startsWith('--log=')) opts.log = arg.slice('--log='.length);
    else if (arg === '--json') {
      opts.json = argv[++i];
      if (!opts.json) {
        console.error(`${PREFIX} — --json requires a path`);
        process.exit(2);
      }
    } else if (arg.startsWith('--json=')) opts.json = arg.slice('--json='.length);
    else if (arg === '--prefixes') {
      const raw = argv[++i];
      if (!raw) {
        console.error(`${PREFIX} — --prefixes requires comma-separated list`);
        process.exit(2);
      }
      opts.prefixes = raw.split(',').map((s) => s.trim()).filter(Boolean);
    } else if (arg.startsWith('--prefixes=')) {
      opts.prefixes = arg.slice('--prefixes='.length).split(',').map((s) => s.trim()).filter(Boolean);
    } else {
      console.error(`${PREFIX} — unknown argument: ${arg}`);
      process.exit(2);
    }
  }
  return opts;
}

function printHelp() {
  console.log(`Usage: node scripts/evidence-grep.js --log <file> [options]

Options:
  --log <path>           Log file to scan (Saved/Logs/HomeWorld.log typical)
  --stdin                Read log text from stdin instead of --log
  --json <path>          Write machine-readable report JSON
  --strict               Exit 1 if any required prefix has 0 matches
  --success-path         D19-C: count success-path lines only (not component ready / soft-fail)
  --prefixes a:,b:       Override default prefix list (comma-separated)
  -h, --help             Show this help

Default prefixes: ${DEFAULT_PREFIXES.join(' ')}

Exit codes: 0 ok, 1 missing file or --strict fail, 2 misconfiguration`);
}

function normalizeNewlines(text) {
  return String(text).replace(/\r\n/g, '\n').replace(/\r/g, '\n');
}

function isSoftFailLine(line) {
  return SOFT_FAIL_MARKERS.some((marker) => line.includes(marker));
}

/**
 * Count lines containing prefix as a token (case-sensitive, as UE_LOG emits).
 * @param {string} text
 * @param {string} prefix
 */
function countPrefix(text, prefix) {
  const lines = normalizeNewlines(text).split('\n');
  let count = 0;
  const excerpts = [];
  for (const line of lines) {
    if (line.includes(prefix)) {
      count += 1;
      if (excerpts.length < 3) excerpts.push(line.trim().slice(0, 240));
    }
  }
  return { count, excerpts };
}

/**
 * D19-C success-path scoring for a prefix.
 * @param {string} text
 * @param {string} prefix
 * @param {string} successSubstring
 */
function countSuccessPath(text, prefix, successSubstring) {
  const lines = normalizeNewlines(text).split('\n');
  let count = 0;
  const excerpts = [];
  for (const line of lines) {
    if (!line.includes(prefix)) continue;
    if (!line.includes(successSubstring)) continue;
    if (isSoftFailLine(line)) continue;
    count += 1;
    if (excerpts.length < 3) excerpts.push(line.trim().slice(0, 240));
  }
  return { count, excerpts };
}

function score(text, prefixes, options = {}) {
  const successPath = Boolean(options.successPath);
  return prefixes.map((prefix) => {
    const successSubstring = SUCCESS_PATH_SUBSTRINGS[prefix];
    const useSuccessPath = successPath && successSubstring;
    const { count, excerpts } = useSuccessPath
      ? countSuccessPath(text, prefix, successSubstring)
      : countPrefix(text, prefix);
    return {
      prefix,
      count,
      status: count > 0 ? 'PASS' : 'MISSING',
      mode: useSuccessPath ? 'success-path' : 'prefix',
      successPattern: useSuccessPath ? successSubstring : null,
      excerpts,
    };
  });
}

function printTable(rows, successPath) {
  const modeLabel = successPath ? ' (success-path mode)' : '';
  console.log(`${PREFIX} — prefix score${modeLabel}`);
  console.log('| Prefix | Count | Status |');
  console.log('|--------|------:|--------|');
  for (const row of rows) {
    console.log(`| \`${row.prefix}\` | ${row.count} | **${row.status}** |`);
  }
  const pass = rows.filter((r) => r.status === 'PASS').length;
  const missing = rows.length - pass;
  console.log(`${PREFIX} — summary: ${pass}/${rows.length} PASS, ${missing} MISSING`);
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    printHelp();
    process.exit(0);
  }
  if (!opts.stdin && !opts.log) {
    console.error(`${PREFIX} — require --log <path> or --stdin`);
    printHelp();
    process.exit(2);
  }
  if (opts.prefixes.length === 0) {
    console.error(`${PREFIX} — empty --prefixes`);
    process.exit(2);
  }

  let text;
  if (opts.stdin) {
    text = fs.readFileSync(0, 'utf8');
  } else {
    const abs = path.resolve(opts.log);
    if (!fs.existsSync(abs)) {
      console.error(`${PREFIX} — log not found: ${abs}`);
      process.exit(1);
    }
    text = fs.readFileSync(abs, 'utf8');
  }

  const rows = score(text, opts.prefixes, { successPath: opts.successPath });
  printTable(rows, opts.successPath);

  const report = {
    tool: PREFIX,
    version: 2,
    generatedAt: new Date().toISOString(),
    log: opts.stdin ? '(stdin)' : path.resolve(opts.log),
    strict: opts.strict,
    successPath: opts.successPath,
    rows,
    allPass: rows.every((r) => r.status === 'PASS'),
  };

  if (opts.json) {
    const outAbs = path.resolve(opts.json);
    fs.mkdirSync(path.dirname(outAbs), { recursive: true });
    fs.writeFileSync(outAbs, JSON.stringify(report, null, 2) + '\n', 'utf8');
    console.log(`${PREFIX} — wrote ${outAbs}`);
  }

  if (opts.strict && !report.allPass) {
    console.error(`${PREFIX} — --strict: one or more prefixes MISSING`);
    process.exit(1);
  }
  process.exit(0);
}

if (require.main === module) {
  main();
}

module.exports = {
  DEFAULT_PREFIXES,
  SUCCESS_PATH_SUBSTRINGS,
  SOFT_FAIL_MARKERS,
  score,
  countPrefix,
  countSuccessPath,
  normalizeNewlines,
  parseArgs,
  isSoftFailLine,
};
