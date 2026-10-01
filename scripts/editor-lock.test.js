const test = require('node:test');
const assert = require('node:assert');

test('the editor lock is exclusive and fails closed', () => {
  const L = require('./editor-lock.js');
  const fs = require('fs');
  const saved = fs.existsSync(L.LOCK_PATH) ? fs.readFileSync(L.LOCK_PATH, 'utf8') : null;

  try {
    // A second agent is refused while the first holds it.
    const a = L.acquire({ owner: 'agent-a', operation: 'drive-editor' });
    assert.strictEqual(a.ok, true);
    const b = L.acquire({ owner: 'agent-b', operation: 'drive-editor' });
    assert.strictEqual(b.ok, false, 'a second acquire MUST be refused');
    assert.strictEqual(b.held, true);
    assert.match(b.reason, /held by "agent-a"/);

    // Release by the owner works; release by a stranger does not.
    assert.strictEqual(L.release({ owner: 'agent-b' }).ok, false, 'a stranger must not release');
    assert.strictEqual(L.release({ owner: 'agent-a' }).ok, true);
    assert.strictEqual(L.status().held, false);

    // Released means available again.
    assert.strictEqual(L.acquire({ owner: 'agent-c' }).ok, true);
    L.release({ owner: 'agent-c', force: true });
  } finally {
    if (saved === null) fs.rmSync(L.LOCK_PATH, { force: true });
    else fs.writeFileSync(L.LOCK_PATH, saved);
  }
});

test('a stale lock is reported as stale and requires a deliberate break', () => {
  // Auto-expiring a lock would let two agents in - the exact failure it prevents.
  // But a lock that never expires strands the harness after a crash. So stale is
  // REPORTED, and breaking it is an explicit act.
  const L = require('./editor-lock.js');
  const fs = require('fs');
  const saved = fs.existsSync(L.LOCK_PATH) ? fs.readFileSync(L.LOCK_PATH, 'utf8') : null;

  try {
    const old = Date.now() - L.STALE_MS - 60_000;
    L.acquire({ owner: 'agent-old', operation: 'build', now: old });

    const blocked = L.acquire({ owner: 'agent-new' });
    assert.strictEqual(blocked.ok, false, 'a stale lock still blocks by default');
    assert.strictEqual(blocked.stale, true, 'and it must be REPORTED as stale');
    assert.match(blocked.reason, /STALE/);
    assert.match(blocked.reason, /--break/);

    const broke = L.acquire({ owner: 'agent-new', breakStale: true });
    assert.strictEqual(broke.ok, true, 'an explicit break must succeed');
    assert.strictEqual(broke.brokeStale, true);

    // A fresh lock is NOT stale, so --break does nothing surprising.
    L.release({ force: true });
    L.acquire({ owner: 'fresh' });
    assert.strictEqual(L.acquire({ owner: 'other' }).stale, false);
    L.release({ force: true });
  } finally {
    if (saved === null) fs.rmSync(L.LOCK_PATH, { force: true });
    else fs.writeFileSync(L.LOCK_PATH, saved);
  }
});

test('a corrupt lockfile is treated as held, not as absent', () => {
  // The safe response to a broken state is to stop. Reading a corrupt lock as
  // "unlocked" would hand the Editor to two agents on the strength of a bad read.
  const L = require('./editor-lock.js');
  const fs = require('fs');
  const saved = fs.existsSync(L.LOCK_PATH) ? fs.readFileSync(L.LOCK_PATH, 'utf8') : null;

  try {
    fs.writeFileSync(L.LOCK_PATH, '{ this is not json');
    const r = L.acquire({ owner: 'anyone' });
    assert.strictEqual(r.ok, false, 'corrupt lock must block');
    assert.strictEqual(r.lock.corrupt, true);
    assert.match(r.reason, /corrupt/);
    assert.strictEqual(L.release({ force: true }).ok, true);
  } finally {
    if (saved === null) fs.rmSync(L.LOCK_PATH, { force: true });
    else fs.writeFileSync(L.LOCK_PATH, saved);
  }
});

test('an owner is required, because an unowned lock has no one to release it', () => {
  const L = require('./editor-lock.js');
  assert.throws(() => L.acquire({}), /owner is required/);
});