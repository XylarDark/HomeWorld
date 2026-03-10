# Agent task list (vision-aligned)

**Purpose:** Single ordered list for agents to "fetch next task." Derived from [VISION.md](VISION.md), [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md), and [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md). Agents take the first **pending** task; update status as tasks complete.

**Convention:** `pending` | `in_progress` | `completed` | `blocked`

---

## V1. Week 1 playtest sign-off (vision gate)

- **goal:** Survive 3 missions: crash → scout → boss → claim home; explore → fight → build playable; doc or checklist updated.
- **success criteria:** Playtest criteria from VISION met; sign-off or checklist in DAY5_PLAYTEST_SIGNOFF / VERTICAL_SLICE_CHECKLIST.
- **doc:** [VISION.md](VISION.md), [DAY5_PLAYTEST_SIGNOFF.md](../tasks/DAY5_PLAYTEST_SIGNOFF.md), [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md).
- **status:** completed

---

## V2. Lock vertical slice (one moment + one corner)

- **goal:** Moment and corner chosen and locked in PROTOTYPE_SCOPE; pre-demo checklist in VERTICAL_SLICE_CHECKLIST run (or documented).
- **success criteria:** PROTOTYPE_SCOPE has chosen moment and corner; pre-demo checklist completed or documented.
- **doc:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md).
- **status:** completed

---

## V3. Close State Tree gap (Defend/Night branch)

- **goal:** ST_FamilyGatherer has Night? branch and Defend behavior; or GUI automation script run + refs; or manual steps documented and gap log updated.
- **success criteria:** State Tree Defend/Night branch present and validated (e.g. PIE with hw.TimeOfDay.Phase 2), or AUTOMATION_GAPS Gap 2 updated with solution/manual steps.
- **doc:** [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) Gap 2, [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md), [FAMILY_AGENTS_MASS_STATETREE.md](../tasks/FAMILY_AGENTS_MASS_STATETREE.md).
- **status:** completed

---

## V4. Act 2 prep: day/night Defend at home

- **goal:** TimeOfDay drives Defend; family at homestead; optional night encounter.
- **success criteria:** PIE with hw.TimeOfDay.Phase 2 validates family Defend; doc or stub for night spawn.
- **doc:** [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md) N3, [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md), [VISION.md](VISION.md) Act 2.
- **status:** pending

---

## V5. Deferred: one of (agentic building / SaveGame / death→spirit / boss reward)

- **goal:** Implement at least one deferred item: full agentic building flow, role persistence across sessions, spirit roster on death, or boss GAS + reward.
- **success criteria:** At least one implemented and verified (e.g. full agentic flow, SaveGame load/save roles, spirit on death, boss GAS + reward).
- **doc:** [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) T10, [DAY10_AGENTIC_BUILDING.md](../tasks/DAY10_AGENTIC_BUILDING.md), [DAY15_ROLE_PERSISTENCE.md](../tasks/DAY15_ROLE_PERSISTENCE.md), [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md) Day 21/25.
- **status:** pending

---

## V6. Steam EA prep (optional)

- **goal:** Ship-ready packaged build; optional Steam depots and store page checklist.
- **success criteria:** Packaged build runs; checklist for store page if applicable.
- **doc:** [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md) N4, [SETUP.md](../SETUP.md).
- **status:** pending

---

**Order:** V1 → V2 → V3 → V4 → V5 → V6. See [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) for full context and [CYCLE_TASKLIST.md](CYCLE_TASKLIST.md) for prior cycle (T1–T9, N1–N4).
