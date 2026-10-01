#!/usr/bin/env node
/**
 * Keyless tests for the task-lift runner.
 *
 * The dangerous bugs in an eval harness are the ones that manufacture a lift:
 * a glob that matches pre-existing files, a newOnly filter that lets the harness
 * arm pass on someone else's work, a check kind that fails open, or a denominator
 * that quietly shrinks. Each is pinned below.
 */

const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const M = require('./task-lift.js');

function fixture(files) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'tasklift-'));
  for (const [rel, content] of Object.entries(files)) {
    const full = path.join(dir, rel);
    fs.mkdirSync(path.dirname(full), { recursive: true });
    fs.writeFileSync(full, content, 'utf8');
  }
  return dir;
}

test('globToRegExp handles the patterns this manifest uses', () => {
  // `*` must NOT cross a path separator; `**/` must. Getting this backwards would
  // let a check match a file in an unrelated directory.
  assert.ok(M.globToRegExp('*.mdc').test('a.mdc'));
  assert.ok(!M.globToRegExp('*.mdc').test('rules/a.mdc'), '* must not cross a separator');
  assert.ok(M.globToRegExp('**/COMMIT_MSG.txt').test('COMMIT_MSG.txt'));
  assert.ok(M.globToRegExp('**/COMMIT_MSG.txt').test('deep/dir/COMMIT_MSG.txt'));
  assert.ok(M.globToRegExp('.cursor/rules/*.mdc').test('.cursor/rules/x.mdc'));
  assert.ok(!M.globToRegExp('.cursor/rules/*.mdc').test('other/x.mdc'));
  assert.ok(M.globToRegExp('**/*.ps1').test('Tools/b.ps1'));
});

test('listFiles skips .git but descends elsewhere', () => {
  const dir = fixture({ '.git/config': 'x', '.cursor/rules/a.mdc': 'x', 'Tools/b.ps1': 'x' });
  const files = M.listFiles(dir).sort();
  assert.ok(files.includes('.cursor/rules/a.mdc'));
  assert.ok(files.includes('Tools/b.ps1'));
  assert.ok(!files.some((f) => f.startsWith('.git')), 'must not walk into .git');
});

test('seed returns the post-seed file list, used as the newOnly baseline', () => {
  const dir = fixture({ 'keep.txt': 'x' });
  const before = M.seed(dir, { seed: { 'docs/NEW.md': 'hello' } });
  assert.ok(before.has('keep.txt'));
  assert.ok(before.has('docs/NEW.md'));
  assert.ok(fs.existsSync(path.join(dir, 'docs/NEW.md')));
});

test('newOnly excludes pre-existing files so the harness cannot pass on old work', () => {
  // This is the single most important test in the file: without it the `with`
  // condition scores 31 pre-existing rules as the agent's output.
  const dir = fixture({ '.cursor/rules/old.mdc': '---\nname: Old\n---\nGetPlayerState\n' });
  const before = M.seed(dir, {});
  const created = M.listFiles(dir).filter((f) => !before.has(f));
  const targets = M.matchFiles(dir, '.cursor/rules/*.mdc', created);
  assert.deepStrictEqual(targets, [], 'pre-existing rule must not be scored');

  fs.writeFileSync(path.join(dir, '.cursor/rules/new.mdc'), '---\nname: New\n---\nGetPlayerState\n', 'utf8');
  const after = M.listFiles(dir).filter((f) => !before.has(f));
  assert.deepStrictEqual(M.matchFiles(dir, '.cursor/rules/*.mdc', after), ['.cursor/rules/new.mdc']);
});

test('anyMatches fails closed when the target file is absent', () => {
  const dir = fixture({ 'a.txt': 'hello' });
  const r = M.evaluateCheck(dir, { kind: 'anyMatches', glob: '**/*.mdc', pattern: 'x', class: 'completion', label: 'l' }, new Set());
  assert.strictEqual(r.pass, false);
  assert.strictEqual(r.detail, 'no target file');
});

test('noneMatch fails closed too, rather than passing on absence', () => {
  // Vacuous truth would hand the ablated arm free passes for producing nothing.
  const dir = fixture({ 'a.txt': 'hello' });
  const r = M.evaluateCheck(dir, { kind: 'noneMatch', glob: '**/*.ps1', pattern: '&&', class: 'conformance', label: 'l' }, new Set());
  assert.strictEqual(r.pass, false);
});

test('matches and lacks operate on a fixed path and report absence', () => {
  const dir = fixture({ 'f.md': 'alpha\nbeta\n' });
  assert.strictEqual(M.evaluateCheck(dir, { kind: 'matches', path: 'f.md', pattern: 'beta', class: 'c', label: 'l' }, new Set()).pass, true);
  assert.strictEqual(M.evaluateCheck(dir, { kind: 'lacks', path: 'f.md', pattern: 'gamma', class: 'c', label: 'l' }, new Set()).pass, true);
  const missing = M.evaluateCheck(dir, { kind: 'matches', path: 'nope.md', pattern: 'x', class: 'c', label: 'l' }, new Set());
  assert.strictEqual(missing.pass, false);
  assert.strictEqual(missing.detail, 'file absent');
});

test('commitSubjectCase judges only the text after the conventional prefix', () => {
  const dir = fixture({ 'COMMIT_MSG.txt': 'fix(gate): stop false pass\n\nbody\n' });
  const r = M.evaluateCheck(dir, { kind: 'commitSubjectCase', glob: '**/COMMIT_MSG.txt', newOnly: true, class: 'conformance', label: 'l' }, new Set());
  assert.strictEqual(r.pass, true, r.detail);
});

test('commitSubjectCase fails on a shouted subject', () => {
  const dir = fixture({ 'COMMIT_MSG.txt': 'fix: Stop False Pass\n' });
  const r = M.evaluateCheck(dir, { kind: 'commitSubjectCase', glob: '**/COMMIT_MSG.txt', newOnly: true, class: 'conformance', label: 'l' }, new Set());
  assert.strictEqual(r.pass, false);
});

test('commitSubjectLength measures the first non-comment line', () => {
  const long = 'x'.repeat(80);
  const dir = fixture({ 'COMMIT_MSG.txt': `\n# a comment line that is quite long ${'y'.repeat(70)}\nfix: ${long}\n` });
  const r = M.evaluateCheck(dir, { kind: 'commitSubjectLength', glob: '**/COMMIT_MSG.txt', newOnly: true, max: 72, class: 'conformance', label: 'l' }, new Set());
  assert.strictEqual(r.pass, false);
  assert.ok(r.detail.startsWith('8'), r.detail);
});

test('an unknown check kind fails rather than silently passing', () => {
  const dir = fixture({ 'a.txt': 'x' });
  const r = M.evaluateCheck(dir, { kind: 'bogus', class: 'conformance', label: 'l' }, new Set());
  assert.strictEqual(r.pass, false);
  assert.match(r.detail, /unknown check kind/);
});

test('summary computes lift on conformance only, not on the control', () => {
  const results = [
    { taskId: 'a', condition: 'with', completion: 1, conformance: 1 },
    { taskId: 'a', condition: 'without', completion: 0.5, conformance: 0 },
    { taskId: 'b', condition: 'with', completion: 1, conformance: 0.5 },
    { taskId: 'b', condition: 'without', completion: 0.5, conformance: 0.5 },
  ];
  const s = M.summarize(results);
  assert.strictEqual(s.tasks, 2);
  assert.ok(Math.abs(s.completionWith - 1) < 1e-9);
  assert.ok(Math.abs(s.completionWithout - 0.5) < 1e-9);
  assert.ok(Math.abs(s.conformanceWith - 0.75) < 1e-9);
  assert.ok(Math.abs(s.conformanceWithout - 0.25) < 1e-9);
  assert.ok(Math.abs(s.lift - 0.5) < 1e-9);
});

test('summary lift is null when an arm produced nothing, not zero', () => {
  // A null lift must not read as "no difference".
  const s = M.summarize([{ taskId: 'a', condition: 'with', completion: 1, conformance: 1 }]);
  assert.strictEqual(s.lift, null);
});

test('summary counts timeouts and agent errors', () => {
  const s = M.summarize([
    { taskId: 'a', condition: 'with', completion: 1, conformance: 1, agent: { timedOut: true } },
    { taskId: 'a', condition: 'without', completion: 0, conformance: 0, agent: { error: 'boom' } },
  ]);
  assert.strictEqual(s.failures, 1);
  assert.strictEqual(s.agentErrors, 1);
});

test('the manifest declares a valid harness and both check classes', () => {
  const m = M.loadTasks();
  assert.ok(Array.isArray(m.tasks) && m.tasks.length >= 4, 'expected at least 4 tasks');
  for (const t of m.tasks) {
    assert.ok(t.id && t.prompt, `task ${t.id} missing id/prompt`);
    const classes = new Set(t.checks.map((c) => c.class));
    assert.ok(classes.has('completion'), `${t.id} has no completion control`);
    assert.ok(classes.has('conformance'), `${t.id} has no conformance checks`);
    for (const c of t.checks) {
      assert.ok(c.kind && c.label, `${t.id} has an unlabelled check`);
    }
  }
});

test('every manifest check kind is implemented', () => {
  // A typo'd kind fails closed, so it would silently depress one arm's score.
  const m = M.loadTasks();
  const dir = fixture({ 'a.txt': 'x' });
  const seen = new Set();
  for (const t of m.tasks) for (const c of t.checks) seen.add(c.kind);
  for (const kind of seen) {
    const r = M.evaluateCheck(dir, { ...c0(kind), class: 'c', label: 'l' }, new Set());
    assert.ok(!/unknown check kind/.test(r.detail || ''), `unimplemented check kind: ${kind}`);
  }
});

function c0(kind) {
  return { kind, path: 'a.txt', pattern: 'x', glob: '**/*.mdc' };
}

test('compilePattern accepts PCRE-style inline flags, which JS otherwise rejects', () => {
  // `(?i)` is PCRE. Handed straight to `new RegExp` it throws "Invalid group" and
  // aborts the entire run, so a manifest author writing it out of habit is fatal.
  const re = M.compilePattern('(?i)t0_m3|prove');
  assert.ok(re.test('the T0_M3 prove script'));
  assert.ok(re.flags.includes('i'));
  assert.ok(!re.source.startsWith('(?'), 'the inline group must be stripped');
});

test('compilePattern keeps multiline on by default and honours multiline:false', () => {
  assert.ok(M.compilePattern('^fix:').flags.includes('m'));
  assert.ok(!M.compilePattern('^fix:', { multiline: false }).flags.includes('m'));
  // With multiline off, ^ only ever matches the very start of the document.
  assert.ok(M.compilePattern('^fix:', { multiline: false }).test('fix: a\nfix: b'));
  assert.ok(!M.compilePattern('^fix:', { multiline: false }).test('\nfix: a'));
});

test('every manifest pattern compiles', () => {
  // A single invalid pattern would abort the run mid-task and shrink the denominator.
  for (const t of M.loadTasks().tasks) {
    for (const c of t.checks) {
      if (!c.pattern) continue;
      assert.doesNotThrow(() => M.compilePattern(c.pattern, c), `${t.id}: ${c.pattern}`);
    }
  }
});

test('resolveAgentBin finds the real exe behind the Windows .cmd shim', () => {
  // Node cannot exec a `.cmd` without a shell, and using shell:true would push the
  // prompts (backticks, quotes, parens) through cmd.exe as metacharacters.
  const bin = M.resolveAgentBin();
  if (process.platform !== 'win32') {
    assert.strictEqual(bin, 'opencode');
    return;
  }
  assert.ok(bin.endsWith('.exe'), `expected an .exe, got ${bin}`);
  assert.ok(fs.existsSync(bin), `resolved binary does not exist: ${bin}`);
});

test('resolveAgentBin falls back to the bare name when the exe is absent', () => {
  const env = { APPDATA: path.join(os.tmpdir(), 'definitely-not-here-xyz') };
  assert.strictEqual(M.resolveAgentBin(env, 'win32', env.APPDATA), 'opencode');
});

test('resolveAgentBin honours an explicit override first', () => {
  const bin = M.resolveAgentBin({ TASKLIFT_OPENCODE: '/custom/oc' }, 'linux', undefined);
  assert.strictEqual(bin, '/custom/oc');
});

test('firstLine tolerates a failed spawn instead of throwing', () => {
  // spawnSync('opencode') on Windows returns stdout undefined; calling .trim() on it
  // crashed the whole run after the tasks had already executed.
  assert.strictEqual(M.firstLine({ status: null, stdout: undefined }), 'unavailable');
  assert.strictEqual(M.firstLine({ stdout: '\n  opencode v2.0.18  \n' }), 'opencode v2.0.18');
});

test('readFlag returns null when absent and the value when present', () => {
  assert.strictEqual(M.readFlag(['--run', '--dry'], '--out-md'), null);
  assert.strictEqual(M.readFlag(['--run', '--out-md', 'a/b.md'], '--out-md'), 'a/b.md');
  // A trailing flag with no value must be null, not `undefined`, or the caller
  // would try to mkdir a directory named "undefined".
  assert.strictEqual(M.readFlag(['--run', '--out-md'], '--out-md'), null);
});

test('the write script runs the eval once, not twice', () => {
  // Running the agent suite twice to emit a JSON and a Markdown copy would double
  // the cost, and the expensive part is the agent sessions.
  const pkg = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'package.json'), 'utf8'));
  const cmd = pkg.scripts['tasklift:write'];
  const runs = (cmd.match(/task-lift\.js/g) || []).length;
  assert.strictEqual(runs, 1, `tasklift:write invokes the runner ${runs} times`);
  assert.ok(cmd.includes('--out-md') && cmd.includes('--out-json'), 'both outputs must be requested');
});

test('the ablation list covers the always-on agent context', () => {
  for (const p of ['AGENTS.md', '.cursor', '.agents', 'swarm']) {
    assert.ok(M.ABLATE_PATHS.includes(p), `ablation must remove ${p}`);
  }
});