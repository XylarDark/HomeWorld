#!/usr/bin/env node
/**
 * Tests for harness-fitness.
 *
 * The harness has a documented history of confidently-wrong numbers: McNemar
 * comparing one check per task and calling it "no discordance" on a 23-point
 * difference; --resume re-running every cell because two key formats never
 * matched; a report that printed the opposite sign on its headline number. All
 * three were fixed with regression tests, and the pattern behind them is named
 * in the handoff: a transformation broad enough to be convenient is usually
 * broad enough to be wrong.
 *
 * So these tests are mostly negative. Each one constructs the failure this
 * script could plausibly get wrong and asserts it does NOT pass.
 */

const { test } = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');

const {
  premiseShape,
  premiseBounds,
  premisePurposeful,
  premiseProduct,
  recordOutOfBounds,
} = require('./harness-fitness');
const budget = require('./instruction-budget');

function files(list) {
  return list.map((f) => ({ files: Array.isArray(f) ? f : [f] }));
}

/* --------------------------------------------------------------- premise 4
 *
 * This is the premise most able to lie, because it reads a commit log and
 * classifies the files. A classifier that is too broad marks product work as
 * harness work and reports a false crisis; too narrow hides a real one.
 * A subject line is not evidence. The paths are.
 */

test('product premise: harness work counts toward the numerator', () => {
  const commits = [
    ...files(['AGENTS.md', '.cursor/rules/a.mdc', '.agents/skills/x/SKILL.md', 'scripts/instruction-budget.js']),
    ...files(Array.from({ length: 10 }, (_, i) => `Source/HomeWorld/P${i}.cpp`)),
  ];
  const r = premiseProduct(commits);
  assert.strictEqual(r.skipped, undefined);
  assert.match(r.detail, /4 harness \/ 10 product/);
  assert.strictEqual(r.ok, true, r.detail);
});

test('product premise: a harness-heavy window is reported as broken, not excused', () => {
  const commits = [
    ...files(Array.from({ length: 8 }, (_, i) => `.cursor/rules/${i}.mdc`)),
    ...files(['Source/HomeWorld/A.cpp', 'Source/HomeWorld/B.cpp']),
  ];
  const r = premiseProduct(commits);
  assert.strictEqual(r.ok, false, 'the old 24:8 shape must read as broken');
});

test('product premise: too few commits is a skip, never a pass and never a break', () => {
  // THE failure mode this guards: a 3-commit window has no ratio in it. Reading
  // it as "fine" because harnessCommits(2) < productCommits(1) is false by
  // ordering, and reading it as broken is noise. It is neither - it is skipped.
  const r = premiseProduct(files(['AGENTS.md', '.cursor/rules/a.mdc', 'Source/HomeWorld/A.cpp']));
  assert.strictEqual(r.skipped, true, 'small windows must be skipped');
  assert.strictEqual(r.ok, true, 'skipped is not broken');
});

test('product premise: an all-product window is unambiguously fine', () => {
  const commits = files(Array.from({ length: 12 }, (_, i) => `Source/HomeWorld/P${i}.cpp`));
  const r = premiseProduct(commits);
  assert.strictEqual(r.ok, true);
  assert.strictEqual(r.skipped, undefined);
});

test('product premise: an exactly-balanced window passes (tied is not over budget)', () => {
  const commits = [
    ...files(Array.from({ length: 5 }, () => 'scripts/harness-fitness.js')),
    ...files(Array.from({ length: 5 }, (_, i) => `Content/Maps/P${i}.umap`)),
  ];
  const r = premiseProduct(commits);
  assert.strictEqual(r.ok, true, '5/5 is product-dominant enough; the bar is not "> product"');
});

test('product premise: the Slate pointer commit is harness work without a (harness) subject', () => {
  const slate = {
    subject: 'Point a failed editor write at the Slate skill instead of the deleted clicker scripts.',
    files: [
      'AGENTS.md',
      '.agents/skills/automation-gap-solutions/SKILL.md',
      '.agents/skills/pcg-validate/SKILL.md',
      '.cursor/rules/18-game-development-principles.mdc',
      '.cursor/rules/19-automation-gaps.mdc',
      '.cursor/rules/20-full-automation-no-manual-steps.mdc',
      '.cursor/rules/automation-standards.mdc',
    ],
  };
  const product = files(Array.from({ length: 12 }, (_, i) => `Source/HomeWorld/File${i}.cpp`));
  const r = premiseProduct([slate, ...product]);
  assert.strictEqual(r.skipped, undefined);
  assert.match(r.detail, /1 harness \/ 12 product/);
  assert.strictEqual(r.ok, true, r.detail);
});

test('product premise: a commit that touches harness and product paths is excluded', () => {
  const mixed = { files: ['AGENTS.md', 'Source/HomeWorld/X.cpp'] };
  const product = files(Array.from({ length: 10 }, (_, i) => `Source/HomeWorld/P${i}.cpp`));
  const r = premiseProduct([mixed, ...product]);
  assert.match(r.detail, /0 harness \/ 10 product/);
  assert.match(r.detail, /1 mixed excluded/);
  assert.strictEqual(r.ok, true, r.detail);
});

/* --------------------------------------------------------------- premise 1 */

test('product premise: a commit that only edits Docs is not harness work', () => {
  // P1-P8 of PRODUCT_SPRINT_01 are docs: commits and must count as product. If the
  // classifier called them harness, the fitness check would keep reporting a
  // harness crisis while the team shipped the sprint - a false alarm, which is
  // the failure mode that makes a gate get ignored.
  const commits = files([
    'Docs/28_TASTE_GATES.md',
    'docs/art/pipeline.md',
    'Docs/context/SESSION_START.md',
    ...Array.from({ length: 9 }, (_, i) => `Docs/sprint/P${i}.md`),
  ]);
  const r = premiseProduct(commits);
  assert.strictEqual(r.skipped, undefined);
  assert.match(r.detail, /0 harness \/ 12 product/);
  assert.strictEqual(r.ok, true, `docs commits are product work: ${r.detail}`);
});

test('shape premise: reads the real package.json', () => {
  const r = premiseShape();
  assert.strictEqual(r.ok, true, `six declared commands must be present: ${r.detail}`);
  assert.ok(!/missing/.test(r.detail), 'no command may be reported missing');
});

test('bounds premise: a missing budget record is not a pass', () => {
  // Docs/qa/instruction_budget.json is not in the tree. The old premise skipped
  // and still returned ok, which is "could not measure" reported as a pass.
  const r = premiseBounds();
  const measured = budget.measure();
  assert.ok(!r.skipped, 'a missing JSON record must not skip');
  assert.match(r.detail, new RegExp(`${measured.total} instruction lines`));
  assert.strictEqual(r.ok, measured.total <= budget.TOTAL_HIGH_WATER);
});

test('purposefulness: a non-empty file does not claim a recent disagreement', () => {
  const r = premisePurposeful();
  if (r.ok) assert.match(r.detail, /does not prove a recent disagreement/);
});

/* --------------------------------------------------- out-of-bounds ledger */

test('out-of-bounds: first sighting records seen=1', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'oob-'));
  try {
    const r = recordOutOfBounds('test:sig', 'a response', tmp);
    assert.strictEqual(r.seen, 1);
    assert.strictEqual(r.firstTime, true);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});

test('out-of-bounds: a second sighting increments to 2 in place, not as a duplicate row', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'oob-'));
  try {
    recordOutOfBounds('test:sig', 'first response', tmp);
    const r = recordOutOfBounds('test:sig', 'second response', tmp);
    assert.strictEqual(r.seen, 2, 'the count must reflect a real second sighting');

    const text = fs.readFileSync(
      path.join(tmp, 'Docs/decisions/OUT_OF_BOUNDS.md'),
      'utf8'
    );
    const rows = text.split('\n').filter((l) => l.includes('`test:sig`'));
    assert.strictEqual(rows.length, 1, 'one row per signature, not one per sighting');
    assert.ok(rows[0].includes('| 2 |'), 'the count column shows 2');
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});

test('out-of-bounds: two different signatures get two rows', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'oob-'));
  try {
    recordOutOfBounds('sig:one', 'response one', tmp);
    recordOutOfBounds('sig:two', 'response two', tmp);
    const text = fs.readFileSync(
      path.join(tmp, 'Docs/decisions/OUT_OF_BOUNDS.md'),
      'utf8'
    );
    assert.ok(text.includes('`sig:one`'), 'first signature present');
    assert.ok(text.includes('`sig:two`'), 'second signature present');
    assert.strictEqual(
      text.split('\n').filter((l) => l.startsWith('| 20')).length,
      2,
      'exactly two data rows'
    );
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});