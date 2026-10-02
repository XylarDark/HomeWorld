const test = require('node:test');
const assert = require('node:assert');
const C = require('./complexity-check.js');
const A = require('./anti-sycophancy.js');

test('complexity ignores comments and strings, or it is noise', () => {
  // A complexity checker that counts a `&&` inside a doc comment is worse than none:
  // it cries wolf on every well-explained function and gets ignored. This is the
  // specific way that failure happens.
  const withComment = 'function f(a, b) {\n  // we use a && b here deliberately\n  return 1;\n}';
  const withString = 'function f() {\n  return "a && b || c";\n}';
  assert.strictEqual(C.complexityOf(withComment).score, 1, 'a comment must not add a decision point');
  assert.strictEqual(C.complexityOf(withString).score, 1, 'a string must not add a decision point');

  // And real decision points must still count, or the gate is vacuous.
  const real = 'function f(a, b) {\n  if (a) { return 1; } else { return 2; }\n}';
  assert.ok(C.complexityOf(real).score > 1, 'a real `if` must count');
});

test('complexity gate is a ratchet, not a permanently red light', () => {
  // 13 functions already exceed the junior ceiling. A gate that fails 13 times on
  // first run is a gate that stops being read within a week - worse than none,
  // because it manufactures the impression something is watched.
  const m = C.measure();
  assert.ok(m.functions.length > 50, 'must actually find functions');
  assert.strictEqual(m.max, C.DEFAULT_MAX);
  assert.ok(C.DEFAULT_MAX > C.JUNIOR_CEILING, 'the fail threshold must sit above the warn threshold');

  // The current worst function sets the high-water mark and must not exceed it.
  const worst = m.functions[0];
  assert.ok(worst.score <= C.DEFAULT_MAX, `high-water ${C.DEFAULT_MAX} must cover current worst ${worst.score}`);
});

test('the anti-sycophancy gate can never fail the build', () => {
  // Requiring a quota of disagreements per commit produces manufactured
  // disagreements, which is worse than sycophancy: false, and dressed as candour.
  // So it only ever warns, and that is asserted rather than assumed.
  const anyState = { logExists: true, live: 0, total: 0, struck: 0, newestDate: null, daysSince: null };
  assert.strictEqual(A.evaluate(anyState).errors.length, 0, 'must never produce an error');

  const stale = { logExists: true, live: 1, total: 1, struck: 0, newestDate: '2026-01-01', daysSince: 300 };
  assert.ok(A.evaluate(stale).warnings.length > 0, 'a stale log must warn');
  assert.match(A.evaluate(stale).warnings[0], /never disagrees/, 'the warning must say what it means');

  const missing = { logExists: false, live: 0, total: 0, struck: 0, newestDate: null, daysSince: null };
  assert.ok(A.evaluate(missing).warnings.length > 0, 'a missing log must warn');
});

test('the disagreement log parses bodies, not just headings', () => {
  // Regression for a real bug: the body was sliced to the end of the HEADING line,
  // so every entry parsed as empty, every date read as missing, and the gate
  // reported "no date found" on a correctly formatted log - plausible numbers
  // while measuring nothing.
  const m = A.measure();
  if (m.logExists && m.total > 0) {
    assert.ok(m.newestDate, `a formatted log must yield a date - got ${JSON.stringify(m)}`);
  }
});

test('an agent that never disagrees is flagged as untested, not as reliable', () => {
  // The warning's wording matters: it is read every session, and "zero
  // disagreements" must not read as a clean sheet.
  const r = A.evaluate({ logExists: true, live: 1, total: 1, struck: 0, newestDate: '2026-01-01', daysSince: 400 });
  const text = r.warnings.join(' ');
  assert.match(text, /not more reliable/i, 'must frame silence as untested, not as quality');
});