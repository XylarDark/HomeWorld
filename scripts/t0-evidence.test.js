#!/usr/bin/env node
/**
 * Keyless tests for the T0 evidence ledger.
 *
 * The failure modes worth pinning are the ones that would make the ledger lie:
 * reading a BOM'd artifact as absent, and reading a missing `pass` field as a
 * pass. A ledger that overstates proof is worse than no ledger, because it would
 * let the board stop saying NOT PROVEN.
 */

const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const script = path.join(__dirname, 't0-evidence.js');
const M = require('./t0-evidence.js');

/** Build a throwaway gate directory. Never touches the real Saved/. */
function fixture(files) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 't0ev-'));
  for (const [name, content] of Object.entries(files)) {
    fs.writeFileSync(path.join(dir, name), content, 'utf8');
  }
  return dir;
}

const run = (args) => spawnSync(process.execPath, [script, ...args], { encoding: 'utf8', timeout: 60000 });

test('readJsonLoose parses a file written with a UTF-8 BOM', () => {
  // 6 of 14 real gate files are BOM'd. Plain JSON.parse throws on them.
  const dir = fixture({ 't0_m1_x_gate.json': '\uFEFF{"pass":true,"bite":"B"}' });
  const parsed = M.readJsonLoose(path.join(dir, 't0_m1_x_gate.json'));
  assert.strictEqual(parsed.pass, true);
  assert.strictEqual(M.hasBom(path.join(dir, 't0_m1_x_gate.json')), true);
});

test('readJsonLoose still parses a file without a BOM', () => {
  const dir = fixture({ 't0_m1_x_gate.json': '{"pass":true}' });
  assert.strictEqual(M.readJsonLoose(path.join(dir, 't0_m1_x_gate.json')).pass, true);
  assert.strictEqual(M.hasBom(path.join(dir, 't0_m1_x_gate.json')), false);
});

test('a missing pass field is NO_VERDICT, never a pass', () => {
  // The m2-m7 schema has no `pass` key at all. Inferring either way invents a result.
  const r = M.classifyGate({ bite: 'T0_M2_KETTLE', soft_fail: false, closed_fail: false });
  assert.strictEqual(r.status, 'NO_VERDICT');
  assert.strictEqual(r.pass, null);
});

test('provisional true outranks a pass flag', () => {
  // A self-flagged provisional artifact is not a verdict even if pass is set.
  const r = M.classifyGate({ pass: true, provisional: true });
  assert.strictEqual(r.status, 'PROVISIONAL');
});

test('LOCAL_PASS requires pass, no provisional, and no closed fail', () => {
  assert.strictEqual(M.classifyGate({ pass: true }).status, 'LOCAL_PASS');
  assert.strictEqual(M.classifyGate({ pass: true, provisional: false }).status, 'LOCAL_PASS');
  assert.strictEqual(M.classifyGate({ pass: true, closed_fail: false }).status, 'LOCAL_PASS');
  assert.strictEqual(M.classifyGate({ pass: true, closed_fail: true }).status, 'LOCAL_FAIL');
});

test('acceptance is never inferred from a local artifact', () => {
  // Hard guarantee: the ledger cannot mark a beat accepted, whatever the file says.
  for (const gate of [{ pass: true }, { pass: true, provisional: false }, {}]) {
    assert.strictEqual(M.classifyGate(gate).accepted, false);
  }
  assert.ok(M.classifyGate({ pass: true }).acceptanceReason.includes('unstamped'));
});

test('schema aliases are probed, not assumed', () => {
  // m8 uses `pass`, m9 uses different keys; both must classify without crashing.
  assert.strictEqual(M.pick({ passed: true }, ['pass', 'passed']), true);
  assert.strictEqual(M.pick({ map: 'M' }, ['map']), 'M');
  assert.strictEqual(M.pick({}, ['map'], 'fallback'), 'fallback');
  assert.strictEqual(M.pick({ sha: null }, ['sha'], 'fallback'), 'fallback');
});

test('beat ids are derived from filenames in beat order', () => {
  assert.strictEqual(M.beatFromFilename('t0_m14_camp_night_gate.json'), 'T0_M14');
  assert.strictEqual(M.beatFromFilename('t0_m3_plant_gate.json'), 'T0_M3');
  assert.strictEqual(M.beatFromFilename('t0_default_skybox_day_gate.json'), 'T0_DEFAULT_SKYBOX_DAY');
  // M3 must sort before M14, not after it as a string would.
  assert.ok(M.beatOrder('T0_M3') < M.beatOrder('T0_M14'));
});

test('collectGates sorts by beat number and flags BOMs', () => {
  const dir = fixture({
    't0_m14_z_gate.json': '\uFEFF{"pass":true}',
    't0_m2_a_gate.json': '{"soft_fail":false}',
  });
  const rows = M.collectGates(dir);
  assert.deepStrictEqual(rows.map((r) => r.beat), ['T0_M2', 'T0_M14']);
  assert.strictEqual(rows.find((r) => r.beat === 'T0_M14').bom, true);
  assert.strictEqual(rows.find((r) => r.beat === 'T0_M2').bom, false);
});

test('an unparseable artifact is reported UNREADABLE, not skipped', () => {
  // A silent skip would make an unprovable beat look merely absent.
  const dir = fixture({ 't0_m5_x_gate.json': '{ this is not json' });
  const rows = M.collectGates(dir);
  assert.strictEqual(rows.length, 1);
  assert.strictEqual(rows[0].status, 'UNREADABLE');
  assert.ok(rows[0].parseError);
});

test('no row is ever marked trackedInGit, because Saved/ is gitignored', () => {
  const dir = fixture({ 't0_m1_x_gate.json': '{"pass":true}' });
  for (const r of M.collectGates(dir)) assert.strictEqual(r.trackedInGit, false);
});

test('summarize counts status, accepted, and BOM files', () => {
  const dir = fixture({
    't0_m1_a_gate.json': '{"pass":true}',
    't0_m2_b_gate.json': '{"provisional":true}',
    't0_m3_c_gate.json': '{"soft_fail":false}',
    't0_m4_d_gate.json': '\uFEFF{"pass":true}',
  });
  const s = M.summarize(M.collectGates(dir));
  assert.strictEqual(s.total, 4);
  assert.strictEqual(s.accepted, 0);
  assert.strictEqual(s.localPass, 2);
  assert.strictEqual(s.byStatus.PROVISIONAL, 1);
  assert.strictEqual(s.byStatus.NO_VERDICT, 1);
  assert.strictEqual(s.bomFiles, 1);
});

test('an empty directory yields no rows rather than throwing', () => {
  const dir = fixture({});
  assert.deepStrictEqual(M.collectGates(dir), []);
});

test('--json emits a parseable report with accepted:0', () => {
  const dir = fixture({ 't0_m1_a_gate.json': '{"pass":true}' });
  const p = run(['--json', '--saved', dir]);
  assert.strictEqual(p.status, 0, p.stderr);
  const doc = JSON.parse(p.stdout);
  assert.strictEqual(doc.accepted, 0);
  assert.strictEqual(doc.total, 1);
  assert.strictEqual(doc.beats[0].status, 'LOCAL_PASS');
});

test('the markdown names the accepted count and never claims proof', () => {
  const dir = fixture({ 't0_m1_a_gate.json': '{"pass":true}' });
  const p = run(['--saved', dir]);
  assert.strictEqual(p.status, 0, p.stderr);
  assert.ok(p.stdout.includes('Accepted beats: 0 of 1'), p.stdout.slice(0, 200));
  assert.ok(p.stdout.includes('LOCAL_PASS'));
  // The word "PROVEN" must only appear as a denial, never as a status.
  assert.ok(!/\*\*PROVEN\*\*/.test(p.stdout), 'must not assert a beat is proven');
});

test('a nonexistent --saved directory exits 0 with a message, not a stack', () => {
  const p = run(['--saved', path.join(os.tmpdir(), 'definitely-not-here-xyz')]);
  assert.strictEqual(p.status, 0, p.stderr);
  assert.ok(p.stderr.includes('no gate artifacts'), p.stderr);
});