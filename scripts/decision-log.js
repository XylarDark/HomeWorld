#!/usr/bin/env node
/**
 * Fail a boundary change that nobody wrote down.
 *
 * This is the enforcement half of the 2026-10-01 ownership reset. The reset moved
 * architecture, code design and harness refactoring from human-stamped to
 * agent-owned, and replaced the stamp with a written record in
 * Docs/decisions/AGENT_DECISIONS.md.
 *
 * A record nothing checks is a suggestion. The whole risk of removing a stamp is
 * that a decision gets made in the gap the stamp used to fill, and nobody can tell
 * later. So: if a commit moves a boundary, it must add a DEC-NNNN entry, in that
 * commit or a later one in the same range.
 *
 * Scope is deliberately narrow. This checks that the *record exists*, not that the
 * decision was good. Judging the reasoning is a human taste call; checking that
 * reasoning was written down is mechanical, and that is the part worth automating.
 *
 * Exit codes: 0 clean, 1 unlogged boundary change, 2 usage/base error.
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('node:child_process');

const PROJECT_ROOT = path.resolve(__dirname, '..');
const DECISION_LOG = 'Docs/decisions/AGENT_DECISIONS.md';
const DEC_HEADING = /^###\s+(DEC-\d{4})\b/m;

/**
 * Paths whose modification is a boundary change: a module moved, an always-on
 * instruction edited, a dependency or gate altered.
 *
 * This list is itself a boundary decision, so it is recorded in the log rather
 * than hidden here. Keep it to surfaces that change how later work behaves.
 */
const BOUNDARY_PATHS = [
  'AGENTS.md',
  'package.json',
  'docs/human-use/architecture.md',
  'docs/architecture/',
  '.cursor/rules/',
  '.agents/skills/',
  '.github/workflows/',
  'scripts/',
  'Config/',
];

function isBoundaryPath(file) {
  const f = file.replace(/\\/g, '/');
  return BOUNDARY_PATHS.some((p) => (p.endsWith('/') ? f.startsWith(p) : f === p));
}

function git(repo, args) {
  const r = spawnSync('git', args, { cwd: repo, encoding: 'utf8', maxBuffer: 32 * 1024 * 1024 });
  if (r.status !== 0) {
    return { ok: false, error: (r.stderr || r.stdout || '').trim() };
  }
  return { ok: true, out: r.stdout || '' };
}

/** Commits in `base..head`, oldest first, each with its changed files. */
function readCommits(repo, base, head) {
  // A space, not a NUL: spawnSync rejects arguments containing null bytes.
  // The hash is fixed-width hex, so the first space is an unambiguous split.
  const r = git(repo, ['log', '--format=%H %s', '--name-only', `${base}..${head}`]);
  if (!r.ok) return { ok: false, error: r.error };
  const out = r.out.trim();
  if (!out) return { ok: true, commits: [] };

  const commits = [];
  for (const chunk of out.split(/\n(?=[0-9a-f]{40} )/)) {
    const lines = chunk.split('\n').filter((l) => l.length);
    if (!lines.length) continue;
    const sp = lines[0].indexOf(' ');
    const hash = lines[0].slice(0, sp);
    const subject = lines[0].slice(sp + 1);
    const files = lines.slice(1).map((l) => l.trim()).filter(Boolean);
    commits.push({ hash, subject, files });
  }
  commits.reverse(); // oldest first: a log entry may come after the change
  return { ok: true, commits };
}

/** DEC ids added by a commit, read from that commit's diff of the log. */
function decsAddedBy(repo, hash) {
  const r = git(repo, ['show', '--format=', '--unified=0', hash, '--', DECISION_LOG]);
  if (!r.ok || !r.out) return [];
  const ids = new Set();
  for (const line of r.out.split('\n')) {
    if (!line.startsWith('+') || line.startsWith('+++')) continue;
    const m = DEC_HEADING.exec(line.slice(1));
    if (m) ids.add(m[1]);
  }
  return [...ids];
}

/**
 * Boundary commits with no DEC entry in the same commit.
 *
 * Same-commit only, deliberately. An earlier "a later entry covers it" rule was
 * tried and is decorative: one entry appended at the end of a branch excuses every
 * unlogged change before it, which is exactly the gap the check exists to close.
 * If a change and its reasoning genuinely cannot ship together, the honest fix is
 * to amend or squash, not to weaken the check.
 */
function findUnlogged({ repo = PROJECT_ROOT, base = 'main', head = 'HEAD' } = {}) {
  const read = readCommits(repo, base, head);
  if (!read.ok) return { ok: false, error: read.error };

  const violations = [];
  for (const c of read.commits) {
    const boundaryFiles = c.files.filter(isBoundaryPath);
    if (boundaryFiles.length === 0) continue;
    if (decsAddedBy(repo, c.hash).length > 0) continue;
    violations.push({ hash: c.hash.slice(0, 7), subject: c.subject, files: boundaryFiles });
  }
  return { ok: true, violations, commits: read.commits.length };
}

function main(argv) {
  const arg = (name, fallback) => {
    const i = argv.indexOf(name);
    return i !== -1 && argv[i + 1] ? argv[i + 1] : fallback;
  };
  const repo = path.resolve(arg('--repo', PROJECT_ROOT));
  const head = arg('--head', 'HEAD');
  let base = arg('--base', 'main');

  if (git(repo, ['rev-parse', '--verify', base]).ok !== true) {
    const m = git(repo, ['rev-parse', '--verify', 'origin/main']);
    if (m.ok) {
      base = 'origin/main';
    } else if (base !== head) {
      process.stderr.write(
        `decisions: base ref "${base}" not found and origin/main is unavailable.\n` +
          `  Pass an explicit range: --base <ref>  (e.g. --base HEAD~5)\n`
      );
      return 2;
    } else {
      base = `${head}~1`;
    }
  }

  const res = findUnlogged({ repo, base, head });
  if (!res.ok) {
    process.stderr.write(`decisions: ${res.error}\n`);
    return 2;
  }

  process.stdout.write(`# Decision-log check\n\n`);
  process.stdout.write(`- range: \`${base}..${head}\`\n`);
  process.stdout.write(`- commits scanned: ${res.commits}\n`);
  process.stdout.write(`- boundary surfaces: ${BOUNDARY_PATHS.map((p) => `\`${p}\``).join(', ')}\n\n`);

  if (res.violations.length === 0) {
    process.stdout.write(
      `Every boundary change in this range has a \`DEC-NNNN\` entry in ${DECISION_LOG}.\n`
    );
    return 0;
  }

  process.stdout.write(`## Unlogged boundary changes (${res.violations.length})\n\n`);
  process.stdout.write('| Commit | Subject | Boundary files |\n|---|---|---|\n');
  for (const v of res.violations) {
    process.stdout.write(
      `| \`${v.hash}\` | ${v.subject} | ${v.files.slice(0, 4).map((f) => `\`${f}\``).join(', ')}${v.files.length > 4 ? `, +${v.files.length - 4} more` : ''} |\n`
    );
  }
  process.stdout.write(
    `\nThese commits moved a module, an always-on instruction, a dependency or a gate ` +
      `without writing down why. Add a \`DEC-NNNN\` entry to ${DECISION_LOG} naming the ` +
      `alternative you rejected. Judging the reasoning stays a human call; recording it ` +
      `is mechanical.\n`
  );
  return 1;
}

if (require.main === module) process.exit(main(process.argv.slice(2)));

module.exports = { main, findUnlogged, isBoundaryPath, BOUNDARY_PATHS, DECISION_LOG };
