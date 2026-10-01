#!/usr/bin/env node
/**
 * Unit tests for score-mdc-rules.js (no UE, no SkillEvaluator required).
 * Run: node --test scripts/score-mdc-rules.test.js
 */
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const test = require('node:test');

const script = path.join(__dirname, 'score-mdc-rules.js');
const projectRoot = path.resolve(__dirname, '..');
const {
  DEFAULT_THRESHOLD,
  FORMAT_OFFSET_COMPOSITE,
  parseFrontmatter,
  yamlQuote,
  slugify,
  parseScore,
  toolVersion,
  classifyTombstone,
  readRule,
  materializeSkill,
} = require('./score-mdc-rules.js');

function runCli(args) {
  return spawnSync(process.execPath, [script, ...args], {
    cwd: projectRoot,
    encoding: 'utf8',
  });
}

function tmpDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'hw-mdc-test-'));
}

test('parseFrontmatter reads quoted and bare values', () => {
  const text = [
    '---',
    'name: "MCP-First Workflow"',
    'description: "Use when driving the Editor via MCP"',
    'alwaysApply: false',
    '---',
    '',
    '# Body',
    '',
  ].join('\n');
  const { data, body, present } = parseFrontmatter(text);
  assert.strictEqual(present, true);
  assert.strictEqual(data.name, 'MCP-First Workflow');
  assert.strictEqual(data.description, 'Use when driving the Editor via MCP');
  assert.strictEqual(data.alwaysApply, 'false');
  assert.match(body, /# Body/);
  assert.doesNotMatch(body, /alwaysApply/);
});

test('parseFrontmatter reports absence instead of throwing', () => {
  const { data, present } = parseFrontmatter('# No frontmatter here\n');
  assert.strictEqual(present, false);
  assert.deepStrictEqual(data, {});
});

test('yamlQuote escapes backslashes and double quotes', () => {
  assert.strictEqual(yamlQuote('plain'), '"plain"');
  assert.strictEqual(yamlQuote('say "hi"'), '"say \\"hi\\""');
  assert.strictEqual(yamlQuote('back\\slash'), '"back\\\\slash"');
});

test('slugify satisfies the SKILL.md name constraint', () => {
  assert.strictEqual(slugify('MCP-First Workflow'), 'mcp-first-workflow');
  assert.strictEqual(slugify('JSON/YAML Configuration Standards'), 'json-yaml-configuration-standards');
  assert.ok(/^[a-z0-9-]+$/.test(slugify('Unreal Engine (general)')));
});

test('slugify falls back to the file stem when name is absent', () => {
  // 16-feature-debug-instrumentation.mdc genuinely has no `name:` key.
  assert.strictEqual(slugify('', '16-feature-debug-instrumentation'), '16-feature-debug-instrumentation');
});

test('parseScore returns null on unrecognised output, never 0', () => {
  // A zero here would masquerade as a failing grade.
  assert.strictEqual(parseScore('totally unparseable'), null);
  assert.strictEqual(parseScore(undefined), null);
  assert.strictEqual(parseScore(''), null);
  assert.deepStrictEqual(parseScore('Overall: 88.5/100 (Grade: B)'), { score: 88.5, grade: 'B' });
  assert.deepStrictEqual(parseScore('Overall: 79/100 (Grade: C)'), { score: 79, grade: 'C' });
});

test('materializeSkill writes a scorable Agent Skill and keeps provenance', () => {
  const dir = tmpDir();
  try {
    const rule = readRule(path.join(projectRoot, '.cursor/rules/unreal-gas.mdc'), '.cursor/rules');
    const out = materializeSkill(rule, dir);
    const written = fs.readFileSync(path.join(out, 'SKILL.md'), 'utf8');
    assert.ok(written.startsWith('---'));
    // `version` must survive: dropping it makes SkillEvaluator deduct 5
    // correctness points against every rule for an adapter's own omission.
    assert.match(written, /^version: /m);
    assert.match(written, /^name: unreal-gas-standards$/m);
    // alwaysApply / globs are preserved but explicitly NOT scored.
    assert.match(written, /alwaysApply: false/);
    assert.match(written, /source: \.cursor\/rules\/unreal-gas\.mdc/);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test('every repo rule materializes with a name and a description', () => {
  const dir = tmpDir();
  try {
    const rulesDir = path.join(projectRoot, '.cursor/rules');
    const files = fs.readdirSync(rulesDir).filter((f) => f.endsWith('.mdc'));
    assert.ok(files.length > 0, 'expected .mdc rules to exist');
    for (const file of files) {
      const rule = readRule(path.join(rulesDir, file), rulesDir);
      assert.ok(/^[a-z0-9-]+$/.test(rule.slug), `${file} slug is not skill-safe: ${rule.slug}`);
      assert.ok(rule.description.length > 0, `${file} has no description`);
    }
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test('CLI exits 2 and refuses a report when the scorer is missing', () => {
  // Fail-loud is the whole point: without the real scorer we must NOT print a
  // clean run, because an unmeasured rule cannot be reported as passing.
  const r = runCli(['--tool', path.join(os.tmpdir(), 'definitely-not-here'), '--limit', '1']);
  assert.strictEqual(r.status, 2);
  assert.match(r.stderr, /SkillEvaluator not found/);
  // It must refuse rather than crash: a stack trace is not a clean refusal.
  assert.doesNotMatch(r.stderr, /at Object|node:internal|TypeError/);
});

test('an explicit --tool is never silently substituted by a PATH binary', () => {
  // Falling back would attribute one scorer's numbers to another, which is the
  // fail-open trap. Even though a real skillevaluator IS on this machine, a
  // bogus --tool must exit 2 rather than quietly using it.
  const r = runCli(['--tool', path.join(os.tmpdir(), 'definitely-not-here'), '--limit', '1']);
  assert.strictEqual(r.status, 2);
  assert.match(r.stderr, /never substituted|not falling back/i);
  assert.doesNotMatch(r.stdout, /mean\s+:/, 'must not emit a scored report');
});

test('CLI exits 2 on an unknown argument', () => {
  const r = runCli(['--bogus']);
  assert.strictEqual(r.status, 2);
  assert.match(r.stderr, /unknown arg/);
});

test('CLI exits 2 on a missing rules directory', () => {
  const r = runCli(['--rules-dir', '.cursor/definitely-not-here']);
  assert.strictEqual(r.status, 2);
  assert.match(r.stderr, /no rules directory/);
});

test('declared offsets and defaults are self-consistent', () => {
  // 5 points each for metadata.author and metadata.tags, weighted 0.35.
  assert.strictEqual(FORMAT_OFFSET_COMPOSITE, 3.5);
  assert.strictEqual(DEFAULT_THRESHOLD, 80);
});

test('classifyTombstone fires only on a self-declaration in the description', () => {
  // The corpus declares five tombstones, each by starting its description
  // with a status marker.
  for (const desc of [
    'QUARANTINE - WAVE F / run_automation_cycle removed. Do not resurrect.',
    'HISTORICAL: HomeWorld targets UE 5.8. Use ue58-sources.mdc.',
    'RETIRED P4. AGENTS.md is the single project-context surface.',
    'DEPRECATED - replaced by the 5.8 rules.',
  ]) {
    const c = classifyTombstone({ description: desc });
    assert.strictEqual(c.tombstone, true, `should classify as tombstone: ${desc}`);
    assert.ok(c.marker, 'marker must be recorded');
  }
  // A marker anywhere else in the sentence is not a self-declaration.
  assert.strictEqual(classifyTombstone({ description: 'Use when the API is deprecated' }).tombstone, false);
  assert.strictEqual(classifyTombstone({ description: 'Apply when quarantine rules apply' }).tombstone, false);
  assert.strictEqual(classifyTombstone({ description: 'Never run the retired agent loop' }).tombstone, false);
  assert.strictEqual(classifyTombstone({ description: '' }).tombstone, false);
});

test('classifyTombstone ignores body-only mentions of removed/deprecated', () => {
  // The real hazard: 14 of 31 rules mention "deprecated"/"removed" somewhere,
  // almost always describing a UE API or a deleted tool rather than the rule
  // itself. Matching body text would exempt most of the corpus.
  const dir = path.join(projectRoot, '.cursor/rules');
  for (const file of ['unreal-cpp.mdc', '00-core-principles.mdc', '05-error-handling.mdc', '20-full-automation-no-manual-steps.mdc', '19-automation-gaps.mdc']) {
    const rule = readRule(path.join(dir, file), dir);
    assert.strictEqual(
      classifyTombstone(rule).tombstone,
      false,
      `${file} must stay substantive — it mentions removed/deprecated only in its body`
    );
  }
});

test('the tombstone corpus is exactly the five self-declared rules', () => {
  const dir = path.join(projectRoot, '.cursor/rules');
  const files = fs.readdirSync(dir).filter((f) => f.endsWith('.mdc'));
  const tombs = files
    .filter((f) => classifyTombstone(readRule(path.join(dir, f), dir)).tombstone)
    .sort();
  assert.deepStrictEqual(tombs, [
    '07-ai-agent-behavior.mdc',
    '08-project-context.mdc',
    '19-automation-cycle.mdc',
    'ue57-editor-ui.mdc',
    'ue57-sources.mdc',
  ]);
});

test('toolVersion reads a semver from --version output', () => {
  const probe = spawnSync(process.execPath, ['--version'], { encoding: 'utf8' });
  const v = toolVersion(process.execPath);
  assert.match(v, /^\d+\.\d+\.\d+/);
  assert.ok(v !== 'unknown', `expected a version from: ${probe.stdout}`);
});

test('toolVersion returns unknown rather than throwing when unparseable', () => {
  // A missing version must not fail a run whose scores are otherwise valid;
  // the report carries rubricComparable:false instead.
  const stub = path.join(tmpDir(), 'fake-tool.js');
  fs.writeFileSync(stub, 'console.log("no version here");\n', 'utf8');
  assert.strictEqual(toolVersion(process.execPath + ' ' + stub), 'unknown');
});