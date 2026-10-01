#!/usr/bin/env node
/**
 * Tests for the decision-log enforcement check.
 *
 * A record nothing checks is a suggestion. This is the part that makes the
 * 2026-10-01 ownership reset safe: the reset removed the human stamp on
 * architecture and harness decisions, so the written record is now the only
 * evidence that a decision was ever made.
 *
 * The tests build a throwaway git repo rather than mocking, because the failure
 * modes here are all in the git plumbing (NUL bytes in args, `--name-only` framing,
 * merge commits) and a mock would not exercise them.
 */

const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const D = require('./decision-log.js');

const created = [];
process.on('exit', () => {
  for (const d of created) {
    try {
      fs.rmSync(d, { recursive: true, force: true });
    } catch {
      /* best effort */
    }
  }
});

function git(repo, args) {
  return spawnSync('git', args, {
    cwd: repo,
    encoding: 'utf8',
    // Identity is passed per-command: relying on a global config would make the
    // test pass or fail depending on whose machine it runs on.
    ...(args[0] === 'commit' ? ['-c'] : []),
  });
}

function makeRepo() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'declog-'));
  created.push(dir);
  const g = (args) => {
    const r = spawnSync('git', args, { cwd: dir, encoding: 'utf8' });
    assert.strictEqual(r.status, 0, `git ${args.join(' ')} failed: ${r.stderr || r.stdout}`);
    return r.stdout;
  };
  g(['init', '-q', '-b', 'main']);
  g(['config', 'user.email', 'test@example.invalid']);
  g(['config', 'user.name', 'Test']);
  return { dir, g };
}

function write(dir, rel, content) {
  const full = path.join(dir, rel);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, content, 'utf8');
}

function commit(g, message) {
  g(['add', '-A']);
  g(['commit', '-q', '-m', message]);
  return g(['rev-parse', 'HEAD']).trim();
}

const DEC_HEADING = '### DEC-0001 — a logged decision\n\n- **Area:** harness refactor\n- **Decision:** something\n';

test('boundary path matching covers dirs and exact files', () => {
  assert.ok(D.isBoundaryPath('scripts/task-lift.js'));
  assert.ok(D.isBoundaryPath('scripts/deep/nested/file.js'));
  assert.ok(D.isBoundaryPath('AGENTS.md'));
  assert.ok(D.isBoundaryPath('package.json'));
  assert.ok(D.isBoundaryPath('.cursor/rules/01-x.mdc'));
  assert.ok(!D.isBoundaryPath('docs/KNOWN_ERRORS.md'));
  assert.ok(!D.isBoundaryPath('Content/HomeWorld/Meshes/M_Cabin.uasset'));
  // A sibling that merely starts with the same letters is not the boundary file.
  assert.ok(!D.isBoundaryPath('scripts-legacy/thing.js'));
});

test('a boundary change with no DEC entry is a violation', () => {
  const { dir, g } = makeRepo();
  write(dir, D.DECISION_LOG, '# Log\n');
  const base = commit(g, 'chore: seed');
  write(dir, 'scripts/thing.js', 'module.exports = 1;\n');
  commit(g, 'feat: add a script with no recorded reason');

  const res = D.findUnlogged({ repo: dir, base, head: 'HEAD' });
  assert.ok(res.ok);
  assert.strictEqual(res.violations.length, 1, 'expected exactly one violation');
  assert.match(res.violations[0].subject, /no recorded reason/);
  assert.ok(res.violations[0].files.includes('scripts/thing.js'));
});

test('a DEC entry in the same commit clears the violation', () => {
  const { dir, g } = makeRepo();
  write(dir, D.DECISION_LOG, '# Log\n');
  const base = commit(g, 'chore: seed');
  write(dir, 'scripts/thing.js', 'module.exports = 1;\n');
  write(dir, D.DECISION_LOG, `# Log\n\n${DEC_HEADING}`);
  commit(g, 'feat: add a script and say why');

  const res = D.findUnlogged({ repo: dir, base, head: 'HEAD' });
  assert.strictEqual(res.violations.length, 0, 'a same-commit entry must clear it');
});

test('a DEC entry does NOT retroactively cover an earlier commit', () => {
  // This is the permissiveness that got removed. One entry appended at the end of
  // a branch used to excuse everything before it, which made the check decorative.
  const { dir, g } = makeRepo();
  write(dir, D.DECISION_LOG, '# Log\n');
  const base = commit(g, 'chore: seed');
  write(dir, 'scripts/thing.js', 'module.exports = 1;\n');
  commit(g, 'feat: unlogged change');
  write(dir, D.DECISION_LOG, `# Log\n\n${DEC_HEADING}`);
  commit(g, 'docs: log it much later');

  const res = D.findUnlogged({ repo: dir, base, head: 'HEAD' });
  assert.strictEqual(
    res.violations.length,
    1,
    'a later entry must not excuse an earlier unlogged change'
  );
});

test('a non-boundary change needs no DEC entry', () => {
  const { dir, g } = makeRepo();
  write(dir, D.DECISION_LOG, '# Log\n');
  const base = commit(g, 'chore: seed');
  write(dir, 'Content/HomeWorld/Meshes/M_Cabin.uasset', 'binary-ish');
  write(dir, 'docs/KNOWN_ERRORS.md', '# Known Errors\n');
  commit(g, 'docs: content only');

  const res = D.findUnlogged({ repo: dir, base, head: 'HEAD' });
  assert.strictEqual(res.violations.length, 0);
});

test('an empty range is clean', () => {
  const { dir, g } = makeRepo();
  write(dir, D.DECISION_LOG, '# Log\n');
  const base = commit(g, 'chore: seed');
  const res = D.findUnlogged({ repo: dir, base, head: 'HEAD' });
  assert.ok(res.ok);
  assert.strictEqual(res.violations.length, 0);
  assert.strictEqual(res.commits, 0);
});

test('a missing base ref is an error, not a silent pass', () => {
  const { dir, g } = makeRepo();
  write(dir, D.DECISION_LOG, '# Log\n');
  commit(g, 'chore: seed');
  const res = D.findUnlogged({ repo: dir, base: 'no-such-ref', head: 'HEAD' });
  assert.strictEqual(res.ok, false, 'an unresolvable range must not report clean');
});
