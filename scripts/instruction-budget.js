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
 * WHAT IS ENFORCED HARD, AND WHY
 *
 * Three numbers are errors, not warnings, because all three are in context on
 * literally every request: the AGENTS.md line count (150 - OpenAI ships ~100
 * because theirs is a table of contents, not the manual), the total size of the
 * skill descriptions, and the MCP tool count. Everything else is a ratchet.
 *
 * The descriptions and the MCP surface were reported for a long time before they
 * were gated. Printing a number is not watching it: the MCP bucket in particular
 * reported "0 tool schemas" as a measurement for a session injecting 114, and a
 * zero nobody disputes is worse than no measurement at all.
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
 *
 * WHAT THIS GATE CANNOT SEE
 *
 * It counts lines. It cannot tell whether a line still points at something that
 * exists, and on 2026-10-12 twenty paths across the instruction corpus did not.
 * scripts/harness-paths.test.js is the other half of that job: this file measures
 * how much surface there is, that one measures whether any of it resolves.
 */

const ROOT = path.resolve(__dirname, '..');

/** OpenAI's shipped AGENTS.md is ~100 lines. Ceiling below that, per HumanLayer. */
const ALWAYS_ON_MAX = 150;

/**
 * Skill descriptions, in characters.
 *
 * These are the second always-on cost after AGENTS.md: every description is in
 * the context on every request whether or not the skill is ever used. The report
 * has always shown this number and the gate has always ignored it, which is the
 * same shape as the MCP bug this file was rewritten to fix - the expensive thing
 * is printed and nothing watches it.
 *
 * 3943 is the measured surface, not a target. It carries no headroom on
 * purpose: growing it should be a deliberate act, exactly like raising
 * TOTAL_HIGH_WATER. (First applied at 4007; lowering it to 3943 the same day
 * the ue57 tombstone stopped advertising the retired engine is the ratchet
 * doing its job in both directions.)
 */
const ADVERTISED_MAX = 3943;

/** Current measured total. Only ever lowers; raises are deliberate and reviewed. */
const TOTAL_HIGH_WATER = 3240;
/** The ratchet target from DEC-0035. Reaching it clears the warning. */
const TOTAL_LOW_WATER = 3000;

/**
 * MCP tool surface, from Config/mcp-tool-snapshot.json.
 *
 * This is the largest thing in context on every request and it used to be
 * reported as zero, because an MCP config declares a command and the tools only
 * appear after the server answers tools/list. Ratchet only, no low-water band:
 * a warning that fires while the surface sits at its measured value is noise,
 * and noise is what makes a gate stop being read.
 */
const MCP_TOOLS_HIGH_WATER = 114;

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

/**
 * Host configs that DECLARE servers.
 *
 * Only `live` configs are used for drift detection. `template` files describe a
 * server that MAY be set up on another host and are not proof that anything is
 * running; treating them as live produced a permanent warning about a Slate
 * inspector that this host never injects. A warning that cannot be cleared is
 * noise, and noise is how a gate stops being read.
 */
const MCP_HOST_CONFIGS = [
  { rel: 'opencode.json', key: 'mcp.servers', host: 'opencode', live: true },
  { rel: '.cursor/mcp.json.example', key: 'mcpServers', host: 'cursor', live: false },
];

function pick(obj, dotted) {
  return dotted.split('.').reduce((o, k) => (o && typeof o === 'object' ? o[k] : undefined), obj);
}

function declaredServerNames(root) {
  const names = [];
  const seen = new Set();
  for (const cfg of MCP_HOST_CONFIGS) {
    const file = path.join(root, cfg.rel);
    if (!fs.existsSync(file)) continue;
    let block;
    try {
      block = pick(JSON.parse(readText(file)), cfg.key);
    } catch {
      continue;
    }
    if (!block || typeof block !== 'object') continue;
    for (const name of Object.keys(block)) {
      if (seen.has(name)) continue;
      seen.add(name);
      names.push({ name, host: cfg.host, live: cfg.live });
    }
  }
  return names;
}

/**
 * The MCP surface, measured from a recorded snapshot rather than guessed.
 *
 * A snapshot is the only honest source: an MCP config declares a command, and
 * the tool schemas exist only after the server starts. Reading `server.tools`
 * out of the config returned a structural zero, and zero was reported as a
 * measurement - the largest always-on surface in the session, described as free.
 *
 * Missing snapshot => toolCount is null and measured is false. It is never
 * coerced back to 0, because "we did not measure it" and "it costs nothing" are
 * different claims and only one of them is true.
 */
function readMcpSurface(root) {
  const file = path.join(root, 'Config', 'mcp-tool-snapshot.json');
  const declared = declaredServerNames(root);
  if (!fs.existsSync(file)) {
    return {
      measured: false,
      toolCount: null,
      schemaBytes: null,
      snapshotServers: 0,
      capturedAt: null,
      declared: declared.map((d) => d.name),
      declaredTemplateOnly: declared.filter((d) => !d.live).map((d) => d.name),
      missingFromSnapshot: declared.filter((d) => d.live).map((d) => d.name),
      staleInSnapshot: [],
    };
  }

  let json;
  try {
    json = JSON.parse(readText(file));
  } catch {
    return {
      measured: false,
      toolCount: null,
      schemaBytes: null,
      snapshotServers: 0,
      capturedAt: null,
      declared: declared.map((d) => d.name),
      declaredTemplateOnly: declared.filter((d) => !d.live).map((d) => d.name),
      missingFromSnapshot: declared.filter((d) => d.live).map((d) => d.name),
      staleInSnapshot: [],
    };
  }

  const servers = json.servers && typeof json.servers === 'object' ? json.servers : {};
  const entries = Object.entries(servers);
  let toolCount = 0;
  const pending = [];
  for (const [name, v] of entries) {
    // `tools: null` means "declared, never counted" - an uncaptured surface. It is
    // reported as pending and contributes nothing, which is the one honest option:
    // inventing a number would be a false measurement, and counting it as zero
    // would be the exact bug this file exists to fix.
    if (!v || typeof v.tools !== 'number') {
      pending.push(name);
      continue;
    }
    toolCount += v.tools;
  }

  const snapshotted = new Set(entries.map(([name]) => name));
  const liveDeclared = declared.filter((d) => d.live);
  // Only a LIVE config can be missing. A template names a server that may not run
  // anywhere, so treating it as live produced a warning that could never be cleared.
  const missingFromSnapshot = liveDeclared.filter((d) => !snapshotted.has(d.name)).map((d) => d.name);
  const declaredTemplateOnly = declared
    .filter((d) => !d.live && !snapshotted.has(d.name))
    .map((d) => d.name);
  // A snapshot entry is stale only when NOTHING declares it. A template naming it is
  // enough to keep it alive, because the other host may still run it.
  const declaredNames = new Set(declared.map((d) => d.name));
  const staleInSnapshot = entries
    .filter(([name, v]) => v && v.source === 'repo' && !declaredNames.has(name))
    .map(([name]) => name);

  return {
    measured: true,
    toolCount,
    schemaBytes: typeof json.schemaBytes === 'number' ? json.schemaBytes : null,
    snapshotServers: entries.length,
    pending,
    capturedAt: typeof json.capturedAt === 'string' ? json.capturedAt : null,
    declared: declared.map((d) => d.name),
    declaredTemplateOnly,
    missingFromSnapshot,
    staleInSnapshot,
  };
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
  // Three buckets, by what actually reaches the model:
  //
  //   alwaysOn         AGENTS.md - in context on literally every request.
  //   advertised       every skill description - also on every request, used or
  //                    not. Reported long before it was gated.
  //   stored/reachable .cursor/rules (glob-scoped opt-in) plus the skill bodies.
  //                    Reachable on demand, so a ratchet, not a hard ceiling.
  //
  // `.cursor/skills` belongs in the stored bucket, not outside it. opencode.json
  // lists that tree under `skills`, so a loader does read it; excluding it meant
  // a second copy of the corpus could grow without the ratchet noticing.
  const agentsMd = path.join(root, 'AGENTS.md');
  const agentsText = readText(agentsMd);
  const alwaysOn = agentsText ? countText(agentsText) : 0;

  const rules = walk(path.join(root, '.cursor', 'rules'), [], (f) => f.endsWith('.mdc'));
  const skills = walk(path.join(root, '.agents'), [], (f) => f.endsWith('.md'));
  const cursorSkills = walk(path.join(root, '.cursor', 'skills'), [], (f) => f.endsWith('.md'));
  const extras = walk(path.join(root, '.agents', 'skills-extras'), [], (f) => f.endsWith('.md'));

  const rulesLines = rules.reduce((n, f) => n + countLines(f), 0);
  const skillsLines = skills.reduce((n, f) => n + countLines(f), 0);
  const cursorSkillsLines = cursorSkills.reduce((n, f) => n + countLines(f), 0);
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
    mcp: readMcpSurface(root),
    rules: { files: rules.length, lines: rulesLines },
    skills: { files: skills.length, lines: skillsLines },
    cursorSkills: { files: cursorSkills.length, lines: cursorSkillsLines },
    extras: { files: extras.length, lines: extrasLines },
    // Extras live under .agents/skills and are counted in both figures by design:
    // they are discoverable by a loader, so they are reachable context.
    total: rulesLines + skillsLines + cursorSkillsLines,
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
  if (m.advertised.chars > ADVERTISED_MAX) {
    errors.push(
      `skill descriptions total ${m.advertised.chars} chars, over the ${ADVERTISED_MAX} ` +
        `high-water mark. Every description is in context on every request whether the ` +
        `skill is used or not - shorten it, or delete the skill.`
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

  if (m.mcp.measured) {
    if (m.mcp.toolCount > MCP_TOOLS_HIGH_WATER) {
      errors.push(
        `MCP surface is ${m.mcp.toolCount} tool schemas, over the ${MCP_TOOLS_HIGH_WATER} ` +
          `high-water mark. Servers pay for every tool on every request - drop a server or narrow one.`
      );
    }
    if (m.mcp.pending.length > 0) {
      warnings.push(
        `MCP server(s) declared but never counted, so the surface is under-counted: ` +
          `${m.mcp.pending.join(', ')}. Set a tool count in Config/mcp-tool-snapshot.json.`
      );
    }
    if (m.mcp.missingFromSnapshot.length > 0) {
      warnings.push(
        `server(s) declared in a host config but absent from Config/mcp-tool-snapshot.json: ` +
          `${m.mcp.missingFromSnapshot.join(', ')}. Recapture, or the surface is under-counted.`
      );
    }
    if (m.mcp.staleInSnapshot.length > 0) {
      warnings.push(
        `snapshot server(s) no longer declared by any host config: ` +
          `${m.mcp.staleInSnapshot.join(', ')}. Recapture, or the surface is over-counted.`
      );
    }
  } else {
    warnings.push(
      'no usable MCP tool snapshot (Config/mcp-tool-snapshot.json). The MCP surface is the ' +
        'largest thing loaded per request and is currently UNMEASURED, not zero. Recapture it.'
    );
  }

  return { errors, warnings };
}

if (require.main === module) {
  const m = measure();
  const { errors, warnings } = evaluate(m);
  const out = {
    measured: m,
    limits: { ALWAYS_ON_MAX, ADVERTISED_MAX, MCP_TOOLS_HIGH_WATER, TOTAL_HIGH_WATER, TOTAL_LOW_WATER },
    errors,
    warnings,
  };
  if (process.argv.includes('--json')) {
    process.stdout.write(JSON.stringify(out, null, 2) + '\n');
  } else {
    const broad = m.advertised.broad.map((e) => `${e.tree}/${e.name}`).join(', ') || 'none';
    const dupBodies = m.duplicates.bodies.join(', ') || 'none';
    const mcpTools = m.mcp.toolCount === null ? 'UNMEASURED' : `${m.mcp.toolCount} tool schemas`;
    const mcpBytes = m.mcp.schemaBytes === null ? 'bytes not captured' : `${m.mcp.schemaBytes} schema bytes`;
    const mcpWhen = m.mcp.capturedAt ? `snapshot ${m.mcp.capturedAt}` : 'no snapshot';
    const mcpPending = m.mcp.pending.length > 0 ? `; UNCOUNTED ${m.mcp.pending.join(', ')}` : '';
    const mcpTemplate = m.mcp.declaredTemplateOnly.length > 0 ? `; template-only ${m.mcp.declaredTemplateOnly.join(', ')}` : '';

    process.stdout.write('instruction budget\n');
    process.stdout.write('  LOADED EVERY REQUEST\n');
    process.stdout.write(`    AGENTS.md            ${m.alwaysOn} lines, ${m.alwaysOnChars} chars   (ceiling ${ALWAYS_ON_MAX})\n`);
    process.stdout.write(`    skill descriptions   ${m.advertised.chars} chars in ${m.advertised.count} skills   (high-water ${ADVERTISED_MAX})\n`);
    process.stdout.write(`    mcp tool surface     ${m.mcp.snapshotServers} servers, ${mcpTools}, ${mcpBytes} (${mcpWhen}${mcpPending}${mcpTemplate})\n`);
    process.stdout.write('  REACHED ON DEMAND - a ratchet, not a ceiling\n');
    process.stdout.write(`    .cursor/rules        ${m.rules.lines} lines in ${m.rules.files} files\n`);
    process.stdout.write(`    .agents/skills       ${m.skills.lines} lines in ${m.skills.files} files\n`);
    process.stdout.write(`    .cursor/skills       ${m.cursorSkills.lines} lines in ${m.cursorSkills.files} files\n`);
    process.stdout.write(`    reachable total      ${m.total} lines   (high-water ${TOTAL_HIGH_WATER}, target ${TOTAL_LOW_WATER})\n`);
    process.stdout.write('  QUALITY\n');
    process.stdout.write(`    broad descriptions   ${broad}\n`);
    process.stdout.write(`    duplicate bodies     ${dupBodies}\n`);
    for (const w of warnings) process.stdout.write(`  warn  ${w}\n`);
    for (const e of errors) process.stdout.write(`  ERROR ${e}\n`);
  }
  process.exit(errors.length ? 1 : 0);
}

module.exports = {
  measure,
  evaluate,
  countText,
  readMcpSurface,
  ALWAYS_ON_MAX,
  ADVERTISED_MAX,
  TOTAL_HIGH_WATER,
  TOTAL_LOW_WATER,
  MCP_TOOLS_HIGH_WATER,
};