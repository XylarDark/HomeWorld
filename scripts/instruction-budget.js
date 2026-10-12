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
function countText(text) {
  return text.split(/\r?\n/).filter((l) => l.trim() !== '').length;
}

function countLines(file) {
  try {
    return countText(fs.readFileSync(file, 'utf8'));
  } catch {
    return 0;
  }
}

/** Descriptions that would match a routine edit, so the body is not really deferred. */
const BROAD_DESCRIPTION = /any coding task|every task/i;

function readText(file) {
  try {
    return fs.readFileSync(file, 'utf8');
  } catch {
    return '';
  }
}

/**
 * The first `---` pair is front matter. Later `---` lines are table rules or
 * horizontal rules and must stay in the body. Eating every delimiter is the bug
 * that reported 0 lines for a file that was mostly a table.
 */
function splitFrontMatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!m) return { front: '', body: text };
  return { front: m[1], body: text.slice(m[0].length) };
}

function parseDescription(front) {
  const lines = front.split(/\r?\n/);
  const start = lines.findIndex((l) => /^description:/.test(l));
  if (start < 0) return '';
  const first = lines[start].replace(/^description:\s*/, '').trim();
  const folded = first === '>-' || first === '>' || first === '|' || first === '|-';
  if (!folded && first) return first.replace(/^["']|["']$/g, '');
  const parts = [];
  for (let i = start + 1; i < lines.length; i++) {
    if (/^\S/.test(lines[i])) break;
    parts.push(lines[i].trim());
  }
  return parts.join(' ').replace(/\s+/g, ' ').trim();
}

function skillFiles(root, tree) {
  return walk(path.join(root, tree, 'skills'), [], (f) => f.endsWith('SKILL.md'));
}

function skillName(file) {
  return path.basename(path.dirname(file));
}

function isPointer(text) {
  const { body } = splitFrontMatter(text);
  const lines = body.split(/\r?\n/).filter((l) => l.trim() !== '');
  if (lines.length > 12) return false;
  return /second copy|Read that file|\.cursor\/skills\/|\.agents\/skills\//.test(body);
}

function collectAdvertised(root) {
  const entries = [];
  for (const tree of ['.agents', '.cursor']) {
    for (const file of skillFiles(root, tree)) {
      const description = parseDescription(splitFrontMatter(readText(file)).front);
      if (!description) continue;
      entries.push({ tree, name: skillName(file), description });
    }
  }
  const broad = entries.filter((e) => BROAD_DESCRIPTION.test(e.description));
  const chars = entries.reduce((n, e) => n + e.description.length, 0);
  return { chars, count: entries.length, broad, entries };
}

function collectDuplicates(root) {
  const byTree = {};
  for (const tree of ['.agents', '.cursor']) {
    byTree[tree] = new Map();
    for (const file of skillFiles(root, tree)) {
      byTree[tree].set(skillName(file), readText(file));
    }
  }
  const bodies = [];
  const pointers = [];
  for (const name of byTree['.agents'].keys()) {
    if (!byTree['.cursor'].has(name)) continue;
    const agentText = byTree['.agents'].get(name);
    const cursorText = byTree['.cursor'].get(name);
    if (isPointer(agentText) || isPointer(cursorText)) pointers.push(name);
    else bodies.push(name);
  }
  bodies.sort();
  pointers.sort();
  return { bodies, pointers };
}

function readMcpManifest(root) {
  const note = 'manifest estimate, not a live Cursor injection';
  const file = path.join(root, '.cursor', 'mcp.json.example');
  if (!fs.existsSync(file)) {
    return { servers: 0, tools: 0, schemaBytes: 0, measured: false, note };
  }
  const text = readText(file);
  let servers = 0;
  let tools = 0;
  let measured = true;
  try {
    const json = JSON.parse(text);
    const block = json.mcpServers && typeof json.mcpServers === 'object' ? json.mcpServers : {};
    servers = Object.keys(block).length;
    for (const server of Object.values(block)) {
      if (server && Array.isArray(server.tools)) tools += server.tools.length;
    }
  } catch {
    measured = false;
  }
  return { servers, tools, schemaBytes: Buffer.byteLength(text), measured, note };
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

function measure(root = ROOT) {
  // Always-on: the root AGENTS.md. The .cursor/rules corpus is glob-scoped and was
  // deliberately made opt-in during the P4 trim, so it is not always-on context.
  // The extra buckets below are a split of what is loaded versus what is stored.
  // They are not a second score: evaluate() still gates only alwaysOn and total.
  const agentsMd = path.join(root, 'AGENTS.md');
  const agentsText = readText(agentsMd);
  const alwaysOn = agentsText ? countText(agentsText) : 0;

  const rules = walk(path.join(root, '.cursor', 'rules'), [], (f) => f.endsWith('.mdc'));
  const skills = walk(path.join(root, '.agents'), [], (f) => f.endsWith('.md'));
  const extras = walk(path.join(root, '.agents', 'skills-extras'), [], (f) => f.endsWith('.md'));

  const rulesLines = rules.reduce((n, f) => n + countLines(f), 0);
  const skillsLines = skills.reduce((n, f) => n + countLines(f), 0);
  const extrasLines = extras.reduce((n, f) => n + countLines(f), 0);
  const skillBodyFiles = [
    ...skillFiles(root, '.agents'),
    ...skillFiles(root, '.cursor'),
  ];
  const skillBodyLines = skillBodyFiles.reduce((n, f) => n + countLines(f), 0);

  return {
    alwaysOn,
    alwaysOnChars: agentsText.length,
    alwaysOnFiles: ['AGENTS.md'],
    advertised: collectAdvertised(root),
    duplicates: collectDuplicates(root),
    onDemand: { label: 'not per-turn', rulesLines, skillBodyLines },
    mcp: readMcpManifest(root),
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
    const broad = m.advertised.broad.map((e) => `${e.tree}/${e.name}`).join(', ') || 'none';
    const dupBodies = m.duplicates.bodies.join(', ') || 'none';
    process.stdout.write('instruction budget\n');
    process.stdout.write(`  always-on (AGENTS.md)   ${m.alwaysOn} lines, ${m.alwaysOnChars} chars   (ceiling ${ALWAYS_ON_MAX})\n`);
    process.stdout.write(`  always-advertised       ${m.advertised.chars} chars in ${m.advertised.count} skill descriptions\n`);
    process.stdout.write(`  broad descriptions      ${broad}\n`);
    process.stdout.write(`  duplicate bodies        ${dupBodies}\n`);
    process.stdout.write(`  on demand (${m.onDemand.label})  rules ${m.onDemand.rulesLines} lines; skill bodies ${m.onDemand.skillBodyLines} lines\n`);
    process.stdout.write(
      `  mcp manifest estimate   ${m.mcp.servers} servers, ${m.mcp.tools} tool schemas, ${m.mcp.schemaBytes} bytes (${m.mcp.note})\n`
    );
    process.stdout.write(`  .cursor/rules           ${m.rules.lines} lines in ${m.rules.files} files\n`);
    process.stdout.write(`  .agents/skills          ${m.skills.lines} lines in ${m.skills.files} files\n`);
    process.stdout.write(`  TOTAL                   ${m.total} lines   (high-water ${TOTAL_HIGH_WATER}, target ${TOTAL_LOW_WATER})\n`);
    for (const w of warnings) process.stdout.write(`  warn  ${w}\n`);
    for (const e of errors) process.stdout.write(`  ERROR ${e}\n`);
  }
  process.exit(errors.length ? 1 : 0);
}

module.exports = {
  measure,
  evaluate,
  countText,
  ALWAYS_ON_MAX,
  TOTAL_HIGH_WATER,
  TOTAL_LOW_WATER,
};