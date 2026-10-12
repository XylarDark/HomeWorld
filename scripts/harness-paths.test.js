const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');

/**
 * Harness path gate.
 *
 * WHY THIS EXISTS
 *
 * The instruction budget counts the lines in AGENTS.md, .cursor/rules and the
 * skill corpus. It cannot see whether any of those lines still point at
 * something that exists. On 2026-10-12 a scan of 38 harness files found 11
 * repository paths that no longer resolve - including a rule that still told the
 * agent to run `Content/Python/gui_automation`, a directory deleted in WAVE F,
 * and three PCG docs that had moved into docs/PCG/.
 *
 * Those are worse than no instruction at all. A missing instruction is simply
 * not followed; a confident pointer to a deleted script is followed into a
 * failure, and the failure reads as the agent's fault rather than the doc's.
 * test_canon_map.py guards path resolution for the CANON_MAP lookup table and
 * for nothing else, so the harness corpus had no equivalent protection.
 *
 * WHAT COUNTS AS A PATH
 *
 * Two forms, because both are in use across the corpus:
 *   1. repo-rooted,  `docs/PCG/PCG_SETUP.md`
 *   2. relative markdown links, `[setup](../../../docs/PCG/PCG_SETUP.md)`
 *
 * WHAT IS DELIBERATELY LENIENT
 *
 * Three things, each of which would otherwise produce noise the next author
 * learns to route around:
 *
 *   - Prefix fragments such as `docs/UE/UE57_*` or `Content/Python/tests/test_`
 *     resolve when the parent directory holds an entry starting with the same
 *     stem. They are glob stems, not paths; failing on them teaches vagueness
 *     rather than repair.
 *   - Links resolve FILE-RELATIVE or REPO-ROOT-RELATIVE, whichever exists. The
 *     corpus mixes both conventions and docs/AGENTS_REFERENCE.md in particular
 *     writes `.cursor/rules/...` from inside docs/. Picking one convention would
 *     flag half the file for style, not for breakage.
 *   - `Saved/` is not scanned. It is gitignored editor scratch: references to it
 *     are not durable and would fail on any clean clone.
 */

const ROOT = path.resolve(__dirname, '..');

/** Directories whose contents are the always-on or on-demand instruction surface. */
const SCAN_ROOTS = [
  'AGENTS.md',
  'docs/AGENTS_REFERENCE.md',
  '.cursor/rules',
  '.agents/skills',
  '.cursor/skills',
];

/** Repo-rooted path stems. Kept short on purpose: a bare prefix would match prose. */
const REPO_STEM =
  '(?:Content|Source|Docs|docs|Config|Lib|Scripts|scripts|Tools|tools|swarm|UserHarness|\\.cursor|\\.agents|\\.planning)\\/[A-Za-z0-9_.\\-/\\\\]+';

const PATH_RE = new RegExp(`(?:^|[\\s(\\[\`'">])(${REPO_STEM})`, 'g');
const MD_LINK_RE = /\[[^\]]*\]\(([^)\s]+)\)/g;

/**
 * Opt-out for a line that names a dead path DELIBERATELY, e.g. "the
 * `Content/Python/gui_automation/` directory was removed WAVE F, do not cite it."
 *
 * It is line-scoped and it must carry a reason, because the failure mode of an
 * unguarded allowlist is that the next red build gets silenced instead of fixed.
 */
const EXCEPTION_RE = /<!--\s*path-exception:\s*(.+?)\s*-->/;

/** Characters that mark a token as a pattern or a placeholder rather than a path. */
const IS_PATTERN = /[<>*{}?|]/;

/**
 * `Docs/NN engineering` and friends: a doc-number placeholder, not a filename.
 * Failing on these would push the author toward a vaguer placeholder.
 */
const IS_PLACEHOLDER_STEM = /^[A-Z]{2,3}$/;

const EXTENSIONS = ['.md', '.mdc', '.js', '.ts', '.py', '.json', '.ps1', '.uasset', '.umap', '.fbx', '.txt', '.yaml', '.yml'];

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  if (fs.statSync(dir).isFile()) return [...out, dir];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else out.push(full);
  }
  return out;
}

function scanFiles() {
  return SCAN_ROOTS.flatMap((rel) => walk(path.join(ROOT, rel)));
}

function normalize(candidate) {
  return candidate.replace(/\\/g, '/').replace(/[.,;:)+]+$/, '').replace(/\/$/, '');
}

/**
 * A candidate resolves if it exists as written, exists with a conventional
 * extension, or shares a stem with a real entry in an existing directory.
 * The stem case is what keeps `docs/UE/UE57_*` from failing while
 * `docs/PCG_BEST_PRACTICES.md` (whose real home is docs/PCG/) still does.
 */
function resolves(candidate) {
  const abs = path.join(ROOT, candidate);
  if (fs.existsSync(abs)) return true;
  if (EXTENSIONS.some((ext) => fs.existsSync(abs + ext))) return true;

  const parent = path.dirname(abs);
  if (!fs.existsSync(parent) || !fs.statSync(parent).isDirectory()) return false;
  const stem = path.basename(candidate).toLowerCase();
  return fs
    .readdirSync(parent)
    .some((entry) => entry.toLowerCase().startsWith(stem));
}

function deadReferences() {
  const dead = [];
  for (const file of scanFiles()) {
    const rel = path.relative(ROOT, file).replace(/\\/g, '/');
    const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);

    lines.forEach((line, i) => {
      const found = [];

      // Link LABELS are prose, not paths: `[docs/PCG_SETUP.md](../../docs/PCG/PCG_SETUP.md)`
      // names a correct href under a stale caption, and flagging the caption would be
      // a style complaint reported as a breakage. Blank the labels out, then scan what
      // is left for repo-rooted paths.
      const bare = line.replace(/\[[^\]]*\]\(/g, '[](');
      PATH_RE.lastIndex = 0;
      for (let m = PATH_RE.exec(bare); m; m = PATH_RE.exec(bare)) found.push(m[1]);
      for (const m of line.matchAll(MD_LINK_RE)) found.push(m[1]);

      for (const raw of found) {
        if (IS_PATTERN.test(raw) || raw.startsWith('http')) continue;
        const target = normalize(raw.split('#')[0]);
        // Only repository paths. `./thing`, a bare `#anchor` and bare filenames are out of scope.
        if (!target || !target.includes('/')) continue;
        const stem = path.posix.basename(target);
        if (IS_PLACEHOLDER_STEM.test(stem)) continue;

        // The corpus mixes both conventions, so a reference is good if EITHER reading resolves.
        const fileRelative = normalize(path.posix.join(path.posix.dirname(rel), target));
        if (resolves(target) || resolves(fileRelative)) continue;
        dead.push({ file: rel, line: i + 1, ref: raw });
      }

      // A deliberate citation of a deleted path must still carry its reason.
      if (EXCEPTION_RE.test(line)) {
        const idx = dead.findIndex((d) => d.file === rel && d.line === i + 1);
        if (idx >= 0) dead.splice(idx, 1);
      }
    });
  }
  return dead;
}

test('every repository path named in the instruction corpus still resolves', () => {
  const dead = deadReferences();
  if (dead.length > 0) {
    const detail = dead.map((d) => `  ${d.file}:${d.line}  ->  ${d.ref}`).join('\n');
    assert.fail(
      `${dead.length} reference(s) point at paths that do not exist.\n` +
        `${detail}\n` +
        `Fix the reference or restore the file. Do not weaken this test: a confident ` +
        `pointer to a missing path is followed into a failure that reads as the agent's fault.`
    );
  }
  // A gate that scanned nothing would pass forever. Floor is the current corpus.
  const scanned = scanFiles().length;
  assert.ok(scanned >= 30, `only ${scanned} instruction files were scanned - the walk is broken`);
});

test('the gate actually fails on a dead reference', () => {
  // Mutation guard. A resolver that returned true for everything would keep this
  // file green while the corpus rotted, which is the state it was written to end.
  assert.strictEqual(resolves('docs/PCG/PCG_SETUP.md'), true, 'a real path must resolve');
  assert.strictEqual(resolves('docs/PCG_BEST_PRACTICES.md'), false, 'a moved doc must not');
  assert.strictEqual(resolves('Content/Python/gui_automation'), false, 'a deleted dir must not');
  // Lenient on glob stems, strict on real paths.
  assert.strictEqual(resolves('docs/UE/UE57_'), true, 'a glob stem with a real sibling must resolve');
  assert.strictEqual(resolves('Content/Python/tests/test_'), true, 'a test-name stem must resolve');
});

test('the gate accepts both link conventions and real placeholders', () => {
  // docs/AGENTS_REFERENCE.md writes `[docs/human-use/OWNERSHIP.md](human-use/OWNERSHIP.md)`:
  // the link is file-relative while the label is repo-rooted. Both are valid in this
  // corpus, and flagging the file-relative half would be a style failure dressed as
  // a breakage.
  const refs = new Set(deadReferences().map((d) => `${d.file}:${d.line}:${d.ref}`));
  for (const known of [
    'docs/AGENTS_REFERENCE.md:32:human-use/OWNERSHIP.md',
    '.agents/skills/swarm-mode-routing/SKILL.md:8:Docs/NN',
  ]) {
    assert.ok(!refs.has(known), `${known} must not be reported - it resolves or is a placeholder`);
  }
});

module.exports = { deadReferences, resolves, scanFiles };
