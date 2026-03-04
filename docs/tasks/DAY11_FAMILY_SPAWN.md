# Day 11 [2.1]: Family spawn in homestead

**Goal:** Spawn **N family members at start** in the homestead (DemoMap), with a **tag or role ID per member** so later days (e.g. Day 15 role assignment and persistence) can identify each agent.

**See also:** [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md) Day 11, [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md), [DEMO_MAP.md](../DEMO_MAP.md).

---

## 1. Prerequisites

- **Week 2 plugins** enabled: MassEntity, MassGameplay, MassAI, StateTree, ZoneGraph, SmartObjects. See [SETUP.md](../SETUP.md).
- **Folders:** Run `Content/Python/ensure_week2_folders.py` in Editor so `/Game/HomeWorld/Mass/`, `AI/`, `ZoneGraph/`, `SmartObjects/`, `Building/` exist.
- **Level:** Open **DemoMap** (`/Game/HomeWorld/Maps/DemoMap`) — family spawn happens here.

---

## 2. Family agents base (FAMILY_AGENTS Steps 2–4)

Follow [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md) in order.

### Step 2 — MEC_FamilyGatherer

1. **Content Browser** → **Content → HomeWorld → Mass**. Right-click → **Miscellaneous → Mass Entity Config** (or **Mass → Mass Entity Config**). Name **MEC_FamilyGatherer** (or create it via the commandlet below).
2. **Add representation trait via commandlet (recommended):** The Editor module links **MassRepresentation** so the CreateMEC commandlet can add the representation trait. With the Editor **closed**, run: `UnrealEditor.exe HomeWorld.uproject -run=HomeWorldEditor.CreateMEC [Path=/Game/HomeWorld/Mass/MEC_FamilyGatherer]`. This adds **MassRepresentationFragmentTrait** (and other traits) to the MEC. Rebuild with `Build-HomeWorld.bat` first if you changed the Editor module.
3. **Details → Traits → Add** (for any traits not added by the commandlet): **StateTree**, **Movement**, **ZoneGraph Navigation** (or **NavMesh Navigation**). Optional: **Avoidance**, **Agent Capsule Collision Sync**, etc.
4. **StateTree trait:** Set **State Tree** = **ST_FamilyGatherer** (create in Step 3 first if needed).
5. **Representation trait (mesh):** If the commandlet added the representation trait, open **MEC_FamilyGatherer** and in Details find the **Mass Representation Fragment** (or representation) section. Set **Static Mesh** to a placeholder (e.g. cube). To get a cube or other engine mesh: follow [UE57_EDITOR_UI.md](../UE57_EDITOR_UI.md) (Show Engine Content, then browse or search for Cube/Shape). Set **Scale** = **1.0**. If no representation trait is present, add MassRepresentation to the Editor module (see [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) MEC mesh entry), rebuild, and run the commandlet again. Save.

### Step 3 — ST_FamilyGatherer

1. **Content Browser** → **Content → HomeWorld → AI**. Right-click → **AI → State Tree**.
2. Name **ST_FamilyGatherer**, save under `/Game/HomeWorld/AI/`. Open it.
3. Root: **Selector**. Add at least one branch for Day 11 (e.g. **Idle** → **Wander** with MoveTo random point, or a single “Stand” state) so agents spawn and are visible; full gather/sleep can come later.
4. **Blackboard:** HomePos (Vector); optionally Hunger, IsNight for later.
5. **MEC_FamilyGatherer** → **StateTree** trait → set **State Tree** = **ST_FamilyGatherer**. **Compile** State Tree.

### Step 4 — Spawn in level

**Option A (script):** With DemoMap open, run `Content/Python/place_mass_spawner_demomap.py` (Tools → Execute Python Script or MCP). Config from `demo_map_config.json` (mass_spawner_position, mass_spawner_spawn_count). If Config/Spawn count did not apply via script, set in Details (see Option B).

**Option B (manual):** Open **DemoMap**. **Modes** → search **Mass Spawner** → drag into level. Select Mass Spawner. **Details:** **Config** = MEC_FamilyGatherer, **Spawn count** = N (e.g. 5–10), **Bounds** around homestead/play area so agents spawn in view.

**Representation mesh:** Run `Content/Python/set_mec_representation_mesh.py` to set Cube on MEC representation trait; or open MEC_FamilyGatherer and set Static Mesh in Details (see Step 2.5).

4. **ZoneGraph:** Add minimal navigation (lanes or nav) so agents can move; if not set up yet, a minimal State Tree without movement is enough for “spawn and visible.”
5. **Smart Objects** (gather/sleep): Optional for Day 11; add in Day 12+ if needed.

---

## 3. Tag or role ID per member

Day 15 (role assignment and persistence) needs a way to identify each family member.

- **Option A (Mass):** If your UE 5.7 Mass setup supports per-entity data, add a **Mass tag** or **fragment** (e.g. FamilyMember tag + RoleID or Index fragment) to MEC_FamilyGatherer so each spawned entity has an identity. Document the trait/fragment names in this doc or [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) if the API differs.
- **Option B (fallback):** If the Mass spawner does not expose per-entity tag in this setup, document: “Day 11: spawn N agents; Day 15 will add role assignment (e.g. by spawn index or via a subsystem).” Ensure **spawn count** and **spawn location** are correct; identity can be added when implementing persistence.

---

## 4. Validation

- **PIE** on DemoMap: press Play, confirm **N family agents** appear in the spawn bounds.
- Agents **visible** (representation-trait mesh); if State Tree + ZoneGraph are set up, agents **move** or idle.
- **Success:** N agents spawn at start without player input.

---

## 5. After Day 11

- Check off Day 11 in [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md).
- Update [DAILY_STATE.md](../workflow/DAILY_STATE.md): Yesterday = Day 11 family spawn; Today = Day 12 (Role: Protector).
- Append [SESSION_LOG.md](../SESSION_LOG.md) with what was done.
- Day 12: Add Role: Protector (State Tree/combat); see [FAMILY_AGENTS_MASS_STATETREE.md](FAMILY_AGENTS_MASS_STATETREE.md).
