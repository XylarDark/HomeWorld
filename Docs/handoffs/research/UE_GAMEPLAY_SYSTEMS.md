# UE gameplay systems

How a new mechanic is added. Not NPC paths. Not collision rules.

## 2026-10-17

Ask: a high-level structure for movement and interaction so a later mechanic is a new type, not another method on the player.

Already covered: nothing. This file is the first entry for this body.

### Sources

- Interfaces in Unreal Engine. Epic. https://dev.epicgames.com/documentation/en-us/unreal-engine/interfaces-in-unreal-engine Retrieved 2026-10-17.
- Using Gameplay Tags in Unreal Engine. Epic. https://dev.epicgames.com/documentation/en-us/unreal-engine/using-gameplay-tags-in-unreal-engine Retrieved 2026-10-17.
- Using Gameplay Abilities in Unreal Engine. Epic. https://dev.epicgames.com/documentation/unreal-engine/using-gameplay-abilities-in-unreal-engine Retrieved 2026-10-17.
- Understanding Networked Movement in the Character Movement Component. Epic. https://dev.epicgames.com/documentation/unreal-engine/understanding-networked-movement-in-the-character-movement-component-for-unreal-engine Retrieved 2026-10-17.

### What HomeWorld already has

`UHomeWorldInteractAbility` calls a chain of `Try*` methods on `AHomeWorldCharacter`. A new verb is a new method and a new branch. On SizeTest, Q toggles aim, a ray from the camera selects the actor, and E runs that ability. The ability does not ask the aimed actor. Each method traces again.

`UHomeWorldGlideMovementComponent` is the one character movement component. Glide is a custom mode. Walking stays the inherited walk mode, with `bOrientRotationToMovement`. The opening partner and child are `AHomeWorldOpeningWalker`, a second character that copies those walk settings and is driven with `AddMovementInput`.

C++ owns behavior. Blueprint assigns assets. A pass-through wrapper and a second copy of a rule are already refused.

### Structure

The player owns input and aim. The object owns the verb.

- Q toggles aim mode. While it is on, the ray from the camera is the only target. E activates the one interact ability.
- The ability asks that actor through one C++ interface: can this actor be used right now, and if so, do the verb.
- A new mechanic implements that interface on its own actor or component. It does not add a `Try*` method or a branch in the ability.
- Gates such as day, body, and carrying a herb stay inside the object that cares. Partner dialogue is text, not a gate.
- Actor `FName` tags stay until a verb moves. New verbs use a gameplay tag (`UE_DECLARE_GAMEPLAY_TAG_EXTERN` / `UE_DEFINE_GAMEPLAY_TAG`). Once a verb has moved, that fact has one label system.

One character movement component. New locomotion is a mode, not a new mover.

- Walk, jump, and facing stay the inherited walk mode and `bOrientRotationToMovement`. Walker speed and mesh-facing offset belong on that component, not as a second copy in the walker constructor.
- A movement that is not walking is another custom mode on `UHomeWorldGlideMovementComponent`: `SetMovementMode(MOVE_Custom, SubMode)` and `PhysCustom`. `MOVE_Custom` suspends normal physics, so that mode implements its own motion.
- An NPC who walks like the player is an `ACharacter` using that same component and `AddMovementInput` along a path. `bRunPhysicsWithNoController` lets an unpossessed character move. Do not teleport with `SetActorLocation`.

### Reuse

KEEP

- One interact ability, plus one interface on the target.
- One character movement component. Custom modes only for movement that is not walking.
- Gameplay tags for new verbs.
- Gameplay abilities keep `CanActivateAbility`, `ActivateAbility`, `CommitAbility`, and `EndAbility`.
- A rune is a component on the collectible, drawn with a spline mesh. Static placement stays fixed, like a mark on a wall. Camera-parallel placement keeps the ribbon facing the camera. Do not add a second outline builder on the player.

CANDIDATE

- Move an existing verb onto the interface the next time that verb is edited. Do not batch-migrate the current `Try*` list.

PARK

- A second movement component.
- A Blueprint interact graph.
- A wrapper whose only job is to forward the call.
