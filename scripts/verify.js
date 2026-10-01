#!/usr/bin/env node
/**
 * verify - the one command that proves the game is real.
 *
 * WHY THIS EXISTS
 *
 * The audit found that every automated fact we had about HomeWorld was "it compiles."
 * `Source/` contained zero automation tests. All the Node suites tested harness
 * tooling. The build and test entry points lived in PowerShell under `Tools/`, in a
 * different system from the gates, so the documented path and the verified path were
 * different paths.
 *
 * This puts them in one place, in order, with one exit code.
 *
 * IT IS TIERED, BECAUSE THE EXPENSIVE CHECKS ARE EXPENSIVE
 *
 *   fast    JS suite only. Seconds. Safe on every save.
 *   build   + compile the C++. Minutes, and needs the Editor closed.
 *   ue      + run UE automation tests. Minutes, and needs the Editor closed and
 *           $env:UE_EDITOR set.
 *
 * `npm run verify` runs `fast` + `build`, because compiling is the only product-level
 * signal we have until automation tests exist. That is deliberate: it is the weakest
 * useful bar, and a weak bar that is always run beats a strong bar nobody runs.
 *
 * EVERYTHING EXCLUSIVE TO UE TAKES THE EDITOR LOCK
 *
 * Builds and headless tests both require the Editor closed. Two agents doing either at
 * once will produce a failure that belongs to neither of them. `verify` acquires the
 * lock for the duration and releases it in a finally block, so a crash mid-build does
 * not strand it.
 */

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const lock = require('./editor-lock');

const PROJECT_ROOT = path.resolve(__dirname, '..');
const arg = (n) => {
  const i = process.argv.indexOf(n);
  return i !== -1 ? process.argv[i + 1] : undefined;
};
const has = (n) => process.argv.includes(n);

const TIERS = ['fast', 'build', 'ue'];
const requested = arg('--tier');
const tier = requested || (has('--ue') ? 'ue' : has('--fast') ? 'fast' : 'build');
if (!TIERS.includes(tier)) {
  process.stderr.write(`verify: unknown --tier "${tier}"; expected one of ${TIERS.join(', ')}\n`);
  process.exit(2);
}

const steps = [];
let failed = null;

function step(name, fn) {
  process.stdout.write(`\n=== ${name} ===\n`);
  const t0 = Date.now();
  try {
    const r = fn();
    const secs = ((Date.now() - t0) / 1000).toFixed(1);
    steps.push({ name, ok: r === 0, secs });
    if (r !== 0) {
      failed = name;
      process.stdout.write(`--- ${name} FAILED (exit ${r}) after ${secs}s\n`);
      return false;
    }
    process.stdout.write(`--- ${name} ok (${secs}s)\n`);
    return true;
  } catch (e) {
    const secs = ((Date.now() - t0) / 1000).toFixed(1);
    steps.push({ name, ok: false, secs, error: e.message });
    failed = name;
    process.stdout.write(`--- ${name} ERROR after ${secs}s: ${e.message}\n`);
    return false;
  }
}

function run(cmd, argv, opts = {}) {
  const r = spawnSync(cmd, argv, {
    cwd: PROJECT_ROOT,
    stdio: 'inherit',
    shell: process.platform === 'win32',
    ...opts,
  });
  return r.status === null ? 1 : r.status;
}

function runPs1(rel, argv = []) {
  return run('powershell', ['-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', path.join(PROJECT_ROOT, rel), ...argv]);
}

/**
 * Run UE automation tests headlessly.
 *
 * The editor path is pinned rather than taken from $env:UE_EDITOR. On this machine
 * UE_EDITOR was already set to a 5.7 binary, and the 5.7 editor cannot load the 5.8
 * project - it aborts on a missing PCGPrimitives plugin. Silently trusting the
 * environment variable meant a green-looking failure that was really the wrong engine.
 */
function runUECmd(execCmds) {
  const editor = process.env.HW_UNREAL_EDITOR
    || 'C:\\Program Files\\Epic Games\\UE_5.8\\Engine\\Binaries\\Win64\\UnrealEditor-Cmd.exe';
  if (!fs.existsSync(editor)) {
    process.stderr.write(`verify: editor not found at ${editor}\n`);
    return 1;
  }
  const r = spawnSync(editor, [
    path.join(PROJECT_ROOT, 'HomeWorld.uproject'),
    `-ExecCmds=${execCmds}`,
    '-unattended', '-nop4', '-nosplash', '-NullRHI',
    '-TestExit=Automation Test Queue Empty',
  ], { cwd: PROJECT_ROOT, stdio: 'inherit', shell: false });
  return r.status === null ? 1 : r.status;
}

/** UE-only steps, wrapped in the editor lock so two agents cannot collide. */
function withEditorLock(label, fn) {
  const owner = `verify:${process.pid}`;
  const acq = lock.acquire({ owner, operation: label });
  if (!acq.ok) {
    process.stdout.write(`verify: cannot run ${label} - ${acq.reason}\n`);
    return 2;
  }
  if (acq.brokeStale) process.stdout.write(`verify: broke a stale lock (${acq.lock.owner})\n`);
  try {
    return fn();
  } finally {
    lock.release({ owner });
  }
}

const results = [];

results.push(step('js suite', () => run('node', ['--test', 'scripts/*.test.js'])));
if (results[results.length - 1] && tier !== 'fast') {
  results.push(
    step('c++ build', () =>
      withEditorLock('build', () => runPs1('Tools/Safe-Build.ps1'))
    )
  );
}
if (results[results.length - 1] && tier === 'ue') {
  if (!process.env.UE_EDITOR) {
    process.stdout.write('\nverify: skipping UE automation tests - $env:UE_EDITOR is not set\n');
    steps.push({ name: 'ue automation tests', ok: true, secs: '0.0', skipped: true });
  } else {
    results.push(
      step('ue automation tests', () =>
        withEditorLock('ue-tests', () => runUECmd('Automation RunTests HomeWorld.;Quit'))
      )
    );
  }
}

process.stdout.write('\n=== verify summary ===\n');
for (const s of steps) {
  const mark = s.skipped ? 'skip' : s.ok ? 'PASS' : 'FAIL';
  process.stdout.write(`  ${mark.padEnd(4)} ${s.name}${s.secs ? ` (${s.secs}s)` : ''}\n`);
}

// A machine-readable record, so a run can be cited later without re-running it.
try {
  fs.mkdirSync(path.join(PROJECT_ROOT, 'Saved'), { recursive: true });
  fs.writeFileSync(
    path.join(PROJECT_ROOT, 'Saved', 'verify_result.json'),
    JSON.stringify({ at: new Date().toISOString(), tier, steps, failed }, null, 2)
  );
} catch {
  /* the summary above is the human-facing record; this is a convenience */
}

if (failed) {
  process.stdout.write(`\nverify: FAILED at "${failed}".\n`);
  process.exit(1);
}
process.stdout.write(`\nverify: PASSED (tier=${tier}).\n`);
process.exit(0);