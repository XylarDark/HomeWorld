# Day 15 [2.5]: Role assignment and persistence

**Goal:** Store **role per family member** so the game knows who is Protector, Healer, or Child (and can persist across save/load). Identity can be by spawn index, tag, or fragment.

**See also:** [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md) Day 15, [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md), [DAY11_FAMILY_SPAWN.md](DAY11_FAMILY_SPAWN.md), [DAY14_ROLE_CHILD.md](DAY14_ROLE_CHILD.md).

---

## 1. Prerequisites

- **Days 11–14 done:** Family spawn, Protector, Healer, Child roles defined (State Tree branches and/or GAS abilities).

---

## 2. Storage options

| Option | Description |
|--------|-------------|
| **A. Mass tag/fragment** | Add a **Role** fragment or tag to MEC (e.g. Role_Protector, Role_Healer, Role_Child). Each spawned entity gets role from spawner variant or from a **Mass Spawner** per role (one spawner per MEC). |
| **B. Spawn index → role table** | At spawn time, assign role by index (e.g. 0=Protector, 1=Healer, 2=Child, 3=Child, …). Store in a **Game State** or **subsystem** (e.g. `UHomeWorldFamilySubsystem`) that maps EntityID or Index → Role. |
| **C. SaveGame** | When saving, write an array of roles (by stable ID or index) into **USaveGame**; on load, reapply roles to spawned family members. |

---

## 3. Minimal implementation (design)

1. **Define role enum or FName set:** e.g. `Protector`, `Healer`, `Child` (and optional `Gatherer`).
2. **At spawn (Day 11):** Either use multiple Mass Spawners (one per role, each with its own MEC or same MEC + different initial tag), or a single spawner + a **processor** that sets a **Role** fragment/tag by spawn index (e.g. index % 3).
3. **Persistence (optional for Day 15):** Add **UHomeWorldFamilySubsystem** (Game Instance subsystem): `TMap<FName, FName> MemberRoles` (member ID → role). On save, serialize this map; on load, restore and apply to spawned entities. If Mass does not expose per-entity ID for SaveGame, use **spawn order** and store `TArray<FName> RoleBySpawnIndex`.
4. **State Tree / behavior:** Already keyed off IsChild, IsNight, etc.; ensure **IsChild** (and optional IsProtector, IsHealer) are set from the stored role so the correct branch runs.

---

## 4. Validation

- **PIE:** Spawn N family members; each has a consistent role (tag or subsystem entry). After (optional) save/load, roles are restored.
- **Success:** Role assignment is deterministic and (if implemented) persists across save/load.

---

## 5. After Day 15

- Update [DAILY_STATE.md](../workflow/DAILY_STATE.md): Yesterday = Day 15; Today = Day 16 (Planetoid level).
- Check off Day 15 in [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md).
- Append [SESSION_LOG.md](../SESSION_LOG.md). Phase 2 (Family) complete; Phase 3 (Planetoid) next.
