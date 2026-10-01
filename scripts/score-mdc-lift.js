#!/usr/bin/env node
/**
 * Skill Lift measurement for .cursor/rules/*.mdc — LLM-as-judge rubric eval.
 *
 * Usage:
 *   node scripts/score-mdc-lift.js [options]
 *   npm run lift:score -- [--json Saved/rules_lift.json] [--repeat N] [--strict]
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
const { spawnSync } = require('child_process');

const PREFIX = 'lift:score';
const projectRoot = path.resolve(__dirname, '..');
const REPEATS_DEFAULT = 1;
// The judge intermittently returns prose instead of JSON, giving no score. That
// is transient, so each attempt is retried; see scoreWithRetries().
const RETRIES_DEFAULT = 2;
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

/** Run rubric-eval once. Returns {score, criteria} or {score:null, reason}. */
function runRubricOnce(tool, skillDir) {
  const proc = spawnSync(tool, ['rubric-eval', skillDir, '-r', 'cli'], {
    encoding: 'utf8',
    maxBuffer: 32 * 1024 * 1024,
  });
  const parsed = parseRubric(proc);
  if (parsed) return { ...parsed, criteria: parseCriteria(proc) };
  return { score: null, reason: failureReason(proc) };
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

function parseArgs(argv) {
  const opts = {
    json: null,
    strict: false,
    repeat: REPEATS_DEFAULT,
    retries: RETRIES_DEFAULT,
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

  // Identify the judge so the number is anchored to a model, not just a tool.
  const probe = spawnSync(tool, ['health-check'], { encoding: 'utf8', maxBuffer: 8 * 1024 * 1024 });
  const health = `${probe.stdout || ''}${probe.stderr || ''}`;
  const model = MODEL_RE.exec(health);
  const judgeModel = model ? `nvidia/${model[1]}` : 'unknown';
  const toolVersion = sibling.toolVersion(tool);

  const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'hw-lift-'));
  const results = [];
  try {
    for (const file of files) {
      const rule = sibling.readRule(path.join(rulesAbs, file), rulesAbs);
      const dir = sibling.materializeSkill(rule, tmpRoot);
      const runs = [];
      for (let r = 0; r < opts.repeat; r += 1) {
        runs.push(scoreWithRetries(() => runRubricOnce(tool, dir), opts.retries));
      }
      const scores = runs.map((x) => x.score).filter((x) => x !== null);
      const mean = scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length : null;
      const attempts = runs.reduce((a, x) => a + (x.attempts || 1), 0);
      // Criterion scores are averaged over whichever runs reported them; a rule
      // judged but with unparseable criteria simply contributes none.
      const critAcc = {};
      for (const run of runs) {
        for (const [k, v] of Object.entries(run.criteria || {})) (critAcc[k] ||= []).push(v);
      }
      const criteria = {};
      for (const [k, arr] of Object.entries(critAcc)) {
        criteria[k] = Number((arr.reduce((a, b) => a + b, 0) / arr.length).toFixed(2));
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
        // A rule that needed a retry is flaky - surface it, do not hide it.
        attempts,
        retried: attempts > runs.length,
        unscoredReason: scores.length ? null : runs[0].reason,
      });
      const shown =
        mean === null
          ? `UNSCORED (${runs[0].reason})`
          : `${mean.toFixed(1)}${opts.repeat > 1 ? ` (spread ${(Math.max(...scores) - Math.min(...scores)).toFixed(1)})` : ''}${attempts > runs.length ? ` [${attempts} attempts]` : ''}`;
      process.stderr.write(`${PREFIX} - ${file} ${shown}\n`);
    }
  } finally {
    fs.rmSync(tmpRoot, { recursive: true, force: true });
  }

  const scored = results.filter((r) => r.score !== null);
  const unscored = results.filter((r) => r.score === null);
  const scores = scored.map((r) => r.score);
  const mean = scores.length ? scores.reduce((a, b) => a + b, 0) / scores.length : null;
  const spreads = scored.map((r) => r.spread).filter((x) => x !== null);
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
  const retriedCount = scored.filter((r) => r.retried).length;
  if (retriedCount > 0 || unscored.length > 0) {
    console.log(
      `  judge flakiness : ${retriedCount} rule(s) needed a retry; the judge sometimes returns prose instead of JSON (--retries ${opts.retries})`
    );
  }
  if (scores.length) {
    console.log(`  mean       : ${mean.toFixed(1)}  (range ${Math.min(...scores).toFixed(1)}-${Math.max(...scores).toFixed(1)})`);
    if (spreads.length) {
      console.log(`  jitter     : mean spread ${(spreads.reduce((a, b) => a + b, 0) / spreads.length).toFixed(1)} pts over ${opts.repeat} run(s) — a single run is not a measurement`);
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
      // Jitter is a property of LLM judging, not of any rule. Recorded so a
      // reader never mistakes a one-run delta for a real regression.
      repeats: opts.repeat,
      meanSpread: spreads.length
        ? Number((spreads.reduce((a, b) => a + b, 0) / spreads.length).toFixed(2))
        : null,
      maxSpread: spreads.length ? Number(Math.max(...spreads).toFixed(2)) : null,
      // The judge sometimes answers in prose and emits no score; that attempt is
      // retried. retriedCount > 0 means the provider is flaky right now, which
      // a reader needs to know before trusting an UNSCORED or a tight delta.
      retries: opts.retries,
      retriedCount: scored.filter((r) => r.retried).length,
      attemptsTotal: results.reduce((a, r) => a + (r.attempts || 1), 0),
    },
    comparability: {
      againstQualityCheck: false,
      note: 'rubric-eval (LLM judge) and quality-check (structural) are different measurements. Their numbers must not be averaged or diffed. arXiv 2608.20614 measures rho = 0.14 between structural gates and LLM-judged quality.',
    },
    credential: {
      provider: cred.provider,
      credentialVar: cred.credentialVar,
      recorded: false,
      note: 'credential value is never persisted; only the variable name and length',
    },
    ruleCount: results.length,
    judgedCount: scored.length,
    unscoredCount: unscored.length,
    mean: mean === null ? null : Number(mean.toFixed(2)),
    criteria: criteriaSummary,
    belowThreshold: scored.filter((r) => r.score < 70).map((r) => r.file),
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
  parseRubric,
  parseCriteria,
  detectCredential,
  resolveTool,
  failureReason,
  scoreWithRetries,
};