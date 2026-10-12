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

// ---------------------------------------------------------------------------
// MCP tool surface. The bug these guard against: an MCP config declares a
// COMMAND, not a tool list. The old counter read `server.tools` out of the
// config, always got undefined, summed to 0, and then printed that 0 as a
// measurement - "3 servers, 0 tool schemas" - for a session injecting 114.
// ---------------------------------------------------------------------------

test('the MCP surface is measured from a snapshot, not guessed from the config', () => {
  // No snapshot at all. The surface is UNMEASURED, and the one thing it must
  // never do is collapse that back to zero - "we did not count it" and "it is
  // free" are different claims and only one is true.
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'budget-mcp-nosnap-'));
  try {
    writeFixture(dir, 'opencode.json', JSON.stringify({ mcp: { servers: { unrealMCP: {}, mixar: {} } } }));
    writeFixture(dir, '.cursor/mcp.json.example', JSON.stringify({ mcpServers: { unrealMCP: {} } }));

    const m = B.measure(dir);
    assert.strictEqual(m.mcp.measured, false, 'a missing snapshot must not read as measured');
    assert.strictEqual(m.mcp.toolCount, null, 'an unmeasured surface must be null, never 0');
    assert.deepStrictEqual(
      m.mcp.missingFromSnapshot.sort(),
      ['mixar', 'unrealMCP'],
      'every declared server must be reported as un-snapshotted'
    );

    const r = B.evaluate(m);
    assert.strictEqual(r.errors.length, 0, 'a missing snapshot is not a hard failure by itself');
    assert.match(r.warnings.join(' '), /UNMEASURED/, 'the warning must say unmeasured, not zero');
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test('a declared-but-uncounted server is pending, not zero', () => {
  // `tools: null` means "declared, never captured". Counting it as 0 would
  // silently understate the surface; inventing a number would be worse.
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'budget-mcp-pending-'));
  try {
    writeFixture(dir, '.cursor/mcp.json.example', JSON.stringify({ mcpServers: { slate: {} } }));
    writeFixture(dir, 'Config/mcp-tool-snapshot.json', JSON.stringify({
      capturedAt: '2026-10-12',
      servers: { mcpA: { tools: 10, source: 'repo' }, slate: { tools: null, source: 'repo' } },
    }));
    const m = B.measure(dir);
    assert.strictEqual(m.mcp.toolCount, 10, 'only counted servers contribute');
    assert.deepStrictEqual(m.mcp.pending, ['slate'], 'uncounted servers must be listed as pending');
    assert.match(B.evaluate(m).warnings.join(' '), /under-counted/);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test('the MCP tool surface is a ratchet that fails on growth', () => {
  const m = B.measure();
  assert.ok(m.mcp.measured && m.mcp.toolCount > 0, `MCP surface must be measured, got ${JSON.stringify(m.mcp)}`);
  assert.ok(
    m.mcp.toolCount <= B.MCP_TOOLS_HIGH_WATER,
    `MCP surface is ${m.mcp.toolCount}, over the ${B.MCP_TOOLS_HIGH_WATER} high-water mark`
  );

  const grown = { ...m, mcp: { ...m.mcp, measured: true, toolCount: B.MCP_TOOLS_HIGH_WATER + 1, pending: [], missingFromSnapshot: [], staleInSnapshot: [] } };
  const r = B.evaluate(grown);
  assert.ok(r.errors.length > 0, 'exceeding the MCP high-water mark must fail');
  assert.match(r.errors.join(' '), /MCP surface/);
});

test('host config drift is reported in both directions', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'budget-mcp-drift-'));
  try {
    // Drift is measured against the LIVE config only. A template naming a server
    // is not proof anything runs, so it must not manufacture an unclosable warning.
    writeFixture(dir, 'opencode.json', JSON.stringify({ mcp: { servers: { live: {} } } }));
    writeFixture(dir, '.cursor/mcp.json.example', JSON.stringify({ mcpServers: { templateOnly: {} } }));
    writeFixture(dir, 'Config/mcp-tool-snapshot.json', JSON.stringify({
      servers: { ghost: { tools: 4, source: 'repo' } },
    }));
    const m = B.measure(dir);
    assert.deepStrictEqual(m.mcp.missingFromSnapshot, ['live'], 'declared-but-unsnapshotted');
    assert.deepStrictEqual(m.mcp.staleInSnapshot, ['ghost'], 'snapshotted-but-undeclared');
    assert.deepStrictEqual(
      m.mcp.declaredTemplateOnly,
      ['templateOnly'],
      'template-only servers are tracked but are not drift'
    );

    const warn = B.evaluate(m).warnings.join(' ');
    assert.match(warn, /absent from Config\/mcp-tool-snapshot\.json/);
    assert.match(warn, /no longer declared/);
    assert.doesNotMatch(warn, /templateOnly/, 'a template-only server must not warn');
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

// ---------------------------------------------------------------------------
// The loaded surface. Descriptions and MCP schemas cost context on every single
// request, and both were printed by this gate for a long time before anything
// watched them. Reporting a number is not gating it.
// ---------------------------------------------------------------------------

test('skill descriptions are a hard ceiling, not a printed statistic', () => {
  const m = B.measure();
  assert.ok(
    m.advertised.chars > 0 && m.advertised.chars <= B.ADVERTISED_MAX,
    `descriptions are ${m.advertised.chars} chars against a ${B.ADVERTISED_MAX} high-water mark`
  );

  const over = B.evaluate({ ...m, advertised: { ...m.advertised, chars: B.ADVERTISED_MAX + 1 } });
  assert.ok(over.errors.length > 0, 'growing the description surface must fail, not warn');
  assert.match(over.errors.join(' '), /skill descriptions/);
});

test('.cursor/skills is inside the reachable corpus, not outside the budget', () => {
  // opencode.json lists ".cursor/skills" under `skills`, so a loader reads that
  // tree. It used to sit outside `total` entirely, which meant a second copy of
  // the corpus could be added without the ratchet noticing.
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'budget-cursor-skills-'));
  const body = ['---', 'name: twin', 'description: A twin.', '---', '', '# Twin', '', 'One.', 'Two.', ''].join('\n');
  try {
    writeFixture(dir, '.agents/skills/twin/SKILL.md', body);
    writeFixture(dir, '.cursor/skills/twin/SKILL.md', body);

    const m = B.measure(dir);
    assert.ok(m.cursorSkills.lines > 0, '.cursor/skills must be measured');
    assert.ok(
      m.total >= m.skills.lines + m.cursorSkills.lines,
      'the reachable total must include both skill trees'
    );

    // And the real tree is inside its own ratchet.
    const real = B.measure();
    assert.strictEqual(
      real.total,
      real.rules.lines + real.skills.lines + real.cursorSkills.lines,
      'reachable total must be exactly the three reachable trees'
    );
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});