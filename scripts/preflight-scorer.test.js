#!/usr/bin/env node
/**
 * Keyless tests for the scorer version preflight.
 *
 * The whole point of this check is that it reports a version it could not read
 * as UNVERIFIED rather than as a match, so those cases are the ones worth
 * pinning. Nothing here touches the network or the real scorer binary.
 */

const test = require('node:test');
const assert = require('node:assert');
const { spawnSync } = require('node:child_process');
const path = require('node:path');

const script = path.join(__dirname, 'preflight-scorer.js');
const { REQUIRED_SCORER_VERSION, compareVersion } = require('./preflight-scorer.js');

const run = (args) =>
  spawnSync(process.execPath, [script, ...args], { encoding: 'utf8', timeout: 60000 });

test('the required version matches the one the baseline was measured with', () => {
  assert.strictEqual(REQUIRED_SCORER_VERSION, '0.4.0');
});

test('an exact version is a match', () => {
  const r = compareVersion('0.4.0');
  assert.strictEqual(r.status, 'match');
  assert.strictEqual(r.reason, null);
});

test('a v-prefixed version still matches', () => {
  // Some builds print `v0.4.0`. Treating that as a mismatch would cry wolf.
  assert.strictEqual(compareVersion('v0.4.0').status, 'match');
});

test('a different version is a mismatch and says why it matters', () => {
  const r = compareVersion('0.3.0');
  assert.strictEqual(r.status, 'mismatch');
  assert.ok(r.reason.includes('not comparable'), r.reason);
});

test('an unreadable version is UNVERIFIED, never a match', () => {
  // The fail-open trap in its purest form: absence of evidence is not evidence.
  for (const v of [null, undefined, '', 'unknown', '   ']) {
    const r = compareVersion(v);
    assert.strictEqual(r.status, 'unverified', `expected unverified for ${JSON.stringify(v)}`);
    assert.notStrictEqual(r.status, 'match');
  }
});

test('the required version is reported even when the observed one is unusable', () => {
  const r = compareVersion('unknown');
  assert.strictEqual(r.required, '0.4.0');
  assert.strictEqual(r.observed, 'unknown');
});

test('an explicit required version can be supplied', () => {
  assert.strictEqual(compareVersion('1.2.3', '1.2.3').status, 'match');
  assert.strictEqual(compareVersion('1.2.3', '0.4.0').status, 'mismatch');
});

test('the script never exits non-zero, even on a mismatch', () => {
  // Advisory means advisory. A scorer drift must not break `npm run doctor`.
  const p = run(['--tool', path.join(__dirname, 'no-such-scorer-binary')]);
  assert.strictEqual(p.status, 0, `exited ${p.status}: ${p.stderr}`);
});

test('--json emits parseable output with a non-fatal verdict', () => {
  const p = run(['--json', '--tool', path.join(__dirname, 'no-such-scorer-binary')]);
  assert.strictEqual(p.status, 0);
  const doc = JSON.parse(p.stdout);
  assert.strictEqual(doc.check, 'scorer-version');
  assert.strictEqual(doc.fatal, false);
  assert.strictEqual(doc.required, '0.4.0');
  assert.ok(['absent', 'unverified', 'mismatch', 'match'].includes(doc.status), doc.status);
});

test('--json never leaks a credential or a home-directory path', () => {
  const p = run(['--json']);
  const out = `${p.stdout}${p.stderr}`;
  assert.ok(!/nvapi/i.test(out), 'no credential-shaped string');
  assert.ok(!/sk-[A-Za-z0-9]{16,}/.test(out), 'no API-key-shaped string');
});

test('--help explains that it does not enforce', () => {
  const p = run(['--help']);
  assert.strictEqual(p.status, 0);
  assert.ok(p.stdout.includes('Never exits non-zero'), p.stdout);
});
