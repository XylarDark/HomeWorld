#!/usr/bin/env node
/**
 * Score every task's `control` fixture — the positive control.
 *
 * A task's control fixture is what a CORRECT agent would produce. This must score
 * 100%. If it does not, at least one check in that task is unsatisfiable, and the
 * eval would report a permanent shortfall that reads as "the harness does not
 * help" rather than "the instrument cannot register success".
 *
 * That is not hypothetical. The 2026-10-01 pilot reported a plausible-looking
 * conformance delta while all eight agents had been rejected by the provider and
 * had produced nothing at all. Nothing in the harness could have told the
 * difference, because nothing asserted that a good answer scores well.
 *
 * Exit code is non-zero on any failure, so this can gate a run.
 */

const { loadTasks, scoreControl, readFlag, PREFIX } = require('./task-lift.js');

function main(argv) {
  const onlyIdx = argv.indexOf('--only');
  const only = onlyIdx !== -1 ? argv[onlyIdx + 1] : null;
  const manifestPath = readFlag(argv, '--manifest');

  const manifest = loadTasks(manifestPath || undefined);
  const tasks = only ? manifest.tasks.filter((t) => t.id === only) : manifest.tasks;
  if (tasks.length === 0) {
    process.stderr.write(`${PREFIX} ERROR - no task matched --only ${only}\n`);
    return 2;
  }

  const reports = tasks.map(scoreControl);
  const failed = reports.filter((r) => !r.ok);

  process.stdout.write('# Task-lift positive control\n\n');
  process.stdout.write(`- task manifest: \`${manifestPath || 'default'}\`\n\n`);
  process.stdout.write(
    'Each task ships a `control` fixture: the files a correct agent would produce. ' +
      'This must score 100%. A shortfall means a check is unsatisfiable, not that the ' +
      'harness is ineffective.\n\n'
  );
  process.stdout.write('| Task | Result | Detail |\n|---|---|---|\n');
  for (const r of reports) {
    const detail = r.ok
      ? `${r.checks.length}/${r.checks.length} checks pass`
      : `${r.reason} — ${r.checks
          .filter((c) => !c.pass)
          .map((c) => `${c.label} (${c.verdict})`)
          .join('; ')}`;
    process.stdout.write(`| ${r.taskId} | ${r.ok ? '**pass**' : '**FAIL**'} | ${detail} |\n`);
  }
  process.stdout.write('\n');

  if (failed.length === 0) {
    process.stdout.write(
      `All ${reports.length} task controls reach 100%. The instrument can register success.\n`
    );
    return 0;
  }
  process.stderr.write(
    `${PREFIX} ${failed.length} of ${reports.length} task controls did NOT reach 100%: ` +
      `${failed.map((f) => f.taskId).join(', ')}\n`
  );
  return 1;
}

if (require.main === module) process.exit(main(process.argv.slice(2)));

module.exports = { main };
