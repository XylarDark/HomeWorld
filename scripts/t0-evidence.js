#!/usr/bin/env node
/**
 * T0 beat evidence ledger — make the product's proof state visible and diffable.
 *
 * THE PROBLEM THIS SOLVES
 * -----------------------
 * Every T0 prove run writes `Saved/t0_*_gate.json`, and `Saved/` is gitignored.
 * So the only record of whether a beat was ever proved is local, untracked, and
 * invisible to review. Worse, nothing in the tree ever said "PROVEN" — so the
 * board had to carry "MERGED / NOT PROVEN" on all 14 beats while three of them
 * locally self-report a pass. Both statements were true and the contradiction was
 * invisible.
 *
 * WHAT THIS IS NOT
 * ----------------
 * This does NOT decide that a beat is proven. Acceptance is a human `test` job:
 * somebody has to run the prove script, look at the evidence, and stamp it. This
 * tool only reports, per beat, exactly what the local artifact claims and with
 * what caveats — so the gap between "locally reports pass" and "accepted" is
 * legible instead of implied.
 *
 * THREE SCHEMAS, THREE HONEST STATUSES
 * ------------------------------------
 * The observed gate files use three incompatible schemas:
 *   m2-m7 + skybox : { bite, sha, host, map, soft_fail, closed_fail, evidence,
 *                      notes, ts_utc }                       -- no pass field
 *   m8             : the above plus { must, pr, labels, pass,
 *                      anti_not_scored_as_pass }
 *   m9             : { version, track, impl_sha, prove_loop_status,
 *                      placement_outcome, greps, api_probes, ... }
 * A missing `pass` field is NOT a pass. It is recorded as NO_VERDICT, because
 * inferring either way would be inventing a result nobody measured.
 *
 * Usage:
 *   node scripts/t0-evidence.js              # markdown to stdout
 *   node scripts/t0-evidence.js --json       # machine-readable
 *   node scripts/t0-evidence.js --saved DIR  # override the gate directory
 */

const fs = require('fs');
const path = require('path');

const PREFIX = '[t0-evidence]';
const PROJECT_ROOT = path.resolve(__dirname, '..');

/**
 * Read JSON that may carry a UTF-8 BOM.
 *
 * 6 of the 14 observed gate files are written with a BOM, which makes
 * `JSON.parse` throw `Unexpected token '\uFEFF'`. PowerShell's ConvertFrom-Json
 * tolerates it, which is exactly why this went unnoticed: the file "parses" in
 * one shell and not the other. Strip the BOM before parsing rather than letting
 * a consumer decide.
 */
function readJsonLoose(file) {
  const raw = fs.readFileSync(file, 'utf8');
  const text = raw.charCodeAt(0) === 0xfeff ? raw.slice(1) : raw;
  return JSON.parse(text);
}

/** True when the file starts with a UTF-8 BOM. Reported, because it is a defect. */
function hasBom(file) {
  const buf = fs.readFileSync(file);
  return buf[0] === 0xef && buf[1] === 0xbb && buf[2] === 0xbf;
}

/** Pick the first present key. Gate schemas disagree on names, not on meaning. */
function pick(obj, keys, fallback = null) {
  for (const k of keys) {
    if (obj && Object.prototype.hasOwnProperty.call(obj, k) && obj[k] !== null) return obj[k];
  }
  return fallback;
}

/**
 * Classify one gate artifact into an honest status.
 *
 * The distinction that matters: `LOCAL_PASS` is what the script claimed on this
 * machine; `ACCEPTED` is a human stamp. Neither is inferred from the other.
 */
function classifyGate(gate) {
  const pass = pick(gate, ['pass', 'passed', 'ok']);
  const provisional = pick(gate, ['provisional', 'is_provisional']);
  const closedFail = pick(gate, ['closed_fail', 'hard_fail']);
  const softFail = pick(gate, ['soft_fail']);

  let status;
  if (pass === true && provisional !== true && closedFail !== true) {
    status = 'LOCAL_PASS';
  } else if (provisional === true) {
    status = 'PROVISIONAL';
  } else if (pass === false || closedFail === true) {
    status = 'LOCAL_FAIL';
  } else {
    status = 'NO_VERDICT';
  }

  return {
    status,
    pass: pass === undefined ? null : pass,
    provisional: provisional === undefined ? null : provisional,
    closedFail: closedFail === undefined ? null : closedFail,
    softFail: softFail === undefined ? null : softFail,
    // Never derivable from a local file. This is the whole point of the ledger.
    accepted: false,
    acceptanceReason: 'unstamped — a human must run the prove script and accept the result',
  };
}

/** Beat id from a gate filename: `t0_m14_camp_night_gate.json` -> `T0_M14`. */
function beatFromFilename(file) {
  const base = path.basename(file, '.json');
  const m = /^t0_m(\d+)_/i.exec(base);
  if (m) return `T0_M${Number(m[1])}`;
  if (/^t0_default_/i.test(base)) return 'T0_DEFAULT_SKYBOX_DAY';
  return base.toUpperCase();
}

/** Sort key so beats read M1..M14 then the side packet, not alphabetically. */
function beatOrder(beat) {
  const m = /^T0_M(\d+)$/.exec(beat);
  return m ? Number(m[1]) : 999;
}

/**
 * Scan a directory of gate artifacts.
 *
 * A file that cannot be parsed is reported as UNREADABLE rather than skipped:
 * a silent skip would make an unprovable beat look absent rather than broken.
 */
function collectGates(savedDir) {
  if (!fs.existsSync(savedDir)) return [];
  const files = fs
    .readdirSync(savedDir)
    .filter((f) => /^t0_.*gate\.json$/i.test(f))
    .sort();

  const rows = [];
  for (const f of files) {
    const full = path.join(savedDir, f);
    const rel = path.relative(PROJECT_ROOT, full).split(path.sep).join('/');
    const beat = beatFromFilename(f);
    try {
      const gate = readJsonLoose(full);
      rows.push({
        beat,
        artifact: rel,
        trackedInGit: false, // `Saved/` is gitignored. Stated, never assumed.
        bom: hasBom(full),
        ...classifyGate(gate),
        map: pick(gate, ['map', 'level_path']),
        sha: pick(gate, ['sha', 'impl_sha']),
        host: pick(gate, ['host']),
        notes: pick(gate, ['notes']),
      });
    } catch (e) {
      rows.push({
        beat,
        artifact: rel,
        trackedInGit: false,
        bom: hasBom(full),
        status: 'UNREADABLE',
        pass: null,
        provisional: null,
        closedFail: null,
        softFail: null,
        accepted: false,
        acceptanceReason: 'artifact could not be parsed',
        parseError: e && e.message ? e.message : String(e),
        map: null,
        sha: null,
        host: null,
        notes: null,
      });
    }
  }
  rows.sort((a, b) => beatOrder(a.beat) - beatOrder(b.beat) || a.beat.localeCompare(b.beat));
  return rows;
}

/** Counts by status, plus the single number that matters: accepted beats. */
function summarize(rows) {
  const byStatus = {};
  for (const r of rows) byStatus[r.status] = (byStatus[r.status] || 0) + 1;
  return {
    total: rows.length,
    byStatus,
    accepted: rows.filter((r) => r.accepted === true).length,
    localPass: rows.filter((r) => r.status === 'LOCAL_PASS').length,
    tracked: rows.filter((r) => r.trackedInGit).length,
    bomFiles: rows.filter((r) => r.bom).length,
  };
}

const STATUS_GLOSS = {
  LOCAL_PASS: 'artifact self-reports pass, no provisional flag, no closed fail',
  PROVISIONAL: 'artifact self-flags `provisional: true` — not a verdict',
  LOCAL_FAIL: 'artifact reports a failure',
  NO_VERDICT: 'no pass field in the artifact — outcome unknown, NOT a pass',
  UNREADABLE: 'artifact could not be parsed',
};

function renderMarkdown(rows, savedDirLabel) {
  const s = summarize(rows);
  const lines = [];
  lines.push('# T0 beat evidence ledger');
  lines.push('');
  lines.push('> **Generated file.** Regenerate with `npm run t0:evidence`.');
  lines.push('> The local artifacts in `Saved/` remain the authority; this is a summary.');
  lines.push('');
  lines.push('## The one number');
  lines.push('');
  lines.push(`**Accepted beats: ${s.accepted} of ${s.total}.**`);
  lines.push('');
  lines.push(
    'A beat is *accepted* when a human has run its prove script, inspected the' +
      ' evidence, and stamped it. No beat is. Acceptance is not derivable from a' +
      ' local file, so this tool never sets it — the field is hard-coded `false`.' +
      ' That is the honest state, and it is why the board says NOT PROVEN on all 14.'
  );
  lines.push('');
  lines.push('## What the local artifacts claim');
  lines.push('');
  lines.push('| Beat | Artifact status | Provisional | Closed fail | Accepted |');
  lines.push('|---|---|---|---|---|');
  for (const r of rows) {
    const yn = (v) => (v === null ? '—' : v === true ? 'yes' : v === false ? 'no' : String(v));
    lines.push(
      `| ${r.beat} | **${r.status}** | ${yn(r.provisional)} | ${yn(r.closedFail)} | ${yn(r.accepted)} |`
    );
  }
  lines.push('');
  lines.push('### Status glossary');
  lines.push('');
  for (const [k, v] of Object.entries(STATUS_GLOSS)) lines.push(`- **${k}** — ${v}`);
  lines.push('');
  lines.push('## Findings this ledger surfaced');
  lines.push('');
  const defects = [];
  if (s.bomFiles > 0) {
    defects.push(
      `- **${s.bomFiles} of ${s.total} gate files are written with a UTF-8 BOM.** ` +
        `\`JSON.parse\` throws on them; PowerShell's \`ConvertFrom-Json\` tolerates them. ` +
        `That is why the artifact "parses" in one shell and not the other. \`readJsonLoose\` strips it.`
    );
  }
  const noVerdict = rows.filter((r) => r.status === 'NO_VERDICT').length;
  if (noVerdict > 0) {
    defects.push(
      `- **${noVerdict} artifact(s) carry no pass field at all.** The m2–m7 schema has no ` +
        `\`pass\`. Their outcome is unknown, which is recorded as NO_VERDICT rather than ` +
        `guessed in either direction.`
    );
  }
  defects.push(
    `- **Three incompatible schemas** (m2–m7+skybox, m8, m9) with overlapping-but-different ` +
      `key names, so any consumer must probe for aliases. A single schema would make the ` +
      `gate artifacts comparable across beats.`
  );
  defects.push(
    `- **0 of ${s.total} artifacts are tracked in git.** \`Saved/\` is gitignored by policy, ` +
      `so this ledger is the only reviewable record that a prove run happened at all.`
  );
  if (defects.length === 0) defects.push('- none observed');
  lines.push(...defects);
  lines.push('');
  lines.push('## How to move a beat to ACCEPTED');
  lines.push('');
  lines.push('1. Run the beat\'s prove script (`Content/Python/t0_*_prove.py`) on the Editor host.');
  lines.push('2. Inspect `Saved/t0_*_gate.json` — confirm the evidence, not just the flag.');
  lines.push('3. Stamp acceptance in the beat\'s `T0_M*_PROVE.md` (add a Result section).');
  lines.push('4. Regenerate this ledger; the Accepted column is the receipt.');
  lines.push('');
  lines.push(
    `_Source: \`${savedDirLabel}\`. Regenerating is idempotent — this file is a function ` +
      `of the artifacts, not a record of decisions._`
  );
  lines.push('');
  return lines.join('\n');
}

function main(argv) {
  const asJson = argv.includes('--json');
  const idx = argv.indexOf('--saved');
  const savedDir =
    idx !== -1 && argv[idx + 1]
      ? path.resolve(PROJECT_ROOT, argv[idx + 1])
      : path.join(PROJECT_ROOT, 'Saved');

  const rows = collectGates(savedDir);
  if (rows.length === 0) {
    process.stderr.write(`${PREFIX} - no gate artifacts in ${savedDir}\n`);
    return 0;
  }

  if (asJson) {
    const label = path.relative(PROJECT_ROOT, savedDir).split(path.sep).join('/');
    process.stdout.write(
      `${JSON.stringify(
        {
          tool: PREFIX,
          note: 'A summary of local artifacts. Acceptance is a human stamp and is never inferred.',
          source: label,
          ...summarize(rows),
          beats: rows,
        },
        null,
        2
      )}\n`
    );
  } else {
    const label = path.relative(PROJECT_ROOT, savedDir).split(path.sep).join('/');
    process.stdout.write(renderMarkdown(rows, label));
  }
  return 0;
}

if (require.main === module) {
  try {
    process.exit(main(process.argv.slice(2)));
  } catch (e) {
    process.stderr.write(`${PREFIX} ERROR — ${e && e.message ? e.message : String(e)}\n`);
    process.exit(2);
  }
}

module.exports = {
  PREFIX,
  readJsonLoose,
  hasBom,
  pick,
  classifyGate,
  beatFromFilename,
  beatOrder,
  collectGates,
  summarize,
  renderMarkdown,
  STATUS_GLOSS,
};