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
