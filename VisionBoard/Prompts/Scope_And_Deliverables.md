# Scope and Deliverables — Vision Board

Use this when generating prompts or design that depend on project scope, tech constraints, or MVP/vertical-slice definitions. Content that doesn’t fit Aesthetics, Gameplay Mechanics, World Lore, World Progression, World Building, or Character Creation. Source: [../Core/VISION.md](../Core/VISION.md), [../Core/PROTOTYPE_SCOPE.md](../Core/PROTOTYPE_SCOPE.md), [../Core/STACK_PLAN.md](../Core/STACK_PLAN.md).

---

## Scope lock

- **Engine:** Unreal Engine 5.7 only. Do not add engine or platform variants without team decision.
- **Platform:** PC + Steam Early Access. No console in MVP.
- **Campaign:** 8–12h total; Act 1 solo (2–3h) → Act 2 duo (3–4h) → Act 3 full co-op (3–5h+).

---

## MVP deliverable (what “done” means)

The MVP is **done** when we have a **marketing-ready** slice:

- **One playable loop** (explore → fight → build).
- **One moment** (e.g. claiming the homestead after the first boss, or first family member rescued).
- **One beautiful corner** (e.g. homestead compound).
- **Good-looking marketing material** (screenshots, key art, capsule, short video).

**Launching on Steam is not required for the MVP deliverable** — Steam store and distribution are post-MVP when we choose to ship. **Assets and visuals are mandatory** for the MVP so we can produce that marketing material.

---

## Vertical slice (locked choices)

- **Chosen moment:** **Claim homestead** — player places first home asset (P) after exploring/harvesting.
- **Chosen corner:** **Homestead compound** — DemoMap/Homestead with placed buildings + resource nodes + PCG.
- **By end of 30 days:** Choose one moment and one beautiful corner to polish for a showable vertical slice and/or short demo video (above reflects the locked choice).

---

## Tech and stack (summary)

- **Engine:** Unreal Engine 5.7. Open World, World Partition.
- **Platform:** PC, Steam Early Access. No console in MVP.
- **World:** PCG biomes (forest first, then sand/crystal); portals/sublevels for realm-hop.
- **Combat:** GAS (3 skills Act 1; extend for needs/buffs in Act 2).
- **Building:** Snap/placement; build orders + family agents (Mass + State Tree + Smart Objects) in Week 2+.
- **AI:** Mass Entity + Mass AI (UE 5.7 recommended) for family/swarm agents; AHomeWorldAIController for actor-based NPCs.
- **Day/Night:** DaySequence; TimeOfDay subsystem stub.
- **Multiplayer:** Steam Sockets; 2p Week 2, up to 8p later.
- **Leaderboards:** Steam API or SteamLead; Weeks 3–4.

Full stack (layers, phases, implementation status): [../Core/STACK_PLAN.md](../Core/STACK_PLAN.md).

---

## Prototype and gates

- **MVP (Minimum Viable Product):** Smallest playable version that validates the core promise (one compelling mechanic, minimal art/content). Goal: test fun and engagement early.
- **Vertical slice:** A short, complete section of the game at near-final quality: one clear gameplay loop, one memorable moment, one polished “beautiful corner” to show capability. Used for stakeholders, playtesters, or funding.
- **Week 1 playtest gate:** Survive 3 missions: crash → scout → boss → claim home. Do not start Homestead/Family phases until explore → fight → build is playable and tested.
- **MVP tutorial gate:** The one-day tutorial loop (wake → breakfast → love task → game with child → gather → lunch → dinner → bed → spectral combat → boss → wake to family taken) is the target for the MVP tutorial.

---

## Asset list by type (prototype reference)

| Type | Needed for prototype | Notes |
|------|----------------------|--------|
| Player | 1 character, movement, GAS | FAB / Primitive / Polygon; see STACK_PLAN Free assets. |
| Enemies | 1+ types for scout/boss | Placeholder or free pack. |
| Allies (family) | Protector, Healer, Child | Primitive Characters or Polygon. |
| Buildings | Homestead compound, outbuildings | Medieval Village or Polygon. |
| Environment | Forest biome, homestead area | Quixel + one env pack; PCG + placed. |
| Items / resources | Resource nodes, harvestables | BP_WoodPile etc. |
| Boss | 1 boss for “claim home” beat | Placeholder or themed. |
