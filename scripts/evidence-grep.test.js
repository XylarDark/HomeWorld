#!/usr/bin/env node
/**
 * Unit tests for evidence-grep.js (no UE).
 * Run: node --test scripts/evidence-grep.test.js
 */
const { spawnSync } = require('child_process');
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const test = require('node:test');

const script = path.join(__dirname, 'evidence-grep.js');
const projectRoot = path.resolve(__dirname, '..');
const {
  score,
  countSuccessPath,
  DEFAULT_PREFIXES,
} = require('./evidence-grep.js');

function runCli(args, input) {
  return spawnSync(process.execPath, [script, ...args], {
    cwd: projectRoot,
    encoding: 'utf8',
    input,
  });
}

test('score marks PASS and MISSING correctly', () => {
  const sample = [
    'LogTemp: FORM: phase 2',
    'LogTemp: FALLBACK: glide start',
    'LogTemp: noise line',
    'LogTemp: STORE: deposit WOOD inventory->stored count=1',
    'LogTemp: INVENTORY: dump begin (slots=6 total=1)',
  ].join('\n');
  const rows = score(sample, DEFAULT_PREFIXES);
  const by = Object.fromEntries(rows.map((r) => [r.prefix, r]));
  assert.strictEqual(by['FORM:'].status, 'PASS');
  assert.strictEqual(by['FALLBACK:'].status, 'PASS');
  assert.strictEqual(by['STORE:'].status, 'PASS');
  assert.strictEqual(by['INVENTORY:'].status, 'PASS');
  assert.strictEqual(by['HEAL:'].status, 'MISSING');
  assert.strictEqual(by['GATHER:'].count, 0);
});

test('success-path mode ignores component ready diagnostics', () => {
  const sample = [
    'LogTemp: HEAL: component ready id=Spirit_A state=hurt',
    'LogTemp: NURTURE: component ready target=N1_Crop nurtured=0 requires=RES_SEED',
    'LogTemp: TAME: component ready on GP_BeastPad state=wild',
    'LogTemp: HEAL: success Spirit_A consumed RES_HERB',
    'LogTemp: NURTURE: success N1_Crop M_Nurtured=1 consumed 1x RES_SEED',
    'LogTemp: TAME: offer accepted (RES_HERB consumed) — bond wait 2.0s',
    'LogTemp: GATHER: blocked — night or spirit form',
    'LogTemp: GATHER: RES_WOOD +1 (slot 0 now 1/9)',
    'LogTemp: STORE: deposit fail RES_WOOD — store full (9/9)',
    'LogTemp: STORE: deposit RES_WOOD inventory->stored count=1',
    'LogTemp: DAWN: persisted inventory=3 tame+heal+nurture in slot',
    'LogTemp: INVENTORY: dump begin (slots=6 total=1)',
  ].join('\n');
  const rows = score(sample, DEFAULT_PREFIXES, { successPath: true });
  const by = Object.fromEntries(rows.map((r) => [r.prefix, r]));
  assert.strictEqual(by['HEAL:'].status, 'PASS');
  assert.strictEqual(by['HEAL:'].count, 1);
  assert.strictEqual(by['NURTURE:'].status, 'PASS');
  assert.strictEqual(by['TAME:'].status, 'PASS');
  assert.strictEqual(by['GATHER:'].status, 'PASS');
  assert.strictEqual(by['STORE:'].status, 'PASS');
  assert.strictEqual(by['DAWN:'].status, 'PASS');
  assert.strictEqual(by['INVENTORY:'].status, 'PASS');
});

test('countSuccessPath rejects soft-fail-only HEAL lines', () => {
  const sample = 'LogTemp: HEAL: soft fail Spirit_A — no RES_HERB or RES_SEED\n';
  const result = countSuccessPath(sample, 'HEAL:', 'HEAL: success');
  assert.strictEqual(result.count, 0);
});

test('CLI table exit 0 without --strict when some missing', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'hs-d-ev-'));
  const logPath = path.join(dir, 'sample.log');
  fs.writeFileSync(logPath, 'LogTemp: FORM: only\n', 'utf8');
  const r = runCli(['--log', logPath]);
  assert.strictEqual(r.status, 0, r.stdout + r.stderr);
  assert.match(r.stdout, /FORM:/);
  assert.match(r.stdout, /\*\*PASS\*\*/);
  assert.match(r.stdout, /\*\*MISSING\*\*/);
});

test('CLI --strict exits 1 when prefixes missing', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'hs-d-ev-'));
  const logPath = path.join(dir, 'sample.log');
  fs.writeFileSync(logPath, 'LogTemp: FORM: only\n', 'utf8');
  const r = runCli(['--log', logPath, '--strict']);
  assert.strictEqual(r.status, 1, r.stdout + r.stderr);
});

test('CLI --strict exits 0 when all prefixes present', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'hs-d-ev-'));
  const logPath = path.join(dir, 'full.log');
  const lines = DEFAULT_PREFIXES.map((p) => `LogTemp: ${p} evidence`);
  fs.writeFileSync(logPath, lines.join('\n') + '\n', 'utf8');
  const jsonPath = path.join(dir, 'out.json');
  const r = runCli(['--log', logPath, '--strict', '--json', jsonPath]);
  assert.strictEqual(r.status, 0, r.stdout + r.stderr);
  const report = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  assert.strictEqual(report.allPass, true);
  assert.strictEqual(report.rows.length, DEFAULT_PREFIXES.length);
});

test('CLI --success-path exits 1 under --strict when only component ready', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'hs-d-ev-'));
  const logPath = path.join(dir, 'soft.log');
  fs.writeFileSync(
    logPath,
    [
      'LogTemp: FORM: phase 2',
      'LogTemp: FALLBACK: glide',
      'LogTemp: HEAL: component ready id=Spirit_A',
      'LogTemp: NURTURE: component ready target=N1_Crop',
      'LogTemp: DAWN: phase set to Night',
      'LogTemp: TAME: component ready on pad',
      'LogTemp: GATHER: harvest ok (total Physical: 1)',
      'LogTemp: STORE: deposit fail RES_WOOD',
      'LogTemp: INVENTORY: dump end',
    ].join('\n') + '\n',
    'utf8',
  );
  const r = runCli(['--log', logPath, '--success-path', '--strict']);
  assert.strictEqual(r.status, 1, r.stdout + r.stderr);
  assert.match(r.stdout, /success-path mode/);
});

test('CLI --success-path exits 0 under --strict with success lines', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'hs-d-ev-'));
  const logPath = path.join(dir, 'success.log');
  fs.writeFileSync(
    logPath,
    [
      'LogTemp: FORM: phase 2',
      'LogTemp: FALLBACK: glide',
      'LogTemp: HEAL: success Spirit_A consumed RES_HERB',
      'LogTemp: NURTURE: success N1_Crop M_Nurtured=1',
      'LogTemp: DAWN: persisted inventory=1 tame+heal+nurture',
      'LogTemp: TAME: offer accepted (RES_HERB consumed)',
      'LogTemp: GATHER: RES_WOOD +1 (slot 0 now 1/9)',
      'LogTemp: STORE: deposit RES_WOOD inventory->stored count=1',
      'LogTemp: INVENTORY: dump begin (slots=6 total=1)',
    ].join('\n') + '\n',
    'utf8',
  );
  const r = runCli(['--log', logPath, '--success-path', '--strict']);
  assert.strictEqual(r.status, 0, r.stdout + r.stderr);
});

test('CLI missing log exits 1', () => {
  const r = runCli(['--log', path.join(os.tmpdir(), 'hs-d-no-such-log-xyz.log')]);
  assert.strictEqual(r.status, 1);
});

test('CLI --stdin works', () => {
  const r = runCli(['--stdin', '--prefixes', 'FORM:,HEAL:'], 'x FORM: ok\n');
  assert.strictEqual(r.status, 0, r.stdout + r.stderr);
  assert.match(r.stdout, /1\/2 PASS/);
});
