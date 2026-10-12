const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const B = require('./instruction-budget.js');

function writeFixture(dir, rel, text) {
  const abs = path.join(dir, rel);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  fs.writeFileSync(abs, text, 'utf8');
}

test('the budget gate can count, and its count is not trivially small', () => {
  // Regression guard for a real bug. The first version treated every `---` as YAML
  // front matter, so table separators and horizontal rules swallowed entire files:
  // it reported 8 lines for a 176-line AGENTS.md and 0 across all 25 rules, then
  // PASSED. A gate that cannot count is worse than no gate, because it manufactures
  // confidence that the budget is respected.
  const m = B.measure();
  // Floor is 23: the slimmed AGENTS.md's measured count, not a pad target.
  assert.ok(m.alwaysOn >= 23, `always-on must be countable, got ${m.alwaysOn}`);
  assert.ok(m.rules.lines > 500, `rules must be countable, got ${m.rules.lines}`);
  assert.ok(m.skills.lines > 500, `skills must be countable, got ${m.skills.lines}`);
});

test('the always-on surface has a real ceiling, and it is enforced hard', () => {
  // AGENTS.md is in context on every single request. OpenAI ships ~100 lines because
  // theirs is a table of contents, not the manual. This is the one hard limit.
  const m = B.measure();
  assert.ok(
    m.alwaysOn <= B.ALWAYS_ON_MAX,
    `always-on is ${m.alwaysOn}, over the ${B.ALWAYS_ON_MAX} ceiling - move detail to docs/`
  );
  // And the gate must actually fail when breached, not merely report it.
  const over = B.evaluate({ ...m, alwaysOn: B.ALWAYS_ON_MAX + 1 });
  assert.ok(over.errors.length > 0, 'breaching the always-on ceiling must be an error');
  assert.match(over.errors[0], /always-on/);
});

test('the total is a ratchet that only lowers', () => {
  const m = B.measure();
  const ok = B.evaluate(m);
  assert.strictEqual(ok.errors.length, 0, `current tree must pass: ${ok.errors.join('; ')}`);

  // Above high-water is a failure.
  const above = B.evaluate({ ...m, total: B.TOTAL_HIGH_WATER + 1 });
  assert.ok(above.errors.length > 0, 'exceeding the high-water mark must fail');
  assert.match(above.errors.join(' '), /ratchet/);

  // Between low and high is a warning, not a failure - otherwise the gate fails
  // every run, gets ignored, and stops being watched at all.
  const between = B.evaluate({ ...m, total: B.TOTAL_LOW_WATER + 10 });
  assert.strictEqual(between.errors.length, 0, 'mid-range must not be a hard failure');
  assert.ok(between.warnings.length > 0, 'mid-range must warn');

  // At or below target is silent.
  const done = B.evaluate({ ...m, total: B.TOTAL_LOW_WATER });
  assert.strictEqual(done.warnings.length, 0, 'reaching the target must clear the warning');
});

test('two full copies of one skill are a duplicate body', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'budget-dup-'));
  const body = [
    '---',
    'name: dup-skill',
    'description: Set the forest tag and the mesh list.',
    '---',
    '',
    '# Dup',
    '',
    'This is the procedure.',
    'It is long enough that it is not a pointer.',
    'Step one stays here.',
    'Step two stays here.',
    'Step three stays here.',
    'Step four stays here.',
    'Step five stays here.',
    'Step six stays here.',
    'Step seven stays here.',
    'Step eight stays here.',
    'Step nine stays here.',
    'Step ten stays here.',
    'Step eleven stays here.',
    'Step twelve stays here.',
    'Step thirteen stays here.',
    '',
  ].join('\n');
  try {
    writeFixture(dir, '.agents/skills/dup-skill/SKILL.md', body);
    writeFixture(dir, '.cursor/skills/dup-skill/SKILL.md', body);
    writeFixture(dir, '.agents/skills/wide-skill/SKILL.md', [
      '---',
      'name: wide-skill',
      'description: Use this for any coding task.',
      '---',
      '',
      '# Wide',
      '',
    ].join('\n'));
    const m = B.measure(dir);
    assert.deepStrictEqual(m.duplicates.bodies, ['dup-skill']);
    const descriptions = [
      'Set the forest tag and the mesh list.',
      'Set the forest tag and the mesh list.',
      'Use this for any coding task.',
    ];
    assert.strictEqual(m.advertised.chars, descriptions.reduce((n, d) => n + d.length, 0));
    assert.deepStrictEqual(m.advertised.broad.map((e) => e.name), ['wide-skill']);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test('a markdown table rule does not zero the file', () => {
  // The first counter treated every `---` as the end of YAML front matter, so a
  // table separator swallowed the rest of the file and the gate reported a
  // handful of lines for a real document.
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'budget-table-'));
  const table = [
    '# Title',
    '',
    '| A | B |',
    '|---|---|',
    '| 1 | 2 |',
    '| 3 | 4 |',
    '',
    '---',
    '',
    'After the rule.',
  ].join('\n');
  try {
    writeFixture(dir, 'AGENTS.md', table);
    const m = B.measure(dir);
    assert.strictEqual(m.alwaysOn, B.countText(table));
    assert.ok(m.alwaysOn >= 7, `table file was counted as ${m.alwaysOn}`);
    assert.strictEqual(m.alwaysOnChars, table.length);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test('docs/ is excluded, because it is the system of record', () => {
  // Counting docs/ would penalise exactly the shape OpenAI converged on: a short
  // index plus detail read on demand. The system of record is not context.
  const measured = B.measure();
  assert.strictEqual(
    Object.prototype.hasOwnProperty.call(measured, 'docs'),
    false,
    'docs/ must not be part of the instruction budget'
  );
});