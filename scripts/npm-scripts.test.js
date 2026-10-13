const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');

/**
 * npm script integrity.
 *
 * WHY THIS EXISTS
 *
 * On 2026-10-13 `npm run doctor` ended in MODULE_NOT_FOUND. It chained
 * `node scripts/preflight-scorer.js`, deleted in ae1ebe3b ("delete the
 * self-measurement cluster") along with every scorer that guard existed to
 * check. The chain was never unhooked, and because npm joins it with `;`, the
 * command still ran the deleted file every time and still exited non-zero
 * every time - a permanent, unremarked failure.
 *
 * `harness:sweep` was worse than stale: scripts/harness-sweep.js appears in no
 * commit at all, so the entry was born broken and stayed that way, because
 * nothing ever ran it.
 *
 * This is the same shape harness-paths looks for in prose - an instruction
 * that confidently names something that is not there. The difference is cost.
 * A dead pointer in a doc costs a reader a moment and some trust. A dead
 * pointer in a script costs them an error they will blame on their own
 * checkout, in a command they ran because the docs told them to.
 */

const ROOT = path.resolve(__dirname, '..');
const PKG = JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf8'));

/**
 * A local file a command must read to run.
 *
 * The lookbehind stops `UserHarness/dist/scripts/doctor/cli.js` being read as
 * a repo-rooted `scripts/` path, which it is not - it lives in the submodule.
 *
 * The trailing \b is the whole reason this needs care: `js` is a prefix of
 * `json`, so a bare `\.js` matches the first two letters of `tasks-taste.json`
 * and files the real manifest as missing. That false positive is what a first
 * pass at this check got wrong.
 *
 * Only prefixes a command must READ are listed. `Docs/qa/...` is deliberately
 * absent: the task-lift entries pass `--out-md Docs/qa/TASK_LIFT_TASTE.md`,
 * and failing a command for not yet having written its own output would teach
 * the wrong lesson.
 */
const REF =
  /(?<![\w/.])((?:scripts|Content|Tools|\.github)\/[\w./-]+\.(?:js|py|ps1|sh|json))\b/g;

function refsIn(value) {
  return new Set([...value.matchAll(REF)].map((m) => m[1]));
}

test('every file an npm script reads still exists', () => {
  const missing = [];
  for (const [name, value] of Object.entries(PKG.scripts)) {
    for (const ref of refsIn(value)) {
      if (!fs.existsSync(path.join(ROOT, ref))) missing.push(`${name} -> ${ref}`);
    }
  }
  assert.deepStrictEqual(
    missing,
    [],
    `npm scripts naming files that are not there:\n  ${missing.join('\n  ')}\n` +
      'Remove the entry or point it at what the file became; a script that has\n' +
      'not run in months fails in front of a person, not a test.'
  );
});

test('the check reads the forms that actually appear, and ignores the ones that must not', () => {
  const manifest = refsIn(
    'node scripts/task-lift-control.js --manifest scripts/task-lift/tasks-taste.json'
  );
  assert.ok(manifest.has('scripts/task-lift-control.js'), 'reads the runner');
  assert.ok(
    manifest.has('scripts/task-lift/tasks-taste.json'),
    'reads the manifest as .json, not as .js plus stray letters'
  );

  // The submodule path must not be read as a repo path.
  assert.deepStrictEqual(
    [...refsIn('node UserHarness/dist/scripts/doctor/cli.js --project-root .')],
    [],
    'does not mistake UserHarness/dist for scripts/'
  );

  // Globs are not paths.
  assert.deepStrictEqual(
    [...refsIn('node --test scripts/*.test.js')],
    [],
    'does not treat a shell glob as a file'
  );

  // An output the command has not written yet is not a missing input.
  assert.deepStrictEqual(
    [...refsIn('node scripts/task-lift.js --out-md Docs/qa/TASK_LIFT_TASTE.md')],
    ['scripts/task-lift.js'],
    'does not require an output file to already exist'
  );
});
