#!/usr/bin/env node
/**
 * UE Editor ownership lock.
 *
 * WHY THIS EXISTS
 *
 * One developer, several agents. Two of them can both reach for the Unreal Editor at
 * the same time, and nothing in UE stops them: the second MCP client to call
 * `execute_python_script` runs against a live Editor that the first one is already
 * mutating. The symptoms are a half-applied change, a stale `Saved/` directory, a
 * build that fails only sometimes, and a log full of warnings nobody can attribute.
 *
 * There is no web-dev equivalent of this hazard. It is specific to a shared,
 * stateful, single-instance host application - and it is currently unguarded.
 *
 * IT ALSO COVERS BUILDS AND HEADLESS TESTS
 *
 * `Tools/Safe-Build.ps1` closes the Editor before building, and `Tools/RunTests.ps1`
 * requires the Editor closed for headless automation. So the same lock protects all
 * three exclusive UE operations: driving the Editor over MCP, building, and running
 * automation tests. One lock, one owner, no overlap.
 *
 * FAIL CLOSED, BUT BREAK STALE LOCKS EXPLICITLY
 *
 * A lock that silently expires would let two agents in - which is the failure it
 * exists to prevent. A lock that never expires would strand the harness after any
 * crash. So: stale locks are detectable and reported, but breaking one requires a
 * deliberate `--break` flag. The asymmetry is intentional. It is much cheaper to
 * type `--break` once after a crash than to debug a half-applied asset import.
 */

const fs = require('fs');
const path = require('path');

const PROJECT_ROOT = path.resolve(__dirname, '..');
const LOCK_PATH = path.join(PROJECT_ROOT, 'Saved', 'editor.lock');
/** A lock older than this is reported as stale. It is NOT auto-broken. */
const STALE_MS = 4 * 60 * 60 * 1000; // 4 hours

function readLock() {
  if (!fs.existsSync(LOCK_PATH)) return null;
  try {
    return JSON.parse(fs.readFileSync(LOCK_PATH, 'utf8'));
  } catch {
    // An unreadable lock is treated as held, not as absent. A corrupt lockfile is a
    // broken state, and the safe response to a broken state is to stop.
    return { corrupt: true };
  }
}

function isStale(lock, now = Date.now()) {
  if (!lock || lock.corrupt) return false;
  return now - new Date(lock.acquiredAt).getTime() > STALE_MS;
}

function acquire({ owner, operation, breakStale = false, now = Date.now() } = {}) {
  if (!owner) throw new Error('editor-lock: --owner is required');
  const held = readLock();

  if (held && !breakStale) {
    const stale = isStale(held, now);
    const detail = held.corrupt
      ? 'lockfile is corrupt (treat as held)'
      : `held by "${held.owner}" since ${held.acquiredAt} for ${held.operation || 'unspecified'}`;
    return {
      ok: false,
      held: true,
      stale,
      lock: held,
      reason: stale
        ? `STALE lock - ${detail}. Break it deliberately with --break if you are sure no agent is running.`
        : `lock ${detail}`,
    };
  }

  fs.mkdirSync(path.dirname(LOCK_PATH), { recursive: true });
  const lock = {
    owner,
    operation: operation || 'unspecified',
    acquiredAt: new Date(now).toISOString(),
    pid: process.pid,
  };
  // Write-then-rename so a reader never observes a half-written lockfile.
  const tmp = `${LOCK_PATH}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(lock, null, 2));
  fs.renameSync(tmp, LOCK_PATH);
  return { ok: true, lock, brokeStale: Boolean(held) };
}

function release({ owner, force = false } = {}) {
  const held = readLock();
  if (!held) return { ok: true, released: false, reason: 'no lock held' };
  if (held.corrupt) {
    if (!force) return { ok: false, reason: 'lockfile is corrupt; pass --force to remove it' };
    fs.rmSync(LOCK_PATH, { force: true });
    return { ok: true, released: true, forced: true };
  }
  if (owner && held.owner !== owner && !force) {
    return { ok: false, reason: `lock is held by "${held.owner}", not "${owner}"; pass --force to steal it` };
  }
  fs.rmSync(LOCK_PATH, { force: true });
  return { ok: true, released: true, owner: held.owner };
}

function status() {
  const held = readLock();
  if (!held) return { held: false };
  return { held: true, stale: isStale(held), lock: held };
}

if (require.main === module) {
  const argv = process.argv.slice(2);
  const cmd = argv[0];
  const flag = (n) => {
    const i = argv.indexOf(n);
    return i !== -1 ? argv[i + 1] : undefined;
  };
  const out = (v) => process.stdout.write(JSON.stringify(v, null, 2) + '\n');

  if (cmd === 'acquire') {
    const r = acquire({
      owner: flag('--owner'),
      operation: flag('--operation'),
      breakStale: argv.includes('--break'),
    });
    out(r);
    process.exit(r.ok ? 0 : 2);
  } else if (cmd === 'release') {
    const r = release({ owner: flag('--owner'), force: argv.includes('--force') });
    out(r);
    process.exit(r.ok ? 0 : 2);
  } else {
    out(status());
    process.exit(0);
  }
}

module.exports = { acquire, release, status, isStale, STALE_MS, LOCK_PATH };