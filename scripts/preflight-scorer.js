#!/usr/bin/env node
/**
 * Scorer version preflight — the guard the docs note could not be.
 *
 * Why this exists: SkillEvaluator is a **git-installed uv tool**, not a PyPI
 * package, so nothing in the repo pins it. That has already bitten once — an
 * unanchored reinstall moved the scorer **0.3.0 -> 0.4.0** and the corpus mean
 * with it (87.3 -> 87.4). A version *note* in a doc cannot catch that; only a
 * check at the point of use can.
 *
 * Contract, deliberately narrow:
 *   - ADVISORY, never fatal. A missing or mismatched scorer must not break
 *     `npm run doctor` or a developer's setup; it should say so and move on.
 *   - Never prints the credential or any path outside the project.
 *   - A version it cannot read is `unknown`, which is reported as UNVERIFIED —
 *     never silently treated as a match.
 *
 * Usage:
 *   node scripts/preflight-scorer.js            # human-readable
 *   node scripts/preflight-scorer.js --json     # machine-readable
 *
 * Exit codes: 0 = ok or unverified (advisory never fails), 2 = bad usage.
 */

const { spawnSync } = require('child_process');
const sibling = require('./score-mdc-rules.js');

/**
 * The version every recorded judged number was produced with. Changing it makes
 * prior scores a different measurement, not a better one.
 */
const REQUIRED_SCORER_VERSION = '0.4.0';

/**
 * Compare an observed version against the required one.
 *
 * Returns a status rather than a boolean so the caller can distinguish
 * "checked and fine" from "could not check" — the difference between evidence
 * and the absence of it.
 */
function compareVersion(observed, required = REQUIRED_SCORER_VERSION) {
  // Trim BEFORE deciding whether the value is usable: a whitespace-only version
  // is as unreadable as an empty one, and treating it as a mismatch cries wolf.
  const o = observed === null || observed === undefined ? '' : String(observed).trim();
  const r = String(required === null || required === undefined ? '' : required).trim();

  if (o === '' || o.toLowerCase() === 'unknown') {
    return {
      status: 'unverified',
      observed: o || 'unknown',
      required: r,
      reason: 'version could not be read',
    };
  }
  // Normalise an optional `v` prefix on EITHER side. Some builds print `v0.4.0`;
  // stripping it from only one side turns a correct install into a false alarm.
  const bare = (s) => s.replace(/^v/i, '');
  if (bare(o) === bare(r)) return { status: 'match', observed: o, required: r, reason: null };
  return {
    status: 'mismatch',
    observed: o,
    required: r,
    reason: 'scores from a different rubric version are a different measurement and are not comparable',
  };
}

function main(argv) {
  const asJson = argv.includes('--json');
  const explicitIdx = argv.indexOf('--tool');
  const explicit = explicitIdx !== -1 ? argv[explicitIdx + 1] : undefined;

  let tool = null;
  let resolveError = null;
  try {
    tool = sibling.resolveTool(explicit);
  } catch (e) {
    resolveError = e && e.message ? e.message : String(e);
  }

  const observed = tool ? sibling.toolVersion(tool) : null;
  const cmp = compareVersion(observed);

  const report = {
    check: 'scorer-version',
    required: REQUIRED_SCORER_VERSION,
    observed: cmp.observed,
    status: tool ? cmp.status : 'absent',
    // Advisory by design: this never fails a build or a doctor run.
    fatal: false,
    reason: tool ? cmp.reason : 'skillevaluator not found on PATH or at the known locations',
    resolveError,
    hint:
      tool && cmp.status === 'mismatch'
        ? `Install ${REQUIRED_SCORER_VERSION} (uv tool, git-sourced — not on PyPI). Do not install from git HEAD: that moves the scorer off the recorded version.`
        : 'The judged baseline lives in docs/measured/SKILL_LIFT_BASELINE.md',
  };

  if (asJson) {
    process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  } else {
    const tag = { match: 'OK', mismatch: 'WARN', unverified: 'WARN', absent: 'INFO' }[report.status];
    const line = `[preflight:scorer] ${tag} — required ${REQUIRED_SCORER_VERSION}, observed ${report.observed} (${report.status})`;
    process.stderr.write(`${line}\n`);
    if (report.reason) process.stderr.write(`[preflight:scorer]   ${report.reason}\n`);
    if (report.hint) process.stderr.write(`[preflight:scorer]   ${report.hint}\n`);
    if (report.status === 'match') {
      process.stderr.write('[preflight:scorer]   judged scores from this install are comparable with the tracked baseline.\n');
    }
  }
  return 0;
}

if (require.main === module) {
  const argv = process.argv.slice(2);
  if (argv.some((a) => a === '-h' || a === '--help')) {
    process.stdout.write(
      'Usage: node scripts/preflight-scorer.js [--json] [--tool PATH]\n' +
        'Advisory check that the installed SkillEvaluator is the recorded version.\n' +
        'Never exits non-zero: a mismatch is reported, not enforced.\n'
    );
    process.exit(0);
  }
  try {
    process.exit(main(argv));
  } catch (e) {
    process.stderr.write(`[preflight:scorer] ERROR — ${e && e.message ? e.message : String(e)}\n`);
    process.exit(2);
  }
}

module.exports = { REQUIRED_SCORER_VERSION, compareVersion };
