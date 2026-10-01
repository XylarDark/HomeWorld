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
  parseRubricJson,
  readRubricJson,
  weightedOverall,
  retriedSplit,
  liveSplit,
  CRITERIA,
  CRITERION_IDS,
  IMPORTANCE_WEIGHTS,
  CACHE_MAX_SAMPLES,
  detectCredential,
  resolveTool,
  failureReason,
  scoreWithRetries,
  pooledWithinSd,
  hashSkillDir,
  cacheKeyFor,
  isValidSample,
  loadCache,
  cacheRead,
  cacheStore,
  saveCache,
  flushCache,
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

test('a genuine 0 is a measurement and must survive, not be read as a miss', () => {
  // The contract is "null means unmeasured". A judge really can score 0, and that
  // must be recorded: treating 0 as a miss would both discard a real failure and
  // let a transport failure pass as a grade. scoreWithRetries must therefore test
  // `!== null`, never truthiness.
  assert.deepStrictEqual(parseRubric({ stdout: '  LLM Rubric Score: 0.0/100\n' }), { score: 0 });
  const r = scoreWithRetries(() => ({ score: 0, criteria: {}, reason: null }), 2);
  assert.strictEqual(r.score, 0);
  assert.strictEqual(r.attempts, 1, 'a real 0 must not be retried as if it were a miss');
});

test('the SkillEvaluator transport fallback is UNSCORED, and its warning explains why', () => {
  // Verified against skillevaluator 0.4.0 internals: a non-JSON judge reply makes
  // the validator return _UnavailableRubricReport, which rubric_eval.py intercepts
  // and converts into a judge failure (check_name="llm_unavailable"). The CLI then
  // prints no `LLM Rubric Score:` line at all - the 0 inside the fallback dict is
  // an internal sentinel that never reaches the report. The only correct reading
  // of this output is UNSCORED, and failureReason must surface the warning that
  // says so, including the reply length that distinguishes prose from truncation.
  const out = {
    status: 0,
    stdout: [
      'WARNING LLM call failed (Could not extract valid JSON from LLM response (8123 chars)) - using fallback response',
      'LLM judge unavailable; rubric evaluation did not run',
      '',
    ].join('\n'),
    stderr: '',
  };
  assert.strictEqual(parseRubric(out), null);
  const reason = failureReason(out);
  assert.match(reason, /no score line/);
  assert.match(reason, /Could not extract valid JSON/);
  assert.match(reason, /8123 chars/);
});

test('a truncated judge reply is UNSCORED, not a partial score', () => {
  // RUBRIC_MAX_TOKENS is 4096 on 0.4.0, so a chatty judge can overrun the cap and
  // cut the JSON mid-object. A half-parsed verdict is worse than no verdict, and
  // the absent score line is what makes it correctly unreadable.
  const out = {
    status: 0,
    stdout: '{"overall_pass": false, "score": 42, "checks": [{"id": "description_clarity", "score": 6',
  };
  assert.strictEqual(parseRubric(out), null);
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

test('flushCache persists only when the rule actually judged something', () => {
  // The per-rule flush is what makes a >1h pass crash-safe: samples that live only
  // in memory are samples lost to a restart. The guard matters the other way too -
  // a fully cached pass must not rewrite the same file once per rule.
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'hw-cache-test-'));
  const file = path.join(dir, 'nested', 'c.json');
  const cache = { version: 1, entries: {} };
  cacheStore(cache, 'k', [{ score: 61 }]);

  assert.strictEqual(flushCache(file, cache, 0, () => {}), false, 'nothing judged -> no write');
  assert.strictEqual(fs.existsSync(file), false, 'and no file is created');

  assert.strictEqual(flushCache(file, cache, 2, () => {}), true);
  assert.strictEqual(cacheRead(loadCache(file, () => {}), 'k').length, 1);

  // A null cache path (--no-cache) is a no-op, never a crash.
  assert.strictEqual(flushCache(null, cache, 3, () => {}), false);
  fs.rmSync(dir, { recursive: true, force: true });
});

test('CLI rejects --cache with no value (exit 2, before any provider work)', () => {
  const r = runCli(['--cache']);
  assert.strictEqual(r.status, 2);
  assert.match(r.stderr, /--cache needs a file path/);
});

test('CLI rejects --judge-model with no value, and with a blank value', () => {
  // rubric-eval has no --model flag, so this is the only way to pin the judge.
  // Getting it silently wrong would attribute a verdict to the wrong model.
  for (const args of [['--judge-model'], ['--judge-model', '   ']]) {
    const r = runCli(args);
    assert.strictEqual(r.status, 2);
    assert.match(r.stderr, /--judge-model needs a model name/);
  }
});

// ---------------------------------------------------------------------------
// Uncertainty (W2.5). The corpus mean must not read as exact.
// ---------------------------------------------------------------------------

test('pooledWithinSd measures within-rule jitter, not the spread between rules', () => {
  // Two rules with identical internal spread and very different means. The
  // 30-point difference between them is signal; folding it in would let a
  // measure of "how much the judge wobbles" grow with the corpus's variety.
  const sd = pooledWithinSd([
    [50, 52],
    [80, 82],
  ]);
  assert.ok(Math.abs(sd - Math.SQRT2) < 1e-9, `expected ~1.414, got ${sd}`);
});

test('pooledWithinSd returns null when no rule has two samples', () => {
  // Under --repeat 1 there is no evidence about jitter, so any number would be
  // invented. Null says "unmeasured"; 0 would say "perfectly stable".
  assert.strictEqual(pooledWithinSd([]), null);
  assert.strictEqual(pooledWithinSd([[60], [70]]), null);
  assert.strictEqual(pooledWithinSd(null), null);
  assert.strictEqual(pooledWithinSd(undefined), null);
});

test('pooledWithinSd drops unusable samples instead of reading them as 0', () => {
  const sd = pooledWithinSd([[10, null, 10, NaN]]);
  assert.strictEqual(sd, 0, 'the real pair is identical, so jitter is 0');
});

test('pooledWithinSd pools by degrees of freedom across rules', () => {
  // [0,2] -> ss 2, df 1 ; [10,12,14] -> ss 8, df 2 ; pooled = 10/3
  const sd = pooledWithinSd([
    [0, 2],
    [10, 12, 14],
  ]);
  assert.ok(Math.abs(sd - Math.sqrt(10 / 3)) < 1e-9, `got ${sd}`);
});
// ---------------------------------------------------------------------------
// D1: criteria come from `-r json` checks[].id, not the CLI text table.
//
// The fixture below mirrors real skillevaluator 0.4.0 output captured on
// 2026-10-01. Note `criterion` is the FULL rubric question text, so an
// implementation that keyed on it would fail here — `id` is the only safe key.
// ---------------------------------------------------------------------------

const REAL_REPORT = {
  rubric_eval: {
    execution_status: 'succeeded',
    overall_score: 70.5,
    overall_pass: false,
    judge_score: 72,
    skill_name: 'shell-script-standards',
    aggregation: {
      method: 'importance_weighted_mean',
      importance_weights: { high: 3, medium: 2, low: 1 },
      min_score: 70,
    },
    checks: [
      {
        id: 'description_clarity',
        criterion: 'Description is clear, specific, and explains WHEN to use the skill',
        importance: 'high',
        pass: true,
        score: 8,
      },
      {
        id: 'instruction_clarity',
        criterion: 'Instructions are easy to follow with clear action steps',
        importance: 'high',
        pass: true,
        score: 8,
      },
      {
        id: 'example_quality',
        criterion:
          'Examples are helpful, relevant, show proper usage, AND cover sufficient query variations for robust skill detection',
        importance: 'high',
        pass: false,
        score: 5,
      },
      {
        id: 'documentation_completeness',
        criterion: 'All necessary information is present (purpose, scripts, parameters)',
        importance: 'medium',
        pass: true,
        score: 7,
      },
      {
        id: 'scope_definition',
        criterion:
          'Skill scope is well-defined (clear boundaries, not too broad/narrow)',
        importance: 'medium',
        pass: true,
        score: 8,
      },
      {
        id: 'professional_tone',
        criterion: 'Documentation uses professional, consistent tone and formatting',
        importance: 'low',
        pass: true,
        score: 9,
      },
      {
        id: 'trigger_simulation',
        criterion:
          'Mentally test the skill description against 5 plausible user queries that SHOULD trigger it and 3 that should NOT. Does the description enable correct routing without false positives or false negatives?',
        importance: 'high',
        pass: true,
        score: 7,
      },
      {
        id: 'workflow_completeness',
        criterion:
          'Do the instructions cover a complete end-to-end workflow? Identify any steps where the user or agent would need to figure out what to do next without guidance.',
        importance: 'high',
        pass: false,
        score: 6,
      },
      {
        id: 'error_handling_quality',
        criterion:
          'Are the documented error scenarios realistic and actionable? Would the solutions actually help resolve the issues, or are they generic boilerplate?',
        importance: 'medium',
        pass: true,
        score: 7,
      },
    ],
  },
};

test('parseRubricJson maps all nine checks by id, giving criteria a fixed denominator', () => {
  // The whole point of D1: the CLI text silently lost rows to line-wrapping, so
  // 7 of 29 cold-corpus rules carried partial criteria. checks[] is always nine.
  const r = parseRubricJson(REAL_REPORT);
  assert.ok(r, 'expected a parse');
  assert.strictEqual(Object.keys(r.criteria).length, CRITERIA.length);
  for (const name of CRITERIA) {
    assert.ok(Number.isFinite(r.criteria[name]), `missing criterion ${name}`);
  }
  assert.strictEqual(r.checkCount, 9);
  assert.strictEqual(r.criteria['Example Quality'], 5);
  assert.strictEqual(r.criteria['Workflow Completeness'], 6);
});

test('parseRubricJson keys on id, never on the full criterion question text', () => {
  const r = parseRubricJson(REAL_REPORT);
  // If the parser had keyed on `criterion`, these keys would be sentences.
  for (const name of Object.keys(r.criteria)) assert.ok(CRITERIA.includes(name));
  assert.ok(!Object.keys(r.criteria).some((k) => k.includes('?')));
});

test('parseRubricJson reads importance alongside each criterion', () => {
  const r = parseRubricJson(REAL_REPORT);
  assert.strictEqual(r.importance['Example Quality'], 'high');
  assert.strictEqual(r.importance['Professional Tone'], 'low');
  assert.strictEqual(r.importance['Scope Definition'], 'medium');
});

test('weightedOverall reproduces the scorer composite, verified on two real runs', () => {
  // Captured live from skillevaluator 0.4.0 on 2026-10-01.
  const checks = REAL_REPORT.rubric_eval.checks;
  // 10 * (24+24+15+14+16+9+21+18+14) / 22 = 10 * 155/22 = 70.45 -> 70.5
  assert.strictEqual(weightedOverall(checks), 70.5);
  assert.strictEqual(weightedOverall(checks), REAL_REPORT.rubric_eval.overall_score);
  // A second real run of the same rule: workflow_completeness 6 -> 8.
  const lifted = checks.map((c) => (c.id === 'workflow_completeness' ? { ...c, score: 8 } : c));
  // 10 * 161/22 = 73.18 -> 73.2
  assert.strictEqual(weightedOverall(lifted), 73.2);
});

test('parseRubricJson sets rollupVerified only when we reproduce the reported score', () => {
  assert.strictEqual(parseRubricJson(REAL_REPORT).rollupVerified, true);
  const tampered = {
    rubric_eval: { ...REAL_REPORT.rubric_eval, overall_score: 91 },
  };
  assert.strictEqual(
    parseRubricJson(tampered).rollupVerified,
    false,
    'a mismatch means the JSON shape changed upstream and must not pass silently'
  );
});

test('parseRubricJson returns null rather than a partial guess', () => {
  for (const bad of [
    null,
    undefined,
    42,
    [],
    '',
    '{not json',
    {},
    { rubric_eval: null },
    { rubric_eval: {} },
    { rubric_eval: { checks: [] } },
    { rubric_eval: { checks: [{ id: 'not_a_real_criterion', score: 5 }] } },
    { rubric_eval: { checks: [{ id: 'example_quality' }] } },
  ]) {
    assert.strictEqual(parseRubricJson(bad), null, `expected null for ${JSON.stringify(bad)}`);
  }
});

test('parseRubricJson never reports an unscored run as a zero', () => {
  // The fail-open trap: 0 must mean "measured, awful", never "unmeasured".
  const r = parseRubricJson({ rubric_eval: { checks: null, overall_score: null } });
  assert.strictEqual(r, null);
});

test('readRubricJson reads the one report file and tolerates its absence', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'liftjson-'));
  try {
    assert.strictEqual(readRubricJson(dir), null, 'no report yet');
    fs.writeFileSync(path.join(dir, 'skillevaluator-rubric.json'), JSON.stringify(REAL_REPORT));
    const got = parseRubricJson(readRubricJson(dir));
    assert.strictEqual(Object.keys(got.criteria).length, 9);
    assert.strictEqual(readRubricJson(path.join(dir, 'nope')), null);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test('CRITERION_IDS covers exactly CRITERIA, so a renamed upstream id fails loudly', () => {
  const mapped = Object.values(CRITERION_IDS).sort();
  assert.deepStrictEqual(mapped, [...CRITERIA].sort());
  assert.strictEqual(Object.keys(CRITERION_IDS).length, CRITERIA.length);
});

test('IMPORTANCE_WEIGHTS covers exactly the importances the scorer emits', () => {
  assert.deepStrictEqual(Object.keys(IMPORTANCE_WEIGHTS).sort(), ['high', 'low', 'medium']);
  const seen = new Set(REAL_REPORT.rubric_eval.checks.map((c) => c.importance));
  for (const imp of seen) assert.ok(imp in IMPORTANCE_WEIGHTS, `unweighted importance ${imp}`);
});

test('weightedOverall returns null when there is nothing to weight', () => {
  assert.strictEqual(weightedOverall([]), null);
  assert.strictEqual(weightedOverall(null), null);
  assert.strictEqual(weightedOverall([{ id: 'x', score: 5 }]), null, 'unknown importance is skipped');
  assert.strictEqual(weightedOverall([{ id: 'x', importance: 'high' }]), null, 'no score is skipped');
});

// ---------------------------------------------------------------------------
// D2: retries are counted over every rule, including those that ended UNSCORED.
// ---------------------------------------------------------------------------

test('retriedSplit counts retries that ended UNSCORED instead of hiding them', () => {
  // This is the exact defect: scored-only counting reported 7 for a run in which
  // 9 rules retried, because the two that never scored were filtered out.
  const results = [
    { file: 'a.mdc', score: 70, retried: true },
    { file: 'b.mdc', score: 71, retried: true },
    { file: 'c.mdc', score: null, retried: true, unscoredReason: 'no score line' },
    { file: 'd.mdc', score: null, retried: true, unscoredReason: 'no score line' },
    { file: 'e.mdc', score: 80, retried: false },
  ];
  assert.deepStrictEqual(retriedSplit(results), {
    retriedCount: 4,
    retriedScored: 2,
    retriedUnscored: 2,
  });
});

test('retriedSplit tolerates junk and empty input', () => {
  assert.deepStrictEqual(retriedSplit([]), {
    retriedCount: 0,
    retriedScored: 0,
    retriedUnscored: 0,
  });
  assert.deepStrictEqual(retriedSplit(null), {
    retriedCount: 0,
    retriedScored: 0,
    retriedUnscored: 0,
  });
  assert.strictEqual(retriedSplit([null, undefined, { retried: 'yes' }]).retriedCount, 1);
});

// ---------------------------------------------------------------------------
// P3: the live/tombstone split, pinned to the recorded cold corpus.
// ---------------------------------------------------------------------------

test('liveSplit separates live rules from tombstones', () => {
  const results = [
    { score: 80, tombstone: false },
    { score: 60, tombstone: false },
    { score: 40, tombstone: true },
    { score: null, tombstone: false },
  ];
  const s = liveSplit(results);
  assert.strictEqual(s.liveCount, 2);
  assert.strictEqual(s.tombstoneCount, 1);
  assert.strictEqual(s.meanLive, 70);
  assert.strictEqual(s.meanTombstone, 40);
});

test('liveSplit returns null means rather than zero when a side is empty', () => {
  const only = liveSplit([{ score: 55, tombstone: false }]);
  assert.strictEqual(only.meanLive, 55);
  assert.strictEqual(only.meanTombstone, null, 'no tombstones is unmeasured, not 0');
  const none = liveSplit([]);
  assert.strictEqual(none.meanLive, null);
  assert.strictEqual(none.liveCount, 0);
});

test('liveSplit reproduces the recorded cold corpus split', () => {
  // Guards the headline claim in Docs/handoffs/SKILL_LIFT_CONSOLIDATION.md
  // against drift in how tombstones are classified.
  const reportPath = path.join(projectRoot, 'Saved', 'rules_lift.json');
  if (!fs.existsSync(reportPath)) return; // artifact is gitignored; skip when absent
  const s = liveSplit(JSON.parse(fs.readFileSync(reportPath, 'utf8')).results);
  assert.strictEqual(s.liveCount, 24);
  assert.strictEqual(s.tombstoneCount, 5);
  assert.ok(Math.abs(s.meanLive - 66.25) < 0.01, `meanLive was ${s.meanLive}`);
  assert.ok(Math.abs(s.meanTombstone - 43.45) < 0.01, `meanTombstone was ${s.meanTombstone}`);
});
