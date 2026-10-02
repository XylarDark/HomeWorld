const fs = require('fs');
const path = require('path');

/**
 * Instruction-budget gate.
 *
 * WHY THIS EXISTS
 *
 * DEC-0035 measured the agent instruction surface at 3,254 lines against a
 * published consensus ceiling under 300. Phrasing it as a document would not have
 * survived three commits, because the failure mode is *growth* and nobody grows a
 * document on purpose. This makes the budget mechanical.
 *
 * WHY THE TARGET IS NOT "HIT 300 LINES"
 *
 * Dan Luu (160 runs per condition, Sept 2026) found that Default - NO instructions
 * at all - scored above average, and that large third-party instruction skills
 * UNDERPERFORMED while costing 26-41% more. Instruction-following also decays
 * uniformly with count, not just at the tail. So the target is not an exact
 * number to hit; it is *stop adding, and shrink*. A hard 300-line gate would be
 * theatre - it would fail every run, get ignored, and manufacture the false
 * impression that something is being watched.
 *
 * THE ONE HARD LIMIT
 *
 * The always-on surface has a real ceiling and it IS enforced hard, because that
 * file is in context on literally every request. OpenAI ships a ~100-line
 * AGENTS.md because it is a table of contents, not the manual. 150 is generous.
 *
 * THE RATCHET
 *
 * The total is a high-water mark that only ever lowers, with a separate low-water
 * target that silences the warning once reached. Raising the high-water mark is a
 * deliberate, reviewed act recorded in AGENT_DECISIONS.md - not a number to edit
 * when a check goes red.
 *
 * SCOPE, AND WHAT IS DELIBERATELY EXCLUDED
 *
 * `docs/` is NOT counted. It is the system of record and is read on demand, which
 * is exactly the shape OpenAI's harness-engineering writeup converged on: a short
 * AGENTS.md as an index, detail in docs/, invariants enforced by linters rather
 * than prose. Counting docs/ would penalise the correct shape.
 *
 * `.agents/skills-extras/` is included in the total, because a skill is
 * discoverable by a loader and can still be pulled into context.
 *
 * Counting BLANK and front-matter-only lines. The published figures describe
 * instruction prose, and counting every newline would inflate the number by
 * exactly the amount that makes the gate feel arbitrary.
 */

const ROOT = path.resolve(__dirname, '..');

/** OpenAI's shipped AGENTS.md is ~100 lines. Ceiling below that, per HumanLayer. */
const ALWAYS_ON_MAX = 150;

/** Current measured total. Only ever lowers; raises are deliberate and reviewed. */
const TOTAL_HIGH_WATER = 3240;
/** The ratchet target from DEC-0035. Reaching it clears the warning. */
const TOTAL_LOW_WATER = 3000;

/**
 * Instruction lines only: blank lines are skipped.
 *
 * Front matter is NOT skipped. These files are markdown with a YAML header
 * delimited by `---`, but `---` also appears as a horizontal rule and as a table
 * separator, so treating every delimiter as front matter silently ate the whole
 * corpus - it reported 8 lines for a 176-line AGENTS.md and 0 for all 25 rules.
 * A gate that cannot count is worse than no gate, so front matter is counted and
 * only blank lines are dropped.
 */
function countLines(file) {
  try {
    return fs.readFileSync(file, 'utf8')
      .split(/\r?\n/)
      .filter((l) => l.trim() !== '').length;
  } catch {
    return 0;
  }
}

function walk(dir, out = [], filter = () => true) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out, filter);
    else if (filter(full)) out.push(full);
  }
  return out;
}

function measure() {
  // Always-on: the root AGENTS.md. The .cursor/rules corpus is glob-scoped and was
  // deliberately made opt-in during the P4 trim, so it is not always-on context.
  const agentsMd = path.join(ROOT, 'AGENTS.md');
  const alwaysOn = fs.existsSync(agentsMd) ? countLines(agentsMd) : 0;

  const rules = walk(path.join(ROOT, '.cursor', 'rules'), [], (f) => f.endsWith('.mdc'));
  const skills = walk(path.join(ROOT, '.agents'), [], (f) => f.endsWith('.md'));
  const extras = walk(path.join(ROOT, '.agents', 'skills-extras'), [], (f) => f.endsWith('.md'));

  const rulesLines = rules.reduce((n, f) => n + countLines(f), 0);
  const skillsLines = skills.reduce((n, f) => n + countLines(f), 0);
  const extrasLines = extras.reduce((n, f) => n + countLines(f), 0);

  return {
    alwaysOn,
    alwaysOnFiles: ['AGENTS.md'],
    rules: { files: rules.length, lines: rulesLines },
    skills: { files: skills.length, lines: skillsLines },
    extras: { files: extras.length, lines: extrasLines },
    // Extras live under .agents/skills and are counted in both figures by design:
    // they are discoverable by a loader, so they are reachable context.
    total: rulesLines + skillsLines,
  };
}

function evaluate(m) {
  const errors = [];
  const warnings = [];

  if (m.alwaysOn > ALWAYS_ON_MAX) {
    errors.push(
      `always-on surface is ${m.alwaysOn} lines, over the ${ALWAYS_ON_MAX} ceiling. ` +
        `AGENTS.md is in context on every request; cut or move detail to docs/.`
    );
  }
  if (m.total > TOTAL_HIGH_WATER) {
    errors.push(
      `total instruction surface is ${m.total} lines, over the ${TOTAL_HIGH_WATER} high-water mark. ` +
        `The budget is a ratchet, not a target - it only goes down.`
    );
  } else if (m.total > TOTAL_LOW_WATER) {
    warnings.push(
      `total instruction surface is ${m.total} lines, trending down from ${TOTAL_HIGH_WATER} ` +
        `toward the ${TOTAL_LOW_WATER} target (DEC-0035). Shrink toward it.`
    );
  }
  return { errors, warnings };
}

if (require.main === module) {
  const m = measure();
  const { errors, warnings } = evaluate(m);
  const out = { measured: m, limits: { ALWAYS_ON_MAX, TOTAL_HIGH_WATER, TOTAL_LOW_WATER }, errors, warnings };
  if (process.argv.includes('--json')) {
    process.stdout.write(JSON.stringify(out, null, 2) + '\n');
  } else {
    process.stdout.write('instruction budget\n');
    process.stdout.write(`  always-on (AGENTS.md)   ${m.alwaysOn} lines   (ceiling ${ALWAYS_ON_MAX})\n`);
    process.stdout.write(`  .cursor/rules           ${m.rules.lines} lines in ${m.rules.files} files\n`);
    process.stdout.write(`  .agents/skills          ${m.skills.lines} lines in ${m.skills.files} files\n`);
    process.stdout.write(`  TOTAL                   ${m.total} lines   (high-water ${TOTAL_HIGH_WATER}, target ${TOTAL_LOW_WATER})\n`);
    for (const w of warnings) process.stdout.write(`  warn  ${w}\n`);
    for (const e of errors) process.stdout.write(`  ERROR ${e}\n`);
  }
  process.exit(errors.length ? 1 : 0);
}

module.exports = { measure, evaluate, ALWAYS_ON_MAX, TOTAL_HIGH_WATER, TOTAL_LOW_WATER };