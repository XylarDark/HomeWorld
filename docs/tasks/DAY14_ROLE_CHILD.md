# Day 14 [2.4]: Role — Child

**Goal:** Define the **Child** role: non-combat or limited combat; follow player or stay at safe nodes. Used for family agents that should not engage in combat (e.g. child character).

**See also:** [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md) Day 14, [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md), [DAY11_FAMILY_SPAWN.md](DAY11_FAMILY_SPAWN.md), Day 15 (role assignment and persistence).

---

## 1. Prerequisites

- **Day 11 done:** MEC_FamilyGatherer, ST_FamilyGatherer, Mass Spawner on DemoMap.
- **Day 15** will store role per member (e.g. Role_Child tag or fragment); this day defines behavior only.

---

## 2. Child role behavior (design)

| Aspect | Child role |
|--------|------------|
| **Combat** | No combat or minimal (flee only). Do not grant GA_ProtectorAttack or offensive abilities. |
| **Follow** | Prefer following the player (MoveTo player when not at safe node). |
| **Safe nodes** | When at a designated safe node (e.g. home, camp), stay there (Idle/Wander in bounds). |
| **Identity** | Tag or fragment **Role_Child** (or role enum Child) for Day 15 persistence and to drive which State Tree branch runs. |

---

## 3. Implementation options

### Option A — State Tree only (minimal)

1. **ST_FamilyGatherer** (or a dedicated ST_FamilyChild if you split by role): add a **Child?** branch.
2. **Condition:** Blackboard **IsChild** (Bool) or tag **Role_Child** (set per entity from spawn index or Day 15).
3. **Tasks:** **Follow** = MoveTo player (Blackboard **PlayerActor** or **PlayerLocation**); **SafeNode** = MoveTo **SafeNodeLocation** and Idle. Order: if at safe node → Idle; else → MoveTo player (follow).
4. **Blackboard:** Add **PlayerActor** (Object), **PlayerLocation** (Vector), **SafeNodeLocation** (Vector). A Mass processor or game code sets PlayerActor from the local player pawn; SafeNodeLocation from home/camp.
5. **No GAS ability** for Child (no attack/heal required).

### Option B — Separate State Tree (ST_FamilyChild)

1. Create **ST_FamilyChild** in `/Game/HomeWorld/AI/`: root Selector with **Follow** (MoveTo player) and **Idle at safe node** (MoveTo safe, then Stand).
2. Create **MEC_FamilyChild** (copy of MEC_FamilyGatherer or new config) with **State Tree** = ST_FamilyChild; no combat traits.
3. Mass Spawner: use a second spawner with MEC_FamilyChild for child entities, or assign role at spawn and switch ST at runtime (Day 15).

---

## 4. Validation

- **PIE:** With at least one agent tagged or configured as Child, the agent does not attack; it follows the player or stays at the safe node.
- **Success:** Child agents are visually distinct (optional) and behaviorally non-combat; follow/safe logic runs when Blackboard is set.

---

## 5. After Day 14

- Update [DAILY_STATE.md](../workflow/DAILY_STATE.md): Yesterday = Day 14 (Child); Today = Day 15 (Role assignment and persistence).
- Check off Day 14 in [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md).
- Append [SESSION_LOG.md](../SESSION_LOG.md). Day 15 will add role storage (tag/fragment/subsystem) so Child (and Protector/Healer) persist.
