#!/usr/bin/env node
/**
 * Reconcile the locked T0 scope against what actually exists on disk.
 *
 * WHY THIS IS A SCRIPT AND NOT A REVIEW
 *
 * The prototype canon lives in three places that were written at different times by
 * different hosts: `PROTOTYPE_FEATURE_LIST_V1.md` (APPROVED, Lead-stamped),
 * `T0_MECHANIC_INVENTORIES_V1.md` (14 design packets) and one prove artifact per
 * beat. The question "is the base prototype element set complete and consistent?"
 * has a mechanical answer for most of it, and a human answer only for the rest.
 * This answers the mechanical part so the human part is not buried under bookkeeping.
 *
 * WHAT IS CHECKED (mechanical, from the tree)
 *
 *  1. The scope table's MUST / CUT / DEFER rows are counted and named.
 *  2. Every MUST row has a design packet on disk, and every packet on disk
 *     corresponds to a MUST row. An orphan packet means a beat that is not in scope;
 *     a MUST with no packet means a scope row with nothing behind it.
 *  3. Every MUST row has a prove artifact on disk.
 *  4. What each artifact CLAIMS (LOCAL_PASS / PROVISIONAL / LOCAL_FAIL / NO_VERDICT)
 *     is recorded, and `accepted` is never inferred from it.
 *  5. The night/combat law is checked mechanically where it can be: a beat whose
 *     scope row is combat-adjacent must not be described as a kill.
 *
 * WHAT IS NOT CHECKED (and is the human's, not a gap here)
 *
 *  Whether the 14 MUST beats are the RIGHT 14, whether any should be CUT, whether
 *  the feel is right, and whether a LOCAL_PASS deserves acceptance. All four are
 *  mechanic-canon taste. Mechanic canon is human-owned by decision of 2026-10-01
 *  (Docs/decisions/AGENT_DECISIONS.md), so this report deliberately stops at the
 *  edge of that line and names what it found rather than resolving it.
 */

const fs = require('fs');
const path = require('path');

const PROJECT_ROOT = path.resolve(__dirname, '..');
const FEATURE_LIST = path.join(PROJECT_ROOT, 'Docs', 'handoffs', 'PROTOTYPE_FEATURE_LIST_V1.md');
const HANDOFFS = path.join(PROJECT_ROOT, 'Docs', 'handoffs');
const EVIDENCE = require('./t0-evidence.js');

/** Split a markdown table row into trimmed cells. */
function cells(line) {
  return line
    .replace(/^\||\|$/g, '')
    .split('|')
    .map((c) => c.trim());
}

/**
 * Parse the scope table. The header is `| Feature / beat | Pillar | MUST/CUT/DEFER | ...`,
 * so the verdict is the cell that contains exactly one of the three keywords.
 */
function parseScopeTable(text) {
  const rows = [];
  let inTable = false;
  for (const line of text.split(/\r?\n/)) {
    if (/^\|\s*Feature \/ beat\s*\|/.test(line)) {
      inTable = true;
      continue;
    }
    if (!inTable) continue;
    if (!line.trim().startsWith('|')) {
      if (rows.length) break; // table ended
      continue;
    }
    const c = cells(line);
    if (c.length < 3 || /^-+$/.test(c[0])) continue;
    const verdict = c[2].replace(/[*]/g, '');
    if (!/^(MUST|CUT|DEFER)$/.test(verdict)) continue;
    rows.push({ feature: c[0], pillar: c[1], verdict, proveHint: c[3] || '', taste: c[4] || '' });
  }
  return rows;
}

/** Night/combat law rows: the ones the ejection / avoid-and-soothe rules apply to. */
function isCombatAdjacent(feature) {
  return /camp night|day camp|spirit|combat|enemy|guard|sleeper|eject/i.test(feature);
}

/**
 * A beat claims a lethal removal if it asserts one.
 *
 * NEGATION MATTERS, and the first version of this check got it wrong in exactly the
 * way the pilot's `noneMatch` did: the prove hint for the day-camp row literally reads
 * "**not** lethal; convert-not-kill", and a bare word match flagged that row as a law
 * violation. The canon is *stated* in those rows precisely because the law forbids it,
 * so a check that cannot see negation reports the compliant rows as the violations.
 */
function claimsKill(feature, proveHint) {
  const KILL = /\b(kills?|killed|lethal|slay|slain|die|death|execute[sd]?)\b/i;
  const NEGATED = /\b(not|never|no|non|refus\w*|convert-not|without)\b/i;
  const segments = `${feature} ${proveHint}`.split(/[;.]/);
  return segments.some((s) => KILL.test(s) && !NEGATED.test(s));
}

function listHandoffs(pattern) {
  if (!fs.existsSync(HANDOFFS)) return [];
  return fs
    .readdirSync(HANDOFFS)
    .filter((f) => pattern.test(f))
    .sort();
}

/** Beat ids like M1..M14 from the design-packet filenames. */
function beatIdsFromPackets() {
  const ids = new Set();
  for (const f of listHandoffs(/^T0_M(\d+)_.*_V1\.md$/i)) {
    ids.add(`M${/^T0_M(\d+)_/i.exec(f)[1]}`);
  }
  return [...ids].sort((a, b) => Number(a.slice(1)) - Number(b.slice(1)));
}

function reconcile(options = {}) {
  if (!fs.existsSync(FEATURE_LIST)) {
    return { ok: false, error: `missing ${FEATURE_LIST}` };
  }
  const text = fs.readFileSync(FEATURE_LIST, 'utf8');
  const scope = parseScopeTable(text);
  if (scope.length === 0) {
    return { ok: false, error: 'scope table parsed to zero rows - the parser or the doc changed' };
  }

  const must = scope.filter((r) => r.verdict === 'MUST');
  const cut = scope.filter((r) => r.verdict === 'CUT');
  const defer = scope.filter((r) => r.verdict === 'DEFER');

  // Evidence, via the existing ledger so there is one source of truth for verdicts.
  // collectGates REQUIRES the Saved directory; called with no argument it silently
  // returns [] and every beat then reads NO_ARTIFACT, which looks like a finding
  // rather than a defect in this script.
  let evidence = [];
  try {
    const savedDir = options.savedDir || path.join(PROJECT_ROOT, 'Saved');
    const gates = EVIDENCE.collectGates(savedDir);
    // Beat ids arrive as `T0_M1`; the scope table is indexed by `M1`.
    evidence = gates.map((g) => ({
      beat: /^T0_(M\d+)$/.exec(g.beat) ? /^T0_(M\d+)$/.exec(g.beat)[1] : g.beat,
      status: g.status,
      accepted: g.accepted,
      provisional: g.provisional,
      tracked: g.trackedInGit,
    }));
  } catch (e) {
    return { ok: false, error: `evidence ledger failed: ${e.message}` };
  }
  const byBeat = new Map(evidence.map((e) => [e.beat, e]));
  const nonBeatGates = evidence.filter((e) => !/^M\d+$/.test(e.beat)).map((e) => e.beat);

  const packets = beatIdsFromPackets();
  const proveFiles = listHandoffs(/^T0_M(\d+)_.*_PROVE\.md$/i);
  const proveBeats = new Set(proveFiles.map((f) => `M${/^T0_M(\d+)_/i.exec(f)[1]}`));

  // Numbering check. The MUST rows are numbered 1..14 in the beat documents; a gap
  // in the packet set is a real gap, not a numbering artefact, because the packets
  // are named files.
  const mustNumbers = must
    .map((_, i) => i + 1)
    .filter((n) => !packets.includes(`M${n}`));

  const lawRows = scope.filter((r) => isCombatAdjacent(r.feature));
  const lawViolations = lawRows.filter((r) => claimsKill(r.feature, r.proveHint));

  const beats = must.map((r, i) => {
    const id = `M${i + 1}`;
    const ev = byBeat.get(id);
    return {
      beat: id,
      feature: r.feature,
      packet: packets.includes(id),
      prove: proveBeats.has(id),
      claimed: ev ? ev.status : 'NO_ARTIFACT',
      accepted: ev ? ev.accepted : false,
      tracked: ev ? ev.tracked : false,
    };
  });

  const accepted = beats.filter((b) => b.accepted).length;

  return {
    ok: true,
    counts: { must: must.length, cut: cut.length, defer: defer.length, packets: packets.length },
    cut,
    defer,
    beats,
    orphanPackets: packets.filter((id) => !beats.some((b) => b.beat === id)),
    mustNumbersWithoutPacket: mustNumbers,
    nonBeatGates,
    lawViolations,
    accepted,
    cutRows: cut.map((c) => c.feature),
  };
}

function render(res) {
  if (!res.ok) return `# T0 scope reconciliation\n\n**Could not reconcile:** ${res.error}\n`;
  const L = [];
  L.push('# T0 scope reconciliation — locked base elements vs what exists');
  L.push('');
  L.push('> **Generated file.** Regenerate with `npm run scope:reconcile`.');
  L.push('');
  L.push('> **Read this before quoting any number.** This reconciles *what is declared and');
  L.push('> what exists*. It does **not** judge whether the declared beats are the right');
  L.push('> ones, nor whether any artifact deserves acceptance. Both are mechanic-canon');
  L.push('> taste and stay human-owned.');
  L.push('');
  L.push('## Scope as locked');
  L.push('');
  L.push(`- **MUST** ${res.counts.must} · **DEFER** ${res.counts.defer} · **CUT** ${res.counts.cut}`);
  L.push(`- design packets on disk: ${res.counts.packets}`);
  L.push(`- beats with a human acceptance stamp: **${res.accepted} of ${res.counts.must}**`);
  L.push('');
  L.push('| # | Beat | Feature | Design packet | Prove artifact | Artifact claims | Accepted |');
  L.push('|---|---|---|---|---|---|---|');
  for (const b of res.beats) {
    L.push(
      `| ${b.beat.slice(1)} | ${b.beat} | ${b.feature} | ${b.packet ? 'yes' : '**MISSING**'} | ` +
        `${b.prove ? 'yes' : '**MISSING**'} | ${b.claimed} | ${b.accepted ? 'yes' : 'no'} |`
    );
  }
  L.push('');
  L.push('"Artifact claims" is what the local artifact asserts about itself. It is never');
  L.push('read as acceptance — acceptance is a human stamp and stays `false` until one exists.');
  L.push('');

  const findings = [];
  if (res.mustNumbersWithoutPacket.length) {
    findings.push(
      `- MUST rows with no design packet on disk: **${res.mustNumbersWithoutPacket.join(', ')}**`
    );
  }
  if (res.orphanPackets.length) {
    findings.push(
      `- Packets on disk that match no MUST row: **${res.orphanPackets.join(', ')}** — a beat ` +
        'that is implemented but not in scope, or a numbering mismatch.'
    );
  }
  const noProve = res.beats.filter((b) => !b.prove).map((b) => b.beat);
  if (noProve.length) findings.push(`- MUST beats with no prove artifact: **${noProve.join(', ')}**`);
  const noGate = res.beats.filter((b) => b.claimed === 'NO_ARTIFACT').map((b) => b.beat);
  if (noGate.length) {
    findings.push(
      `- MUST beats with no local gate artifact in \`Saved/\`: **${noGate.join(', ')}** — no run has ` +
        'recorded a verdict for them yet.'
    );
  }
  if (res.nonBeatGates && res.nonBeatGates.length) {
    findings.push(
      `- Gate artifacts that match no beat: ${res.nonBeatGates.join(', ')} (supporting work, not a beat).`
    );
  }
  if (res.lawViolations.length) {
    findings.push(
      `- **Night/combat law**: ${res.lawViolations.length} row(s) describe a lethal removal. ` +
        `The law is eject-to-home and avoid-and-soothe, never kill: ` +
        `${res.lawViolations.map((v) => v.feature).join('; ')}`
    );
  }
  if (!findings.length) findings.push('- No structural inconsistency found between the scope table and the tree.');

  L.push('## Findings');
  L.push('');
  for (const f of findings) L.push(f);
  L.push('');
  L.push('## Cut and deferred — deliberately out of the base prototype');
  L.push('');
  for (const c of res.cut) L.push(`- **CUT** ${c.feature}`);
  for (const d of res.defer) L.push(`- **DEFER** ${d.feature}`);
  L.push('');
  L.push('## What is left for a human');
  L.push('');
  L.push('1. **Which beats are the right 14.** Reconciling what exists says nothing about');
  L.push('   whether the set is right, or whether one should be CUT.');
  L.push(
    `2. **Acceptance.** \`0 of ${res.counts.must}\` accepted. A LOCAL_PASS is a claim, not a verdict.`
  );
  L.push('3. **The unresolved stamp conflict** between the gap walk and the mechanic');
  L.push('   inventories — unchanged, and still mechanic canon.');
  L.push('');
  return L.join('\n');
}

function main(argv) {
  const writeIdx = argv.indexOf('--write');
  const res = reconcile();
  const md = render(res);
  if (writeIdx !== -1) {
    const out = argv[writeIdx + 1] || path.join(PROJECT_ROOT, 'docs', 'qa', 'T0_SCOPE_RECONCILIATION.md');
    fs.mkdirSync(path.dirname(out), { recursive: true });
    fs.writeFileSync(out, md, 'utf8');
    process.stderr.write(`[scope-reconcile] wrote ${out}\n`);
  } else {
    process.stdout.write(md);
  }
  if (!res.ok) return 2;
  return res.lawViolations.length > 0 ? 1 : 0;
}

if (require.main === module) process.exit(main(process.argv.slice(2)));

module.exports = { main, reconcile, render, parseScopeTable, isCombatAdjacent, claimsKill, cells };
