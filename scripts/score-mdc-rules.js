#!/usr/bin/env node
/**
 * HR4-B — score the `.cursor/rules/*.mdc` corpus with the real NVIDIA SkillEvaluator.
 *
 * Why this exists
 * ---------------
 * HR4-A measured 28 `SKILL.md` artifacts (mean 84.5) and found the 31
 * `.cursor/rules/*.mdc` (83,464 B) *unscoreable*:
 *
 *     $ skillevaluator quality-check .cursor/rules
 *     QUALITY | FAIL | 1 errors
 *
 * An Agent Skill is a directory containing `SKILL.md`. A Cursor rule is a
 * `.mdc` file with different frontmatter. The leading skill-evaluation tool
 * cannot read the second-largest instruction surface in this repo.
 *
 * This script bridges that gap WITHOUT re-implementing the rubric. A
 * re-implementation would produce numbers that *look* comparable to HR4-A but
 * are not the same measurement — the exact fail-open trap this repo's
 * verification-evidence rules warn about. Instead each rule is materialized
 * into a throwaway Agent Skill under a temp dir and scored by the actual
 * `skillevaluator` binary, so every number here is a real SkillEvaluator number.
 *
 * The repo is never modified. Temp dirs are removed unless --keep.
 *
 * Usage:
 *   npm run rules:score
 *   node scripts/score-mdc-rules.js --json Saved/rules_score.json
 *   node scripts/score-mdc-rules.js --strict --threshold 80
 *   node scripts/score-mdc-rules.js --tool /path/to/skillevaluator   # for tests
 *
 * Exit: 0 report written (and --strict satisfied), 1 threshold/strict failure
 *       or any rule left UNSCORED, 2 bad CLI or SkillEvaluator not installed
 */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const PREFIX = 'rules:score';

const projectRoot = path.resolve(__dirname, '..');
const DEFAULT_RULES_DIR = '.cursor/rules';
const DEFAULT_THRESHOLD = 80;

/**
 * Composite points every rule loses purely to the .mdc format mismatch.
 * See the `formatOffsetComposite` note in the report body. Scores printed here
 * are LOWER BOUNDS; add this back to compare against a native Agent Skill.
 */
const FORMAT_OFFSET_COMPOSITE = 3.5;

/** Candidate locations for the SkillEvaluator binary, most specific first. */
function toolCandidates(explicit) {
  if (explicit) return [explicit];
  const names = process.platform === 'win32'
    ? ['skillevaluator.exe', 'skillevaluator']
    : ['skillevaluator'];
  const dirs = [];
  if (process.env.UV_TOOL_BIN_DIR) dirs.push(process.env.UV_TOOL_BIN_DIR);
  if (process.env.USERPROFILE) {
    dirs.push(path.join(process.env.USERPROFILE, '.local', 'bin'));
  }
  if (process.env.HOME) dirs.push(path.join(process.env.HOME, '.local', 'bin'));
  dirs.push(path.join(os.homedir(), '.local', 'bin'));
  const out = [];
  for (const dir of dirs) for (const name of names) out.push(path.join(dir, name));
  // Bare name last: relies on PATH resolution.
  return out.concat(names);
}

/** Resolve the SkillEvaluator executable, or null when not installed. */
function resolveTool(explicit) {
  for (const candidate of toolCandidates(explicit)) {
    if (candidate.includes(path.sep)) {
      if (fs.existsSync(candidate)) return candidate;
    } else {
      // Bare command: trust spawnSync to surface ENOENT.
      const probe = spawnSync(candidate, ['--version'], { encoding: 'utf8' });
      if (!probe.error) return candidate;
    }
  }
  return null;
}

/**
 * Minimal frontmatter reader for `.mdc` files.
 * No YAML dependency on purpose — adding one is an ask-first dependency change.
 */
function parseFrontmatter(text) {
  const m = /^---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)/.exec(text);
  if (!m) return { data: {}, body: text, present: false };
  const data = {};
  for (const line of m[1].split(/\r?\n/)) {
    const kv = /^([A-Za-z_][A-Za-z0-9_-]*)[ \t]*:[ \t]*(.*)$/.exec(line);
    if (!kv) continue;
    let value = kv[2].trim();
    if (/^".*"$/.test(value) || /^'.*'$/.test(value)) {
      value = value.slice(1, -1);
    }
    data[kv[1]] = value;
  }
  return { data, body: text.slice(m[0].length), present: true };
}

/** Quote a string as a YAML double-quoted scalar. */
function yamlQuote(value) {
  return '"' + String(value).replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"';
}

/**
 * SkillEvaluator requires `name` to match ^[a-z0-9-]+$. Cursor rules use human
 * titles ("MCP-First Workflow"), so we slugify. DECLARED ADAPTATION: this means
 * SkillEvaluator's "Invalid name format" check cannot fire on a rule — that
 * check is intentionally not emulated here.
 */
function slugify(name, fallback) {
  const slug = String(name || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
  return slug || fallback || 'rule';
}

/** Read one `.mdc` file into a normalized rule record. */
function readRule(absPath, rulesDir) {
  const relPath = path.relative(projectRoot, absPath).split(path.sep).join('/');
  const raw = fs.readFileSync(absPath, 'utf8');
  const { data, body, present } = parseFrontmatter(raw);
  const fileStem = path.basename(absPath).replace(/\.mdc$/i, '');
  return {
    relPath,
    file: path.basename(absPath),
    slug: slugify(data.name, slugify(fileStem, 'rule')),
    declaredName: data.name || '',
    description: data.description || '',
    version: data.version || '',
    alwaysApply: data.alwaysApply || '',
    globs: data.globs || '',
    frontmatterPresent: present,
    body,
    bytes: Buffer.byteLength(raw, 'utf8'),
  };
}

/**
 * Write a throwaway Agent Skill mirroring the rule.
 *
 * DECLARED GAP: `alwaysApply` and `globs` have no SKILL.md equivalent and are
 * NOT scored by SkillEvaluator. They are preserved here as an HTML comment so
 * the materialization is auditable and nothing is silently dropped.
 */
function materializeSkill(rule, outRoot) {
  const dir = path.join(outRoot, rule.slug);
  fs.mkdirSync(dir, { recursive: true });
  const provenance = [
    `<!-- materialized by scripts/score-mdc-rules.js`,
    `     source: ${rule.relPath}`,
    `     declared name: ${rule.declaredName || '(none)'}`,
    `     alwaysApply: ${rule.alwaysApply || '(unset)'}`,
    `     globs: ${rule.globs || '(unset)'}`,
    `-->`,
    '',
  ].join('\n');
  const fm = ['---', `name: ${rule.slug}`, `description: ${yamlQuote(rule.description)}`];
  // Pass `version` through: every .mdc rule carries it, and SkillEvaluator's
  // SKILL_SPEC check deducts 5 correctness points when it is absent. Dropping
  // it here would have manufactured a finding against all 31 rules.
  if (rule.version) fm.push(`version: ${yamlQuote(rule.version)}`);
  fm.push('---', '', '');
  fs.writeFileSync(path.join(dir, 'SKILL.md'), fm.join('\n') + provenance + rule.body, 'utf8');
  return dir;
}

/**
 * Extract the composite score from SkillEvaluator output.
 * Returns null when the shape is unrecognised — deliberately NOT a zero, so an
 * unparseable run can never masquerade as a failing grade.
 */
function parseScore(stdout) {
  const m = /Overall:\s*([\d.]+)\/100\s*\(Grade:\s*([A-F][+-]?)\)/.exec(stdout || '');
  if (!m) return null;
  return { score: Number(m[1]), grade: m[2] };
}

/** Run the real tool against one materialized skill. */
function runQualityCheck(tool, skillDir) {
  const proc = spawnSync(tool, ['quality-check', skillDir], {
    encoding: 'utf8',
    maxBuffer: 32 * 1024 * 1024,
  });
  const combined = `${proc.stdout || ''}\n${proc.stderr || ''}`;
  const parsed = parseScore(combined);
  return {
    parsed,
    // SkillEvaluator returns a non-zero code when findings exist; that is not
    // itself a failure, so only surface it when nothing could be parsed.
    code: proc.status,
    spawnError: proc.error ? proc.error.message : '',
  };
}

function parseArgs(argv) {
  const opts = {
    rulesDir: DEFAULT_RULES_DIR,
    json: '',
    strict: false,
    threshold: DEFAULT_THRESHOLD,
    keep: false,
    tool: '',
    limit: 0,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    const next = () => {
      const v = argv[i + 1];
      if (v === undefined) {
        console.error(`${PREFIX} - missing value for ${a}`);
        process.exit(2);
      }
      i += 1;
      return v;
    };
    if (a === '--rules-dir') opts.rulesDir = next();
    else if (a === '--json') opts.json = next();
    else if (a === '--threshold') opts.threshold = Number(next());
    else if (a === '--tool') opts.tool = next();
    else if (a === '--limit') opts.limit = Number(next());
    else if (a === '--strict') opts.strict = true;
    else if (a === '--keep') opts.keep = true;
    else if (a === '--help' || a === '-h') {
      console.log(fs.readFileSync(__filename, 'utf8').split('*/')[0].replace(/^\/\*\*?/, ''));
      process.exit(0);
    } else {
      console.error(`${PREFIX} - unknown arg: ${a}`);
      process.exit(2);
    }
  }
  if (!Number.isFinite(opts.threshold)) {
    console.error(`${PREFIX} - --threshold must be a number`);
    process.exit(2);
  }
  return opts;
}

function main() {
  const opts = parseArgs(process.argv.slice(2));

  const rulesAbs = path.resolve(projectRoot, opts.rulesDir);
  if (!fs.existsSync(rulesAbs)) {
    console.error(`${PREFIX} - no rules directory: ${rulesAbs}`);
    process.exit(2);
  }

  const tool = resolveTool(opts.tool);
  if (!tool) {
    console.error(`${PREFIX} - SkillEvaluator not found. Install it with:`);
    console.error(`${PREFIX}   uv tool install --python 3.13 "skillevaluator[all] @ git+https://github.com/NVIDIA/SkillEvaluator.git"`);
    console.error(`${PREFIX} - Refusing to emit a report without the real scorer (exit 2).`);
    process.exit(2);
  }

  const files = fs
    .readdirSync(rulesAbs)
    .filter((f) => f.toLowerCase().endsWith('.mdc'))
    .sort();
  const selected = opts.limit > 0 ? files.slice(0, opts.limit) : files;
  if (selected.length === 0) {
    console.error(`${PREFIX} - no .mdc files under ${rulesAbs}`);
    process.exit(2);
  }

  const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'hw-mdc-score-'));
  const results = [];
  try {
    for (const file of selected) {
      const rule = readRule(path.join(rulesAbs, file), rulesAbs);
      const dir = materializeSkill(rule, tmpRoot);
      const run = runQualityCheck(tool, dir);
      results.push({
        file: rule.file,
        relPath: rule.relPath,
        slug: rule.slug,
        declaredName: rule.declaredName,
        hasDeclaredName: Boolean(rule.declaredName),
        description: rule.description,
        alwaysApply: rule.alwaysApply,
        globs: rule.globs,
        bytes: rule.bytes,
        score: run.parsed ? run.parsed.score : null,
        grade: run.parsed ? run.parsed.grade : null,
        unscoredReason: run.parsed
          ? null
          : run.spawnError || `unparseable output (exit ${run.code})`,
      });
    }
  } finally {
    if (opts.keep) {
      console.log(`${PREFIX} - kept materialized skills: ${tmpRoot}`);
    } else {
      fs.rmSync(tmpRoot, { recursive: true, force: true });
    }
  }

  const scored = results.filter((r) => r.score !== null);
  const unscored = results.filter((r) => r.score === null);
  const scoredList = scored.map((r) => r.score);
  const mean = scoredList.length
    ? scoredList.reduce((a, b) => a + b, 0) / scoredList.length
    : 0;
  const below = scored.filter((r) => r.score < opts.threshold);
  const missingName = results.filter((r) => !r.hasDeclaredName);

  const pad = (s, n) => String(s).padEnd(n);
  console.log('');
  console.log(`${PREFIX} - SkillEvaluator quality-check on .cursor/rules/*.mdc`);
  console.log(`  tool       : ${tool}`);
  console.log(`  rules      : ${results.length} (${scored.length} scored, ${unscored.length} UNSCORED)`);
  if (scoredList.length) {
    const lo = Math.min(...scoredList);
    const hi = Math.max(...scoredList);
    console.log(`  mean       : ${mean.toFixed(1)}  (range ${lo.toFixed(1)}-${hi.toFixed(1)})`);
    console.log(`  offset     : +${FORMAT_OFFSET_COMPOSITE} format artifact (metadata.author/tags have no .mdc`);
    console.log(`               equivalent) -> true mean ~${(mean + FORMAT_OFFSET_COMPOSITE).toFixed(1)}, best ~${(hi + FORMAT_OFFSET_COMPOSITE).toFixed(1)}`);
  }
  console.log(`  threshold  : ${opts.threshold}  -> ${below.length} below`);
  console.log('');
  for (const r of [...results].sort((a, b) => (a.score ?? -1) - (b.score ?? -1))) {
    const s = r.score === null ? 'UNSCORED' : `${r.score.toFixed(1)} (${r.grade})`;
    const flag = r.hasDeclaredName ? '' : '  [!] no frontmatter name';
    console.log(`  ${pad(r.file, 40)} ${pad(s, 16)}${flag}`);
  }
  for (const r of unscored) {
    console.error(`${PREFIX} - UNSCORED ${r.file}: ${r.unscoredReason}`);
  }
  for (const r of missingName) {
    console.error(`${PREFIX} - MISSING frontmatter "name" in ${r.relPath}`);
  }

  const report = {
    tool: PREFIX,
    version: 1,
    generatedAt: new Date().toISOString(),
    scorer: tool,
    rulesDir: opts.rulesDir,
    threshold: opts.threshold,
    declaredAdaptations: [
      'name is slugified to satisfy SkillEvaluator ^[a-z0-9-]+$; rule titles are not scored',
      'version is passed through from .mdc frontmatter so the SKILL_SPEC check measures the rule, not this adapter',
      'alwaysApply and globs have no SKILL.md equivalent and are NOT scored',
      'skill-type detection resolves to guide-only for single-file rules',
    ],
    // SkillEvaluator deducts 5 correctness points each for metadata.author and
    // metadata.tags. A Cursor .mdc rule has no author or tags concept, and
    // inventing either would fabricate provenance. Those 10 correctness points
    // are therefore structurally unreachable for this corpus: 10 * 0.35 =
    // 3.5 composite points of constant, format-caused offset on every rule.
    // Treat reported scores as LOWER BOUNDS by this amount.
    formatOffsetComposite: FORMAT_OFFSET_COMPOSITE,
    ruleCount: results.length,
    scoredCount: scored.length,
    unscoredCount: unscored.length,
    missingNameCount: missingName.length,
    mean: Number(mean.toFixed(2)),
    belowThreshold: below.map((r) => r.file),
    results,
  };

  if (opts.json) {
    const outAbs = path.resolve(projectRoot, opts.json);
    fs.mkdirSync(path.dirname(outAbs), { recursive: true });
    fs.writeFileSync(outAbs, JSON.stringify(report, null, 2) + '\n', 'utf8');
    console.log(`${PREFIX} - wrote ${outAbs}`);
  }

  // Fail loudly rather than reporting a clean run we cannot substantiate.
  if (unscored.length > 0) {
    console.error(`${PREFIX} - ${unscored.length} rule(s) UNSCORED; report is not trustworthy`);
    process.exit(1);
  }
  if (opts.strict && below.length > 0) {
    console.error(`${PREFIX} - --strict: ${below.length} rule(s) below ${opts.threshold}`);
    process.exit(1);
  }
  process.exit(0);
}

if (require.main === module) {
  main();
}

module.exports = {
  PREFIX,
  DEFAULT_THRESHOLD,
  FORMAT_OFFSET_COMPOSITE,
  parseFrontmatter,
  yamlQuote,
  slugify,
  parseScore,
  readRule,
  materializeSkill,
  resolveTool,
  parseArgs,
};