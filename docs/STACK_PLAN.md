# HomeWorld – High-Level Stack Plan

This document aligns the development group on engine, plugins, services, and content pipeline. Scope is driven by the prototype vision and roadmap: explore → fight → build (Act 1), then bonds, co-op, day/night defense, and leaderboards (Act 2–3).

---

## Stack Overview

```mermaid
flowchart TB
  subgraph platform [Platform]
    Steam[Steam EA]
  end
  subgraph client [Game Client]
    UE[Unreal Engine 5.7]
  end
  subgraph world [World and Content]
    PCG[PCG Biomes]
    WP[World Partition]
  end
  subgraph gameplay [Combat and Building]
    GAS[GAS Combat]
    Build[Snap Building]
  end
  subgraph ai [AI and Systems]
    FamilyAI[Family AI]
    Mass[Mass or Epic replacement swarms]
    DayNight[Day/Night]
  end
  subgraph net [Multiplayer]
    SteamSockets[Steam Sockets]
  end
  subgraph services [Services]
    Leaderboards[Leaderboards]
  end
  Steam --> UE --> PCG
  UE --> WP
  PCG --> GAS
  GAS --> Build
  Build --> FamilyAI
  FamilyAI --> Mass
  Mass --> DayNight
  DayNight --> SteamSockets
  SteamSockets --> Leaderboards
```

---

## Layer 1 – Engine and Platform

- **Engine:** Unreal Engine 5.7. Open World template, World Partition.
- **Platform:** PC, Steam Early Access. No console in MVP.
- **Lock:** Engine 5.7 only; platform PC + Steam Early Access. Do not add engine or platform variants (e.g. console, different engine version) without team decision.
- **Rationale:** Single codebase; Lumen/Nanite for whimsical look; World Partition for large proc-gen realms.

---

## Layer 2 – World and Procedural Content

- **Core:** UE PCG (Procedural Content Generation) – already enabled in project.
- **Recommended:** PCG for biomes (forest first, then sand/crystal); portals or sublevels for “realm-hop.” Optional: PCGEx or Biome Core (free) for more complex graphs.
- **Phase:** Week 1 – forest biome; Weeks 3–4 – second biome. Load on-demand via World Partition/streaming.

---

## Layer 3 – Combat and Abilities

- **Core:** Gameplay Ability System (GAS) – already enabled. Base ability and attribute classes are in C++; specific abilities and data (e.g. 3 survivor skills) in Blueprint.
- **Recommended:** Blueprint-first (Ninja GAS Blueprint or similar) for 3 survivor skills in Act 1; extend for needs/buffs in Act 2 (family sim). Optional paid: Advanced ARPG Template (~$50) for PoE-style trees/combos.
- **Phase:** Week 1 – 3 skills; Week 2 – GAS for relationship/needs if desired.
- **Week 2 extension (needs/relationship):** Add needs or relationship attributes to `UHomeWorldAttributeSet`, or introduce a second attribute set (e.g. `UHomeWorldNeedsAttributeSet`) and add it to the same `AbilitySystemComponent`. No mandatory second set; extend existing or add as needed.

## Layer 4 – Building and Home

- **Recommended:** Blueprint-based snap/placement; optional Behavior or State Trees for “home” logic. No mandatory plugin; Week 1 = basic placement or placeholder.
- **Phase:** Week 1 – minimal build/claim; Week 2 – home as first-class space for duo and night defense.
- **Agentic building (Week 2+):** Player places build orders (holograms) via placement API; family agents detect (EQS), gather resources, claim Smart Object, complete build. Uses Mass + State Tree BUILD branch + Smart Objects. See [AGENTIC_BUILDING.md](tasks/AGENTIC_BUILDING.md) and C++ bases [AHomeWorldBuildOrder](../Source/HomeWorld/HomeWorldBuildOrder.h), [AHomeWorldResourcePile](../Source/HomeWorld/HomeWorldResourcePile.h).

---

## Layer 5 – AI and Simulation

- **Family/NPCs:** Behavior Trees or State Trees (UE built-in); needs/morale can use GAS attributes. Use **AHomeWorldAIController** (C++) as the controller base for actor-based NPCs (e.g. key story characters); assign BT/ST in Blueprint.
- **Scalable agents/swarms:** Use **UE 5.7 recommended Mass Entity + Mass AI** (MassEntity, MassGameplay, MassAI, StateTree, ZoneGraph, SmartObjects) for 5–100+ family gatherers/defenders and night swarms. This is Epic's current stack; no deprecated tech. See [KNOWN_ERRORS.md](KNOWN_ERRORS.md) for plugin list and [docs/tasks/FAMILY_AGENTS_MASS_STATETREE.md](tasks/FAMILY_AGENTS_MASS_STATETREE.md) for Week 2 setup.
- **Phase:** Week 2 – first family agents (Mass config + State Tree + spawner); Weeks 3–4 – roles (Protector/Healer trees), needs sim (GAS attributes or Mass processor).

---

## Layer 6 – Day/Night and Systems

- **Recommended:** Day/Night sequencer (plugin or custom); PCG or level logic for night spawns. Tied to “family defends at night” pillar.
- **Tech choice:** Day/night uses **DaySequence** plugin (no custom sequencer). No implementation required until Week 2+.
- **Phase:** Weeks 3–4 (Alpha).
- **TimeOfDay implementation:** Game code reads phase and time via **UHomeWorldTimeOfDaySubsystem** (GetCurrentPhase, GetNormalizedTime). Drive values from DaySequence in level Blueprint (e.g. Event Tick or DaySequence callback), or implement in C++ with DaySequence plugin when ready.

---

## Layer 7 – Multiplayer and Co-op

- **Recommended:** Steam Sockets (replaces SteamCore/Steam Sessions) for 2–8p; replication for roles, buffs, and state. Optional: AWS GameLift (free tier) for dedicated servers if needed later.
- **Tech choice:** Multiplayer uses **SteamSockets** (replaces SteamCore). No implementation required until Week 2+.
- **Phase:** Week 2 – 2p; Weeks 3–4 – up to 8p clans.

---

## Layer 8 – Leaderboards and Services

- **Recommended:** Steam API (free) for leaderboards; or SteamLead (~$20) for turnkey. Score formula: (family size × happiness) + clears.
- **Phase:** Weeks 3–4; polish post-alpha.

---

## Content Pipeline and Assets

- **Recommended:** FAB for character(s) (e.g. survival char); Quixel for biomes/vegetation; UE Marketplace / Quixel for stylized fantasy where needed. Pipeline: import → Blueprint/PCG; no custom engine.
- **Phase:** Week 1 – FAB + Quixel for forest; expand in later phases.

---

## Phase–Tech Map

| Phase      | World/PCG | Combat/GAS | Building | AI   | Day/Night | Multiplayer | Leaderboards | Assets |
| ---------- | --------- | ---------- | -------- | ---- | --------- | ----------- | ------------ | ------ |
| Pre-prod   | —         | —          | —        | —    | —         | —           | —            | —      |
| Week 1     | In use    | In use     | In use   | —    | —         | —           | —            | In use |
| Week 2     | In use    | In use     | In use   | In use | —       | In use      | —            | In use |
| Weeks 3–4  | In use    | In use     | In use   | In use | In use   | In use      | In use       | In use |
| Post-alpha | In use    | In use     | In use   | In use | In use   | In use      | In use       | In use |

---

## Budget and “Free First”

- **Free:** UE5, PCG, GAS, Steam API, FAB/Quixel free assets, Open World template. Mass/replacement when adding swarms.
- **Optional paid:** Advanced ARPG Template (~$50), SteamLead (~$20), GameLift if needed. Total optional ~$70–150; time is the main cost.

---

## References

- [PROTOTYPE_VISION.md](PROTOTYPE_VISION.md) – theme, Act 1 focus, Week 1 playtest goal
- [../ROADMAP.md](../ROADMAP.md) – phases, pillars, campaign
- [TASKLIST.md](TASKLIST.md) – Current task list (links to task docs in docs/tasks/)
- [SETUP.md](SETUP.md) – developer setup checklist
- [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md) – content paths contract

---

## Implementation status (core tech)

Core technology foundations implemented per bare-bones stack plan (contracts, base classes, stubs). Content (abilities, buildables, AI behaviors, leaderboard data) is out of scope.

| Layer | Status | Notes |
|-------|--------|--------|
| 1 – Engine/Platform | Done | Lock in docs; Main map WP; plugins in .uproject. |
| 2 – World/PCG | Done | PCG enabled; CONTENT_LAYOUT paths. |
| 3 – GAS | Done | Base classes; DefaultAbilities granting; Week 2 needs extension documented. |
| 4 – Building | Done | GetPlacementHit + GetPlacementTransform. |
| 5 – AI | Done | AHomeWorldAIController stub; Mass Entity + Mass AI (UE 5.7 recommended) for family/swarm agents, see FAMILY_AGENTS_MASS_STATETREE.md. |
| 6 – Day/Night | Done | UHomeWorldTimeOfDaySubsystem stub; implementation via DaySequence documented. |
| 7 – Multiplayer | Done | UHomeWorldSessionSubsystem stub. |
| 8 – Leaderboards | Done | UHomeWorldLeaderboardSubsystem stub. |
