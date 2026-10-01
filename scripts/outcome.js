#!/usr/bin/env node
/**
 * One vocabulary for harness outcomes, and an honest account of how it relates to
 * the Week 1 PDF's three-state scheme.
 *
 * WHY THIS FILE EXISTS
 *
 * Three tools in this repo each grew their own outcome words, and a reader who
 * saw `soft_fail` in one and `void` in another reasonably assumed they meant the
 * same thing. They do not. The confusion was not cosmetic: the 2026-10-01 task-lift
 * pilot scored eight crashed agent runs as a clean-looking conformance delta,
 * because the vocabulary had no way to say "this was never measured" — so the
 * only honest-sounding option was to call it a failure.
 *
 * THE PDF'S THREE STATES
 *
 * The Week 1 harness-engineering guidance asks for three outcomes:
 *
 *   pass          measured, and it met the criterion
 *   soft_fail     measured, but inconclusive — a hedge, not a yes
 *   closed_fail   measured, and definitively wrong
 *
 * All three presuppose that a measurement happened.
 *
 * WHAT THIS REPO ADDS, AND WHY IT IS NOT A FOURTH STATE
 *
 * `void` is the absence of a state, not another state. It means the subject of
 * the check did not exist, or the thing that would have produced it never ran.
 * Collapsing `void` into `closed_fail` is the specific mistake that made the void
 * pilot look like a result: eight runs that produced nothing were reported as
 * eight runs that failed, which reads as "the agent tried and did badly" instead
 * of "the agent never ran".
 *
 * So: three states for a measurement, plus one non-state for its absence. If you
 * are counting a rate, `void` is excluded from the denominator, not scored 0.
 *
 * SCOPE — THESE ARE NOT THE SAME SUBJECT
 *
 * Other tools in this repo use similar words for different things. They are not
 * implementations of this scheme and must not be read as if they were:
 *
 *   t0-evidence.js   reads `soft_fail` / `closed_fail` FIELDS out of a beat's
 *                    prove artifact, and reports its own statuses
 *                    (LOCAL_PASS / PROVISIONAL / LOCAL_FAIL / NO_VERDICT).
 *                    Subject: a product beat's self-report.
 *   evidence-grep.js `SOFT_FAIL_MARKERS` are hedge PHRASES in prose
 *                    ("component ready"), used to catch claims that read like
 *                    results but are not. Subject: a sentence.
 *   task-lift.js     verdicts on individual checks of agent output.
 *                    Subject: one assertion about one file.
 *
 * The common thread is a refusal to let an unmeasured thing read as a pass. The
 * words differ because the subjects differ.
 */

/** Verdicts for a check whose subject actually existed and was read. */
const CHECK_VERDICTS = Object.freeze(['pass', 'soft_fail', 'closed_fail']);

/** The non-state: the subject did not exist, or the producer never ran. */
const VOID = 'void';

/** Every value a check result may carry. */
const ALL_VERDICTS = Object.freeze([...CHECK_VERDICTS, VOID]);

/**
 * Phrases that mark a rule as a deliberate tombstone.
 *
 * Discriminate on the `description:` field ONLY, never on body text. A live rule
 * may legitimately discuss retirement in its prose; three rules in this repo are
 * retired on purpose and must keep resolving as pointers.
 *
 * This mirrors the rule already used by harness-coverage.js: a tombstone is not a
 * quality signal, and the self-declared description is the only trustworthy signal
 * of intent.
 */
const TOMBSTONE_MARKERS = Object.freeze([
  'retired',
  'quarantine',
  'do not restore',
  'do not resurrect',
]);

/** True when the frontmatter `description:` declares the rule a tombstone. */
function isTombstoneDescription(description) {
  const d = String(description || '').toLowerCase();
  return TOMBSTONE_MARKERS.some((m) => d.includes(m));
}

/**
 * The PDF's three states, in the PDF's own words, for documentation and reports.
 * A `void` verdict has no PDF equivalent and is deliberately not mapped.
 */
const PDF_MAPPING = Object.freeze({
  pass: 'measured and met the criterion',
  soft_fail: 'measured, but the evidence is a hedge rather than a result',
  closed_fail: 'measured and definitively wrong',
  void: 'NOT MEASURED - no PDF state applies; excluded from the denominator',
});

/**
 * Decide a verdict from whether the subject existed, whether it matched, and
 * whether the evidence is merely weak.
 *
 * `subjectPresent` false must always win. That single ordering rule is what keeps
 * a missing file from being reported as a failed one.
 */
function verdictFor({ subjectPresent, pass, soft = false }) {
  if (!subjectPresent) return VOID;
  if (!pass) return 'closed_fail';
  return soft ? 'soft_fail' : 'pass';
}

module.exports = {
  CHECK_VERDICTS,
  ALL_VERDICTS,
  VOID,
  PDF_MAPPING,
  TOMBSTONE_MARKERS,
  isTombstoneDescription,
  verdictFor,
};
