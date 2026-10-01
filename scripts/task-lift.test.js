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

const TASTE_MANIFEST = path.join(__dirname, 'task-lift', 'tasks-taste.json');

const fixtureDirs = [];

// Without this, every run leaves one `tasklift-*` directory in %TEMP%. 147 had
// accumulated; a stale fixture is indistinguishable from a real leftover worktree.
process.on('exit', () => {
  for (const dir of fixtureDirs) {
    try {
      fs.rmSync(dir, { recursive: true, force: true });
    } catch {
      /* best effort */
    }
  }
});

function fixture(files) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'tasklift-'));
  fixtureDirs.push(dir);
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
    { taskId: 'a', condition: 'with', voided: false, completion: 1, conformance: 1, agent: { status: null, timedOut: true } },
    { taskId: 'a', condition: 'without', voided: true, completion: 0, conformance: 0, agent: { status: 0, error: 'boom' } },
  ]);
  assert.strictEqual(s.failures, 1);
  // A timeout is also an unclean exit, so it counts in both; `boom` counts once.
  assert.strictEqual(s.agentErrors, 2);
  assert.strictEqual(s.voidedRuns, 1);
  assert.strictEqual(s.lift, null, 'a timed-out run must not produce a lift');
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

test('every script that spends agent sessions says --run explicitly', () => {
  // The old default was to run agents unless --dry was passed, so asking for a
  // report cost eight sessions. Every spending entry point must now opt in, or the
  // guard is bypassed and nobody notices.
  const pkg = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'package.json'), 'utf8'));
  const spending = Object.entries(pkg.scripts).filter(
    ([name, cmd]) => /scripts\/task-lift\.js/.test(cmd) && !name.includes('dry') && !name.includes('test')
  );
  assert.ok(spending.length > 0, 'expected at least one spending script');
  for (const [name, cmd] of spending) {
    assert.ok(
      /(^|\s)--run(\s|$)/.test(cmd),
      `${name} spends agent sessions without --run: ${cmd}`
    );
  }
});

test('the runner refuses to spend without --run', () => {
  // Behavioural proof of the guard, not just a grep of package.json.
  const { spawnSync } = require('node:child_process');
  const r = spawnSync(
    process.execPath,
    [path.join(__dirname, 'task-lift.js'), '--out-md', path.join(os.tmpdir(), 'must-not-exist.md')],
    { encoding: 'utf8', cwd: path.join(__dirname, '..') }
  );
  assert.strictEqual(r.status, 2, 'must exit 2 without --run');
  assert.match(r.stderr, /refusing to start agent sessions/);
});

test('both manifests declare a control for every task', () => {
  for (const file of [M.MANIFEST, TASTE_MANIFEST]) {
    for (const t of M.loadTasks(file).tasks) {
      assert.ok(t.control && Object.keys(t.control).length > 0, `${file} / ${t.id} has no control`);
    }
  }
});

test('the ablation list covers the always-on agent context', () => {
  for (const p of ['AGENTS.md', '.cursor', '.agents', 'swarm']) {
    assert.ok(M.ABLATE_PATHS.includes(p), `ablation must remove ${p}`);
  }
});

// ---------------------------------------------------------------------------
// Regressions from the 2026-10-01 pilot, which reported lift 0.25 while all
// eight agents had been rejected by the provider and had done nothing at all.
// ---------------------------------------------------------------------------

test('extractAgentError finds the real reason in the event stream', () => {
  // spawnSync gives no `error` for a clean non-zero exit. The reason is an event.
  const stdout = [
    '{"type":"step_start","timestamp":1,"sessionID":"s","part":{}}',
    '{"type":"error","timestamp":2,"sessionID":"s","error":{"type":"provider.quota","message":"Rate limit exceeded. Please try again later.","status":429}}',
  ].join('\n');
  const err = M.extractAgentError(stdout, '');
  assert.match(err, /Rate limit exceeded/);
  assert.match(err, /429/, 'the provider status code must survive');
  assert.match(err, /provider\.quota/, 'the error type must survive');
});

test('extractAgentError ignores noise and survives a partial line', () => {
  assert.strictEqual(M.extractAgentError('{"type":"step_start","part":{}}\n', ''), null);
  // A truncated last line must not throw and must not invent an error.
  assert.strictEqual(M.extractAgentError('{"type":"error","error":', ''), null);
});

test('a clean non-zero exit counts as an agent error', () => {
  // The exact bug: `error` was only set from r.error, so 8 quota-blocked runs
  // reported agentErrors 0 and the failure looked like a weak result.
  const s = M.summarize([
    { taskId: 't', condition: 'with', voided: true, conformance: 0, completion: 0, agent: { status: 1, error: null } },
  ]);
  assert.strictEqual(s.agentErrors, 1, 'a non-zero exit with no spawn error is still an error');
  assert.strictEqual(s.voidedRuns, 1);
});

test('summarize refuses a lift when any run is void', () => {
  // A lift over a partial set reads as data. It must be null, not a number.
  const s = M.summarize([
    { taskId: 'a', condition: 'with', voided: false, conformance: 1, completion: 1, agent: { status: 0, error: null } },
    { taskId: 'a', condition: 'without', voided: true, conformance: 0, completion: 0, agent: { status: 1, error: 'x' } },
  ]);
  assert.strictEqual(s.lift, null, 'lift must be null when any run is void');
  assert.strictEqual(s.validRuns, 1);
  assert.strictEqual(s.voidedRuns, 1);
});

test('summarize still reports a lift when every run is valid', () => {
  const s = M.summarize([
    { taskId: 'a', condition: 'with', voided: false, conformance: 0.75, completion: 1, agent: { status: 0, error: null } },
    { taskId: 'a', condition: 'without', voided: false, conformance: 0.25, completion: 1, agent: { status: 0, error: null } },
  ]);
  assert.strictEqual(s.lift, 0.5);
  assert.strictEqual(s.voidedRuns, 0);
});

test('every glob check in the manifest is newOnly', () => {
  // The exact bug: `ue58-rule` omitted newOnly on all 9 checks, so they matched the
  // 31 pre-existing .cursor/rules/*.mdc. The harness arm won by matching files it
  // never wrote — precisely the confound the ablation exists to remove.
  const tasks = M.loadTasks().tasks;
  const offenders = [];
  for (const task of tasks) {
    for (const c of task.checks) {
      if (!c.glob) continue; // path-based checks are seeded by the task itself
      if (c.newOnly === true) continue;
      if (c.newOnlyIntent) continue; // explicit whole-tree opt-out
      offenders.push(`${task.id}/${c.label}`);
    }
  }
  assert.deepStrictEqual(offenders, [], `glob checks must be newOnly: ${offenders.join(', ')}`);
});

test('newOnly actually withholds pre-existing files', () => {
  // Behavioural proof for the guard above: a seeded file must not satisfy a check.
  const dir = fixture({ '.cursor/rules/old.mdc': 'name: old\ndescription: old\n' });
  const seeded = M.seed(dir, {});
  fs.writeFileSync(path.join(dir, '.cursor/rules/new.mdc'), 'name: new\n', 'utf8');
  const check = { kind: 'anyMatches', glob: '.cursor/rules/*.mdc', newOnly: true, pattern: 'name:' };
  const res = M.evaluateCheck(dir, check, seeded);
  assert.strictEqual(res.pass, true, 'passes on the file the agent created');
  // Now delete the new file: the check must fail rather than fall back to `old.mdc`.
  fs.unlinkSync(path.join(dir, '.cursor/rules/new.mdc'));
  const after = M.evaluateCheck(dir, check, seeded);
  assert.strictEqual(after.pass, false, 'must not fall back to a pre-existing file');
});

// ---------------------------------------------------------------------------
// 2026-10-01: the three gaps found while auditing the instrument against the
// harness best practices. Each of these could produce a confident wrong number.
// ---------------------------------------------------------------------------

test('verifyAblation reports a surviving harness surface as a failure', () => {
  // The whole experiment is unfalsifiable without this. If a delete half-fails, the
  // "without harness" arm is a "with harness" arm in disguise, the arms agree, and
  // the finding is "no effect" — silently, and in the comfortable direction.
  const survivors = {};
  for (const p of M.ABLATE_PATHS) survivors[p] = 'x';
  const dirty = fixture(survivors);
  const v = M.verifyAblation(dirty);
  assert.strictEqual(v.ok, false, 'a surviving surface must fail the check');
  assert.deepStrictEqual(v.present.slice().sort(), M.ABLATE_PATHS.slice().sort());
  assert.strictEqual(v.checked, M.ABLATE_PATHS.length);
});

test('verifyAblation passes when every surface is gone', () => {
  const clean = fixture({ 'README.md': 'no harness here' });
  const v = M.verifyAblation(clean);
  assert.strictEqual(v.ok, true);
  assert.deepStrictEqual(v.present, []);
  assert.ok(v.fileCount > 0, 'the file count is recorded so a reader can compare arms');
});

test('every task control fixture scores 100%', () => {
  // The positive control. Without it, a check whose pattern can never be satisfied
  // reports a permanent 0% that reads as "the harness does not help" rather than
  // "the instrument cannot register success".
  for (const task of M.loadTasks().tasks) {
    const r = M.scoreControl(task);
    const failed = r.checks.filter((c) => !c.pass).map((c) => `${c.label} (${c.verdict})`);
    assert.strictEqual(
      r.ok,
      true,
      `control for ${task.id} did not reach 100%: ${r.reason} -> ${failed.join('; ')}`
    );
    assert.strictEqual(r.rate, 1);
  }
});

test('a task with no control fixture is reported, not silently skipped', () => {
  const r = M.scoreControl({ id: 'x', checks: [] });
  assert.strictEqual(r.ok, false);
  assert.match(r.reason, /no control fixture/);
});

test('declaresScope accepts a live rule that scopes via globs', () => {
  const dir = fixture({
    '.cursor/rules/a.mdc':
      '---\nname: "x"\ndescription: "a live rule"\nalwaysApply: false\nglobs: "src/**/*.cpp"\n---\n\nbody\n',
  });
  const r = M.evaluateCheck(dir, { kind: 'declaresScope', glob: '.cursor/rules/*.mdc' }, new Set());
  assert.strictEqual(r.pass, true);
  assert.strictEqual(r.verdict, 'pass');
});

test('declaresScope accepts a tombstone that declares retirement in description', () => {
  // Three rules in this repo are deliberate tombstones with alwaysApply:false and no
  // globs. Requiring globs of them would push a future agent to "fix" a retired rule
  // back into an always-on load.
  const dir = fixture({
    '.cursor/rules/b.mdc':
      '---\nname: "x RETIRED"\ndescription: "RETIRED P4. Do not restore this duplicate card."\nalwaysApply: false\n---\n\nbody\n',
  });
  const r = M.evaluateCheck(dir, { kind: 'declaresScope', glob: '.cursor/rules/*.mdc' }, new Set());
  assert.strictEqual(r.pass, true);
  assert.strictEqual(r.verdict, 'soft_fail', 'a tombstone is a weak pass, not a clean one');
});

test('declaresScope rejects a live rule with neither globs nor a tombstone note', () => {
  const dir = fixture({
    '.cursor/rules/c.mdc':
      '---\nname: "x"\ndescription: "a live rule"\nalwaysApply: false\n---\n\nbody\n',
  });
  const r = M.evaluateCheck(dir, { kind: 'declaresScope', glob: '.cursor/rules/*.mdc' }, new Set());
  assert.strictEqual(r.pass, false);
  assert.strictEqual(r.verdict, 'closed_fail');
});

test('declaresScope is void, not failed, when the agent wrote no rule', () => {
  const dir = fixture({});
  const r = M.evaluateCheck(dir, { kind: 'declaresScope', glob: '.cursor/rules/*.mdc' }, new Set());
  assert.strictEqual(r.verdict, 'void', 'no file is not the same as a wrong file');
});

test('commitSubjectNoPeriod judges the subject, not the end of the file', () => {
  // The old check was a `noneMatch` on `\.\s*$`, which reads end-of-string. A
  // well-formed message whose body ended in a sentence failed a check labelled
  // "subject has no trailing period".
  const ok = fixture({ 'COMMIT_MSG.txt': 'fix: correct the prove script\n\nThe body ends in a sentence.\n' });
  assert.strictEqual(
    M.evaluateCheck(ok, { kind: 'commitSubjectNoPeriod', glob: '**/COMMIT_MSG.txt' }, new Set()).pass,
    true,
    'a body ending in a period must not fail a subject check'
  );
  const bad = fixture({ 'COMMIT_MSG.txt': 'fix: correct the prove script.\n\nbody\n' });
  const r = M.evaluateCheck(bad, { kind: 'commitSubjectNoPeriod', glob: '**/COMMIT_MSG.txt' }, new Set());
  assert.strictEqual(r.pass, false);
  assert.match(r.detail, /subject ends with a period/);
});

test('an absent subject is void across every check kind that looks for a file', () => {
  // One rule, applied uniformly: "no target" is never "wrong target".
  const dir = fixture({});
  for (const kind of ['anyMatches', 'noneMatch', 'declaresScope', 'anyNewFiles']) {
    const r = M.evaluateCheck(dir, { kind, glob: '**/*.mdc' }, new Set());
    assert.strictEqual(r.verdict, 'void', `${kind} must be void when nothing exists`);
  }
});

// ---------------------------------------------------------------------------
// The taste-beat benchmark, and the P0 runner guarantees.
// ---------------------------------------------------------------------------

test('the taste-beat benchmark controls all reach 100%', () => {
  // The chore set is at ceiling - both arms already do those jobs. The taste beats
  // are the real benchmark, and they are only meaningful if a correct answer can
  // score full marks. If one cannot, the task measures the check, not the harness.
  for (const task of M.loadTasks(TASTE_MANIFEST).tasks) {
    const r = M.scoreControl(task);
    const failed = r.checks.filter((c) => !c.pass).map((c) => `${c.label} (${c.verdict})`);
    assert.strictEqual(
      r.ok,
      true,
      `taste control ${task.id} did not reach 100%: ${r.reason} -> ${failed.join('; ')}`
    );
  }
});

test('a taste check actually rejects a wrong answer', () => {
  // A control reaching 100% only proves the checks CAN pass. It does not prove they
  // would catch a bad artifact. This is the other half: the same checks, scored
  // against a plausible-but-wrong answer, must fail.
  const bad = {
    'Docs/qa/art-master-ground.md':
      '# Ground material\n\nNew family `MAT_GrassScan` - photoreal scanned grass, PBR scan based.\nScale 1.\n',
  };
  const dir = fixture(bad);
  const seeded = M.seed(dir, {});
  const task = M.loadTasks(TASTE_MANIFEST).tasks.find((t) => t.id === 'art-master-spec');
  const results = task.checks.map((c) => M.evaluateCheck(dir, c, seeded));
  const passed = results.filter((r) => r.pass).length;
  assert.ok(
    passed < task.checks.length,
    `a photoreal new-family answer scored ${passed}/${task.checks.length}; the checks are too weak`
  );
  // Specifically, the two most important ones.
  const reuse = results.find((r) => r.label.includes('reuses an existing master'));
  const look = results.find((r) => r.label.includes('rejected look language'));
  assert.strictEqual(reuse.pass, false, 'must reject inventing a new master family');
  assert.strictEqual(look.pass, false, 'must reject photoreal scan language');
});

test('allLinesMatch fails when only some lines conform', () => {
  // The exact gap an `anyMatches` check would hide: five names, four right.
  const dir = fixture({ 'names.txt': 'SM_PathStone_B\nMAT_Planter\nSK_Moth\n' });
  const any_ = M.evaluateCheck(dir, { kind: 'anyMatches', path: 'names.txt', pattern: '^SM_' }, new Set());
  const all = M.evaluateCheck(
    dir,
    { kind: 'allLinesMatch', path: 'names.txt', pattern: '^(M_|SM_|SK_)[A-Za-z0-9_]+$' },
    new Set()
  );
  assert.strictEqual(any_.pass, true, 'anyMatches is satisfied by one good line - which is the bug');
  assert.strictEqual(all.pass, false, 'allLinesMatch must reject the list');
  assert.match(all.detail, /MAT_Planter/);
});

test('the manifest path is recorded so a report says which set it measured', () => {
  assert.strictEqual(M.loadTasks(TASTE_MANIFEST).manifestPath, TASTE_MANIFEST);
});

test('a dry run withholds the lift instead of reporting an artifact zero', () => {
  // In dry mode nothing is measured, so a conformance rate of 0 in both arms and a
  // "0pp lift" is an artifact of no agent running. Reporting it as a number is the
  // same class of error as scoring a crashed run.
  const s = M.summarize(
    [
      { taskId: 'a', condition: 'with', voided: false, conformance: 0, completion: 0, agent: { status: 0, error: null, attempts: 1 } },
      { taskId: 'a', condition: 'without', voided: false, conformance: 0, completion: 0, agent: { status: 0, error: null, attempts: 1 } },
    ],
    { dry: true }
  );
  assert.strictEqual(s.lift, null);
  assert.match(s.liftWithheld, /dry run/);
  assert.strictEqual(s.retries, 0, 'a first-try success is zero retries, never negative');
});

test('one void run voids its own cell, not the whole experiment', () => {
  // With 8 runs, a single timeout used to discard all eight. That made the
  // instrument too brittle to survive ordinary infrastructure noise.
  const ok = (taskId, condition, conf) => ({
    taskId,
    condition,
    voided: false,
    conformance: conf,
    completion: 1,
    agent: { status: 0, error: null, attempts: 1 },
  });
  const dead = (taskId, condition) => ({
    taskId,
    condition,
    voided: true,
    conformance: 0,
    completion: 0,
    agent: { status: 1, error: 'timeout', attempts: 3 },
  });
  const s = M.summarize([ok('a', 'with', 1), ok('a', 'without', 0.5), dead('b', 'with'), ok('b', 'without', 0.5)]);
  assert.strictEqual(s.voidedRuns, 1);
  // Task b is dropped because only one of its arms has a valid run. Comparing
  // a/with against a/without+b/without would be an unpaired comparison.
  assert.deepStrictEqual(s.droppedPairs, ['b']);
  assert.strictEqual(s.pairedTasks, 1);
  assert.strictEqual(s.lift, 0.5, 'the complete pair still yields a lift');
  assert.deepStrictEqual(s.validByCell, { 'a/with': 1, 'a/without': 1, 'b/with': 0, 'b/without': 1 });
  assert.strictEqual(s.retries, 2, 'the dead run took 3 attempts = 2 retries');
  assert.deepStrictEqual(s.missingCells, ['b/with']);
});

test('a task with only one valid arm is dropped rather than compared unpaired', () => {
  const s = M.summarize([
    { taskId: 'a', condition: 'with', voided: false, conformance: 1, completion: 1, agent: { status: 0, error: null, attempts: 1 } },
    { taskId: 'a', condition: 'without', voided: true, conformance: 0, completion: 0, agent: { status: 1, error: 'x', attempts: 1 } },
  ]);
  assert.strictEqual(s.lift, null, 'no complete pair means no lift');
  assert.deepStrictEqual(s.missingCells, ['a/without']);
  assert.deepStrictEqual(s.droppedPairs, ['a']);
});

test('min-valid-per-cell is enforced when repeats are in play', () => {
  const one = (condition, conf) => ({
    taskId: 'a',
    condition,
    voided: false,
    conformance: conf,
    completion: 1,
    agent: { status: 0, error: null, attempts: 1 },
  });
  const res = M.summarize([one('with', 1), one('without', 0)], { minValidPerCell: 3 });
  assert.strictEqual(res.lift, null, 'one trial per cell is below the minimum asked for');
  assert.strictEqual(res.shortCells.length, 2);
  assert.strictEqual(res.shortCells[0].required, 3);
});

test('noneMatch does not fire on a line that rejects the banned term', () => {
  // Found by the first real taste run: the correct answer said "not photoreal, not a
  // scan" - it was REJECTING the canon's banned look - and the naive noneMatch
  // failed it. A check that punishes stating the rule is a bad check.
  const check = {
    kind: 'noneMatch',
    glob: '**/spec.md',
    pattern: 'photoreal|grimdark|sci-?fi|pbr scan',
    unless: '(?i)\\b(not|never|no|avoid|without|refus\\w*|reject\\w*)\\b',
  };
  const rejecting = fixture({
    'spec.md': 'Roughness stays high. Not photoreal, no grimdark, never a pbr scan.\n',
  });
  assert.strictEqual(M.evaluateCheck(rejecting, check, new Set()).pass, true);

  const using = fixture({ 'spec.md': 'Roughness from a photoreal pbr scan of real grass.\n' });
  assert.strictEqual(M.evaluateCheck(using, check, new Set()).pass, false, 'genuine use must still fail');
});

test('noneMatch without an unless clause behaves as before', () => {
  const dir = fixture({ 'f.md': 'photoreal\n' });
  assert.strictEqual(M.evaluateCheck(dir, { kind: 'noneMatch', glob: '**/f.md', pattern: 'photoreal' }, new Set()).pass, false);
});

test('the NightMix range check accepts the ways people actually write it', () => {
  // Brittle phrasing matching measures punctuation, not knowledge. The first run
  // failed this because the agent declared NightMix without writing "0 to 1".
  const check = { kind: 'anyMatches', glob: '**/spec.md', pattern: '0\\s*(?:→|->|–|—|-|to|through)\\s*1' };
  for (const phrasing of ['NightMix 0→1', 'NightMix 0 to 1', 'NightMix 0-1', 'NightMix 0 – 1', 'NightMix 0 through 1']) {
    const dir = fixture({ 'spec.md': `${phrasing} shifts the masters.\n` });
    assert.strictEqual(
      M.evaluateCheck(dir, check, new Set()).pass,
      true,
      `should accept "${phrasing}"`
    );
  }
});

test('trials raise the minimum valid runs a cell needs', () => {
  // One trial per cell is noise-dominated: a single timeout or one unusual answer
  // moves the rate as much as any real effect. `--min-valid` defaults to the trial
  // count, so asking for 2 trials cannot be satisfied by 1.
  const one = (condition, conf) => ({
    taskId: 'a',
    condition,
    trial: 1,
    voided: false,
    conformance: conf,
    completion: 1,
    agent: { status: 0, error: null, attempts: 1 },
  });
  const two = (condition, conf, trial) => ({ ...one(condition, conf), trial });
  assert.strictEqual(M.summarize([one('with', 1), one('without', 0)], { minValidPerCell: 2 }).lift, null);
  assert.strictEqual(
    M.summarize([one('with', 1), one('with', 1), one('without', 0), two('without', 0, 2)], {
      minValidPerCell: 2,
    }).lift,
    1,
    'two valid runs per cell should satisfy the requirement'
  );
});

test('only transport failures are retried, never a substantive non-zero exit', () => {
  // Retrying a run that failed for a substantive reason would silently replace a
  // measurement with a more flattering one.
  assert.ok(M.isTransient('[error/provider.quota] (HTTP 429) Rate limit exceeded', false));
  assert.ok(M.isTransient('[error/provider] (HTTP 503) upstream unavailable', false));
  assert.ok(M.isTransient('socket hang up', false));
  assert.ok(M.isTransient('', true), 'a timeout is transport, not a result');
  assert.ok(!M.isTransient('[error/provider] the model refused to continue', false));
  assert.ok(!M.isTransient(null, false), 'no error is not a transport failure');
  assert.ok(!M.isTransient('exit 1', false));
});