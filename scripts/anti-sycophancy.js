#!/usr/bin/env node
/**
 * Anti-sycophancy gate.
 *
 * WHY THIS EXISTS
 *
 * "Week 1 - Agentic Engineering", under Agent-specific Information and Suggestions:
 *
 *   "Sycophancy - Agents are programmed to try to answer you anyhow first, and to be
 *    accurate as a secondary priority. Most LLM Agents will also try to flatter you to
 *    keep your attention. That's by design, so disable it as soon as possible!"
 *
 * "As soon as possible" is the instruction, and a document stating a virtue is not a
 * mechanism. This is the mechanism, and it is deliberately weak: a warning gate, not
 * a hard fail.
 *
 * WHY IT CANNOT BE A HARD GATE, AND WHAT THAT COSTS
 *
 * The obvious design - require N disagreements per commit - is gameable in one
 * move: the agent writes token disagreements to pass. A gate that rewards
 * disagreement creates manufactured disagreement, which is **worse than sycophancy**
 * because it is now false *and* dressed up as candour. So:
 *
 *   - It only WARNS. Nothing fails.
 *   - It counts *recorded* disagreements, and cannot verify they were real.
 *   - It names that limitation in its own output, every run.
 *
 * A warning nobody has to satisfy cannot be gamed into meaninglessness. Its whole
 * value is that it puts the question in front of the reader every session: "has this
 * agent disagreed with me once recently, or has it just agreed with me?"
 *
 * WHERE DISAGREEMENTS LIVE
 *
 * `Docs/decisions/DISAGREEMENTS.md`. One entry per substantive disagreement: what was
 * proposed, what was actually wrong with it, and what was done instead. Entries that
 * turn out to be wrong on review get struck rather than deleted - a deleted
 * disagreement is indistinguishable from one that never happened.
 *
 * NOT A QUALITY SCORE
 *
 * Zero disagreements in 90 days is information, not failure. A week where everything
 * proposed was correct is a legitimate week. This gate reports; a human judges.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const LOG = path.join(ROOT, 'Docs', 'decisions', 'DISAGREEMENTS.md');
// `\r?` before the anchor: these files have CRLF endings on Windows, and `$` with the
// `m` flag does not match before a carriage return, so the naive pattern silently
// matched nothing on a checked-out tree.
const ENTRY_RE = /^##[ \t]+(.+?)[ \t]*\r?$/gm;

/** Days back with no recorded disagreement before this warns. */
const QUIET_DAYS = 90;

function readLog() {
  if (!fs.existsSync(LOG)) return { exists: false, entries: [] };
  const raw = fs.readFileSync(LOG, 'utf8');
  // Collect heading positions first, then slice each body up to the NEXT heading.
  // Slicing to `ENTRY_RE.lastIndex` instead truncates the body at the end of the
  // heading line, so every entry looks empty and every date reads as missing - a
  // gate that reports plausible numbers while measuring nothing.
  const heads = [];
  let m;
  ENTRY_RE.lastIndex = 0;
  while ((m = ENTRY_RE.exec(raw)) !== null) {
    heads.push({ title: m[1].trim(), start: m.index, end: ENTRY_RE.lastIndex });
  }
  const entries = heads.map((h, i) => {
    const body = raw.slice(h.end, i + 1 < heads.length ? heads[i + 1].start : raw.length);
    return {
      title: h.title,
      body,
      date: (body.match(/(\d{4}-\d{2}-\d{2})/) || [])[1] || null,
      struck: /~~/.test(body),
    };
  });
  return { exists: true, entries, raw };
}

function measure(now = new Date()) {
  const log = readLog();
  const live = log.entries.filter((e) => !e.struck);
  const dated = live.filter((e) => e.date).map((e) => ({ ...e, t: new Date(`${e.date}T00:00:00Z`) }));
  const newest = dated.length ? dated.reduce((a, b) => (a.t > b.t ? a : b)) : null;
  const daysSince = newest ? Math.floor((now - newest.t) / 86400000) : null;
  return {
    logExists: log.exists,
    total: log.entries.length,
    live: live.length,
    struck: log.entries.length - live.length,
    newestDate: newest ? newest.date : null,
    daysSince,
  };
}

function evaluate(m, { quietDays = QUIET_DAYS } = {}) {
  const warnings = [];
  if (!m.logExists) {
    warnings.push(
      'no disagreement log at Docs/decisions/DISAGREEMENTS.md. Sycophancy cannot be ' +
        'measured, only noticed. The log is how noticing becomes possible.'
    );
    return { warnings, errors: [] };
  }
  if (m.live === 0) {
    warnings.push('every recorded disagreement has been struck. That is a signal, not a clean sheet.');
  } else if (m.daysSince === null) {
    warnings.push('no disagreement entry carries a YYYY-MM-DD date, so recency cannot be checked.');
  } else if (m.daysSince > quietDays) {
    warnings.push(
      `no substantive disagreement recorded in ${m.daysSince} days. That may be a good ` +
        `run - or it may mean nothing was challenged. An agent that never disagrees is ` +
        `not more reliable, it is less tested.`
    );
  }
  return { warnings, errors: [] };
}

if (require.main === module) {
  const m = measure();
  const { warnings } = evaluate(m);
  process.stdout.write('anti-sycophancy\n');
  process.stdout.write(`  ${m.live} live disagreement(s) of ${m.total} recorded`);
  process.stdout.write(m.newestDate ? `, newest ${m.newestDate} (${m.daysSince}d ago)\n` : '\n');
  for (const w of warnings) process.stdout.write(`  warn  ${w}\n`);
  if (!warnings.length) process.stdout.write('  ok    no warning conditions\n');
  // Never fails. A gate that can be satisfied by manufacturing disagreement is worse
  // than no gate, because the failure is invisible.
  process.stdout.write('\n  This gate only ever warns. It cannot verify a disagreement was\n');
  process.stdout.write('  real, and requiring N per commit would just produce fake ones.\n');
  process.exit(0);
}

module.exports = { measure, evaluate, QUIET_DAYS, LOG };