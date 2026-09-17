#!/usr/bin/env node
/**
 * UE host doctor wrapper (HR2-A).
 * Runs DevEnvTemplate doctor, then treats DOCTOR_POLICY accepted declines as non-fatal.
 * Exit 0 when only accepted declines remain; exit 1 when any other critical is present.
 */
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const projectRoot = path.resolve(__dirname, '..');
const declinesPath = path.join(projectRoot, 'config', 'doctor-ue-declines.json');
const reportPath = path.join(projectRoot, '.devenv', 'health-report.json');
const doctorCli = path.join(
  projectRoot,
  'DevEnvTemplate',
  'dist',
  'scripts',
  'doctor',
  'cli.js'
);

function loadDeclines() {
  if (!fs.existsSync(declinesPath)) {
    console.error(`doctor:ue — missing decline registry: ${declinesPath}`);
    process.exit(2);
  }
  const data = JSON.parse(fs.readFileSync(declinesPath, 'utf8'));
  if (!Array.isArray(data.acceptedCriticalMessages) || data.acceptedCriticalMessages.length === 0) {
    console.error('doctor:ue — acceptedCriticalMessages must be a non-empty array');
    process.exit(2);
  }
  return new Set(data.acceptedCriticalMessages);
}

function readCriticalMessages() {
  if (!fs.existsSync(reportPath)) {
    return null;
  }
  try {
    const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
    const critical = Array.isArray(report.critical) ? report.critical : [];
    return critical.map((item) => item.message).filter(Boolean);
  } catch (err) {
    console.error(`doctor:ue — failed to parse ${reportPath}: ${err.message}`);
    return null;
  }
}

function main() {
  if (!fs.existsSync(doctorCli)) {
    console.error('doctor:ue — DevEnvTemplate doctor CLI not built. Run: npm run doctor:build');
    process.exit(2);
  }

  const accepted = loadDeclines();
  const doctorArgs = [doctorCli, '--project-root', projectRoot, ...process.argv.slice(2)];

  const result = spawnSync(process.execPath, doctorArgs, {
    cwd: projectRoot,
    stdio: 'inherit',
    env: process.env,
  });

  const doctorExit = result.status ?? 1;
  const criticalMessages = readCriticalMessages();

  if (criticalMessages === null) {
    process.exit(doctorExit);
  }

  const declined = [];
  const actionable = [];

  for (const message of criticalMessages) {
    if (accepted.has(message)) {
      declined.push(message);
    } else {
      actionable.push(message);
    }
  }

  console.log('');
  console.log('--- doctor:ue (UE host) ---');
  console.log(`Raw doctor exit: ${doctorExit}`);
  console.log(`Critical total: ${criticalMessages.length}`);
  console.log(`Accepted declines (non-fatal): ${declined.length}`);
  if (declined.length > 0) {
    for (const message of declined) {
      console.log(`  ✓ ${message}`);
    }
  }
  if (actionable.length > 0) {
    console.log(`Actionable criticals: ${actionable.length}`);
    for (const message of actionable) {
      console.log(`  ✗ ${message}`);
    }
    console.log('doctor:ue exit: 1 (new criticals — see DOCTOR_POLICY.md)');
    process.exit(1);
  }

  if (doctorExit !== 0 && declined.length === criticalMessages.length && criticalMessages.length > 0) {
    console.log('doctor:ue exit: 0 (only accepted declines remain)');
    process.exit(0);
  }

  console.log(`doctor:ue exit: ${doctorExit}`);
  process.exit(doctorExit);
}

main();
