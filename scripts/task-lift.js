#!/usr/bin/env node
/**
 * Task-level eval — does the harness layer change what the agent produces?
 *
 * WHY THIS EXISTS
 * ---------------
 * The project measures its rules two ways: a structural score (87.5) and a judged
 * score (62.32). Both measure the *inputs* — how good the rule text is. Neither can
 * answer the only question that matters: does having those rules make the agent
 * produce better work? A harness that scores well and changes nothing is a
 * maintenance burden, not an improvement.
 *
 * The field answers this with task success-rate lift: same model, same task, with
 * and without the scaffold, measure the delta. That is what this does.
 *
 * THE DESIGN, and why it splits checks into two classes
 * ----------------------------------------------------
 * Each task has `completion` checks (was the task done at all?) and `conformance`
 * checks (does the artifact follow this repo's documented conventions?).
 *
 * Lift is measured on conformance ONLY. Without the completion class, a harness
 * could "win" by making the agent produce more files, more prose, more anything —
 * which is not an improvement, it is volume. The completion class is the control
 * that keeps the comparison honest: if the harness arm does not complete tasks at
 * least as often, the conformance delta means nothing.
 *
 * ABLATION IS REAL
 * ----------------
 * The `without` condition is a separate git worktree at the same commit with
 * AGENTS.md, .cursor/, .agents/, swarm/ and UserHarness physically deleted, and
 * the agent run as a fresh `opencode run --standalone` process with its working
 * directory inside it. That is genuine removal, not a prompt asking the agent to
 * ignore the rules — a suggestion is not an ablation.
 *
 * WHAT THIS CANNOT DO
 * -------------------
 * Four tasks x two conditions x one trial has almost no statistical power. The
 * output reports the delta AND its weakness every time. Do not quote the number
 * without the caveat; it is a smoke signal that the instrument works, not evidence
 * of a harness effect. A real measurement needs 12-15 tasks and 2+ trials per arm.
 *
 * Usage:
 *   node scripts/task-lift.js --run              # full run (costs agent sessions)
 *   node scripts/task-lift.js --dry              # build + score, no agent runs
 *   node scripts/task-lift.js --only <id>        # one task
 *   node scripts/task-lift.js --keep             # leave worktrees for inspection
 */

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('node:child_process');
const { verdictFor, isTombstoneDescription } = require('./outcome.js');

const PREFIX = '[task-lift]';
const PROJECT_ROOT = path.resolve(__dirname, '..');
const MANIFEST = path.join(__dirname, 'task-lift', 'tasks.json');

/** Files removed to ablate the harness. These are the agent's always-on context. */
const ABLATE_PATHS = ['AGENTS.md', '.cursor', '.agents', 'swarm', 'UserHarness', 'START_HERE.md'];

const AGENT_TIMEOUT_MS = 15 * 60 * 1000;

function loadTasks(file = MANIFEST) {
  const raw = JSON.parse(fs.readFileSync(file, 'utf8'));
  // Record which manifest produced a result. Two manifests share one JSON filename
  // in practice, and a report that does not say which set it measured is unreadable.
  raw.manifestPath = file;
  return raw;
}

/**
 * Compile a glob to a regex by walking the string, with no placeholder tokens.
 *
 * Two earlier versions were wrong, and both failed in the same silent way — by
 * matching nothing:
 *   1. Converting `?` to `.` as a *final* pass rewrote the already-injected
 *      "match any number of directories" group into a broken form, and every
 *      recursive glob stopped matching.
 *   2. Using text placeholders for the wildcards let the regex-escape step corrupt
 *      them.
 * A glob that matches nothing makes its check fail closed, which then looks like a
 * bad agent result instead of a broken evaluator. Walking the string gives that
 * class of bug nowhere to live.
 *
 * Semantics are conventional: a single star and `?` do not cross a path separator,
 * while a double star followed by a slash matches zero or more directories.
 */
function globToRegExp(glob) {
  const SPECIAL = /[.+^$()|[\]\\{}]/;
  const g = String(glob);
  let out = '';
  for (let i = 0; i < g.length; i++) {
    const c = g[i];
    if (c === '*') {
      if (g[i + 1] === '*') {
        i += 1;
        if (g[i + 1] === '/') {
          out += '(?:.*/)?';
          i += 1;
        } else {
          out += '.*';
        }
      } else {
        out += '[^/]*';
      }
    } else if (c === '?') {
      out += '[^/]';
    } else {
      out += SPECIAL.test(c) ? '\\' + c : c;
    }
  }
  return new RegExp(`^${out}$`);
}

/**
 * Compile a check pattern to a RegExp.
 *
 * `(?i)` is accepted and stripped, adding the `i` flag instead. JavaScript has no
 * inline case-insensitive flag — that is PCRE syntax — so a pattern written out of
 * habit throws `Invalid group` and aborts the whole run. Normalising here means a
 * manifest author reaches for the familiar spelling without crashing the evaluator.
 * `m` is on by default so a pattern can match a line anywhere in a document.
 */
function compilePattern(pattern, opts = {}) {
  let flags = opts.flags || '';
  let src = String(pattern);
  const inline = /^\(\?([a-z]+)\)/.exec(src);
  if (inline) {
    src = src.slice(inline[0].length);
    for (const f of inline[1]) if (!flags.includes(f)) flags += f;
  }
  if (opts.multiline === false) flags = flags.replace(/m/g, '');
  else if (!flags.includes('m')) flags += 'm';
  return new RegExp(src, flags);
}

/**
 * Resolve the opencode executable.
 *
 * On Windows the npm shim is `opencode.cmd`, which delegates to a real
 * `opencode.exe`. Node cannot execute a `.cmd` without a shell, so spawning the
 * bare name fails with ENOENT — and using `shell: true` to work around that would
 * push the task prompts (backticks, quotes, parens) through cmd.exe, where they are
 * metacharacters. Spawning the resolved binary avoids both problems.
 *
 * Order: explicit override, then the known npm install path, then bare name
 * (correct on macOS/Linux, where the shim is a symlink Node can exec).
 */
function resolveAgentBin(env = process.env, platform = process.platform, home = env.APPDATA) {
  if (env.TASKLIFT_OPENCODE) return env.TASKLIFT_OPENCODE;
  if (platform === 'win32' && home) {
    const winExe = path.join(home, 'npm', 'node_modules', '@opencode', 'cli', 'bin', 'opencode.exe');
    if (fs.existsSync(winExe)) return winExe;
  }
  return 'opencode';
}

/** Capture a spawned command's first stdout line, tolerating a failed spawn. */
function firstLine(result) {
  const out = result && typeof result.stdout === 'string' ? result.stdout : '';
  const line = out.split(/\r?\n/).find((l) => l.trim().length > 0);
  return line ? line.trim() : 'unavailable';
}

/** Recursively list files under a root, as repo-relative posix paths. Skips .git. */
function listFiles(root, rel = '', out = []) {
  const dir = rel ? path.join(root, rel) : root;
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const e of entries) {
    if (e.name === '.git') continue;
    const r = rel ? `${rel}/${e.name}` : e.name;
    if (e.isDirectory()) listFiles(root, r, out);
    else out.push(r);
  }
  return out;
}

/** Files matching a glob, restricted to `allowed` when provided. */
function matchFiles(root, glob, allowed) {
  const re = globToRegExp(glob);
  const pool = allowed || listFiles(root);
  return pool.filter((f) => re.test(f));
}

/**
 * Confirm the ablation actually removed the harness surfaces.
 *
 * Without this the experiment is unfalsifiable: if a delete silently half-fails —
 * a path typo, Windows case-folding, a tool recreating `.cursor` — the "without
 * harness" arm is secretly a *with harness* arm, and the two arms agree for a
 * reason that has nothing to do with the harness. That failure is silent and it
 * biases toward finding no effect, which is the comfortable direction to be wrong
 * in. So it is checked, and it is reported into the JSON.
 */
function verifyAblation(root) {
  const present = ABLATE_PATHS.filter((p) => fs.existsSync(path.join(root, p)));
  return {
    ok: present.length === 0,
    present,
    checked: ABLATE_PATHS.length,
    // A reader must be able to see the arms differ, not take it on trust.
    fileCount: listFiles(root).length,
  };
}

/**
 * Create a worktree at HEAD. When `ablate` is set, delete the harness surfaces and
 * verify the deletion. Throws with the git error rather than returning a half-built
 * tree, and throws on an incomplete ablation rather than measuring a fake arm.
 */
function buildWorktree(dest, ablate) {
  const r = spawnSync('git', ['worktree', 'add', '--detach', dest, 'HEAD'], {
    cwd: PROJECT_ROOT,
    encoding: 'utf8',
    timeout: 10 * 60 * 1000,
  });
  if (r.status !== 0) throw new Error(`git worktree add failed: ${r.stderr || r.stdout}`);

  if (ablate) {
    for (const p of ABLATE_PATHS) {
      const full = path.join(dest, p);
      if (fs.existsSync(full)) fs.rmSync(full, { recursive: true, force: true });
    }
    const v = verifyAblation(dest);
    if (!v.ok) {
      throw new Error(
        `ablation incomplete, refusing to measure a fake "without harness" arm. ` +
          `Still present: ${v.present.join(', ')}`
      );
    }
  }
  return dest;
}

function removeWorktree(dest) {
  spawnSync('git', ['worktree', 'remove', '--force', dest], {
    cwd: PROJECT_ROOT,
    encoding: 'utf8',
    timeout: 5 * 60 * 1000,
  });
}

/** Write the task's starting state. Returns the file list present AFTER seeding. */
function seed(root, task) {
  for (const [rel, content] of Object.entries(task.seed || {})) {
    const full = path.join(root, rel);
    fs.mkdirSync(path.dirname(full), { recursive: true });
    fs.writeFileSync(full, content, 'utf8');
  }
  return new Set(listFiles(root));
}

/**
 * Pull the real failure reason out of opencode's JSON event stream.
 *
 * A non-zero exit is not an error to `spawnSync`: `r.error` stays null unless the
 * process failed to launch, was killed, or blew the buffer. The actual reason is
 * in stdout as a `{"type":"error",...}` event. Without this, a quota-blocked run
 * looks exactly like a run that did nothing wrong.
 */
function extractAgentError(stdout, stderr) {
  let reason = null;
  for (const line of String(stdout || '').split('\n')) {
    if (!line.includes('"type":"error"')) continue;
    let ev;
    try {
      ev = JSON.parse(line);
    } catch {
      continue; // partial line
    }
    const e = ev.error;
    if (!e) continue;
    const text = typeof e === 'string' ? e : e.message || e.type || JSON.stringify(e);
    const kind = typeof e === 'object' && e.type ? `/${e.type}` : '';
    const code = typeof e === 'object' && e.status ? ` (HTTP ${e.status})` : '';
    reason = `[error${kind}]${code} ${text}`.trim();
  }
  return reason || (String(stderr || '').trim() || null);
}

/** Run one agent session in `root`. Never throws; transport problems are reported. */
function runAgent(root, prompt, timeoutMs = AGENT_TIMEOUT_MS) {
  const bin = resolveAgentBin();
  const r = spawnSync(bin, ['run', '--standalone', '--auto', '--format', 'json', prompt], {
    cwd: root,
    encoding: 'utf8',
    timeout: timeoutMs,
    maxBuffer: 32 * 1024 * 1024,
  });
  // Keep the last lines, then keep the END of them: the failure event is the last
  // thing written, and slicing from the front used to cut it off exactly where the
  // message began.
  const tail = (r.stdout || '')
    .split('\n')
    .filter(Boolean)
    .slice(-3)
    .join('\n')
    .slice(-400);
  const error = r.error ? r.error.message : extractAgentError(r.stdout, r.stderr);
  return {
    status: r.status,
    signal: r.signal,
    timedOut: Boolean(r.error && r.error.code === 'ETIMEDOUT'),
    error,
    // A run is only good if the agent exited clean AND reported no error event.
    ok: r.status === 0 && !r.error && !error,
    outputTail: tail,
  };
}

/** The commit subject: first non-empty, non-comment line. */
function commitSubject(text) {
  for (const line of text.split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    return t;
  }
  return '';
}

/**
 * Evaluate one check against the worktree.
 *
 * Returns a result object rather than throwing. A check that cannot be evaluated
 * (target absent) is a FAIL with a reason, never a crash that aborts the run and
 * silently shrinks the task count — a shrinking denominator would inflate lift.
 */
function evaluateCheck(root, check, createdAfterSeed) {
  const base = { class: check.class, label: check.label, kind: check.kind };
  const patterns = check.pattern ? compilePattern(check.pattern, check) : null;

  // Every result carries a verdict from the shared vocabulary (scripts/outcome.js).
  // `void` is the absence of a measurement, not a failure: it is what stops a
  // missing subject from being reported as a wrong one.
  const result = (pass, detail, { subjectPresent = true, soft = false } = {}) => ({
    ...base,
    pass,
    detail,
    subjectPresent,
    verdict: verdictFor({ subjectPresent, pass, soft }),
  });

  const readTargets = () => {
    if (check.path) {
      const full = path.join(root, check.path);
      return fs.existsSync(full) ? [check.path] : [];
    }
    let pool = listFiles(root);
    if (check.newOnly) pool = pool.filter((f) => !createdAfterSeed.has(f));
    return matchFiles(root, check.glob, pool);
  };

  switch (check.kind) {
    case 'exists': {
      const present = fs.existsSync(path.join(root, check.path));
      return result(present, check.path, { subjectPresent: present });
    }

    case 'matches': {
      const full = path.join(root, check.path);
      if (!fs.existsSync(full)) return result(false, 'file absent', { subjectPresent: false });
      return result(patterns.test(fs.readFileSync(full, 'utf8')), check.path);
    }

    case 'lacks': {
      const full = path.join(root, check.path);
      if (!fs.existsSync(full)) return result(false, 'file absent', { subjectPresent: false });
      return result(!patterns.test(fs.readFileSync(full, 'utf8')), check.path);
    }

    case 'anyMatches': {
      const targets = readTargets();
      if (targets.length === 0) return result(false, 'no target file', { subjectPresent: false });
      const hits = targets.filter((t) => patterns.test(fs.readFileSync(path.join(root, t), 'utf8')));
      return result(hits.length > 0, hits[0] || `none of ${targets.length} targets`);
    }

    case 'noneMatch': {
      const targets = readTargets();
      if (targets.length === 0) return result(false, 'no target file', { subjectPresent: false });
      const hits = targets.filter((t) => patterns.test(fs.readFileSync(path.join(root, t), 'utf8')));
      return result(hits.length === 0, hits[0] ? `matched in ${hits[0]}` : 'clean');
    }

    case 'allLinesMatch': {
      // Every non-blank line must match. Used where the rule is about the whole set -
      // "every asset name uses an approved prefix" cannot be checked by asking
      // whether ANY line matches, which would pass a list of five names where one is
      // right and four are invented.
      const full = path.join(root, check.path);
      if (!fs.existsSync(full)) return result(false, 'file absent', { subjectPresent: false });
      const lines = fs
        .readFileSync(full, 'utf8')
        .split(/\r?\n/)
        .map((l) => l.trim())
        .filter((l) => l.length > 0);
      if (lines.length === 0) return result(false, 'file has no content lines', { subjectPresent: false });
      const bad = lines.filter((l) => !patterns.test(l));
      return result(
        bad.length === 0,
        bad.length === 0 ? `${lines.length} lines conform` : `non-conforming: ${bad[0].slice(0, 60)}`,
        { soft: lines.length < (check.min || 1) }
      );
    }

    case 'declaresScope': {
      // A live rule must declare how it is scoped. A tombstone must not: this repo
      // keeps three rules alive as pointers with `alwaysApply: false` and no globs,
      // and requiring globs of them would push a future agent to "fix" a retired
      // rule back into an always-on load. Discriminate on the self-declared
      // `description:` only, never on body text.
      const targets = readTargets();
      if (targets.length === 0) return result(false, 'no target file', { subjectPresent: false });
      for (const t of targets) {
        const text = fs.readFileSync(path.join(root, t), 'utf8');
        const fm = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
        const description = fm ? (/^description:\s*(.*)$/m.exec(fm[1]) || [])[1] : '';
        if (isTombstoneDescription(description)) return result(true, `${t} (tombstone)`, { soft: true });
        if (/^globs:/m.test(fm ? fm[1] : '')) return result(true, t);
      }
      return result(false, 'no globs and no tombstone declaration');
    }

    case 'anyNewFiles': {
      const targets = readTargets();
      return result(targets.length > 0, `${targets.length} new file(s)`, {
        subjectPresent: targets.length > 0,
      });
    }

    case 'commitSubjectCase': {
      const targets = readTargets();
      if (targets.length === 0) return result(false, 'no message file', { subjectPresent: false });
      const subject = commitSubject(fs.readFileSync(path.join(root, targets[0]), 'utf8'));
      const after = subject.replace(/^(\w+)(\([^)]*\))?!?:\s*/, '');
      // The type prefix is legitimately lowercase; only the subject text is judged.
      return result(after === after.toLowerCase(), subject.slice(0, 80));
    }

    case 'commitSubjectNoPeriod': {
      // Judged on the SUBJECT, not the end of the file. A `noneMatch` on `\.\s*$`
      // looks at end-of-string, so a well-formed message whose body ends in a
      // sentence failed a check labelled "subject has no trailing period".
      const targets = readTargets();
      if (targets.length === 0) return result(false, 'no message file', { subjectPresent: false });
      const subject = commitSubject(fs.readFileSync(path.join(root, targets[0]), 'utf8'));
      const bad = /\.$/.test(subject.trim());
      return result(!bad, bad ? 'subject ends with a period' : 'clean');
    }

    case 'commitSubjectLength': {
      const targets = readTargets();
      if (targets.length === 0) return result(false, 'no message file', { subjectPresent: false });
      const subject = commitSubject(fs.readFileSync(path.join(root, targets[0]), 'utf8'));
      return result(subject.length <= (check.max || 72), `${subject.length} chars`);
    }

    default:
      return result(false, `unknown check kind: ${check.kind}`, { subjectPresent: false });
  }
}

/** Run one task in one condition and score every check. */
function runTask(worktreeRoot, task, { dry, ...retryOpts } = {}) {
  const createdAfterSeed = seed(worktreeRoot, task);
  const agent = dry
    ? { status: 0, dry: true, ok: true, attempts: 0 }
    : runAgentWithRetry(worktreeRoot, task.prompt, retryOpts);

  const checks = task.checks.map((c) => evaluateCheck(worktreeRoot, c, createdAfterSeed));
  const byClass = (cls) => checks.filter((c) => c.class === cls);
  const rate = (cls) => {
    const list = byClass(cls);
    return list.length === 0 ? null : list.filter((c) => c.pass).length / list.length;
  };

  // A run whose agent never succeeded is not a measurement: its checks describe a
  // worktree nobody touched. Scoring them reports a broken agent as a weak one.
  const voided = !agent.ok;

  return {
    taskId: task.id,
    agent,
    voided,
    checks,
    completion: rate('completion'),
    conformance: rate('conformance'),
    completionPassed: byClass('completion').filter((c) => c.pass).length,
    conformancePassed: byClass('conformance').filter((c) => c.pass).length,
    completionTotal: byClass('completion').length,
    conformanceTotal: byClass('conformance').length,
  };
}

/**
 * Score a task's `control` fixture: the files a *correct* agent would produce.
 *
 * This is the positive control the manifest lacked. Without it, a check whose
 * pattern can never be satisfied would report a permanent 0% forever, and that
 * reads as "the harness does not help" rather than "the instrument is broken" —
 * the same shape of error as scoring eight crashed runs as a weak agent.
 *
 * Returns per-check results plus a pass rate. `ok` is true only at a clean sweep.
 */
function scoreControl(task) {
  const control = task.control || {};
  const files = Object.keys(control);
  if (files.length === 0) {
    return { taskId: task.id, ok: false, reason: 'no control fixture declared', checks: [], rate: null };
  }
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'tasklift-control-'));
  try {
    for (const [rel, content] of Object.entries(control)) {
      const full = path.join(root, rel);
      fs.mkdirSync(path.dirname(full), { recursive: true });
      fs.writeFileSync(full, content, 'utf8');
    }
    // The fixture IS the agent's output, so the "created after seed" baseline is
    // empty: every control file counts as new, exactly as a real run would see it.
    const checks = task.checks.map((c) => evaluateCheck(root, c, new Set()));
    const passed = checks.filter((c) => c.pass).length;
    return {
      taskId: task.id,
      ok: passed === checks.length,
      reason: passed === checks.length ? null : `${passed}/${checks.length} checks failed`,
      rate: checks.length ? passed / checks.length : null,
      checks,
    };
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
}

function rate(list, key) {
  const vals = list.map((r) => r[key]).filter((v) => typeof v === 'number');
  return vals.length === 0 ? null : vals.reduce((a, b) => a + b, 0) / vals.length;
}

function summarize(results, { minValidPerCell = 1, dry = false } = {}) {
  const voidedRuns = results.filter((r) => r.voided);
  const valid = results.filter((r) => !r.voided);

  // Per-cell accounting. A void run voids ITS cell, not the whole experiment: with
  // 8 runs, one timeout used to discard all eight.
  const cells = {};
  for (const r of results) {
    const key = `${r.taskId}/${r.condition}`;
    cells[key] = (cells[key] || 0) + (r.voided ? 0 : 1);
  }
  const shortCells = Object.entries(cells).filter(([, n]) => n < minValidPerCell);
  const missingCells = Object.keys(cells).filter((k) => cells[k] === 0);

  // PAIRED analysis. A task contributes to the comparison only if BOTH of its arms
  // have a valid run. Comparing a/with against (a/without + b/without) while b/with is
  // missing is an unpaired proportion comparison - the same fallacy as comparing two
  // groups built from different subjects. Dropped pairs are reported, not hidden.
  const taskIds = [...new Set(results.map((r) => r.taskId))];
  const completePairs = taskIds.filter(
    (t) => (cells[`${t}/with`] || 0) >= minValidPerCell && (cells[`${t}/without`] || 0) >= minValidPerCell
  );
  const droppedPairs = taskIds.filter((t) => !completePairs.includes(t));
  const paired = valid.filter((r) => completePairs.includes(r.taskId));
  const withArm = paired.filter((r) => r.condition === 'with');
  const withoutArm = paired.filter((r) => r.condition === 'without');

  const conf = (l) => rate(l, 'conformance');
  const comp = (l) => rate(l, 'completion');
  const lift =
    conf(withArm) !== null && conf(withoutArm) !== null ? conf(withArm) - conf(withoutArm) : null;
  const enough = completePairs.length > 0;

  return {
    tasks: taskIds.length,
    pairedTasks: completePairs.length,
    droppedPairs,
    // Rates describe only the runs that measured something.
    validRuns: valid.length,
    voidedRuns: voidedRuns.length,
    validByCell: cells,
    missingCells,
    shortCells: shortCells.map(([k, n]) => ({ cell: k, valid: n, required: minValidPerCell })),
    completionWith: comp(withArm),
    completionWithout: comp(withoutArm),
    conformanceWith: conf(withArm),
    conformanceWithout: conf(withoutArm),
    // Withheld when nothing was measured, when a dry run produced the numbers, or
    // when no task has both arms. A lift over a partial set is worse than none: it
    // still reads as data.
    lift: enough && !dry ? lift : null,
    liftWithheld: dry
      ? 'dry run - no agent executed, so nothing was measured'
      : enough
        ? null
        : 'no task has a valid run in both arms',
    failures: results.filter((r) => r.agent && r.agent.timedOut).length,
    // Count any run the agent did not complete cleanly, not only spawn-level ones.
    // Counting only `r.error` reported 0 errors for 8 quota-blocked runs. A missing
    // `status` is not treated as a failure, so synthetic fixtures stay meaningful.
    agentErrors: results.filter((r) => r.agent && (r.agent.error || !agentExitedClean(r.agent)))
      .length,
    // Retries, not attempts: a first-try success is 0. A dry run has no attempts and
    // must not contribute a negative count.
    retries: results.reduce((n, r) => n + Math.max(0, ((r.agent && r.agent.attempts) || 1) - 1), 0),
  };
}

/** true when the agent process is known to have failed. */
function agentExitedClean(agent) {
  if (typeof agent.status === 'number') return agent.status === 0;
  if (agent.status === null) return false; // killed by signal or timeout
  return true; // unknown: do not invent a failure
}

function renderMarkdown(results, summary, meta, ablation) {
  const pct = (v) => (v === null ? 'n/a' : (v * 100).toFixed(0) + '%');
  const pp = (a, b) => (a === null || b === null ? 'n/a' : ((a - b) * 100).toFixed(0) + 'pp');
  const s = summary;
  const lines = [];

  lines.push('# Task-level eval — does the harness change the output?');
  lines.push('');
  lines.push('> **Generated file.** Regenerate with `npm run tasklift:write`.');
  lines.push('');
  lines.push('## Read this before quoting the number');
  lines.push('');
  lines.push(
    `**This is a pilot, not evidence.** ${s.tasks} tasks x 2 conditions x 1 trial. ` +
      'That has almost no statistical power. It proves the instrument works, and it ' +
      'is worth acting on the *per-check* failures, which are unambiguous. Do not ' +
      'quote the lift delta as a harness effect.'
  );
  lines.push('');
  lines.push(
    'Completion is the control. If the harness arm does not complete tasks at least ' +
      'as often, the conformance delta means nothing.'
  );
  lines.push('');
  if (s.voidedRuns > 0) {
    lines.push('## **Void run — this file contains no data**');
    lines.push('');
    lines.push(
      `${s.voidedRuns} of ${s.voidedRuns + s.validRuns} agent runs did not complete. Their checks ` +
        'scored worktrees that no agent ever touched. Each is excluded from its own cell only; ' +
        (s.lift === null
          ? 'the lift is withheld because a cell has no valid run.'
          : 'the remaining cells still produced a lift — treat it with the missing cell in mind.') +
        (s.voidedRuns >= s.validRuns
          ? ' **More runs failed than succeeded: treat every number below as unusable.**'
          : '')
    );
    lines.push('');
    lines.push('| Task | Condition | Exit | Attempts | Reported error |');
    lines.push('|---|---|---|---|---|');
    for (const r of results.filter((x) => x.voided)) {
      lines.push(
        `| ${r.taskId} | ${r.condition} | ${r.agent.status} | ${r.agent.attempts || 1} | ${r.agent.error || '(none reported)'} |`
      );
    }
    lines.push('');
  }
  if (ablation) {
    const w = ablation.without || {};
    const withPresent = (ablation.with && ablation.with.present) || [];
    lines.push('## Ablation check');
    lines.push('');
    lines.push(
      'The two arms must genuinely differ. If a harness file survived the delete, ' +
        'the "without" arm would be a "with" arm in disguise and the whole comparison ' +
        'would be void — silently, and in the direction that finds no effect. This is ' +
        'verified, not assumed.'
    );
    lines.push('');
    lines.push(`- **without** — ${w.ok ? 'all ' + w.checked + ' harness surfaces confirmed absent' : '**INCOMPLETE: still present — ' + (w.present || []).join(', ') + '**'}`);
    lines.push(`- **without** — ${w.fileCount} files remain in the ablated tree`);
    lines.push(`- **with** — ${withPresent.length} of ${(ablation.with && ablation.with.checked) || ABLATE_PATHS.length} harness surfaces present (expected: non-zero)`);
    lines.push('');
  }
  lines.push('## Result');  lines.push('');
  lines.push('| Measure | With harness | Without | Delta |');
  lines.push('|---|---|---|---|');
  lines.push(`| Task completion (control) | ${pct(s.completionWith)} | ${pct(s.completionWithout)} | ${pp(s.completionWith, s.completionWithout)} |`);
  lines.push(`| Convention conformance | ${pct(s.conformanceWith)} | ${pct(s.conformanceWithout)} | ${pp(s.conformanceWith, s.conformanceWithout)} |`);
  const liftText = s.lift === null ? `withheld — ${s.liftWithheld || 'insufficient data'}` : pp(s.conformanceWithout, s.conformanceWith);
  lines.push(`| **Lift on conformance** | — | — | **${liftText}** |`);
  lines.push('');
  lines.push(
    `Agent sessions: ${results.length} run, ${s.validRuns} measured, ${s.voidedRuns} void, ` +
      `${s.retries} retried after a transport failure.`
  );
  if (s.voidedRuns > 0) {
    lines.push('');
    lines.push(
      'A void run is excluded from its own cell, not from the whole experiment. ' +
        'A cell with no valid run still withholds the lift.'
    );
  }
  lines.push('');
  lines.push('## Per-task detail');
  lines.push('');
  for (const taskId of [...new Set(results.map((r) => r.taskId))]) {
    const w = results.find((r) => r.taskId === taskId && r.condition === 'with');
    const o = results.find((r) => r.taskId === taskId && r.condition === 'without');
    lines.push(`### ${taskId}`);
    lines.push('');
    if (w.voided || o.voided) {
      lines.push(
        '> **VOID** — the agent did not complete at least one condition of this task. The ' +
          'scores below describe an untouched worktree and are not a measurement.'
      );
      lines.push('');
    }
    lines.push(`- with: completion ${pct(w.completion)}, conformance ${pct(w.conformance)}`);
    lines.push(`- without: completion ${pct(o.completion)}, conformance ${pct(o.conformance)}`);
    lines.push('');
    lines.push('| Check | Class | With | Without |');
    lines.push('|---|---|---|---|');
    for (let i = 0; i < w.checks.length; i++) {
      const cw = w.checks[i];
      const co = o.checks[i] || { pass: false };
      lines.push(`| ${cw.label} | ${cw.class} | ${cw.pass ? 'pass' : '**FAIL**'} | ${co.pass ? 'pass' : '**FAIL**'} |`);
    }
    lines.push('');
  }
  lines.push('## Run identity');
  lines.push('');
  lines.push(`- commit: \`${meta.commit}\``);
  if (meta.manifest) lines.push(`- task manifest: \`${meta.manifest}\``);
  if (s.pairedTasks !== undefined && s.droppedPairs && s.droppedPairs.length > 0) {
    lines.push(
      `- dropped pairs (one arm had no valid run, so it cannot be compared): ${s.droppedPairs.join(', ')}`
    );
  }
  lines.push(`- agent binary: \`${meta.agentBin}\` (${meta.agentVersion})`);
  lines.push('- driver: `opencode run --standalone --auto` (fresh process, no parent session context)');
  lines.push(`- ablation: git worktree at the same commit with ${ABLATE_PATHS.join(', ')} deleted`);
  lines.push(`- agent timeouts: ${s.failures}, agent errors: ${s.agentErrors}`);
  lines.push('');
  lines.push('_The raw per-check results are in `docs/qa/TASK_LIFT.json`._');
  lines.push('');
  return lines.join('\n');
}

/** Failures worth retrying: the infrastructure, not the agent's work. */
const TRANSIENT_PATTERNS = [
  /HTTP 429/,
  /rate limit/i,
  /HTTP 5\d\d/,
  /ECONNRESET|ECONNREFUSED|ETIMEDOUT|EAI_AGAIN|ENOTFOUND/,
  /socket hang up|premature close|fetch failed/i,
];

/**
 * True when a failure is transport noise rather than a result.
 *
 * This distinction is the whole reason a retry loop is safe here. A 429 or a
 * dropped socket says nothing about the harness and should be retried. A non-zero
 * exit that is NOT transport noise is the agent's own outcome - it may have
 * refused, crashed, or finished - and retrying it would quietly replace a
 * measurement with a more flattering one.
 */
function isTransient(error, timedOut) {
  if (timedOut) return true;
  const e = String(error || '');
  if (!e) return false;
  return TRANSIENT_PATTERNS.some((re) => re.test(e));
}

const sleep = (ms) => Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);

/**
 * Run one agent session, retrying only transport failures.
 *
 * Retries are capped and spaced so a rate-limited provider is not hammered, which
 * would extend the outage it is recovering from.
 */
function runAgentWithRetry(root, prompt, { attempts = 3, backoffMs = 5000, timeoutMs } = {}) {
  let last = null;
  for (let i = 1; i <= attempts; i++) {
    last = runAgent(root, prompt, timeoutMs);
    if (last.ok) return { ...last, attempts: i };
    if (!isTransient(last.error, last.timedOut)) {
      return { ...last, attempts: i, retriedOut: false };
    }
    if (i < attempts) {
      const wait = backoffMs * i;
      process.stderr.write(
        `${PREFIX}   transport failure (${last.timedOut ? 'timeout' : last.error}), ` +
          `retry ${i}/${attempts - 1} in ${wait}ms\n`
      );
      sleep(wait);
    }
  }
  return { ...last, attempts, retriedOut: true };
}

function main(argv) {
  const dry = argv.includes('--dry');
  const keep = argv.includes('--keep');
  const onlyIdx = argv.indexOf('--only');
  const only = onlyIdx !== -1 ? argv[onlyIdx + 1] : null;
  const resume = argv.includes('--resume');
  const manifestPath = readFlag(argv, '--manifest') || MANIFEST;

  // Spending guard. Every agent session costs money, and the previous default was
  // to run them unless `--dry` was passed - so asking for a report cost 8 sessions.
  // Now the opposite: `--run` is required, and this message says so.
  if (!dry && !argv.includes('--run')) {
    process.stderr.write(
      `${PREFIX} refusing to start agent sessions without --run.\n` +
        `${PREFIX}   --dry    run the pipeline with no agent sessions (free)\n` +
        `${PREFIX}   --run    spend agent sessions: one real agent run per task per condition\n` +
        `${PREFIX} This guard exists because asking for a report previously ran the\n` +
        `${PREFIX} whole suite. Pass --dry to explore first.\n`
    );
    return 2;
  }

  const manifest = loadTasks(manifestPath);
  const tasks = only ? manifest.tasks.filter((t) => t.id === only) : manifest.tasks;
  if (tasks.length === 0) {
    process.stderr.write(`${PREFIX} ERROR - no task matched --only ${only}\n`);
    return 2;
  }

  const writeJsonEarly = readFlag(argv, '--out-json');
  let results = [];
  if (resume && writeJsonEarly && fs.existsSync(writeJsonEarly)) {
    try {
      const prior = JSON.parse(fs.readFileSync(writeJsonEarly, 'utf8'));
      if (Array.isArray(prior.results)) {
        results = prior.results;
        process.stderr.write(
          `${PREFIX} resume: ${results.length} prior run(s) from ${writeJsonEarly}\n`
        );
      }
    } catch (e) {
      process.stderr.write(`${PREFIX} resume: could not read prior results (${e.message}); starting fresh\n`);
    }
  }
  const done = new Set(results.map((r) => `${r.taskId}/${r.condition}`));

  const base = fs.mkdtempSync(path.join(os.tmpdir(), 'tasklift-'));
  const roots = { with: path.join(base, 'with'), without: path.join(base, 'without') };
  process.stderr.write(`${PREFIX} worktrees under ${base}\n`);

  let ablation = null;
  try {
    buildWorktree(roots.with, false);
    buildWorktree(roots.without, true);
    // Recorded so a reader can see the arms genuinely differ, rather than trusting
    // that the delete worked. `with` is expected to still hold the harness.
    ablation = {
      without: verifyAblation(roots.without),
      with: {
        present: ABLATE_PATHS.filter((p) => fs.existsSync(path.join(roots.with, p))),
        checked: ABLATE_PATHS.length,
        fileCount: listFiles(roots.with).length,
      },
    };

    for (const task of tasks) {
      for (const condition of ['with', 'without']) {
        const key = `${task.id}/${condition}`;
        if (done.has(key)) {
          process.stderr.write(`${PREFIX} ${key} ... skipped (already in results)\n`);
          continue;
        }
        process.stderr.write(`${PREFIX} ${key} ...\n`);
        const r = runTask(roots[condition], task, { dry });
        results.push({ ...r, condition });
        if (r.agent.error) process.stderr.write(`${PREFIX}   agent error: ${r.agent.error}\n`);
        if (r.voided) process.stderr.write(`${PREFIX}   VOID - excluded from every rate\n`);

        // Persist after EVERY run. An experiment that dies at task 6 of 8 must not
        // cost all eight sessions.
        if (writeJsonEarly) {
          fs.mkdirSync(path.dirname(writeJsonEarly), { recursive: true });
          fs.writeFileSync(
            writeJsonEarly,
            `${JSON.stringify({ tool: PREFIX, dry, ablation, results }, null, 2)}\n`,
            'utf8'
          );
        }
      }
    }
  } finally {
    if (keep) {
      process.stderr.write(`${PREFIX} --keep: worktrees left at ${base}\n`);
    } else {
      for (const r of Object.values(roots)) {
        try {
          removeWorktree(r);
        } catch {
          /* best effort */
        }
      }
      try {
        fs.rmSync(base, { recursive: true, force: true });
      } catch {
        /* best effort */
      }
    }
  }

  const minValid = Number(readFlag(argv, '--min-valid') || 1);
  const summary = summarize(results, { minValidPerCell: minValid, dry });
  const meta = {
    commit: firstLine(spawnSync('git', ['rev-parse', '--short', 'HEAD'], { cwd: PROJECT_ROOT, encoding: 'utf8' })),
    manifest: manifestPath,
    agentBin: resolveAgentBin(),
    agentVersion: firstLine(spawnSync(resolveAgentBin(), ['--version'], { encoding: 'utf8' })),
  };

  const payload = { tool: PREFIX, dry, meta, summary, ablation, results };

  if (argv.includes('--json')) {
    process.stdout.write(`${JSON.stringify(payload, null, 2)}\n`);
  } else {
    process.stdout.write(renderMarkdown(results, summary, meta, ablation));
  }

  // Emit both reports from this one pass. Running the eval twice to produce a JSON
  // and a Markdown copy would double the agent cost, which is the expensive part.
  const writeMd = readFlag(argv, '--out-md');
  const writeJson = readFlag(argv, '--out-json');
  if (writeMd || writeJson) {
    if (writeMd) {
      fs.mkdirSync(path.dirname(writeMd), { recursive: true });
      fs.writeFileSync(writeMd, renderMarkdown(results, summary, meta, ablation), 'utf8');
      process.stderr.write(`${PREFIX} wrote ${writeMd}\n`);
    }
    if (writeJson) {
      fs.mkdirSync(path.dirname(writeJson), { recursive: true });
      fs.writeFileSync(writeJson, `${JSON.stringify(payload, null, 2)}\n`, 'utf8');
      process.stderr.write(`${PREFIX} wrote ${writeJson}\n`);
    }
  }
  return 0;
}

/** Read `--flag value` from argv, or null when absent. */
function readFlag(argv, flag) {
  const i = argv.indexOf(flag);
  return i !== -1 && argv[i + 1] ? argv[i + 1] : null;
}

if (require.main === module) {
  try {
    process.exit(main(process.argv.slice(2)));
  } catch (e) {
    process.stderr.write(`${PREFIX} ERROR - ${e && e.message ? e.message : String(e)}\n`);
    process.exit(2);
  }
}

module.exports = {
  PREFIX,
  ABLATE_PATHS,
  MANIFEST,
  AGENT_TIMEOUT_MS,
  loadTasks,
  globToRegExp,
  compilePattern,
  readFlag,
  resolveAgentBin,
  firstLine,
  listFiles,
  matchFiles,
  verifyAblation,
  scoreControl,
  isTransient,
  seed,
  evaluateCheck,
  commitSubject,
  extractAgentError,
  runAgent,
  runTask,
  summarize,
  renderMarkdown,
  buildWorktree,
  removeWorktree,
};