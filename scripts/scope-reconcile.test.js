#!/usr/bin/env node
/**
 * Tests for the T0 scope reconciler.
 *
 * The reconciler answers "does the locked scope agree with the tree?". Its dangerous
 * failure mode is reporting a finding that is actually its own defect — which is what
 * happened twice on its first run: an evidence column that read NO_ARTIFACT for every
 * beat because a function was called without its required argument, and two law
 * "violations" that were the canon being correctly restated.
 */

const test = require('node:test');
const assert = require('node:assert');
const R = require('./scope-reconcile.js');

test('scope table parsing separates MUST, CUT and DEFER', () => {
  const md = [
    '| Feature / beat | Pillar | MUST/CUT/DEFER | Prove hint | Taste? |',
    '|---|---|---|---|---|',
    '| Wake / start day | 1 | **MUST** | day start | Later |',
    '| Other plants | 3 | **DEFER** | loop | - |',
    '| Player death | - | **CUT** | - | - |',
    '',
    'not a table row',
  ].join('\n');
  const rows = R.parseScopeTable(md);
  assert.strictEqual(rows.length, 3);
  assert.deepStrictEqual(rows.map((r) => r.verdict), ['MUST', 'DEFER', 'CUT']);
  assert.strictEqual(rows[0].feature, 'Wake / start day');
  assert.strictEqual(rows[0].pillar, '1');
});

test('the parser stops at the end of the table', () => {
  // A later pipe-table in the same file must not be folded into the scope rows.
  const md = [
    '| Feature / beat | Pillar | MUST/CUT/DEFER | Prove hint | Taste? |',
    '|---|---|---|---|---|',
    '| Wake | 1 | **MUST** | x | y |',
    '',
    '## Something else',
    '',
    '| A | B | MUST | C | D |',
  ].join('\n');
  assert.strictEqual(R.parseScopeTable(md).length, 1);
});

test('the combat law check is negation-aware', () => {
  // The canon is *stated* in the compliant rows precisely because the law forbids it.
  // A bare word match flagged "not lethal; convert-not-kill" as a violation, i.e. it
  // reported the compliant rows as the breaches.
  assert.strictEqual(
    R.claimsKill('Day camp: cartoon eject', 'Eject-to-home; **not** lethal; convert-not-kill'),
    false,
    'a negated mention is not a claim'
  );
  assert.strictEqual(R.claimsKill('Camp night', 'Avoid + soothe (not kill)'), false);
  assert.strictEqual(R.claimsKill('Player death', 'the player dies'), true, 'a real claim must still fire');
  assert.strictEqual(R.claimsKill('New beat', 'guards are killed by the player'), true);
});

test('combat adjacency does not miss the rows the law applies to', () => {
  for (const f of ['Day camp: cartoon eject', 'Camp night: avoid 1 guard', 'Bed -> spirit', 'Home portal -> camp portal (spirit)']) {
    assert.ok(R.isCombatAdjacent(f), `${f} should be law-checked`);
  }
  assert.ok(!R.isCombatAdjacent('Equip backpack -> inventory'));
});

test('the reconciler runs against the real locked scope', () => {
  const res = R.reconcile();
  assert.ok(res.ok, res.error);
  assert.strictEqual(res.counts.must, 14, 'the APPROVED feature list locks 14 MUST rows');
  assert.strictEqual(res.beats.length, 14);
  // Acceptance is a human stamp and must never be inferred from an artifact claim.
  assert.strictEqual(res.accepted, 0, 'accepted must stay false until a human stamps it');
  for (const b of res.beats) {
    assert.ok(
      ['LOCAL_PASS', 'PROVISIONAL', 'LOCAL_FAIL', 'NO_VERDICT', 'NO_ARTIFACT'].includes(b.claimed),
      `unexpected claim status ${b.claimed} on ${b.beat}`
    );
  }
});

test('the evidence column is populated, not silently empty', () => {
  // Regression guard for the real bug: collectGates() called without its required
  // Saved directory returns [], which made every beat read NO_ARTIFACT and looked
  // like a finding rather than a defect in the script. That regression must still
  // be caught here — so assert it directly, against a call with no directory.
  const EVIDENCE = require('./t0-evidence.js');
  const noDir = (() => {
    try {
      return EVIDENCE.collectGates();
    } catch {
      return [];
    }
  })();
  assert.deepStrictEqual(noDir, [], 'collectGates with no directory must yield no rows');

  // The populated-ledger half of the guard uses a temp fixture directory, not the
  // gitignored Saved/ folder: a clean checkout has no Saved/ and must still pass.
  const fs = require('fs');
  const os = require('os');
  const path = require('path');
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 't0-gates-'));
  try {
    // NO_VERDICT on purpose: a real artifact that records no pass field. Not a pass.
    fs.writeFileSync(path.join(tmp, 't0_m1_wake_gate.json'), JSON.stringify({ notes: 'fixture' }));
    const res = R.reconcile({ savedDir: tmp });
    assert.ok(res.ok, res.error);
    const withClaim = res.beats.filter((b) => b.claimed !== 'NO_ARTIFACT');
    assert.ok(
      withClaim.length > 0,
      'no beat has a claim; the evidence ledger is not being read'
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});

test('the rendered report has no uninterpolated template holes', () => {
  // A single-quoted string containing ${...} renders literally and looks like data.
  const md = R.render(R.reconcile());
  assert.ok(!/\$\{/.test(md), 'report contains an uninterpolated ${...}');
  assert.ok(md.includes('of 14'), 'the acceptance count must be interpolated');
});
