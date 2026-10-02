const test = require('node:test');
const assert = require('node:assert');
const W = require('./write-serialisation.js');

test('a dirty tree fails, a clean tree passes', () => {
  // The precondition for silent loss is an unowned dirty tree: two agents cannot
  // both be right about it, and an uncommitted asset deletion is a permission
  // decision made by accident. OWNERSHIP.md reserves isolation and permissions for
  // the human, so the harness must not let an agent settle it by omission.
  const clean = { branch: 'b', dirty: false, trackedChanges: 0, files: [] };
  assert.strictEqual(W.evaluate(clean).errors.length, 0);

  const dirty = { branch: 'b', dirty: true, trackedChanges: 3, files: [' M a'] };
  const r = W.evaluate(dirty);
  assert.strictEqual(r.errors.length, 1, 'a dirty tree must fail');
  assert.match(r.errors[0], /uncommitted tracked change/);
  assert.match(r.errors[0], /--allow-dirty/, 'the error must say how to proceed');
});

test('the bypass is deliberate and leaves a record', () => {
  // A dirty tree is NORMAL during agent work - that is what an agent does. Failing
  // hard on it would make the gate useless within a day and it would get routed
  // around silently. So the bypass exists, and it is recorded rather than silent:
  // a guard that cannot be used gets bypassed; a guard that records its own use
  // gets reviewed.
  const dirty = { branch: 'b', dirty: true, trackedChanges: 2, files: [] };
  const bypassed = W.evaluate(dirty, { allowDirty: 'mid-refactor' });
  assert.strictEqual(bypassed.errors.length, 0, 'the bypass must work');
  assert.strictEqual(bypassed.warnings.length, 1, 'and it must warn');
  assert.match(bypassed.warnings[0], /mid-refactor/, 'and carry the reason');
});

test('untracked files do not block', () => {
  // Untracked output is generated Content, build artefacts and reports. Blocking on
  // those would fire constantly and protect nothing. The loss risk is a tracked
  // deletion or modification, which is what the gate counts.
  const { spawnSync } = require('node:child_process');
  const r = spawnSync('node', ['-e', "console.log(JSON.stringify(require('./scripts/write-serialisation.js').measure()))"], {
    encoding: 'utf8',
    shell: process.platform === 'win32',
  });
  const m = JSON.parse(r.stdout.trim());
  // Whatever the tree state, untracked entries must never appear as tracked changes.
  assert.ok(Array.isArray(m.files));
  assert.ok(
    m.files.every((f) => !f.startsWith('??')),
    `untracked files leaked into the gate: ${JSON.stringify(m.files)}`
  );
});

test('the gate reports the branch it measured', () => {
  // Without the branch name the error is unactionable - you cannot tell which tree
  // is dirty when several worktrees exist.
  const m = W.measure();
  assert.ok(typeof m.branch === 'string' && m.branch.length > 0, 'branch must be reported');
  assert.strictEqual(typeof m.dirty, 'boolean');
  assert.strictEqual(typeof m.trackedChanges, 'number');
});