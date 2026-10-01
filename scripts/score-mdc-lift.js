#!/usr/bin/env node
/**
 * Skill Lift measurement for .cursor/rules/*.mdc — LLM-as-judge rubric eval.
 *
 * Usage:
 *   node scripts/score-mdc-lift.js [options]
 *   npm run lift:score -- [--json Saved/rules_lift.json] [--repeat N] [--strict]
 *
 * Options of note:
 *   --repeat N     independent judge samples per rule (jitter is real; 1 is a
 *                  sweep, 3+ before calling any before/after delta real)
 *   --retries N    attempts per sample before it counts as UNSCORED (default 2)
 *   --cache FILE   sample cache, default Saved/lift-cache.json
 *   --no-cache     ignore and do not write the cache (clean before/after)
 *   --judge-model NAME  pin the judge (SKILL_EVAL_JUDGE_MODEL for the child)
 *
 * Choosing a judge: rubric-eval has NO --model, --temperature, or JSON-mode flag
 * (verified against its --help). The judge is selected purely by environment, so
 * --judge-model is the supported way to pin it. There is therefore no way to ask
 * the judge for strict JSON from here; the retry path is the mitigation.
 *
 * Caching: a judged score is only meaningful relative to the judge and the
 * scorer, so samples are keyed by content hash + judge model + scorer version.
 * An unchanged rule under the same judge is reused instead of re-judged, which
 * turns a 31-rule re-measure from ~60 judge calls into ~2 after an edit. The
 * cache trades cost, not jitter — every sample is still one draw — and it may
 * mix draws from different days, so use --no-cache for a defensible delta.
 *
 * Companion to score-mdc-rules.js. That one measures STRUCTURE with Tier 1
 * `quality-check` (no LLM, deterministic). This one measures a real LLM judge's
 * verdict via Tier 1 `rubric-eval`. They are different measurements and their
 * numbers are NOT comparable — do not average them or diff them.
 *
 * Why this exists: HR4-A/HR4_B could only say the corpus is healthy on FORM.
 * arXiv 2608.20614 measures Spearman rho = 0.14 between structural gates and
 * LLM-judged skill quality over 947 trials, so "it looks good" is close to
 * orthogonal to "it helps". This closes that gap with a judged number.
 *
 * The credential is read from the environment and NEVER written to a report,
 * a log line, or any file:  SKILL_EVAL_LLM_PROVIDER + NVIDIA_API_KEY
 *
 * Exit:
 *   0  every rule was judged and reported
 *   1  one or more rules came back UNSCORED (report not trustworthy)
 *   2  bad arguments, or no provider credential configured (no report emitted)
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const PREFIX = 'lift:score';
const projectRoot = path.resolve(__dirname, '..');
const REPEATS_DEFAULT = 1;
// The judge intermittently returns prose instead of JSON, giving no score. That
// is transient, so each attempt is retried; see scoreWithRetries().
const RETRIES_DEFAULT = 2;
const CACHE_DEFAULT = 'Saved/lift-cache.json';
// Bound the cache so a long-lived checkout cannot grow it without limit. More
// samples than --repeat are kept on purpose: a later run at a higher repeat
// reuses them instead of re-judging.
const CACHE_MAX_SAMPLES = 8;
const SCORE_RE = /LLM Rubric Score:\s*([0-9]+(?:\.[0-9]+)?)\s*\/\s*100/;
const MODEL_RE = /nvidia\/([A-Za-z0-9._-]+)/;
const PROVIDER_RE = /SKILL_EVAL_LLM_PROVIDER/i;

/** Resolve the SkillEvaluator executable, or null when not installed. */
function resolveTool(explicit) {
  if (explicit) return fs.existsSync(explicit) ? explicit : null;
  const names = ['skillevaluator.exe', 'skillevaluator'];
  const dirs = [];
  if (process.env.UV_TOOL_BIN_DIR) dirs.push(process.env.UV_TOOL_BIN_DIR);
  if (process.env.USERPROFILE) dirs.push(path.join(process.env.USERPROFILE, '.local', 'bin'));
  if (process.env.HOME) dirs.push(path.join(process.env.HOME, '.local', 'bin'));
  dirs.push(path.join(os.homedir(), '.local', 'bin'));
  const out = [];
  for (const dir of dirs) for (const name of names) out.push(path.join(dir, name));
  return out.concat(names).find((c) => {
    if (c.includes(path.sep)) return fs.existsSync(c);
    return !spawnSync(c, ['--version'], { encoding: 'utf8' }).error;
  }) || null;
}

/**
 * A credential exists only if the provider selector AND a key are both set.
 * Returns a redacted description. The key value itself is never returned,
 * logged, or persisted — only its length, which is enough to spot a truncated
 * paste without revealing the secret.
 */
function detectCredential() {
  const provider = process.env.SKILL_EVAL_LLM_PROVIDER || '';
  const key = process.env.NVIDIA_API_KEY || process.env.OPENAI_API_KEY || process.env.ANTHROPIC_API_KEY || '';
  const which = process.env.NVIDIA_API_KEY
    ? 'NVIDIA_API_KEY'
    : process.env.OPENAI_API_KEY
      ? 'OPENAI_API_KEY'
      : process.env.ANTHROPIC_API_KEY
        ? 'ANTHROPIC_API_KEY'
        : '(none)';
  return {
    configured: Boolean(provider && key),
    provider: provider || '(unset)',
    credentialVar: which,
    // Length only. Never the value.
    credentialLength: key ? key.length : 0,
  };
}

/**
 * Parse one rubric-eval run.
 * Returns null when the score cannot be read — NEVER 0. A zero would look like
 * a failing grade when it actually means "unmeasured", which is the fail-open
 * trap this repo treats as a hard error.
 */
function parseRubric(output) {
  // Accept a spawnSync result, a raw string, or nothing at all. A caller must
  // not be able to turn a missing value into a crash, and must never see 0.
  let text;
  if (typeof output === 'string') {
    text = output;
  } else if (output && typeof output === 'object') {
    text = `${output.stdout || ''}${output.stderr || ''}`;
  } else {
    return null;
  }
  const m = SCORE_RE.exec(text);
  if (!m) return null;
  return { score: Number(m[1]) };
}

/**
 * The judge's nine criteria, in the fixed order rubric-eval reports them.
 *
 * The CLI prints two shapes depending on outcome — a named table on pass and a
 * numbered list on fail — but the numbered list is ordered, and its order is
 * stable across runs. Mapping by index lets both shapes feed one vocabulary, so
 * criterion scores can be aggregated across the corpus instead of looked at per
 * rule.
 */
const CRITERIA = [
  'Description Clarity',
  'Instruction Clarity',
  'Example Quality',
  'Documentation Completeness',
  'Scope Definition',
  'Professional Tone',
  'Trigger Simulation',
  'Workflow Completeness',
  'Error Handling Quality',
];

// Numbered form: `3. [RUBRIC_EVAL-MEDIUM] [5/10] Examples are helpful, ...`
// Item 10 is the overall verdict and carries no `/10`, so it is not matched.
const CRITERION_LINE_RE = /^\s*(\d{1,2})\.\s*\[RUBRIC_EVAL-[A-Z_]+\]\s*\[(\d{1,2})\/10\]/gm;
// Named-table form: `| Description Clarity | 7/10 | Yes | ...`
const CRITERION_TABLE_RE = /^\|\s*([A-Z][A-Za-z ]+?)\s*\|\s*(\d{1,2})\/10\s*\|/gm;

/**
 * Extract per-criterion scores (each /10) from one run.
 * Returns {} when nothing parseable is present — never partial guesses, and
 * never throws. Criterion data is a bonus over the composite score, so a miss
 * here must not be able to fail a run that otherwise scored.
 */
function parseCriteria(output) {
  let text;
  if (typeof output === 'string') {
    text = output;
  } else if (output && typeof output === 'object') {
    text = `${output.stdout || ''}${output.stderr || ''}`;
  } else {
    return {};
  }
  const out = {};
  let m;
  CRITERION_LINE_RE.lastIndex = 0;
  while ((m = CRITERION_LINE_RE.exec(text)) !== null) {
    const idx = Number(m[1]);
    const score = Number(m[2]);
    if (idx >= 1 && idx <= CRITERIA.length && Number.isFinite(score)) {
      out[CRITERIA[idx - 1]] = score;
    }
  }
  // Fall back to the named table only if the numbered form yielded nothing.
  if (Object.keys(out).length === 0) {
    CRITERION_TABLE_RE.lastIndex = 0;
    while ((m = CRITERION_TABLE_RE.exec(text)) !== null) {
      const name = m[1].trim();
      const score = Number(m[2]);
      if (CRITERIA.includes(name) && Number.isFinite(score)) out[name] = score;
    }
  }
  return out;
}

/**
 * rubric-eval `-r json` output: the RELIABLE criteria source.
 *
 * The CLI text is now a fallback rather than the primary. It prints a box-drawn
 * table whose Criterion column WRAPS across lines when the terminal is narrow,
 * and the numbered "Failure Details" list is matched by row index — so a wrapped
 * row silently loses its criterion. Measured consequence in the cold corpus:
 * 7 of 29 rules carried partial criteria, 5 of them missing 7 of 9, even though
 * the scorer had emitted all nine. `checks[]` is always exactly nine and is
 * keyed by a stable `id`, so it has neither failure mode.
 *
 * Shape verified against skillevaluator 0.4.0 on 2026-10-01:
 *   rubric_eval.checks[].id           description_clarity | instruction_clarity | ...
 *   rubric_eval.checks[].criterion    the FULL rubric question text, not a short
 *                                    name — so `id` is the only safe key
 *   rubric_eval.checks[].score        0-10
 *   rubric_eval.checks[].importance   high | medium | low
 *   rubric_eval.overall_score         0-100, importance-weighted (weightedOverall)
 *   rubric_eval.judge_score           0-100, the judge's own unweighted figure
 */
const CRITERION_IDS = {
  description_clarity: 'Description Clarity',
  instruction_clarity: 'Instruction Clarity',
  example_quality: 'Example Quality',
  documentation_completeness: 'Documentation Completeness',
  scope_definition: 'Scope Definition',
  professional_tone: 'Professional Tone',
  trigger_simulation: 'Trigger Simulation',
  workflow_completeness: 'Workflow Completeness',
  error_handling_quality: 'Error Handling Quality',
};

/** `rubric_eval.aggregation` names the method importance_weighted_mean. */
const IMPORTANCE_WEIGHTS = { high: 3, medium: 2, low: 1 };

/**
 * Reproduce the scorer's own composite: 10 * sum(w*s) / sum(w).
 *
 * Verified twice against real scorer output — 75.0 and 70.5, each matching
 * `overall_score` exactly — so it is used as a CHECK on the parse rather than a
 * formula we trust blindly. If this disagrees with the reported score, the JSON
 * shape changed upstream and the run is flagged rather than silently accepted.
 */
function weightedOverall(checks) {
  let num = 0;
  let den = 0;
  for (const c of checks || []) {
    const w = IMPORTANCE_WEIGHTS[c && c.importance];
    if (!Number.isFinite(w) || !Number.isFinite(c.score)) continue;
    num += w * c.score;
    den += w;
  }
  return den === 0 ? null : Number(((10 * num) / den).toFixed(1));
}

/** Read the one report file rubric-eval writes. Null if absent/unreadable. */
function readRubricJson(dir) {
  try {
    const file = path.join(dir, 'skillevaluator-rubric.json');
    return fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : null;
  } catch {
    return null;
  }
}

/**
 * Parse a `-r json` report. Returns null when unusable so the caller falls back
 * to the CLI text — never a partial guess, and never throws.
 */
function parseRubricJson(json) {
  let doc = json;
  if (typeof json === 'string') {
    try {
      doc = JSON.parse(json);
    } catch {
      return null;
    }
  }
  if (!doc || typeof doc !== 'object') return null;
  const re = doc.rubric_eval;
  if (!re || typeof re !== 'object') return null;
  const checks = Array.isArray(re.checks) ? re.checks : null;
  if (!checks || checks.length === 0) return null;

  const criteria = {};
  const importance = {};
  for (const c of checks) {
    const name = CRITERION_IDS[c && c.id];
    if (!name || !Number.isFinite(c.score)) continue;
    criteria[name] = c.score;
    importance[name] = c.importance || null;
  }
  if (Object.keys(criteria).length === 0) return null;

  const overall = Number.isFinite(re.overall_score) ? re.overall_score : null;
  const derived = weightedOverall(checks);
  return {
    criteria,
    importance,
    overallScore: overall,
    judgeScore: Number.isFinite(re.judge_score) ? re.judge_score : null,
    derivedOverall: derived,
    // True = we reproduced the scorer's own composite from the checks we read.
    rollupVerified: overall !== null && derived !== null && Math.abs(derived - overall) <= 0.1,
    checkCount: checks.length,
  };
}

/**
 * Split retries by outcome (D2).
 *
 * Counting only the rules that ended up scored hid the retries that ended
 * UNSCORED — the most informative ones, since those are the judge failing
 * repeatedly. The cold report claimed 7 against the 9 rules that actually
 * retried for exactly this reason. Every number a reader needs to judge the
 * judge comes from here, so none of it can be quietly filtered away.
 */
function retriedSplit(results) {
  const all = (results || []).filter((r) => r && r.retried);
  const scored = all.filter((r) => r.score !== null);
  return {
    retriedCount: all.length,
    retriedScored: scored.length,
    retriedUnscored: all.length - scored.length,
  };
}

/**
 * Live vs tombstone split (P3).
 *
 * A rule that declares itself QUARANTINE / RETIRED / HISTORICAL is not meant to
 * be live guidance, so `meanLive` describes what a reader is actually served.
 * This is a POLICY split and NOT a quality ranking: in the cold corpus the
 * highest-scoring tombstone (ue57-editor-ui, 76.35) outranked 23 of the 24 live
 * rules, so a judge score cannot decide what to keep or retire.
 */
function liveSplit(results) {
  const scored = (results || []).filter((r) => r && r.score !== null);
  const live = scored.filter((r) => !r.tombstone);
  const tomb = scored.filter((r) => r.tombstone);
  const avg = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);
  return {
    meanLive: avg(live.map((r) => r.score)),
    liveCount: live.length,
    meanTombstone: avg(tomb.map((r) => r.score)),
    tombstoneCount: tomb.length,
  };
}

/**
 * Build a short, diagnostic reason from a run that produced no score.
 *
 * `spawnSync` returns `status`/`signal`, NOT `code` (that field is for the async
 * API). Reading `proc.code` printed "exit undefined" for every failure and threw
 * away the one piece of data needed to tell a crash from a bad response.
 */
function failureReason(proc) {
  const text = `${proc.stdout || ''}${proc.stderr || ''}`;
  const warn = text
    .split(/\r?\n/)
    .map((l) => l.trim())
    .find((l) => /WARNING|LLM call failed|Error/i.test(l));
  const bits = [];
  if (proc.error) {
    bits.push(`spawn failed: ${proc.error.message}`);
  } else {
    bits.push(`no score line (status ${proc.status}${proc.signal ? `, signal ${proc.signal}` : ''})`);
  }
  if (warn) bits.push(warn.slice(0, 140));
  return bits.join(' - ');
}

/**
 * Run rubric-eval once. Returns {score, criteria} or {score:null, reason}.
 *
 * `env` is threaded through so a caller can pin the judge model for the child
 * process (SKILL_EVAL_JUDGE_MODEL). rubric-eval has no --model flag, so the
 * environment is the only way to choose a judge — see the header note.
 */
function runRubricOnce(tool, skillDir, env) {
  // `-r cli,json` is honored exactly by the scorer, so the proven CLI text is
  // unchanged for reading the score, and the JSON adds a criteria source that
  // cannot lose a row to line-wrapping. `-o` is required: without it the scorer
  // writes html+json into ./reports on every call.
  const reportsDir = fs.mkdtempSync(path.join(os.tmpdir(), 'skilleval-'));
  try {
    const proc = spawnSync(tool, ['rubric-eval', skillDir, '-r', 'cli,json', '-o', reportsDir], {
      encoding: 'utf8',
      maxBuffer: 32 * 1024 * 1024,
      env: env || process.env,
    });
    const json = parseRubricJson(readRubricJson(reportsDir));
    const parsed = parseRubric(proc);

    if (parsed) {
      // The CLI score stays primary: it is what the recorded corpus measured, so
      // taking it keeps every score comparable with Saved/rules_lift.json.
      const useJson = json !== null;
      return {
        ...parsed,
        criteria: useJson ? json.criteria : parseCriteria(proc),
        criteriaSource: useJson ? 'json' : 'cli',
        importance: useJson ? json.importance : null,
        judgeScore: json ? json.judgeScore : null,
        derivedOverall: json ? json.derivedOverall : null,
        rollupVerified: json ? json.rollupVerified : null,
      };
    }
    // No CLI score line, but the JSON still carries one. A run must not be lost
    // just because the human-facing summary was missing.
    if (json && json.overallScore !== null) {
      return {
        score: json.overallScore,
        criteria: json.criteria,
        criteriaSource: 'json',
        importance: json.importance,
        judgeScore: json.judgeScore,
        derivedOverall: json.derivedOverall,
        rollupVerified: json.rollupVerified,
      };
    }
    return { score: null, reason: failureReason(proc) };
  } finally {
    // Never leave a ~21 KB report per judge call behind.
    fs.rmSync(reportsDir, { recursive: true, force: true });
  }
}

/**
 * Retry wrapper for a single judge attempt.
 *
 * The judge intermittently answers in prose instead of JSON; SkillEvaluator then
 * logs `Could not extract valid JSON ... using fallback response` and emits no
 * numeric score. Observed on 6 of 31 rules in one clean full-corpus pass, and the
 * same rules score normally on a later attempt — so this is transient, and a
 * single miss must be retried rather than recorded as UNSCORED.
 *
 * A rule is UNSCORED only after every attempt misses; the reported `attempts`
 * makes a flaky rule visible instead of silently average-looking.
 */
function scoreWithRetries(attempt, retries) {
  let last = { score: null, reason: 'no attempt made' };
  for (let i = 0; i <= retries; i += 1) {
    const r = attempt(i);
    if (r.score !== null) return { ...r, attempts: i + 1 };
    last = r;
  }
  return { score: null, reason: last.reason, attempts: retries + 1 };
}

/**
 * Content hash of the artifact that is actually judged.
 *
 * Hash the MATERIALIZED SKILL.md, not the source .mdc: the materializer is what
 * turns a rule into the prompt, so if its output changes (e.g. a frontmatter
 * field starts being passed through), the hash changes and the cached verdict is
 * correctly discarded. Hashing the source would silently reuse a verdict taken
 * against different bytes.
 */
function hashSkillDir(dir) {
  const skill = path.join(dir, 'SKILL.md');
  const buf = fs.existsSync(skill) ? fs.readFileSync(skill) : Buffer.from('');
  return crypto.createHash('sha256').update(buf).digest('hex').slice(0, 16);
}

/**
 * Cache key. A judged score is only meaningful relative to the judge and the
 * scorer that produced it, so both are part of the identity — a key of just the
 * content would let a model swap or a scorer upgrade silently reuse stale
 * numbers. This is the cache equivalent of `scorerVersion` in the report.
 */
function cacheKeyFor(dir, judgeModel, scorerVersion) {
  return `${hashSkillDir(dir)}|${judgeModel}|${scorerVersion}`;
}

/** A cached sample is usable only if it carries a finite numeric score. */
function isValidSample(s) {
  return Boolean(s) && typeof s === 'object' && Number.isFinite(s.score);
}

/**
 * Load the cache. Never throws and never fabricates.
 *
 * A missing file is a cold cache (normal). A corrupt file is treated as cold
 * with a warning — the run proceeds and simply re-judges. The one thing that
 * must NOT happen is a parse failure being read as "these rules scored well".
 */
function loadCache(file, warn) {
  const empty = { version: 1, entries: {} };
  if (!file || !fs.existsSync(file)) return empty;
  let text;
  try {
    text = fs.readFileSync(file, 'utf8');
  } catch (err) {
    if (warn) warn(`${PREFIX} - cache unreadable (${err.message}); re-judging everything`);
    return empty;
  }
  try {
    const parsed = JSON.parse(text);
    if (!parsed || typeof parsed !== 'object' || typeof parsed.entries !== 'object' || !parsed.entries) {
      throw new Error('unexpected shape');
    }
    parsed.version = parsed.version || 1;
    return parsed;
  } catch (err) {
    if (warn) warn(`${PREFIX} - cache corrupt (${err.message}); re-judging everything`);
    return empty;
  }
}

/** Read usable samples for a key. Returns [] on any miss or malformed entry. */
function cacheRead(cache, key) {
  if (!cache || !cache.entries) return [];
  const entry = cache.entries[key];
  if (!entry || !Array.isArray(entry.samples)) return [];
  return entry.samples.filter(isValidSample);
}

/**
 * Append freshly judged samples to a key.
 *
 * `fresh` must contain ONLY samples judged in this run — passing the merged list
 * would re-append samples that came from the cache and inflate the entry with
 * duplicates of itself on every run.
 */
function cacheStore(cache, key, fresh) {
  if (!cache || !cache.entries || fresh.length === 0) return;
  const prev = Array.isArray(cache.entries[key] && cache.entries[key].samples)
    ? cache.entries[key].samples.filter(isValidSample)
    : [];
  cache.entries[key] = { samples: prev.concat(fresh).slice(-CACHE_MAX_SAMPLES) };
}

/** Persist the cache. A write failure is a warning, never a run failure. */
function saveCache(file, cache, warn) {
  try {
    fs.mkdirSync(path.dirname(path.resolve(file)), { recursive: true });
    fs.writeFileSync(path.resolve(file), `${JSON.stringify(cache, null, 2)}\n`, 'utf8');
    return true;
  } catch (err) {
    if (warn) warn(`${PREFIX} - could not write cache (${err.message}); results are still valid`);
    return false;
  }
}

/**
 * Persist the cache after a rule, but only when that rule actually judged
 * something.
 *
 * A full pass runs for well over an hour and has already been killed mid-run by
 * a restart, so samples held only in memory are samples lost. Flushing per rule
 * makes the cache a running ledger: whatever completed before a crash is still
 * reusable, and the next run resumes from there instead of starting over. The
 * fresh-count guard keeps a fully cached pass from rewriting the same file once
 * per rule for no reason.
 */
function flushCache(file, cache, freshCount, warn) {
  if (!file || !freshCount) return false;
  return saveCache(file, cache, warn);
}

/**
 * Pooled within-rule standard deviation, across every rule that has 2+ samples.
 *
 * This is the honest resolution of the judge: how much a single rule's own score
 * moves between identical runs. It deliberately does NOT include between-rule
 * variance — that is signal, not noise, and folding it in would inflate the
 * figure while pretending it measured the judge.
 *
 * Returns null when no rule has two samples (e.g. a --repeat 1 sweep), because
 * in that case there is no evidence about jitter and a number would be invented.
 */
function pooledWithinSd(sampleGroups) {
  let sumSquares = 0;
  let degreesOfFreedom = 0;
  for (const group of sampleGroups || []) {
    const xs = (group || []).filter((x) => Number.isFinite(x));
    if (xs.length < 2) continue;
    const m = xs.reduce((a, b) => a + b, 0) / xs.length;
    sumSquares += xs.reduce((a, b) => a + (b - m) ** 2, 0);
    degreesOfFreedom += xs.length - 1;
  }
  if (degreesOfFreedom === 0) return null;
  return Math.sqrt(sumSquares / degreesOfFreedom);
}

function parseArgs(argv) {
  const opts = {
    json: null,
    strict: false,
    repeat: REPEATS_DEFAULT,
    retries: RETRIES_DEFAULT,
    cache: CACHE_DEFAULT,
    noCache: false,
    judgeModel: null,
    rulesDir: '.cursor/rules',
    tool: null,
    limit: null,
    only: null,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '--json') opts.json = argv[++i];
    else if (a === '--repeat') opts.repeat = Number(argv[++i]);
    else if (a === '--retries') opts.retries = Number(argv[++i]);
    else if (a === '--cache') opts.cache = argv[++i];
    else if (a === '--no-cache') opts.noCache = true;
    else if (a === '--judge-model') opts.judgeModel = argv[++i];
    else if (a === '--rules-dir') opts.rulesDir = argv[++i];
    else if (a === '--tool') opts.tool = argv[++i];
    else if (a === '--only') opts.only = argv[++i];
    else if (a === '--limit') opts.limit = Number(argv[++i]);
    else if (a === '--strict') opts.strict = true;
    else {
      console.error(`${PREFIX} - unknown arg: ${a}`);
      return null;
    }
  }
  if (!Number.isInteger(opts.repeat) || opts.repeat < 1) {
    console.error(`${PREFIX} - --repeat must be a positive integer`);
    return null;
  }
  if (!Number.isInteger(opts.retries) || opts.retries < 0) {
    console.error(`${PREFIX} - --retries must be a non-negative integer`);
    return null;
  }
  if (opts.cache !== null && typeof opts.cache !== 'string') {
    console.error(`${PREFIX} - --cache needs a file path`);
    return null;
  }
  if (opts.judgeModel !== null && (typeof opts.judgeModel !== 'string' || !opts.judgeModel.trim())) {
    console.error(`${PREFIX} - --judge-model needs a model name`);
    return null;
  }
  return opts;
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (!opts) process.exit(2);

  const cred = detectCredential();
  if (!cred.configured) {
    console.error(`${PREFIX} - no LLM provider credential configured (exit 2).`);
    console.error(`${PREFIX}   Tier 1 quality-check is keyless; rubric-eval is NOT.`);
    console.error(`${PREFIX}   Set a provider and key in this shell, for example:`);
    console.error(`${PREFIX}     $env:SKILL_EVAL_LLM_PROVIDER="nv_build"`);
    console.error(`${PREFIX}     $env:NVIDIA_API_KEY="<your key>"`);
    console.error(`${PREFIX}   The key is read from the environment only. It is never written`);
    console.error(`${PREFIX}   to this report or to any log line.`);
    console.error(`${PREFIX} - Refusing to emit a report without a judge (exit 2).`);
    process.exit(2);
  }

  const tool = resolveTool(opts.tool);
  if (!tool) {
    console.error(
      opts.tool
        ? `${PREFIX} - SkillEvaluator not found at "${opts.tool}". Not falling back to PATH (exit 2).`
        : `${PREFIX} - SkillEvaluator not found. Install with: uv tool install --python 3.13 "skillevaluator[all] @ git+https://github.com/NVIDIA/SkillEvaluator.git" (exit 2).`
    );
    process.exit(2);
  }

  const rulesAbs = path.resolve(projectRoot, opts.rulesDir);
  if (!fs.existsSync(rulesAbs)) {
    console.error(`${PREFIX} - no rules directory: ${rulesAbs}`);
    process.exit(2);
  }

  // Reuse the sibling scorer's proven materializer so both tools measure the
  // exact same bytes. A second materializer would be a second thing to drift.
  const sibling = require('./score-mdc-rules.js');
  let files = fs.readdirSync(rulesAbs).filter((f) => f.toLowerCase().endsWith('.mdc')).sort();
  if (opts.only) files = files.filter((f) => f.toLowerCase() === opts.only.toLowerCase());
  if (opts.limit) files = files.slice(0, opts.limit);

  // rubric-eval exposes no --model flag, so the judge is chosen by environment.
  // Pin it when asked: a run must record the judge that actually answered, and a
  // judge change is a measurement change, exactly like a scorer upgrade.
  const childEnv = opts.judgeModel
    ? {
        ...process.env,
        SKILL_EVAL_JUDGE_MODEL: opts.judgeModel,
        SKILL_EVAL_LLM_MODEL: opts.judgeModel,
      }
    : process.env;

  // Identify the judge so the number is anchored to a model, not just a tool.
  const probe = spawnSync(tool, ['health-check'], {
    encoding: 'utf8',
    maxBuffer: 8 * 1024 * 1024,
    env: childEnv,
  });
  const health = `${probe.stdout || ''}${probe.stderr || ''}`;
  const model = MODEL_RE.exec(health);
  const judgeModel = opts.judgeModel || (model ? `nvidia/${model[1]}` : 'unknown');
  const judgeModelSource = opts.judgeModel ? 'flag' : model ? 'health-check' : 'unknown';
  const toolVersion = sibling.toolVersion(tool);

  const cacheFile = opts.noCache ? null : path.resolve(projectRoot, opts.cache);
  const cache = opts.noCache
    ? { version: 1, entries: {} }
    : loadCache(cacheFile, (m) => console.error(m));
  const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'hw-lift-'));
  const results = [];
  let cacheHits = 0;
  let fromCacheSamples = 0;
  // Declared before the loop because the cache is flushed per rule, not at the
  // end; `cacheWarned` keeps a persistently unwritable path from spamming a
  // warning line per rule.
  let cacheWritten = false;
  let cacheWarned = false;
  const warnOnce = (m) => {
    if (cacheWarned) return;
    cacheWarned = true;
    console.error(m);
  };
  try {
    for (const file of files) {
      const rule = sibling.readRule(path.join(rulesAbs, file), rulesAbs);
      const dir = sibling.materializeSkill(rule, tmpRoot);
      const key = cacheKeyFor(dir, judgeModel, toolVersion);

      // Cached samples first. An unchanged rule under the same judge and scorer
      // has already been measured; re-judging it spends a call to learn nothing.
      // This is what makes a re-measure cheap after a corpus edit.
      const cachedSamples = cacheRead(cache, key);
      const samples = cachedSamples
        .slice(0, opts.repeat)
        .map((s) => ({ score: s.score, criteria: s.criteria || {} }));
      const samplesFromCache = samples.length;

      let attempts = 0;
      let freshRuns = 0;
      let reason = 'not judged';
      const freshSamples = [];
      for (let i = samples.length; i < opts.repeat; i += 1) {
        freshRuns += 1;
        const r = scoreWithRetries(() => runRubricOnce(tool, dir, childEnv), opts.retries);
        attempts += r.attempts || 1;
        if (r.score === null) {
          reason = r.reason;
        } else {
          const s = {
            score: r.score,
            criteria: r.criteria || {},
            criteriaSource: r.criteriaSource || 'cli',
            importance: r.importance || null,
            rollupVerified: r.rollupVerified === true,
          };
          samples.push(s);
          freshSamples.push(s);
        }
      }

      const scores = samples.map((s) => s.score);
      const mean = scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length : null;
      // Criterion scores are averaged over whichever samples reported them. With
      // the JSON source every sample reports all nine, so the denominator is now
      // the sample count; the CLI fallback can still deliver a short row.
      const critAcc = {};
      for (const s of samples) {
        for (const [k, v] of Object.entries(s.criteria || {})) (critAcc[k] ||= []).push(v);
      }
      const criteria = {};
      for (const [k, arr] of Object.entries(critAcc)) {
        criteria[k] = Number((arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(2));
      }
      // How many samples carried a full nine, and where the criteria came from.
      const fullSamples = samples.filter((s) => Object.keys(s.criteria || {}).length === CRITERIA.length)
        .length;
      const importance = {};
      for (const s of samples) {
        for (const [k, v] of Object.entries(s.importance || {})) if (v) importance[k] = v;
      }
      const cls = sibling.classifyTombstone(rule);
      results.push({
        file: rule.file,
        relPath: rule.relPath,
        slug: rule.slug,
        bytes: rule.bytes,
        tombstone: cls.tombstone,
        tombstoneMarker: cls.marker,
        score: mean === null ? null : Number(mean.toFixed(2)),
        spread:
          scores.length > 1 ? Number((Math.max(...scores) - Math.min(...scores)).toFixed(2)) : null,
        runs: scores,
        criteria,
        // D1 instrumentation: `fullCriteriaSamples`/`samples` is the criteria
        // denominator made visible, so a short row can never hide again.
        criteriaSource: samples.length ? samples[samples.length - 1].criteriaSource : null,
        fullCriteriaSamples: fullSamples,
        criteriaSamples: samples.length,
        importance: Object.keys(importance).length ? importance : null,
        // D2/P4: we reproduced the scorer's importance-weighted composite from
        // the checks we read. False would mean the JSON shape changed upstream.
        rollupVerified: samples.length ? samples.every((s) => s.rollupVerified) : null,
        samplesFromCache,
        cached: samplesFromCache > 0,
        // Attempts spent in THIS run only; a cached sample carries none.
        attempts,
        // A fresh sample needing more than one attempt is flakiness now. A fully
        // cached rule is not flaky now, whatever it cost the run that measured it.
        retried: freshRuns > 0 && attempts > freshRuns,
        unscoredReason: scores.length ? null : reason,
      });
      if (samplesFromCache > 0) {
        cacheHits += 1;
        fromCacheSamples += samplesFromCache;
      }
      cacheStore(cache, key, freshSamples);
      // Flush per rule, not at the end: a pass that dies mid-run must not take its
      // already-judged samples with it.
      if (flushCache(cacheFile, cache, freshSamples.length, warnOnce)) cacheWritten = true;

      const shown =
        mean === null
          ? `UNSCORED (${reason})`
          : `${mean.toFixed(1)}${opts.repeat > 1 ? ` (spread ${(Math.max(...scores) - Math.min(...scores)).toFixed(1)})` : ''}${samplesFromCache ? ` [${samplesFromCache} cached]` : ''}${attempts > freshRuns ? ` [${attempts} attempts]` : ''}`;
      process.stderr.write(`${PREFIX} - ${file} ${shown}\n`);
    }
  } finally {
    fs.rmSync(tmpRoot, { recursive: true, force: true });
  }
  // The cache was already flushed after each rule that judged anything, so a crash
  // here loses nothing. `cacheWritten` is whatever those flushes reported.
  if (!opts.noCache && !cacheWritten) {
    // Nothing was judged from scratch (a fully cached pass) - still persist, so a
    // first cold run that found an existing file keeps it on disk.
    cacheWritten = saveCache(cacheFile, cache, warnOnce);
  }

  const scored = results.filter((r) => r.score !== null);
  const unscored = results.filter((r) => r.score === null);
  const scores = scored.map((r) => r.score);
  const mean = scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length : null;
  const spreads = scored.map((r) => r.spread).filter((x) => x !== null);
  // Live vs tombstone split. A rule that declares itself QUARANTINE / RETIRED /
  // HISTORICAL is not meant to be live guidance, so `meanLive` is the figure that
  // describes what a reader is actually served. This is a POLICY split, not a
  // quality ranking: the highest-scoring tombstone (ue57-editor-ui, 76.35)
  // outranks 23 of the 24 live rules, so judge score does not track rule status.
  const { meanLive, liveCount, meanTombstone, tombstoneCount } = liveSplit(results);
  // Judge noise only. The SE of the corpus mean says how precisely THAT mean is
  // pinned down against judge jitter; it says nothing about which rules are in
  // the corpus, which is the larger source of variation in practice.
  const withinRuleSd = pooledWithinSd(scored.map((r) => r.runs));
  const seOfMean =
    withinRuleSd === null || scored.length === 0 ? null : withinRuleSd / Math.sqrt(scored.length);
  const pad = (s, n) => String(s).padEnd(n);

  // Aggregate each criterion across the corpus. This is what turns "the judge
  // finds the corpus mediocre" into a specific, editable target list.
  const critAcc = {};
  for (const r of results) {
    for (const [k, v] of Object.entries(r.criteria || {})) (critAcc[k] ||= []).push(v);
  }
  const criteriaSummary = Object.fromEntries(
    Object.entries(critAcc)
      .map(([k, arr]) => [
        k,
        { mean: Number((arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(2)), n: arr.length },
      ])
      .sort((a, b) => a[1].mean - b[1].mean)
  );

  console.log('');
  console.log(`${PREFIX} - LLM-as-judge rubric eval on .cursor/rules/*.mdc`);
  console.log(`  judge      : ${cred.provider} / ${judgeModel}  (scorer v${toolVersion})`);
  console.log(`  credential : ${cred.credentialVar}, ${cred.credentialLength} chars (value never recorded)`);
  console.log(`  rules      : ${results.length} (${scored.length} judged, ${unscored.length} UNSCORED)`);
  if (opts.noCache) {
    console.log('  cache      : disabled (--no-cache)');
  } else {
    console.log(
      `  cache      : ${cacheHits}/${results.length} rule(s) served from ${path.relative(projectRoot, cacheFile).split(path.sep).join('/')} (${fromCacheSamples} sample(s) reused)`
    );
  }
  // D2: count EVERY rule that needed a retry, not only the ones that ended up
  // scored. A rule can retry and still land UNSCORED, and those are the most
  // informative retries — the old `scored.filter(...)` hid exactly them, which is
  // why the cold report claimed 7 against the 9 rules that actually retried.
  const { retriedCount, retriedScored, retriedUnscored } = retriedSplit(results);
  if (retriedCount > 0 || unscored.length > 0) {
    console.log(
      `  judge flakiness : ${retriedCount} rule(s) needed a retry (${retriedScored} scored, ${retriedUnscored} ended UNSCORED); the judge sometimes returns prose instead of JSON (--retries ${opts.retries})`
    );
  }
  if (scores.length) {
    const seText = seOfMean === null ? '' : ` +/- ${seOfMean.toFixed(1)} SE (judge noise only)`;
    console.log(`  mean       : ${mean.toFixed(1)}${seText}  (range ${Math.min(...scores).toFixed(1)}-${Math.max(...scores).toFixed(1)})`);
    if (spreads.length) {
      console.log(`  jitter     : mean spread ${(spreads.reduce((a, b) => a + b, 0) / spreads.length).toFixed(1)} pts over ${opts.repeat} run(s) — a single run is not a measurement`);
    }
    if (meanLive !== null) {
      console.log(`  live split : meanLive ${meanLive.toFixed(1)} over ${liveCount} live rule(s); tombstones ${meanTombstone.toFixed(1)} over ${tombstoneCount} (a policy split, not a quality ranking)`);
    }
  }
  console.log(`  threshold  : 70 (rubric-eval's own gate)`);
  const critEntries = Object.entries(criteriaSummary);
  if (critEntries.length) {
    console.log('  criteria   : mean /10 across the corpus, weakest first');
    for (const [k, v] of critEntries) {
      console.log(`               ${pad(k, 26)} ${v.mean.toFixed(1)}  (n=${v.n})`);
    }
  }
  console.log('');
  for (const r of [...results].sort((a, b) => (a.score ?? -1) - (b.score ?? -1))) {
    const s = r.score === null ? 'UNSCORED' : r.score.toFixed(1);
    const tomb = r.tombstone ? `  [${r.tombstoneMarker}]` : '';
    console.log(`  ${pad(r.file, 40)} ${pad(s, 10)}${tomb}`);
  }

  const report = {
    tool: PREFIX,
    version: 1,
    generatedAt: new Date().toISOString(),
    scorer: tool,
    scorerVersion: toolVersion,
    judge: {
      provider: cred.provider,
      model: judgeModel,
      modelPinned: judgeModel !== 'unknown',
      modelSource: judgeModelSource,
      // Jitter is a property of LLM judging, not of any rule. Recorded so a
      // reader never mistakes a one-run delta for a real regression.
      repeats: opts.repeat,
      meanSpread: spreads.length
        ? Number((spreads.reduce((a, b) => a + b, 0) / spreads.length).toFixed(2))
        : null,
      maxSpread: spreads.length ? Number(Math.max(...spreads).toFixed(2)) : null,
      // Pooled within-rule SD and the SE it implies for the corpus mean. Reported
      // so a reader can see the precision of the mean against judge noise instead
      // of reading 60.9 as exact. Null under --repeat 1: with one sample per rule
      // there is no evidence about jitter, and a number would be invented.
      withinRuleSd: withinRuleSd === null ? null : Number(withinRuleSd.toFixed(2)),
      standardErrorOfMean: seOfMean === null ? null : Number(seOfMean.toFixed(2)),
      // The judge sometimes answers in prose and emits no score; that attempt is
      // retried. retriedCount > 0 means the provider is flaky right now, which
      // a reader needs to know before trusting an UNSCORED or a tight delta.
      // D2: counted over ALL results, so retries that ended UNSCORED are included.
      retries: opts.retries,
      retriedCount,
      retriedScored,
      retriedUnscored,
      attemptsTotal: results.reduce((a, r) => a + (r.attempts || 1), 0),
    },
    comparability: {
      againstQualityCheck: false,
      note: 'rubric-eval (LLM judge) and quality-check (structural) are different measurements. Their numbers must not be averaged or diffed. arXiv 2608.20614 measures rho = 0.14 between structural gates and LLM-judged quality.',
    },
    criterionProvenance: {
      source: 'rubric-eval -r json checks[].id',
      rollup: '10 * sum(importance_weight * score) / sum(importance_weight), high=3 medium=2 low=1',
      rollupVerifiedCount: results.filter((r) => r.rollupVerified === true).length,
      fullCriteriaRules: results.filter((r) => r.fullCriteriaSamples > 0).length,
      note: 'The CLI text table wraps on narrow terminals and its numbered form is matched by row index, which silently dropped criteria: 7 of 29 rules in the cold corpus carried partial criteria. checks[] is always nine and is keyed by a stable id, so `criteria` now has a fixed denominator (criteriaSamples).',
    },
    credential: {
      provider: cred.provider,
      credentialVar: cred.credentialVar,
      recorded: false,
      note: 'credential value is never persisted; only the variable name and length',
    },
    cache: {
      enabled: !opts.noCache,
      path: cacheFile ? path.relative(projectRoot, cacheFile).split(path.sep).join('/') : null,
      written: cacheWritten,
      rulesServed: cacheHits,
      samplesReused: fromCacheSamples,
      maxSamplesPerKey: CACHE_MAX_SAMPLES,
      note: 'cached samples are prior draws from the same judge+scorer. Reuse cuts cost, not jitter, and mixes samples across days — use --no-cache for a clean before/after measurement.',
    },
    ruleCount: results.length,
    judgedCount: scored.length,
    unscoredCount: unscored.length,
    mean: mean === null ? null : Number(mean.toFixed(2)),
    // A tombstone is not meant to be live guidance, so `meanLive` is the figure
    // that describes the corpus a reader is actually served. `mean` stays all-29
    // so it remains comparable with the saved report. Neither is a quality
    // ranking: the highest-scoring tombstone outranks 23 of 24 live rules.
    meanLive: meanLive === null ? null : Number(meanLive.toFixed(2)),
    liveCount,
    tombstoneCount,
    meanTombstone: meanTombstone === null ? null : Number(meanTombstone.toFixed(2)),
    criteria: criteriaSummary,
    belowThreshold: scored.filter((r) => r.score < 70).map((r) => r.file),
    belowThresholdLive: (results || [])
      .filter((r) => r && r.score !== null && !r.tombstone && r.score < 70)
      .map((r) => r.file),
    results,
  };

  if (opts.json) {
    const outAbs = path.resolve(projectRoot, opts.json);
    fs.mkdirSync(path.dirname(outAbs), { recursive: true });
    fs.writeFileSync(outAbs, `${JSON.stringify(report, null, 2)}\n`, 'utf8');
    console.log(`${PREFIX} - wrote ${outAbs}`);
  }

  // Fail loud rather than reporting a run we cannot substantiate.
  if (unscored.length > 0) {
    for (const r of unscored) console.error(`${PREFIX} - UNSCORED ${r.file}: ${r.unscoredReason}`);
    console.error(`${PREFIX} - ${unscored.length} rule(s) UNSCORED; report is not trustworthy`);
    process.exit(1);
  }
  if (opts.strict && report.belowThreshold.length > 0) {
    console.error(`${PREFIX} - --strict: ${report.belowThreshold.length} rule(s) below 70: ${report.belowThreshold.join(', ')}`);
    process.exit(1);
  }
  process.exit(0);
}

if (require.main === module) main();

module.exports = {
  PREFIX,
  CRITERIA,
  CRITERION_IDS,
  IMPORTANCE_WEIGHTS,
  CACHE_DEFAULT,
  CACHE_MAX_SAMPLES,
  parseRubric,
  parseRubricJson,
  parseCriteria,
  readRubricJson,
  weightedOverall,
  retriedSplit,
  liveSplit,
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
};