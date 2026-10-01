#!/usr/bin/env node
/**
 * Keyless tests for harness coverage.
 *
 * The failure modes that matter here are all ways of *overstating* coverage:
 * counting preamble as failures, scoring an entry covered on a stopword, or
 * treating "documented in docs/" as "covered by a rule". Each is pinned below.
 */

const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const script = path.join(__dirname, 'harness-coverage.js');
const M = require('./harness-coverage.js');

const run = (args) =>
  spawnSync(process.execPath, [script, ...args], {
    encoding: 'utf8',
    timeout: 120000,
    // The real-corpus JSON is large; the default 1 MB buffer kills the child with
    // ENOBUFS and reports `status: null`, which reads like a mystery.
    maxBuffer: 16 * 1024 * 1024,
  });

test('the JSON report stays small enough to be machine-readable', () => {
  // Guards the ENOBUFS class of bug: unbounded corroboration lists once blew the
  // 1 MB spawnSync buffer, which surfaced as a null exit status, not a clear error.
  const p = run(['--json']);
  assert.ok(p.stdout.length < 1024 * 1024, `JSON grew to ${p.stdout.length} bytes`);
});

test('parseEntries reads only the Entries section, not the preamble', () => {
  // The "Harness traps" section documents traps already turned into tooling.
  // Counting it would inflate coverage with self-referential entries.
  const md = [
    '# Known Errors',
    '### A trap already tooled (preamble)',
    'body',
    '## Entries',
    '### Real failure one',
    'body one',
    '### Real failure two',
    'body two',
    '## Trailing notes',
    '### should not appear',
  ].join('\n');
  const entries = M.parseEntries(md);
  assert.strictEqual(entries.length, 2);
  assert.deepStrictEqual(
    entries.map((e) => e.head),
    ['Real failure one', 'Real failure two']
  );
});

test('extractTerms prefers code spans and splits multi-token spans', () => {
  const e = {
    head: 'World Partition conversion creates a second map (Homestead_WP)',
    body: ['Error: `Homestead_WP` not found. Check `Content/Python/convert_map.py`.'],
  };
  const t = M.extractTerms(e);
  assert.ok(t.includes('Homestead_WP'), 'expected the bare token from the code span');
  assert.ok(t.includes('Content/Python/convert_map.py'), 'expected the path fragment');
});

test('extractTerms drops stopwords and short fragments', () => {
  const e = { head: 'plain heading', body: ['a `returns` and `the` and `xy`'] };
  const t = M.extractTerms(e);
  assert.ok(!t.includes('returns'));
  assert.ok(!t.includes('the'));
  assert.ok(!t.includes('xy'), 'fragments under 5 chars are not distinctive');
});

test('a prose-only entry is UNEXTRACTABLE, not UNCOVERED', () => {
  // Otherwise a heading with no terms would silently count as a rule gap.
  const e = { head: 'Homestead: no ground visible after conversion', body: ['it just is not'] };
  const r = M.scoreEntry(e, new Map(), new Map());
  assert.strictEqual(r.status, 'UNEXTRACTABLE');
});

test('COVERED requires a rule file to contain the term', () => {
  const rules = new Map([['10-ue-cpp.mdc', 'avoid including world.h in GameplayAbilitySpec.h usage']]);
  const r = M.scoreEntry(
    { head: 'GameplayAbilitySpec.h include path', body: ['`GameplayAbilitySpec.h`'] },
    rules,
    new Map()
  );
  assert.strictEqual(r.status, 'COVERED');
  assert.deepStrictEqual(r.rules, ['10-ue-cpp.mdc']);
});

test('mentioned in docs/ but in no rule is UNCOVERED with harnessOnly set', () => {
  // "No rule" and "nobody knows" are different problems with different fixes.
  // This is the regression guard for a Set/length bug that pinned this to false.
  const rules = new Map([['10-ue-cpp.mdc', 'unrelated text']]);
  const harness = new Map([['docs/KNOWN_ERRORS.md', 'compressing homestead_wm']]);
  const r = M.scoreEntry({ head: 'x', body: ['`Homestead_WM`'] }, rules, harness);
  assert.strictEqual(r.status, 'UNCOVERED');
  assert.strictEqual(r.harnessOnly, true);
  assert.deepStrictEqual(r.elsewhere, ['docs/KNOWN_ERRORS.md']);
  assert.strictEqual(r.elsewhereCount, 1);
});

test('mentions is case-insensitive in both directions', () => {
  const rules = new Map([['a.mdc', 'const HOMESTEAD_WM']]);
  assert.deepStrictEqual(M.mentions('homestead_wm', rules, new Map()).inRules, ['a.mdc']);
});

test('summarize computes coverage over extractable entries only', () => {
  // Including UNEXTRACTABLE in the denominator would understate coverage.
  const rows = [
    { status: 'COVERED' },
    { status: 'COVERED' },
    { status: 'UNCOVERED', harnessOnly: false },
    { status: 'UNEXTRACTABLE' },
  ];
  const s = M.summarize(rows);
  assert.strictEqual(s.total, 4);
  assert.strictEqual(s.extractable, 3);
  assert.strictEqual(s.covered, 2);
  assert.strictEqual(s.uncovered, 1);
  assert.ok(Math.abs(s.coverageRate - 2 / 3) < 1e-9);
});

test('coverageRate is null, not NaN, when nothing is extractable', () => {
  const s = M.summarize([{ status: 'UNEXTRACTABLE' }]);
  assert.strictEqual(s.coverageRate, null);
});

test('the markdown states the mention ceiling, not a prevention claim', () => {
  const rows = [{ head: 'Some failure', status: 'UNCOVERED', termCount: 3, rules: [], elsewhere: [], missing: ['AbcDef'] }];
  const md = M.renderMarkdown(rows, M.summarize(rows), 31);
  assert.ok(md.includes('Mention, not prevention'), 'must label the signal honestly');
  assert.ok(md.includes('candidate'), 'uncovered entries must be candidates, not verdicts');
});

test('the coverage source file cannot corroborate itself', () => {
  // KNOWN_ERRORS.md is where the terms come from. If it counted as a corroborating
  // surface, every uncovered term would match it and `harnessOnly` would be always
  // true — a flag that is always on measures nothing.
  const harness = M.loadHarnessContext();
  const keys = [...harness.keys()].map((k) => k.toLowerCase());
  assert.ok(!keys.includes('docs/known_errors.md'), 'source file must be excluded');
  assert.ok(!keys.some((k) => k.endsWith('known_errors.md')), 'source file must be excluded');
  assert.ok(keys.includes('agents.md') || keys.length > 0, 'other surfaces should still load');
});

test('harnessOnly never exceeds uncovered across the real corpus', () => {
  // Current finding, not a bug: all 6 uncovered failures ARE discussed in session
  // logs and setup docs, and none became a rule. That is the actionable result —
  // docs are not loaded into agent context, rules are.
  // This test only guards the invariant; the specific number is corpus-dependent.
  const p = run(['--json']);
  const doc = JSON.parse(p.stdout);
  assert.ok(
    doc.harnessOnly <= doc.uncovered,
    `harnessOnly (${doc.harnessOnly}) cannot exceed uncovered (${doc.uncovered})`
  );
});

test('Docs/ and docs/ are not walked as two separate roots', () => {
  // One physical directory on Windows. Walking both yields every doc twice.
  const keys = [...M.loadHarnessContext().keys()].map((k) => k.toLowerCase());
  const folded = new Set(keys);
  assert.strictEqual(folded.size, keys.length, 'case-folded duplicate paths present');
});

test('--json emits a parseable report against the real corpus', () => {
  const p = run(['--json']);
  assert.strictEqual(p.status, 0, p.stderr);
  const doc = JSON.parse(p.stdout);
  assert.ok(doc.total > 20, `expected the real corpus, got ${doc.total}`);
  assert.ok(doc.ruleCount >= 30, `expected >=30 rules, got ${doc.ruleCount}`);
  assert.ok(doc.covered > 0);
  assert.ok(doc.coverageRate > 0 && doc.coverageRate <= 1);
});

test('--strict exits non-zero when an uncovered failure exists', () => {
  // Ratchet mode. New gaps are normal; this is how a regression becomes visible.
  const p = run(['--strict']);
  assert.strictEqual(p.status, 1, p.stdout.slice(0, 300));
  assert.ok(p.stderr.includes('uncovered'), p.stderr);
});

test('advisory mode exits 0 even with uncovered failures present', () => {
  const p = run([]);
  assert.strictEqual(p.status, 0, p.stderr);
});