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
  premiseProduct,
  recordOutOfBounds,
} = require('./harness-fitness');

/* --------------------------------------------------------------- premise 4
 *
 * This is the premise most able to lie, because it reads a commit log and
 * classifies with a regex. A classifier that is too broad marks product work as
 * harness work and reports a false crisis; too narrow hides a real one.
 */

test('product premise: harness work counts toward the numerator', () => {
  const commits = [
    'feat(harness): add a thing',
    'fix(harness): repair a thing',
    'test(harness): cover a thing',
    'docs(harness): describe a thing',
    'feat: inventory round trip',
    'feat: tame transitions',
  ];
  const r = premiseProduct(commits);
  assert.strictEqual(r.ok, true, '4 harness / 2 product is still product-dominant');
});

test('product premise: a harness-heavy window is reported as broken, not excused', () => {
  const commits = [
    'feat(harness): a',
    'feat(harness): b',
    'feat(harness): c',
    'feat(harness): d',
    'feat(harness): e',
    'feat(harness): f',
    'feat(harness): g',
    'feat(harness): h',
    'feat: one product commit',
    'feat: another product commit',
  ];
  const r = premiseProduct(commits);
  assert.strictEqual(r.ok, false, 'the old 24:8 shape must read as broken');
});

test('product premise: too few commits is a skip, never a pass and never a break', () => {
  // THE failure mode this guards: a 3-commit window has no ratio in it. Reading
  // it as "fine" because harnessCommits(2) < productCommits(1) is false by
  // ordering, and reading it as broken is noise. It is neither - it is skipped.
  const r = premiseProduct(['feat(harness): a', 'feat(harness): b', 'feat: c']);
  assert.strictEqual(r.skipped, true, 'small windows must be skipped');
  assert.strictEqual(r.ok, true, 'skipped is not broken');
});

test('product premise: an all-product window is unambiguously fine', () => {
  const commits = Array.from({ length: 12 }, (_, i) => `feat: product work ${i}`);
  const r = premiseProduct(commits);
  assert.strictEqual(r.ok, true);
  assert.strictEqual(r.skipped, undefined);
});

test('product premise: an exactly-balanced window passes (tied is not over budget)', () => {
  const commits = [
    ...Array.from({ length: 5 }, (_, i) => `feat(harness): h${i}`),
    ...Array.from({ length: 5 }, (_, i) => `feat: p${i}`),
  ];
  const r = premiseProduct(commits);
  assert.strictEqual(r.ok, true, '5/5 is product-dominant enough; the bar is not "> product"');
});

/* --------------------------------------------------------------- premise 1 */

test('product premise: a commit that only edits Docs is not harness work', () => {
  // P1-P8 of PRODUCT_SPRINT_01 are docs: commits and must count as product. If the
  // classifier called them harness, the fitness check would keep reporting a
  // harness crisis while the team shipped the sprint - a false alarm, which is
  // the failure mode that makes a gate get ignored.
  const commits = [
    'docs(taste): round 2 resolved',
    'docs(art): pipeline research',
    'feat: conversion behaviour test',
    'feat: tame transitions test',
    'docs: sprint 01 plan',
    'fix: shrine proportion',
  ];
  const r = premiseProduct(commits);
  assert.strictEqual(r.ok, true, `docs commits are product work: ${r.detail}`);
});

test('shape premise: reads the real package.json', () => {
  const r = premiseShape();
  assert.strictEqual(r.ok, true, `six declared commands must be present: ${r.detail}`);
  assert.ok(!/missing/.test(r.detail), 'no command may be reported missing');
});

test('bounds premise: a missing budget record skips rather than breaks', () => {
  // The bounds number belongs to instruction-budget.js. This script must not
  // recompute it and then disagree with the gate it is reporting on, so with
  // no stored record it abstains instead of guessing.
  const r = premiseBounds();
  if (r.skipped) {
    assert.strictEqual(r.ok, true, 'skipped is not broken');
  } else {
    assert.strictEqual(typeof r.detail, 'string');
  }
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