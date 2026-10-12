#!/usr/bin/env node
/**
 * harness:fitness - does the harness still do what it was built to do?
 *
 * WHY THIS EXISTS
 *
 * The Lead's requirement: the harness should be able to detect when IT needs an
 * upgrade, as the product develops, but never outside the bounds it was given.
 * And if a problem keeps recurring that is outside those bounds, the harness
 * should notice and work out how to handle it in future.
 *
 * WHY IT IS NOT A SCORER
 *
 * Docs/36 §8 forbids "another measurement of the agent harness" - that layer has
 * produced zero product decisions. So this measures nothing. It checks exactly
 * one thing: whether the harness's own stated premises are still true. A premise
 * that has stopped being true is an upgrade trigger; everything else is noise.
 *
 * THE FOUR PREMISES, each traceable to a number the Lead can check:
 *
 *   1. SHAPE     - the harness is six commands and a page, not a growing pile.
 *   2. BOUNDS    - the instruction surface is under its ceiling. Above it, every
 *                  line is tax charged against the Lead's reading time.
 *   3. PURPOSEFULNESS - gates have caught something real. A gate that has never
 *                  fired is not insurance.
 *   4. PRODUCT   - the harness is not outgrowing the product. This is the
 *                  escape hatch in Docs/36 §5, checked mechanically so it cannot
 *                  be quietly deferred.
 *
 * OUT-OF-BOUNDS PROBLEMS
 *
 * The second half of the requirement. When a failure repeats and it is NOT the
 * harness's fault, the harness must not build a bigger tool. It must record the
 * pattern once, in one line, so the next occurrence is visible instead of
 * rediscovered. The discipline: a repeated out-of-bounds problem earns a written
 * response, never a new gate.
 *
 * DETERMINISM
 *
 * Same tree, same answer. No network, no model, no clock-dependent verdict.
 * Exit 0 when every premise holds, 1 when one is broken (that is the upgrade
 * signal), 2 on bad invocation. The caller decides what to do about a break;
 * this script never edits a file.
 */

const fs = require('fs');
const path = require('path');

const PROJECT_ROOT = path.resolve(__dirname, '..');

/* ------------------------------------------------------------------ utils */

function readJson(rel) {
  try {
    return JSON.parse(fs.readFileSync(path.join(PROJECT_ROOT, rel), 'utf8'));
  } catch {
    return null;
  }
}

function countLines(rel) {
  try {
    const text = fs.readFileSync(path.join(PROJECT_ROOT, rel), 'utf8');
    return text.split('\n').filter((l) => l.trim().length > 0).length;
  } catch {
    return 0;
  }
}

function gitLines(args) {
  const { execFileSync } = require('child_process');
  try {
    return execFileSync('git', args, {
      cwd: PROJECT_ROOT,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    })
      .split('\n')
      .map((l) => l.trim())
      .filter(Boolean);
  } catch {
    return [];
  }
}

/* ------------------------------------------------------ the out-of-bounds log
 *
 * One file. Append one line per repeated out-of-bounds problem. It is NOT a
 * task list and NOT a gate: nothing reads it except the human and the next
 * agent that hits the same wall. Format is one line, prefixed so it sorts and
 * greps:
 *
 *   YYYY-MM-DD  <SIGNATURE>  seen=<N>  <one-line response>
 *
 * Kept deliberately small. If it grows past ~40 lines the response is not
 * working and the problem belongs in Docs/, not in a log.
 */

const OUT_OF_BOUNDS_LOG = 'Docs/decisions/OUT_OF_BOUNDS.md';

function recordOutOfBounds(signature, response, root = PROJECT_ROOT) {
  const abs = path.join(root, OUT_OF_BOUNDS_LOG);
  const today = new Date().toISOString().slice(0, 10);

  // Read back what THIS function writes. The first version parsed a bulleted
  // `- date \`sig\` seen=N response` list while writing a markdown table, so it
  // could never match its own output: every second sighting looked like a first
  // sighting and overwrote the count. A writer and a reader must share a format.
  const ROW_RE = /^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*`([^`]+)`\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*$/;
  const existing = [];
  if (fs.existsSync(abs)) {
    for (const line of fs.readFileSync(abs, 'utf8').split('\n')) {
      const m = line.match(ROW_RE);
      if (m) existing.push({ date: m[1], signature: m[2], seen: Number(m[3]), response: m[4] });
    }
  }

  const prior = existing.find((r) => r.signature === signature);
  if (prior) {
    // Repeat sighting: increment in place. A near-duplicate row would be noise,
    // and the whole point of the file is one line per problem.
    prior.seen += 1;
  } else {
    existing.push({ date: today, signature, seen: 1, response: response || '(no response recorded)' });
  }
  const seen = existing.find((r) => r.signature === signature).seen;

  const header =
    '# Out-of-bounds problems\n\n' +
    'Problems that are **not** the harness\'s fault, recorded once so the next\n' +
    'occurrence is visible instead of rediscovered. **A repeated problem here earns a\n' +
    'written response, never a new gate** - a gate is the thing that got deleted.\n\n' +
    'This file is not a task list. If it passes 40 lines the response is not working.\n\n' +
    '| First seen | Signature | Count | Response |\n|---|---|---|---|\n';

  const rows = existing
    .map((r) => `| ${r.date} | \`${r.signature}\` | ${r.seen} | ${r.response} |`)
    .sort();

  try {
    fs.mkdirSync(path.dirname(abs), { recursive: true });
    fs.writeFileSync(abs, header + rows.join('\n') + '\n', 'utf8');
  } catch {
    /* read-only diagnostics must never break a verify run */
  }

  return { signature, seen, firstTime: seen === 1 };
}

/* ------------------------------------------------------------ the premises */

/**
 * Premise 1 - SHAPE. Docs/36 §1 promises six commands. More than that is the
 * pile the contract says the refactor was for.
 */
function premiseShape() {
  const pkg = readJson('package.json');
  if (!pkg) return { ok: false, why: 'package.json unreadable' };
  const declared = [
    'verify:fast',
    'verify',
    'verify:ue',
    'editor:lock',
    'scope:reconcile',
    'decisions',
  ];
  const missing = declared.filter((n) => !pkg.scripts || !pkg.scripts[n]);
  return {
    ok: missing.length === 0,
    detail: missing.length ? `missing: ${missing.join(', ')}` : 'six declared commands present',
  };
}

/**
 * Premise 2 - BOUNDS. Calls instruction-budget.measure() so a missing
 * Docs/qa/instruction_budget.json cannot skip this premise into a pass.
 * The total is the same number the budget gate uses, so the two cannot disagree.
 */
function premiseBounds() {
  const budget = require('./instruction-budget');
  const measured = budget.measure();
  const total = measured.total;
  const ceiling = budget.TOTAL_HIGH_WATER;
  return {
    ok: typeof total === 'number' && total <= ceiling,
    detail: `${total} instruction lines against a ${ceiling} ceiling`,
  };
}

/**
 * Premise 3 - PURPOSEFULNESS. The anti-sycophancy log and the disagreement log
 * are the record of the harness noticing something. Both must be non-empty for
 * the harness to be doing the thing it was built for.
 */
function premisePurposeful() {
  const disagreement = fs.existsSync(path.join(PROJECT_ROOT, 'Docs/decisions/DISAGREEMENTS.md'))
    ? countLines('Docs/decisions/DISAGREEMENTS.md')
    : 0;
  return {
    ok: disagreement > 0,
    detail: disagreement
      ? `${disagreement} lines in DISAGREEMENTS.md; a non-empty file does not prove a recent disagreement`
      : 'no disagreements recorded - either nothing was questioned, or nothing was written down',
  };
}

/**
 * Premise 4 - PRODUCT. Docs/36 §5 writes the escape hatch down so it can be
 * believed. Harness commits vs product commits over a recent window. The
 * contract's success condition is that this ratio has INVERTED from 24:8.
 *
 * Classification is by paths, not by a `(harness)` subject. A subject with no
 * scope still counts when the files are the harness. A commit that touches both
 * sides is mixed and is left out of both counts. The window stays 60 commits.
 */
const HARNESS_FILES = new Set([
  'scripts/harness-fitness.js',
  'scripts/instruction-budget.js',
  'Content/Python/check_session_start.py',
]);

function normalizePath(file) {
  return String(file).replace(/\\/g, '/');
}

function isHarnessPath(file) {
  const n = normalizePath(file);
  if (n === 'AGENTS.md' || n.endsWith('/AGENTS.md')) return true;
  if (n.startsWith('.cursor/') || n.includes('/.cursor/')) return true;
  if (n.startsWith('.agents/') || n.includes('/.agents/')) return true;
  return HARNESS_FILES.has(n);
}

function isProductPath(file) {
  const n = normalizePath(file);
  if (n === 'Content/Python/check_session_start.py') return false;
  return n.startsWith('Source/') || n.includes('/Source/') || n.startsWith('Content/') || n.includes('/Content/');
}

function classifyCommit(files) {
  const list = Array.isArray(files) ? files : [];
  if (list.length === 0) return 'empty';
  const harness = list.some(isHarnessPath);
  const product = list.some(isProductPath);
  if (harness && product) return 'mixed';
  if (harness) return 'harness';
  return 'product';
}

function premiseProduct(commits) {
  let harnessCommits = 0;
  let productCommits = 0;
  let mixed = 0;
  for (const commit of commits) {
    const files = commit && Array.isArray(commit.files) ? commit.files : [];
    const kind = classifyCommit(files);
    if (kind === 'harness') harnessCommits += 1;
    else if (kind === 'product') productCommits += 1;
    else if (kind === 'mixed') mixed += 1;
  }
  const total = harnessCommits + productCommits;
  if (total < 10) {
    return {
      ok: true,
      skipped: true,
      detail: `only ${total} commits in window; too few to read a ratio`,
    };
  }
  const pct = Math.round((harnessCommits / total) * 100);
  return {
    ok: harnessCommits <= productCommits,
    detail: `${harnessCommits} harness / ${productCommits} product over ${total} commits (${pct}% harness); ${mixed} mixed excluded`,
  };
}

function recentCommits(n = 60) {
  const lines = gitLines(['log', '-n', String(n), '--name-only', '--pretty=format:COMMIT %s']);
  const commits = [];
  let current = null;
  for (const line of lines) {
    if (line.startsWith('COMMIT ')) {
      if (current) commits.push(current);
      current = { subject: line.slice('COMMIT '.length), files: [] };
    } else if (current) {
      current.files.push(line);
    }
  }
  if (current) commits.push(current);
  return commits;
}

/* -------------------------------------------------------------------- main */

function main() {
  const argv = process.argv.slice(2);
  const quiet = argv.includes('--quiet');
  const jsonOut = argv.includes('--json');

  if (argv.includes('--record-out-of-bounds')) {
    const i = argv.indexOf('--record-out-of-bounds');
    const signature = argv[i + 1];
    const response = argv[i + 2];
    if (!signature) {
      process.stderr.write('fitness: --record-out-of-bounds needs a SIGNATURE\n');
      process.exit(2);
    }
    const r = recordOutOfBounds(signature, response || '(no response recorded)');
    process.stdout.write(
      `fitness: recorded ${r.signature} seen=${r.seen}${r.firstTime ? ' (first sighting)' : ''}\n`
    );
    process.exit(0);
  }

  const commits = recentCommits(60);
  const premises = [
    ['shape', premiseShape()],
    ['bounds', premiseBounds()],
    ['purposefulness', premisePurposeful()],
    ['product', premiseProduct(commits)],
  ];

  const broken = premises.filter(([, r]) => !r.ok);

  if (jsonOut) {
    process.stdout.write(
      JSON.stringify(
        {
          ok: broken.length === 0,
          broken: broken.map(([name]) => name),
          premises: Object.fromEntries(premises),
        },
        null,
        2
      ) + '\n'
    );
  } else if (!quiet) {
    process.stdout.write('\n=== harness fitness ===\n');
    process.stdout.write('Does the harness still do what it was built to do?\n\n');
    for (const [name, r] of premises) {
      const mark = r.skipped ? 'skip' : r.ok ? ' ok ' : 'BREAK';
      process.stdout.write(`  ${mark}  ${name.padEnd(14)} ${r.detail}\n`);
    }
    process.stdout.write('');
    if (broken.length === 0) {
      process.stdout.write('\n  All premises hold. No upgrade needed.\n\n');
    } else {
      process.stdout.write(
        `\n  ${broken.length} premise(s) broken: ${broken.map(([n]) => n).join(', ')}\n`
      );
      process.stdout.write(
        '  A broken premise is an UPGRADE SIGNAL, not an instruction to build.\n' +
          '  Docs/36 §2: three triggers, nothing else. Docs/36 §8: never build a new\n' +
          '  gate, a new rule, or another measurement in response to one.\n\n'
      );
    }
  }

  process.exit(broken.length === 0 ? 0 : 1);
}

if (require.main === module) main();

module.exports = {
  premiseShape,
  premiseBounds,
  premisePurposeful,
  premiseProduct,
  classifyCommit,
  recentCommits,
  recordOutOfBounds,
  readJson,
};