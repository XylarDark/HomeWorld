#!/usr/bin/env node
/**
 * Tests for the shared outcome vocabulary.
 *
 * The ordering rule in `verdictFor` is the whole point: an absent subject must
 * never be reported as a failed one. The 2026-10-01 pilot turned eight runs that
 * produced nothing into a plausible-looking conformance delta because there was
 * no way to say "never measured".
 */

const test = require('node:test');
const assert = require('node:assert');
const O = require('./outcome.js');

test('an absent subject is void, never a failure', () => {
  // The single most important assertion in this file. `pass: false` with an absent
  // subject must NOT become closed_fail.
  assert.strictEqual(O.verdictFor({ subjectPresent: false, pass: false }), O.VOID);
  assert.strictEqual(O.verdictFor({ subjectPresent: false, pass: true }), O.VOID);
});

test('a measured subject gets one of the three PDF states', () => {
  assert.strictEqual(O.verdictFor({ subjectPresent: true, pass: true }), 'pass');
  assert.strictEqual(O.verdictFor({ subjectPresent: true, pass: true, soft: true }), 'soft_fail');
  assert.strictEqual(O.verdictFor({ subjectPresent: true, pass: false }), 'closed_fail');
});

test('void is documented as having no PDF equivalent', () => {
  // It is the absence of a state, not a fourth one. If someone later "fixes" this
  // by mapping void to closed_fail, the pilot bug returns.
  assert.ok(!O.CHECK_VERDICTS.includes(O.VOID));
  assert.deepStrictEqual([...O.CHECK_VERDICTS], ['pass', 'soft_fail', 'closed_fail']);
  assert.match(O.PDF_MAPPING[O.VOID], /NOT MEASURED/);
});

test('tombstones are detected from description alone', () => {
  assert.ok(O.isTombstoneDescription('RETIRED P4. Do not restore this duplicate card.'));
  assert.ok(O.isTombstoneDescription('QUARANTINE - WAVE F removed.'));
  assert.ok(O.isTombstoneDescription('retired p4'), 'case insensitive');
  assert.ok(!O.isTombstoneDescription('C++ build helper rules for Unreal 5.8.'));
  assert.ok(!O.isTombstoneDescription(undefined));
  assert.ok(!O.isTombstoneDescription(''));
});

test('tombstone detection is not fooled by a missing description', () => {
  // A rule with no description is not a tombstone. Treating absent as retired would
  // exempt every malformed rule from the scope requirement.
  assert.strictEqual(O.isTombstoneDescription(undefined), false);
  assert.strictEqual(O.isTombstoneDescription(null), false);
});
