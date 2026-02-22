# RealmBond – Setup Validation Checklist

Use this to confirm first-phase setup is complete before starting Week 1.

---

## 1. In-Repo Checks (No Editor Required)

- [ ] **Plugins:** In `HomeWorld.uproject`, the `Plugins` array includes `PCG`, `GameplayAbilities`, and `MassEntity`, each with `"Enabled":true`.
- [ ] **Open World default map:** In `Config/DefaultEngine.ini`, under `[/Script/EngineSettings.GameMapsSettings]`, `GameDefaultMap=/Engine/Maps/Templates/OpenWorld`.
- [ ] **Prototype vision:** `docs/PROTOTYPE_VISION.md` exists and contains theme, Act 1 focus, Week 1 playtest goal, tech spine, success criteria.
- [ ] **Developer setup:** `docs/SETUP.md` exists and lists Engine, Project, Plugins, Free assets, World, Roles.
- [ ] **Approval gate:** `docs/TEAM_APPROVAL_CHECKLIST.md` exists with checkboxes for Vision/Theme, Pillars, Campaign, Tech, Roadmap, Next.
- [ ] **Week 1 tasks:** `docs/WEEK1_TASKS.md` exists with sections Tech, Content, Missions, Art/Story, Playtest.
- [ ] **Roadmap:** `ROADMAP.md` exists and describes Phase 0 and Phase 1 (Week 1).

---

## 2. Developer Checks (Require Human / Editor)

- [ ] UE 5.4+ (or 5.7) is installed and the project opens without plugin errors.
- [ ] In Editor: **Edit > Plugins** shows PCG, Gameplay Abilities, and Mass Entity enabled.
- [ ] FAB/Quixel assets (or equivalents) are acquired and available in the project.
- [ ] Team has run through [TEAM_APPROVAL_CHECKLIST.md](TEAM_APPROVAL_CHECKLIST.md) and committed to Week 1.

---

## 3. Next Step

When all above are checked, setup is complete; proceed to [WEEK1_TASKS.md](WEEK1_TASKS.md) and the Week 1 execution plan (validate → PCG forest → GAS 3 skills → building → playable map → Mission 1 → Mission 2 → Mission 3 → playtest).
