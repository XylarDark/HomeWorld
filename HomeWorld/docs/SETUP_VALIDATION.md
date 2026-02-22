# HomeWorld – Setup Validation Checklist

Use this to confirm first-phase setup is complete before starting Week 1.

---

## 1. In-Repo Checks (No Editor Required)

- [ ] **Plugins:** In `HomeWorld.uproject`, the `Plugins` array includes `PCG`, `GameplayAbilities`, `MassEntity`, `EnhancedInput`, `SteamSockets` (co-op; replaces SteamCore), and `DaySequence` (or `TimeOfDay` if that is the actual engine name), each with `"Enabled":true`.
- [ ] **Open World default map:** In `Config/DefaultEngine.ini`, under `[/Script/EngineSettings.GameMapsSettings]`, `GameDefaultMap` is set to the project default map (e.g. `/Game/HomeWorld/Maps/Main.Main` or `/Engine/Maps/Templates/OpenWorld`).
- [ ] **Prototype vision:** `docs/PROTOTYPE_VISION.md` exists and contains theme, Act 1 focus, Week 1 playtest goal, tech spine, success criteria.
- [ ] **Developer setup:** `docs/SETUP.md` exists and lists Engine, Project, Plugins, Free assets, World, Roles.
- [ ] **Approval gate:** `docs/TEAM_APPROVAL_CHECKLIST.md` exists with checkboxes for Vision/Theme, Pillars, Campaign, Tech, Roadmap, Next.
- [ ] **Week 1 tasks:** `docs/WEEK1_TASKS.md` exists with sections Tech, Content, Missions, Art/Story, Playtest.
- [ ] **Roadmap:** `ROADMAP.md` exists and describes Phase 0 and Phase 1 (Week 1).

---

## 2. C++ and Default Pawn (Programmatic-by-Default)

- [ ] **C++ module builds:** After generating Visual Studio project files, the **HomeWorld** and **HomeWorldEditor** targets build successfully (see [SETUP.md](SETUP.md)#building-c).
- [ ] **Default game mode:** In **Project Settings → Maps & Modes**, **Default GameMode** is set to **HomeWorldGameMode** (C++) so the default pawn is the C++ character. Alternatively confirm `Config/DefaultEngine.ini` has `GlobalDefaultGameMode=/Script/HomeWorld.HomeWorldGameMode`.
- [ ] **Default pawn class:** Default Pawn Class is **HomeWorldCharacter** (or a Blueprint child of it). Movement and camera are driven by C++ and Enhanced Input (see [CONVENTIONS.md](CONVENTIONS.md)#input-setup-enhanced-input).
- [ ] **PIE:** In Play In Editor, the character moves with WASD and the camera follows mouse look (third-person). If not, create and assign **IA_Move**, **IA_Look**, and **IMC_Default** per [CONVENTIONS.md](CONVENTIONS.md).

## 3. Developer Checks (Require Human / Editor)

- [ ] UE 5.4+ (or 5.7) is installed and the project opens without plugin errors.
- [ ] In Editor: **Edit > Plugins** shows PCG, Gameplay Abilities, Mass Entity, Enhanced Input, Steam Sockets (co-op), and Day Night Sequencer enabled. Steam Sockets is required for Week 2 co-op.
- [ ] FAB/Quixel assets (or equivalents) are acquired and available in the project.
- [ ] Team has run through [TEAM_APPROVAL_CHECKLIST.md](TEAM_APPROVAL_CHECKLIST.md) and committed to Week 1.

---

## 4. Next Step

When all above are checked, setup is complete; proceed to [WEEK1_TASKS.md](WEEK1_TASKS.md) and the Week 1 execution plan (validate → PCG forest → GAS 3 skills → building → playable map → Mission 1 → Mission 2 → Mission 3 → playtest).
