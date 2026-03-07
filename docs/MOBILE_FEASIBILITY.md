# Mobile feasibility (Android / iOS)

**Purpose:** Research note on whether HomeWorld can run on mobile. No project or platform changes are made by this doc; enabling mobile requires a **team decision** per [AGENTS.md](AGENTS.md).

---

## 1. UE5 mobile support summary

- **Android:** Supported in Unreal Engine 5 (5.0–5.7). Packaging via **File → Package Project → Android**. Requires **Android Studio** with the correct **Android NDK** and **SDK**; development device with USB debugging enabled. Build produces an APK or AAB.
- **iOS:** Supported. Requires a **Mac** with **Xcode** for building and signing. **Remote Mac Build** is available for teams on Windows. Apple signing and provisioning are required for device/ship.

Documentation: Epic’s “Creating mobile games,” “Packaging Android projects,” “Setting up for Android/iOS.”

---

## 2. Requirements to add mobile targets

| Requirement | Android | iOS |
|-------------|---------|-----|
| **Tooling** | Android Studio, NDK, SDK (version per engine docs) | Mac, Xcode |
| **Project** | Add Android to target platforms; accept SDK license | Add iOS target; signing/provisioning |
| **Build** | Package Project → Android | Package from Mac or Remote Mac Build |

---

## 3. HomeWorld-specific considerations

- **Scope:** Open World, World Partition, C++-heavy, many plugins (PCG, GAS, Mass, StateTree, ZoneGraph, SmartObjects). Mobile devices have less CPU/GPU and memory; packaging and runtime performance will need tuning.
- **Content:** Same content may be too heavy. Consider **scalability** (lower LOD, reduced PCG density, simpler shadows, fewer actors) or a **mobile build variant** (e.g. simplified levels, fewer systems).
- **Input:** Touch and possibly virtual joystick. **Enhanced Input** supports multiple devices; add touch mappings and possibly a touch-to-move or virtual stick scheme.
- **Plugins:** Verify each enabled plugin (MassEntity, MassAI, StateTree, etc.) supports Android/iOS and the engine version you use. Deprecation notices (e.g. MassEntity in 5.5+) may affect mobile builds.

---

## 4. Recommended next steps (if team decides to pursue mobile)

1. **Team decision:** Confirm adding Android and/or iOS as target platforms per [AGENTS.md](AGENTS.md).
2. **Add target:** In `.uproject` or Project Settings, add the Android (and optionally iOS) target; install and accept SDK/NDK (Android) or set up Mac/Xcode (iOS).
3. **Test package:** Run a minimal package (e.g. empty level or a small test map) to confirm the project and plugins build and launch on device.
4. **Profile on device:** Run the current game (or a stripped-down version) on a device; identify CPU/GPU and memory bottlenecks; adjust scalability and content as needed.
5. **Input:** Implement touch/virtual joystick and ensure core flow (move, look, interact) works on touch.

---

## 5. Policy note

**Enabling mobile in the project is a team decision.** Do not add Android or iOS target platforms, or change platform lock in AGENTS.md, without explicit team approval. This document is for research and planning only.

---

**See also:** [AGENTS.md](AGENTS.md) (platform lock), [docs/CHARACTER_GENERATION_AND_CUSTOMIZATION.md](CHARACTER_GENERATION_AND_CUSTOMIZATION.md), Epic’s “Creating mobile games” and packaging docs for your engine version.
