#!/usr/bin/env node
/**
 * Unit tests for preflight-ue.js (repo-side + simulate-fail).
 * Run: node --test scripts/preflight-ue.test.js
 */
const { spawnSync } = require('child_process');
const assert = require('assert');
const path = require('path');
const test = require('node:test');

const script = path.join(__dirname, 'preflight-ue.js');
const projectRoot = path.resolve(__dirname, '..');

function runPreflight(args, env = {}) {
  return spawnSync(process.execPath, [script, ...args], {
    cwd: projectRoot,
    env: { ...process.env, ...env },
    encoding: 'utf8',
  });
}

test('assets-only passes on cloud (repo config present)', () => {
  const r = runPreflight(['--assets-only']);
  assert.strictEqual(r.status, 0, r.stdout + r.stderr);
  assert.match(r.stdout, /repo checks: PASS/);
  assert.match(r.stdout, /exit: 0/);
});

test('simulate-fail exits non-zero with blocker code', () => {
  const r = runPreflight(['--assets-only', '--simulate-fail=MCP_UNREACHABLE']);
  assert.strictEqual(r.status, 1, r.stdout + r.stderr);
  assert.match(r.stdout, /\[MCP_UNREACHABLE\]/);
  assert.match(r.stdout, /exit: 1/);
});

test('simulate-fail ABP skeleton code for VP-A class documentation', () => {
  const r = runPreflight(['--assets-only', '--simulate-fail=EDITOR_ABP_SKELETON']);
  assert.strictEqual(r.status, 1);
  assert.match(r.stdout, /EDITOR_ABP_SKELETON/);
});

test('full mode without MCP skips editor when unreachable (expected on cloud VM)', () => {
  const r = runPreflight(['--skip-mcp'], { HW_PREFLIGHT_SKIP_MCP: '1' });
  // May pass or fail on disk assets depending on checkout; must exit 0 or 1 only
  assert.ok(r.status === 0 || r.status === 1, `unexpected exit ${r.status}`);
  assert.match(r.stdout, /preflight:ue/);
});
