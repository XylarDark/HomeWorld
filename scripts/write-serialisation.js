const fs = require('fs');
const path = require('path');

/**
 * Write-serialisation gate.
 *
 * WHY THIS EXISTS
 *
 * DEC-0035 cited three independent sources against parallel agent WRITES:
 *
 *   - Cognition: writes should stay single-threaded. Multi-agent write parallelism
 *     is a distributed-systems problem wearing a workflow's clothes.
 *   - Simon Willison: one significant change under review at a time. Parallelism
 *     earns its keep on research, PoCs and low-stakes maintenance - not on the
 *     change that has to be right.
 *   - Christopher Meiklejohn documents REAL DATA LOSS from migration collisions
 *     across agent worktrees.
 *
 * The concrete local hazard is narrower and checkable. `docs/human-use/OWNERSHIP.md`
 * declares isolation and permission posture HUMAN-owned. If two agents each `git rm`
 * an asset the other is holding, that is a permission decision made by accident.
 *
 * So this gate checks the thing that is actually true in this repo: **the working
 * tree is clean, or the agent holding it has said so.** An uncommitted tree is the
 * precondition for silent loss, because two agents cannot both be right about it.
 *
 * WHAT THIS DOES NOT DO
 *
 * It does not serialise agents. It cannot, and trying to would be theatre: the
 * upstream platform already runs subagents sequentially, and pretending otherwise
 * would create the false impression of a guarantee. What it does is make an
 * unowned dirty tree a build failure rather than a surprise, and it gives the
 * human one command to see who holds what.
 *
 * THE BYPASS IS DELIBERATE
 *
 * A dirty tree is normal during agent work - that is the whole point of an agent
 * editing files. Failing hard on that would make the gate useless within a day.
 * So `--allow-dirty <reason>` exists and the reason is printed into
 * Saved/verify_result.json, where a later reader can find out why a run happened
 * on top of uncommitted work. A guard that cannot be used gets routed around
 * silently; a guard that records its own use gets reviewed.
 */

const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');

function git(args) {
  const r = spawnSync('git', args, { cwd: ROOT, encoding: 'utf8', shell: process.platform === 'win32' });
  return { ok: r.status === 0, out: (r.stdout || '').trim(), err: (r.stderr || '').trim() };
}

function measure() {
  const status = git(['status', '--porcelain']);
  const branch = git(['rev-parse', '--abbrev-ref', 'HEAD']);

  // Tracked modifications and deletions are the loss risk. Untracked files are
  // almost always build output or generated Content, and blocking on those would
  // fire constantly without protecting anything.
  const tracked = status.ok
    ? status.out
        .split('\n')
        .filter(Boolean)
        .filter((l) => !l.startsWith('??'))
    : [];

  return {
    branch: branch.ok ? branch.out : 'unknown',
    dirty: tracked.length > 0,
    trackedChanges: tracked.length,
    files: tracked.slice(0, 12),
  };
}

function evaluate(m, { allowDirty = null } = {}) {
  const errors = [];
  const warnings = [];

  if (m.dirty && !allowDirty) {
    errors.push(
      `working tree has ${m.trackedChanges} uncommitted tracked change(s) on "${m.branch}". ` +
        `Two agents cannot both be right about this tree, and an uncommitted asset ` +
        `deletion is a permission decision being made by accident. ` +
        `Commit, stash, or re-run with --allow-dirty "<reason>".`
    );
  } else if (m.dirty && allowDirty) {
    warnings.push(`dirty tree accepted on the record: ${allowDirty}`);
  }
  return { errors, warnings };
}

if (require.main === module) {
  const argv = process.argv.slice(2);
  const i = argv.indexOf('--allow-dirty');
  const allowDirty = i !== -1 ? argv[i + 1] || 'unspecified' : null;

  const m = measure();
  const { errors, warnings } = evaluate(m, { allowDirty });
  const out = { measured: m, allowDirty, errors, warnings };

  if (argv.includes('--json')) {
    process.stdout.write(JSON.stringify(out, null, 2) + '\n');
  } else {
    process.stdout.write('write serialisation\n');
    process.stdout.write(`  branch ${m.branch}, ${m.trackedChanges} uncommitted tracked change(s)\n`);
    for (const f of m.files) process.stdout.write(`    ${f}\n`);
    for (const w of warnings) process.stdout.write(`  warn  ${w}\n`);
    for (const e of errors) process.stdout.write(`  ERROR ${e}\n`);
  }
  process.exit(errors.length ? 1 : 0);
}

module.exports = { measure, evaluate };