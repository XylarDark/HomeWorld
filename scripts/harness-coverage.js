#!/usr/bin/env node
/**
 * Harness coverage — which recorded failures has the rule corpus never heard of?
 *
 * THE QUESTION
 * ------------
 * `docs/KNOWN_ERRORS.md` is the project's record of things that actually broke.
 * The rule corpus is the project's attempt to stop them breaking again. Nobody
 * has ever compared the two, so the rules could be comprehensively silent about
 * every failure the team has ever hit and no report would say so.
 *
 * This answers that, for free, with no agent runs.
 *
 * WHAT IT MEASURES (and what it does not)
 * ---------------------------------------
 * It measures **mention**: does any rule file contain a distinctive technical
 * term from the recorded failure? That is a *weak* signal. A rule may mention
 * `GameplayAbilitySpec.h` and still not prevent the include-path error; a rule
 * may prevent the error without using the same word. Mention is a ceiling, not
 * a proof, and the output says so on every run.
 *
 * It is still worth having, because the failure mode it catches is real and
 * silent: a defect class with no mention anywhere in the rules is a defect class
 * the harness cannot be pointing at, no matter how well-written the other rules
 * are. That is a gap, and gaps are what an audit should surface.
 *
 * The three verdicts:
 *   COVERED        - at least one rule file mentions a distinctive term.
 *   UNCOVERED      - the failure has distinctive terms and NO rule mentions any.
 *   UNEXTRACTABLE  - the entry is prose with no distinctive term; not a finding.
 *
 * And a second axis, because "no rule" and "nobody knows" are different problems:
 *   harnessOnly    - mentioned in AGENTS.md, .agents/, or docs/, but in NO rule.
 *                    Knowledge exists; it just never became a rule.
 *
 * Usage:
 *   node scripts/harness-coverage.js             # markdown to stdout
 *   node scripts/harness-coverage.js --json      # machine-readable
 *   node scripts/harness-coverage.js --strict    # exit 1 if any UNCOVERED (ratchet)
 */

const fs = require('fs');
const path = require('path');

const PREFIX = '[harness-coverage]';
const PROJECT_ROOT = path.resolve(__dirname, '..');
const RULES_DIR = path.join(PROJECT_ROOT, '.cursor/rules');
const KNOWN_ERRORS = path.join(PROJECT_ROOT, 'docs/KNOWN_ERRORS.md');

/** Non-distinctive words that would otherwise inflate term counts. */
const STOPWORDS = new Set([
  'the', 'and', 'with', 'from', 'this', 'that', 'when', 'only', 'also', 'true', 'false',
  'none', 'null', 'true', 'returns', 'return', 'error', 'errors', 'fails', 'fail', 'failed',
]);

/**
 * Split `docs/KNOWN_ERRORS.md` into entries.
 *
 * Entries are `###` headings under `## Entries`. Anything before that heading is
 * preamble (format notes, harness-trap sections) and is excluded on purpose: the
 * "Harness traps" section documents traps that were already turned into tooling,
 * so counting it would inflate coverage with self-referential entries.
 */
function parseEntries(markdown) {
  const lines = markdown.split(/\r?\n/);
  let inEntries = false;
  const entries = [];
  let cur = null;

  for (const line of lines) {
    if (/^##\s+Entries/.test(line)) {
      inEntries = true;
      continue;
    }
    if (/^##\s+/.test(line)) {
      if (cur) entries.push(cur);
      cur = null;
      inEntries = false;
      continue;
    }
    if (!inEntries) continue;
    if (/^###\s+/.test(line)) {
      if (cur) entries.push(cur);
      cur = { head: line.replace(/^###\s+/, '').trim(), body: [] };
    } else if (cur) {
      cur.body.push(line);
    }
  }
  if (cur) entries.push(cur);
  return entries;
}

/**
 * Distinctive technical terms from one entry.
 *
 * Inline code spans first (most distinctive and most deterministic), then
 * identifiers in the heading. Multi-token spans are split so that a span like
 * `Abilities/GameplayAbilitySpec.h` still contributes the bare filename.
 */
function extractTerms(entry) {
  const terms = new Set();
  const body = entry.body.join('\n');

  for (const m of body.matchAll(/`([^`\n]{2,60})`/g)) {
    for (const frag of m[1].split(/[\s,;()]+/)) {
      const f = frag.trim().replace(/^["']|["']$/g, '');
      if (f.length < 5) continue;
      if (!/[A-Za-z]/.test(f)) continue;
      if (STOPWORDS.has(f.toLowerCase())) continue;
      terms.add(f);
    }
  }
  for (const m of entry.head.matchAll(/\b([A-Za-z_][A-Za-z0-9_]*[A-Z][A-Za-z0-9_]*)\b/g)) terms.add(m[1]);
  for (const m of entry.head.matchAll(/\b(C\d{4})\b/g)) terms.add(m[1]);

  return [...terms].sort();
}

/** Read every rule file as lowercase text, keyed by filename. */
function loadRules(rulesDir = RULES_DIR) {
  if (!fs.existsSync(rulesDir)) return new Map();
  const map = new Map();
  for (const f of fs.readdirSync(rulesDir).filter((n) => n.endsWith('.mdc')).sort()) {
    map.set(f, fs.readFileSync(path.join(rulesDir, f), 'utf8').toLowerCase());
  }
  return map;
}

/**
 * Non-rule harness surfaces: AGENTS.md, .agents/, docs/, swarm/.
 *
 * Used only to separate "no rule mentions it" from "nobody wrote it down".
 * Matches are reported as corroboration, never as coverage.
 *
 * `docs/KNOWN_ERRORS.md` is EXCLUDED. It is the source of the terms, so letting it
 * match would make every uncovered term trivially "documented elsewhere" and pin
 * `harnessOnly` to true for all of them — a flag that is always on measures nothing.
 * That bug shipped once and the always-true output is what exposed it.
 */
function loadHarnessContext(root = PROJECT_ROOT) {
  const surfaces = new Map();
  const sourceRel = path
    .relative(root, KNOWN_ERRORS)
    .split(path.sep)
    .join('/')
    .toLowerCase();
  const add = (rel, text) => {
    if (rel.toLowerCase() === sourceRel) return;
    surfaces.set(rel, text.toLowerCase());
  };

  const agents = path.join(root, 'AGENTS.md');
  if (fs.existsSync(agents)) add('AGENTS.md', fs.readFileSync(agents, 'utf8'));

  const walk = (dir, rel, depth) => {
    if (depth > 4) return;
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const e of entries) {
      const full = path.join(dir, e.name);
      const relPath = `${rel}/${e.name}`;
      if (e.isDirectory()) {
        if (e.name === 'node_modules' || e.name === '.git') continue;
        walk(full, relPath, depth + 1);
      } else if (/\.(md|mdc)$/i.test(e.name)) {
        try {
          add(relPath, fs.readFileSync(full, 'utf8'));
        } catch {
          /* unreadable surface is not a finding */
        }
      }
    }
  };

  for (const d of ['.agents', 'swarm', 'Docs', 'docs']) {
    const full = path.join(root, d);
    if (fs.existsSync(full)) walk(full, d, 0);
  }
  // On Windows `Docs/` and `docs/` are one physical directory, so walking both roots
  // yields every doc twice — inflating `elsewhereCount` and halving nothing useful.
  // Dedupe by case-folded path, keeping the first casing seen.
  const deduped = new Map();
  for (const [rel, text] of surfaces) {
    const key = rel.toLowerCase();
    if (!deduped.has(key)) deduped.set(key, [rel, text]);
  }
  return new Map([...deduped.values()]);
}

/**
 * Which surfaces mention this term?
 *
 * Both the needle and the haystack are lowercased here rather than relying on
 * callers having done it. An implicit "pass me lowercase" contract is one that
 * silently returns "not mentioned" when violated, and a coverage tool that
 * under-reports is worse than no coverage tool — the gap it invents is fake.
 */
function mentions(term, ruleMap, harnessMap) {
  const t = String(term).toLowerCase();
  if (!t) return { inRules: [], elsewhere: [] };
  const inRules = [];
  const elsewhere = [];
  for (const [name, text] of ruleMap) if (String(text).toLowerCase().includes(t)) inRules.push(name);
  for (const [name, text] of harnessMap) if (String(text).toLowerCase().includes(t)) elsewhere.push(name);
  return { inRules, elsewhere };
}

/** Score one entry against the corpus. */
function scoreEntry(entry, ruleMap, harnessMap) {
  const terms = extractTerms(entry);
  if (terms.length === 0) {
    return { head: entry.head, status: 'UNEXTRACTABLE', termCount: 0, rules: [], elsewhere: [], missing: [] };
  }

  const rules = new Set();
  const elsewhere = new Set();
  const missing = [];
  for (const term of terms) {
    const hit = mentions(term, ruleMap, harnessMap);
    for (const r of hit.inRules) rules.add(r);
    for (const e of hit.elsewhere) elsewhere.add(e);
    if (hit.inRules.length === 0) missing.push(term);
  }

  const status = rules.size > 0 ? 'COVERED' : 'UNCOVERED';
  const elsewhereList = [...elsewhere].sort();
  return {
    head: entry.head,
    status,
    termCount: terms.length,
    rules: [...rules].sort(),
    // Corroboration only, and capped: harnessMap spans every doc in the repo, so an
    // uncapped list is one file name per matching term across hundreds of files and
    // made the JSON report exceed a megabyte. A count is the honest summary.
    elsewhere: elsewhereList.slice(0, 5),
    elsewhereCount: elsewhereList.length,
    missing: missing.sort(),
    // Knowledge exists somewhere but never became a rule. Different problem, smaller fix.
    // NOTE: `elsewhere` is a Set here, so this must use `.size` — `.length` is
    // `undefined` on a Set and would silently pin this flag to false forever.
    harnessOnly: rules.size === 0 && elsewhere.size > 0,
  };
}

function analyze(markdown, ruleMap, harnessMap) {
  return parseEntries(markdown).map((e) => scoreEntry(e, ruleMap, harnessMap));
}

function summarize(rows) {
  const byStatus = {};
  for (const r of rows) byStatus[r.status] = (byStatus[r.status] || 0) + 1;
  const covered = rows.filter((r) => r.status === 'COVERED');
  return {
    total: rows.length,
    byStatus,
    covered: covered.length,
    uncovered: rows.filter((r) => r.status === 'UNCOVERED').length,
    harnessOnly: rows.filter((r) => r.harnessOnly).length,
    extractable: rows.filter((r) => r.status !== 'UNEXTRACTABLE').length,
    coverageRate:
      rows.filter((r) => r.status !== 'UNEXTRACTABLE').length === 0
        ? null
        : covered.length / rows.filter((r) => r.status !== 'UNEXTRACTABLE').length,
  };
}

function renderMarkdown(rows, summary, ruleCount) {
  const pct = summary.coverageRate === null ? 'n/a' : (summary.coverageRate * 100).toFixed(1);
  const uncovered = rows.filter((r) => r.status === 'UNCOVERED');
  const lines = [];

  lines.push('# Harness coverage of recorded failures');
  lines.push('');
  lines.push('> **Generated file.** Regenerate with `npm run harness:coverage`.');
  lines.push('');
  lines.push('## What this measures');
  lines.push('');
  lines.push(
    '**Mention, not prevention.** For each recorded failure in `docs/KNOWN_ERRORS.md`, ' +
      'this asks whether any rule file contains a distinctive technical term from it. ' +
      'That is a ceiling on coverage, not a proof of prevention — a rule can mention the ' +
      'term and still miss the cause, or prevent the cause without the word.'
  );
  lines.push('');
  lines.push(
    'It is still worth running, because the failure it catches is silent: a defect class ' +
      'with no mention anywhere in the rules is one the harness cannot be pointing at.'
  );
  lines.push('');
  lines.push('## Result');
  lines.push('');
  lines.push(`- Recorded failures analyzed: **${summary.total}**`);
  lines.push(`- Extractable (prose-only entries excluded): **${summary.extractable}**`);
  lines.push(`- Covered by mention: **${summary.covered}** (${pct}%)`);
  lines.push(`- **Uncovered: ${summary.uncovered}**`);
  lines.push(`- Uncovered but documented elsewhere (knowledge exists, no rule): **${summary.harnessOnly}**`);
  lines.push(`- Rule files searched: **${ruleCount}**`);
  lines.push('');

  if (uncovered.length > 0) {
    lines.push('## Uncovered failures — candidate rule gaps');
    lines.push('');
    lines.push('| # | Recorded failure | Terms no rule mentions |');
    lines.push('|---|---|---|');
    uncovered.forEach((r, i) => {
      const miss = r.missing.slice(0, 6).map((m) => `\`${m}\``).join(', ');
      const more = r.missing.length > 6 ? `, +${r.missing.length - 6} more` : '';
      const head = r.head.replace(/\|/g, '\\|');
      lines.push(`| ${i + 1} | ${head} | ${miss}${more} |`);
    });
    lines.push('');
    lines.push(
      'These are **candidates**, not verdicts. Each needs a human read: some are genuine ' +
        'rule gaps, some are one-off environment faults that a rule should not encode.'
    );
    lines.push('');
  }

  lines.push('## How to read this as a ratchet');
  lines.push('');
  lines.push('- A new entry that is UNCOVERED is expected — the failure is new.');
  lines.push('- An entry that moves from COVERED to UNCOVERED is a regression. Nothing normally removes rule text, so investigate.');
  lines.push('- `harnessOnly` shrinking toward 0 means knowledge is being promoted into rules. That is the desired direction.');
  lines.push('');
  lines.push('_Source: `docs/KNOWN_ERRORS.md` against `.cursor/rules/*.mdc`._');
  lines.push('');
  return lines.join('\n');
}

function main(argv) {
  const asJson = argv.includes('--json');
  const strict = argv.includes('--strict');

  if (!fs.existsSync(KNOWN_ERRORS)) {
    process.stderr.write(`${PREFIX} ERROR — missing ${KNOWN_ERRORS}\n`);
    return 2;
  }

  const ruleMap = loadRules();
  const harnessMap = loadHarnessContext();
  const rows = analyze(fs.readFileSync(KNOWN_ERRORS, 'utf8'), ruleMap, harnessMap);
  const summary = summarize(rows);

  if (asJson) {
    process.stdout.write(
      `${JSON.stringify(
        {
          tool: PREFIX,
          note: 'Mention-based coverage. A ceiling on rule coverage, never a proof of prevention.',
          ruleCount: ruleMap.size,
          ...summary,
          failures: rows,
        },
        null,
        2
      )}\n`
    );
  } else {
    process.stdout.write(renderMarkdown(rows, summary, ruleMap.size));
  }

  // Ratchet mode: fail only on a regression, never merely because a gap exists.
  // A brand-new uncovered failure is the normal state of a young corpus.
  if (strict && summary.uncovered > 0) {
    process.stderr.write(
      `${PREFIX} ${summary.uncovered} uncovered failure(s) — see report. ` +
        'Advisory: new gaps are expected; investigate only regressions.\n'
    );
    return 1;
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
  parseEntries,
  extractTerms,
  loadRules,
  loadHarnessContext,
  mentions,
  scoreEntry,
  analyze,
  summarize,
  renderMarkdown,
  STOPWORDS,
};