#!/usr/bin/env node
/**
 * Unit tests for score-mdc-lift.js.
 *
 * No network, no API key, no SkillEvaluator required. Every test here must pass
 * on a machine that has never seen a provider credential — that is the point:
 * the fail-loud paths are the ones most worth proving, and they are the ones a
 * credential would otherwise hide.
 *
 * Run: node --test scripts/score-mdc-lift.test.js
 */
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const test = require('node:test');

const script = path.join(__dirname, 'score-mdc-lift.js');
const projectRoot = path.resolve(__dirname, '..');
const {
  parseRubric,
  parseCriteria,
  CRITERIA,
  CACHE_MAX_SAMPLES,
  detectCredential,
  resolveTool,
  failureReason,
  scoreWithRetries,
  hashSkillDir,
  cacheKeyFor,
  isValidSample,
  loadCache,
  cacheRead,
  cacheStore,
  saveCache,
} = require('./score-mdc-lift.js');

const CRED_VARS = ['SKILL_EVAL_LLM_PROVIDER', 'NVIDIA_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY'];

/**
 * Run the CLI.
 *
 * By default every credential is deleted first, so the fail-loud paths are
 * tested on a machine that has no key. Pass extraEnv to supply one where a
 * check sits behind the credential gate. The values used here are deliberate
 * non-secrets; no test in this file may contain a real key.
 */
function runCli(args, extraEnv = null) {
  const env = { ...process.env };
  if (extraEnv) {
    Object.assign(env, extraEnv);
  } else {
    for (const v of CRED_VARS) delete env[v];
  }
  return spawnSync(process.execPath, [script, ...args], { cwd: projectRoot, encoding: 'utf8', env });
}

test('parseRubric reads a score from spawnSync output', () => {
  const r = parseRubric({ stdout: '  LLM Rubric Score: 57.7/100\n', stderr: '' });
  assert.deepStrictEqual(r, { score: 57.7 });
});

test('parseRubric tolerates leading noise and integer scores', () => {
  assert.deepStrictEqual(parseRubric({ stdout: 'junk\n  LLM Rubric Score: 60 / 100\nmore' }), { score: 60 });
});

test('parseRubric returns null for unrecognised output, never 0', () => {
  // A 0 would masquerade as a failing grade when it means "unmeasured".
  assert.strictEqual(parseRubric({ stdout: 'totally unparseable' }), null);
  assert.strictEqual(parseRubric({ stdout: '', stderr: '' }), null);
  assert.strictEqual(parseRubric({}), null);
});

test('parseRubric returns null rather than throwing on bad input types', () => {
  for (const bad of [undefined, null, '', 0, 42, true, [], () => {}]) {
    assert.strictEqual(parseRubric(bad), null, `must not throw on ${JSON.stringify(bad) ?? String(bad)}`);
  }
});

test('detectCredential reports unconfigured when nothing is set', () => {
  const c = detectCredential();
  assert.strictEqual(c.configured, false);
  assert.strictEqual(c.provider, '(unset)');
  assert.strictEqual(c.credentialVar, '(none)');
  assert.strictEqual(c.credentialLength, 0);
});

test('detectCredential never returns the secret, only its length', () => {
  const secret = 'nvapi-SUPERSECRETVALUE-0123456789';
  const prev = { ...process.env };
  process.env.SKILL_EVAL_LLM_PROVIDER = 'nv_build';
  process.env.NVIDIA_API_KEY = secret;
  try {
    const c = detectCredential();
    const serialised = JSON.stringify(c);
    assert.strictEqual(c.configured, true);
    assert.strictEqual(c.provider, 'nv_build');
    assert.strictEqual(c.credentialVar, 'NVIDIA_API_KEY');
    assert.strictEqual(c.credentialLength, secret.length);
    assert.ok(!serialised.includes('SUPERSECRET'), 'secret must not appear anywhere in the object');
    assert.ok(!serialised.includes(secret));
  } finally {
    for (const k of CRED_VARS) {
      if (prev[k] === undefined) delete process.env[k];
      else process.env[k] = prev[k];
    }
  }
});

test('a key without a provider selector is still unconfigured', () => {
  const prev = { ...process.env };
  process.env.SKILL_EVAL_LLM_PROVIDER = '';
  process.env.NVIDIA_API_KEY = 'nvapi-only-a-key';
  try {
    assert.strictEqual(detectCredential().configured, false);
  } finally {
    for (const k of CRED_VARS) {
      if (prev[k] === undefined) delete process.env[k];
      else process.env[k] = prev[k];
    }
  }
});

test('resolveTool never substitutes an explicit path', () => {
  assert.strictEqual(resolveTool(path.join(os.tmpdir(), 'definitely-not-here')), null);
});

test('CLI exits 2 with no credential and emits no report', () => {
  // The central fail-loud property: with no judge there is no measurement, and
  // a missing measurement must never be reported as a pass.
  const out = path.join(os.tmpdir(), `hw-lift-nocred-${process.pid}.json`);
  const r = runCli(['--json', out, '--limit', '1']);
  assert.strictEqual(r.status, 2);
  assert.match(r.stderr, /no LLM provider credential configured/);
  assert.doesNotMatch(r.stderr, /at Object|node:internal|TypeError/, 'refusal must not be a stack trace');
  assert.ok(!fs.existsSync(out), 'a report must not be written without a judge');
});

test('CLI exits 2 on an unknown argument', () => {
  const r = runCli(['--bogus']);
  assert.strictEqual(r.status, 2);
  assert.match(r.stderr, /unknown arg/);
});

test('CLI exits 2 on a non-positive --repeat', () => {
  for (const v of ['0', '-3', 'abc']) {
    const r = runCli(['--repeat', v]);
    assert.strictEqual(r.status, 2, `--repeat ${v} must be rejected`);
    assert.match(r.stderr, /--repeat must be a positive integer/);
  }
});

test('CLI exits 2 on a missing rules directory', () => {
  // A credential IS required to reach this check, because an unconfigured run
  // is refused even earlier. That ordering is deliberate: refuse the missing
  // judge before touching the filesystem, so no path can half-run.
  const r = runCli(['--rules-dir', '.cursor/definitely-not-here'], {
    SKILL_EVAL_LLM_PROVIDER: 'nv_build',
    NVIDIA_API_KEY: 'nvapi-unit-test-not-a-real-key',
  });
  assert.strictEqual(r.status, 2);
  assert.match(r.stderr, /no rules directory/);
});

test('the refusal message documents the env vars but never a value', () => {
  const r = runCli(['--limit', '1']);
  const text = `${r.stdout || ''}${r.stderr || ''}`;
  assert.match(text, /SKILL_EVAL_LLM_PROVIDER/);
  assert.match(text, /NVIDIA_API_KEY/);
  assert.match(text, /never written/, 'must state that the key is not persisted');
  assert.ok(!/nvapi-[A-Za-z0-9]/.test(text), 'no key-shaped token may appear in CLI output');
});

test('CLI exits 2 on a negative --retries', () => {
  const r = runCli(['--retries', '-1']);
  assert.strictEqual(r.status, 2);
  assert.match(r.stderr, /--retries must be a non-negative integer/);
});

test('failureReason reports status and signal, never the nonexistent proc.code', () => {
  // spawnSync returns status/signal, not code. Reading proc.code printed
  // "exit undefined" for every failure and hid the real cause.
  const reason = failureReason({ status: 3, signal: null, stdout: '', stderr: '' });
  assert.match(reason, /status 3/);
  assert.doesNotMatch(reason, /undefined/);
});

test('failureReason surfaces the SkillEvaluator warning that explains a miss', () => {
  const reason = failureReason({
    status: 1,
    stdout: 'noise\nWARNING  LLM call failed (Could not extract valid JSON from LLM response (2382 chars)) - using fallback response\nmore',
    stderr: '',
  });
  assert.match(reason, /Could not extract valid JSON/);
});

test('failureReason handles a spawn error without throwing', () => {
  const reason = failureReason({ error: new Error('ENOENT'), stdout: '', stderr: '' });
  assert.match(reason, /spawn failed: ENOENT/);
});

test('scoreWithRetries returns the first success without retrying', () => {
  let calls = 0;
  const r = scoreWithRetries(() => {
    calls += 1;
    return { score: 71 };
  }, 3);
  assert.deepStrictEqual(
    { score: r.score, attempts: r.attempts },
    { score: 71, attempts: 1 }
  );
  assert.strictEqual(calls, 1);
});

test('scoreWithRetries retries a missed attempt and reports how many it took', () => {
  // The judge intermittently answers in prose (no score line). That is
  // transient, so the miss is retried rather than recorded as UNSCORED.
  const responses = [
    { score: null, reason: 'no score line' },
    { score: null, reason: 'no score line' },
    { score: 64.2 },
  ];
  let calls = 0;
  const r = scoreWithRetries(() => responses[calls++], 5);
  assert.strictEqual(r.score, 64.2);
  assert.strictEqual(r.attempts, 3);
  assert.strictEqual(calls, 3);
});

test('scoreWithRetries is UNSCORED only after every attempt misses', () => {
  let calls = 0;
  const r = scoreWithRetries(() => {
    calls += 1;
    return { score: null, reason: 'still prose' };
  }, 2);
  assert.strictEqual(r.score, null);
  assert.strictEqual(r.attempts, 3, 'retries=2 means 3 attempts total');
  assert.strictEqual(calls, 3);
  assert.match(r.reason, /still prose/);
});

test('parseCriteria reads the numbered form, ignoring the item-10 verdict', () => {
  // Item 10 is the overall verdict and carries no `/10`, so it must not be
  // mistaken for a tenth criterion.
  const out = [
    '  LLM Rubric Score: 57.7/100',
    '  1. [RUBRIC_EVAL-LOW] [8/10] Description is clear, specific, and explains WHEN',
    '  2. [RUBRIC_EVAL-MEDIUM] [6/10] Instructions are easy to follow',
    '  3. [RUBRIC_EVAL-MEDIUM] [5/10] Examples are helpful',
    ' 10. [RUBRIC_EVAL-HIGH] Rubric evaluation failed: score 57.7/100 is below the bar',
  ].join('\n');
  const c = parseCriteria(out);
  assert.strictEqual(c['Description Clarity'], 8);
  assert.strictEqual(c['Instruction Clarity'], 6);
  assert.strictEqual(c['Example Quality'], 5);
  assert.strictEqual(Object.keys(c).length, 3, 'the verdict line must not add a criterion');
});

test('parseCriteria maps all nine criteria by their fixed order', () => {
  const lines = CRITERIA.map((_, i) => `  ${i + 1}. [RUBRIC_EVAL-LOW] [${i + 1}/10] text`);
  const c = parseCriteria(lines.join('\n'));
  assert.deepStrictEqual(Object.keys(c), CRITERIA);
  assert.strictEqual(c['Error Handling Quality'], 9);
});

test('parseCriteria falls back to the named table when no numbered list is present', () => {
  const table = [
    '| Criterion                  | Score | Pass |',
    '| Description Clarity        | 7/10  | Yes  |',
    '| Example Quality            | 0/10  | No   |',
  ].join('\n');
  const c = parseCriteria(table);
  assert.strictEqual(c['Description Clarity'], 7);
  assert.strictEqual(c['Example Quality'], 0, 'a real 0/10 must be kept, not dropped');
});

test('parseCriteria returns {} rather than throwing on bad input', () => {
  for (const bad of [undefined, null, '', {}, 42, []]) {
    assert.deepStrictEqual(parseCriteria(bad), {});
  }
});

// ---------------------------------------------------------------------------
// Cache (W2.1). The cache exists to make a re-measure cheap without making a
// stale verdict look fresh, so the tests that matter are the ones proving it
// MISSES when the bytes, the judge, or the scorer change.
// ---------------------------------------------------------------------------

/** Make a throwaway materialized-skill dir with a given SKILL.md body. */
function makeSkillDir(body) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'hw-cache-test-'));
  fs.writeFileSync(path.join(dir, 'SKILL.md'), body, 'utf8');
  return dir;
}

test('hashSkillDir is stable for identical bytes', () => {
  const a = makeSkillDir('# hello\n');
  const b = makeSkillDir('# hello\n');
  assert.strictEqual(hashSkillDir(a), hashSkillDir(b));
  fs.rmSync(a, { recursive: true, force: true });
  fs.rmSync(b, { recursive: true, force: true });
});

test('hashSkillDir changes when the judged bytes change', () => {
  const a = makeSkillDir('# hello\n');
  const b = makeSkillDir('# hello!\n');
  assert.notStrictEqual(hashSkillDir(a), hashSkillDir(b));
  fs.rmSync(a, { recursive: true, force: true });
  fs.rmSync(b, { recursive: true, force: true });
});

test('hashSkillDir does not throw on a missing SKILL.md', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'hw-cache-test-'));
  assert.doesNotThrow(() => hashSkillDir(dir));
  assert.strictEqual(typeof hashSkillDir(dir), 'string');
  fs.rmSync(dir, { recursive: true, force: true });
});

test('cacheKeyFor changes with the judge model — a different judge is a different measurement', () => {
  const dir = makeSkillDir('# skill\n');
  const a = cacheKeyFor(dir, 'nvidia/model-a', '0.4.0');
  const b = cacheKeyFor(dir, 'nvidia/model-b', '0.4.0');
  assert.notStrictEqual(a, b);
  fs.rmSync(dir, { recursive: true, force: true });
});

test('cacheKeyFor changes with the scorer version — a scorer upgrade invalidates verdicts', () => {
  const dir = makeSkillDir('# skill\n');
  const a = cacheKeyFor(dir, 'nvidia/model-a', '0.4.0');
  const b = cacheKeyFor(dir, 'nvidia/model-a', '0.5.0');
  assert.notStrictEqual(a, b);
  fs.rmSync(dir, { recursive: true, force: true });
});

test('isValidSample accepts only a finite numeric score', () => {
  assert.ok(isValidSample({ score: 71 }));
  assert.ok(isValidSample({ score: 0 }), 'a real 0 is a valid score');
  assert.ok(!isValidSample(null));
  assert.ok(!isValidSample({}));
  assert.ok(!isValidSample({ score: null }));
  assert.ok(!isValidSample({ score: '71' }));
  assert.ok(!isValidSample({ score: NaN }));
  assert.ok(!isValidSample({ score: Infinity }));
});

test('cacheRead returns [] on a miss and filters unusable samples', () => {
  const cache = { version: 1, entries: { k: { samples: [{ score: 60 }, { score: null }, { junk: 1 }] } } };
  assert.deepStrictEqual(cacheRead(cache, 'missing'), []);
  assert.deepStrictEqual(cacheRead(cache, 'k'), [{ score: 60 }]);
  assert.deepStrictEqual(cacheRead(null, 'k'), []);
});

test('cacheStore appends only fresh samples, never re-appending the cached ones', () => {
  // The bug this guards: passing the merged list would duplicate the entry with
  // itself on every run, so the cache would grow without bound and quietly
  // weight old draws more heavily.
  const cache = { version: 1, entries: {} };
  cacheStore(cache, 'k', [{ score: 60 }]);
  cacheStore(cache, 'k', []); // a run that was fully served from cache
  assert.strictEqual(cache.entries.k.samples.length, 1);
  cacheStore(cache, 'k', [{ score: 70 }]);
  assert.strictEqual(cache.entries.k.samples.length, 2);
});

test('cacheStore caps the entry so a long-lived checkout cannot grow it without limit', () => {
  const cache = { version: 1, entries: {} };
  for (let i = 0; i < CACHE_MAX_SAMPLES + 5; i += 1) cacheStore(cache, 'k', [{ score: i }]);
  assert.strictEqual(cache.entries.k.samples.length, CACHE_MAX_SAMPLES);
  // It keeps the most recent, not the oldest.
  const last = cache.entries.k.samples[CACHE_MAX_SAMPLES - 1];
  assert.strictEqual(last.score, CACHE_MAX_SAMPLES + 4);
});

test('loadCache treats a missing file as a cold cache, not an error', () => {
  const missing = path.join(os.tmpdir(), `hw-no-such-cache-${Date.now()}.json`);
  assert.deepStrictEqual(loadCache(missing, () => {}), { version: 1, entries: {} });
});

test('loadCache warns and re-judges on a corrupt cache rather than trusting it', () => {
  const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'hw-cache-test-')), 'c.json');
  fs.writeFileSync(file, '{ this is not json', 'utf8');
  const warnings = [];
  const cache = loadCache(file, (m) => warnings.push(m));
  assert.deepStrictEqual(cache.entries, {});
  assert.strictEqual(warnings.length, 1);
  assert.match(warnings[0], /corrupt/);
  fs.rmSync(path.dirname(file), { recursive: true, force: true });
});

test('loadCache warns on an unexpected shape instead of returning junk', () => {
  const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'hw-cache-test-')), 'c.json');
  fs.writeFileSync(file, JSON.stringify({ version: 1, entries: 'not-an-object' }), 'utf8');
  const warnings = [];
  const cache = loadCache(file, (m) => warnings.push(m));
  assert.deepStrictEqual(cache.entries, {});
  assert.strictEqual(warnings.length, 1);
  fs.rmSync(path.dirname(file), { recursive: true, force: true });
});

test('saveCache/loadCache round-trips samples', () => {
  const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'hw-cache-test-')), 'nested', 'c.json');
  const cache = { version: 1, entries: {} };
  cacheStore(cache, 'k', [{ score: 55.5, criteria: { 'Example Quality': 4 } }]);
  assert.ok(saveCache(file, cache, () => {}));
  const back = loadCache(file, () => {});
  const samples = cacheRead(back, 'k');
  assert.strictEqual(samples.length, 1);
  assert.strictEqual(samples[0].score, 55.5);
  assert.strictEqual(samples[0].criteria['Example Quality'], 4);
  fs.rmSync(path.dirname(path.dirname(file)), { recursive: true, force: true });
});

test('saveCache reports failure without throwing when the path is unusable', () => {
  const warnings = [];
  // A path whose parent is a FILE cannot be created as a directory.
  const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'hw-cache-test-')), 'afile', 'c.json');
  fs.writeFileSync(path.dirname(file), 'x', 'utf8');
  assert.strictEqual(saveCache(file, { version: 1, entries: {} }, (m) => warnings.push(m)), false);
  assert.strictEqual(warnings.length, 1);
  fs.rmSync(path.dirname(path.dirname(file)), { recursive: true, force: true });
});

test('CLI rejects --cache with no value (exit 2, before any provider work)', () => {
  const r = runCli(['--cache']);
  assert.strictEqual(r.status, 2);
  assert.match(r.stderr, /--cache needs a file path/);
});