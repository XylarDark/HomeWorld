#!/usr/bin/env node
/**
 * Cyclomatic complexity gate.
 *
 * WHY THIS EXISTS
 *
 * The Week 1 - Agentic Engineering material says it plainly: **"do not let it build
 * junior-level code"**, and names the offenders - if/else, ternary operators, switch
 * and case blocks, loops, and `&&` / `||`. It also says to **"assess objective metrics
 * versus reading code as often as possible"**, and that cyclomatic complexity
 * "quantifies the number of linearly independent paths through a program's source code".
 *
 * That is a linter rule, and HumanLayer's line applies exactly: **"Claude is not a
 * linter."** Style and complexity rules belong in a deterministic tool, not in prompt
 * text that decays as the corpus grows. DEC-0034 deleted `score-mdc-rules.js` for
 * scoring rule TEXT; this is the replacement that scores behaviour-bearing code
 * instead, and it is the first of the rule-to-linter conversions listed in
 * HARNESS_BRIDGE_TASKS.md P2.3.
 *
 * MCCABE, NOT COGNITIVE COMPLEXITY
 *
 * The source material notes cyclomatic complexity "does not measure cognitive
 * complexity". This implements McCabe as documented: 1 + the number of decision
 * points. It is a crude metric with known blind spots - it cannot see that one
 * function with complexity 4 is trivial and another with complexity 4 is
 * unreadable. It is used here as a *tripwire that prompts a look*, not as a
 * quality score, and the output says so.
 *
 * WHAT IS AND IS NOT MEASURED
 *
 * JS only. C++ needs a build-integrated analyser; hand-rolling one for C++ in JS
 * would be worse than useless, because it would look authoritative and be wrong.
 * The C++ gap is recorded rather than faked.
 *
 * Comment and string contents are stripped before counting, so a `&&` inside a
 * comment does not inflate a function's score. Getting that wrong is the classic way
 * a complexity checker becomes noise, and a noisy gate gets ignored.
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');

/**
 * Two thresholds, because one would be useless.
 *
 * JUNIOR_CEILING is the source material's own standard: "do not let it build
 * junior-level code". Exceeding it means look at it. It only WARNS - 13 functions
 * currently exceed it, and a gate that fails 13 times on first run is a gate that
 * gets ignored within a week.
 *
 * HIGH_WATER is a ratchet at the current worst offender (evaluateCheck, 45). A new
 * function above it FAILS. Existing debt is grandfathered and can only shrink.
 *
 * This is the same shape as the instruction-budget gate, and for the same reason:
 * hard-failing on legacy debt produces a permanently red gate, and a permanently
 * red gate is worse than none because it stops being read.
 */
const JUNIOR_CEILING = 12;
const DEFAULT_MAX = 45;

/** Decision points that each add one path. */
const DECISION_POINTS = [
  { re: /\bif\b/g, label: 'if' },
  { re: /\bfor\b/g, label: 'for' },
  { re: /\bwhile\b/g, label: 'while' },
  { re: /\bcase\b/g, label: 'case' },
  { re: /\bcatch\b/g, label: 'catch' },
  { re: /\?\s*[^:]{0,120}:/g, label: 'ternary' },
  { re: /&&/g, label: '&&' },
  { re: /\|\|/g, label: '||' },
  { re: /\?\./g, label: '?.' },
  { re: /\?\?/g, label: '??' },
];

/** `else`, `else if` and `default` are counted by their `if`/`case`, not again. */
const EXCLUDE = [/\belse\b/g];

/**
 * Strip comments and string/template literals.
 *
 * Without this a `&&` inside a doc comment scores the function, and a comment
 * explaining WHY something is complex is exactly where you will find `&&`.
 */
function stripCommentsAndStrings(src) {
  let out = '';
  let i = 0;
  const n = src.length;
  while (i < n) {
    const c = src[i];
    const two = src.slice(i, i + 2);
    if (two === '//') {
      while (i < n && src[i] !== '\n') i++;
      continue;
    }
    if (two === '/*') {
      i += 2;
      while (i < n && src.slice(i, i + 2) !== '*/') i++;
      i += 2;
      continue;
    }
    if (c === '"' || c === "'" || c === '`') {
      const quote = c;
      i++;
      while (i < n) {
        if (src[i] === '\\') {
          i += 2;
          continue;
        }
        if (src[i] === quote) {
          i++;
          break;
        }
        i++;
      }
      out += ' ';
      continue;
    }
    out += c;
    i++;
  }
  return out;
}

/** Split top-level functions well enough to score them individually. */
function findFunctions(src) {
  const fns = [];
  const re = /(?:^|\n)\s*(?:async\s+)?function\s+([A-Za-z0-9_$]+)\s*\(|=>\s*(?:\(|async\s*\()/g;
  // Simpler and more robust: brace-match from each candidate start.
  const candidates = [];
  const declRe = /(?:^|\n)\s*(?:async\s+)?function\s+([A-Za-z0-9_$]+)\s*\(/g;
  let m;
  while ((m = declRe.exec(src)) !== null) {
    candidates.push({ name: m[1], start: m.index });
  }
  const arrowRe = /(?:^|\n)\s*(?:const|let|var)\s+([A-Za-z0-9_$]+)\s*=\s*(?:async\s*)?\(/g;
  while ((m = arrowRe.exec(src)) !== null) {
    candidates.push({ name: m[1], start: m.index });
  }

  for (const c of candidates) {
    const open = src.indexOf('{', c.start);
    if (open === -1) continue;
    let depth = 0;
    let end = open;
    for (let i = open; i < src.length; i++) {
      if (src[i] === '{') depth++;
      else if (src[i] === '}') {
        depth--;
        if (depth === 0) {
          end = i;
          break;
        }
      }
    }
    fns.push({ name: c.name, start: c.start, end, body: src.slice(c.start, end + 1) });
  }
  return fns;
}

function complexityOf(body) {
  const code = stripCommentsAndStrings(body);
  let score = 1;
  const drivers = [];
  for (const d of DECISION_POINTS) {
    const hits = (code.match(d.re) || []).length;
    if (hits > 0) {
      score += hits;
      drivers.push(`${d.label}x${hits}`);
    }
  }
  return { score, drivers };
}

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name.startsWith('.')) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else if (entry.name.endsWith('.js') && !entry.name.endsWith('.test.js')) out.push(full);
  }
  return out;
}

function measure(max = DEFAULT_MAX) {
  const files = walk(path.join(ROOT, 'scripts'));
  const functions = [];
  for (const f of files) {
    let src;
    try {
      src = fs.readFileSync(f, 'utf8');
    } catch {
      continue;
    }
    for (const fn of findFunctions(src)) {
      const { score, drivers } = complexityOf(fn.body);
      functions.push({
        file: path.relative(ROOT, f).replace(/\\/g, '/'),
        name: fn.name,
        score,
        drivers,
        over: score > max,
      });
    }
  }
  functions.sort((a, b) => b.score - a.score);
  return { max, files: files.length, functions };
}

if (require.main === module) {
  const argv = process.argv.slice(2);
  const i = argv.indexOf('--max');
  const max = i !== -1 && argv[i + 1] ? parseInt(argv[i + 1], 10) : DEFAULT_MAX;
  const m = measure(max);
  const over = m.functions.filter((f) => f.over);
  const junior = m.functions.filter((f) => f.score > JUNIOR_CEILING && !f.over);

  process.stdout.write('cyclomatic complexity (McCabe, JS only)\n');
  process.stdout.write(`  ${m.functions.length} functions in ${m.files} files\n`);
  process.stdout.write(`  junior ceiling ${JUNIOR_CEILING} (warn)   high-water ${max} (fail)\n\n`);
  process.stdout.write('  top 10:\n');
  for (const f of m.functions.slice(0, 10)) {
    process.stdout.write(`    ${String(f.score).padStart(3)}  ${f.name.padEnd(26)} ${f.file}\n`);
  }
  if (over.length) {
    process.stdout.write(`\n  FAIL ${over.length} over high-water ${max}:\n`);
    for (const f of over) process.stdout.write(`    ${f.score}  ${f.name} (${f.file})\n`);
  }
  if (junior.length) {
    process.stdout.write(`\n  warn ${junior.length} over the junior ceiling ${JUNIOR_CEILING} - read these:\n`);
    for (const f of junior) process.stdout.write(`    ${f.score}  ${f.name} (${f.file}) [${f.drivers.join(' ')}]\n`);
    process.stdout.write('\n  McCabe is a tripwire, not a score. It cannot tell a trivial 8 from\n');
    process.stdout.write('  an unreadable 8. Read the function before changing it.\n');
  }
  process.exit(over.length ? 1 : 0);
}

module.exports = { measure, complexityOf, stripCommentsAndStrings, JUNIOR_CEILING, DEFAULT_MAX };