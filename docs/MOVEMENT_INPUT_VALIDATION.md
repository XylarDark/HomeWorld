# Movement input – best-practices validation

This doc records how HomeWorld’s third-person movement setup compares to common UE5 + Enhanced Input practices (Epic docs, Lyra, community templates, wirepair/UE5 movement articles).

## Summary

The current setup **matches recommended practices** for third-person, camera-relative movement with Enhanced Input. No code changes are required for “best practice” alignment.

---

## Practices checked

| Practice | Source | HomeWorld |
|----------|--------|-----------|
| **Triggered + Completed for movement** | Epic/docs, wirepair: bind Move to both Triggered and Completed so key release stops input | ✓ Four directional actions each bound to Triggered (pressed) and Completed (released); axes updated on both. |
| **Camera-relative direction** | UE5 third-person: use camera/control rotation for forward/right, not actor | ✓ `GetControlRotation()`, Yaw-only matrix for Forward/Right, then `Direction = Forward*axis + Right*axis`. |
| **AddMovementInput(world direction, scale)** | Epic API: direction in world space, scale for magnitude | ✓ `AddMovementInput(Direction, 1.0f)` in Tick with normalized direction. |
| **Input consumed in Tick** | CharacterMovementComponent consumes `ControlInputVector` each frame | ✓ We add once per Tick from accumulated axes; engine consumes as usual. |
| **Orient to movement (third-person)** | Common for TPS: character faces move direction, not camera yaw | ✓ `bUseControllerRotationYaw = false`, `bOrientRotationToMovement = true`, `RotationRate` set. |
| **Single Axis2D (IA_Move) as alternative** | Official template: one Axis2D with Swizzle/Negate for WASD | ✓ Fallback: if four directional actions are missing, we bind `MoveAction` (Axis2D) and use `Move()`; Python uses four Bool actions due to IMC modifier issues. |

## Implementation details

- **Input actions:** Four Boolean actions (IA_MoveForward, IA_MoveBack, IA_StrafeLeft, IA_StrafeRight) mapped to W/S/A/D without modifiers. This avoids Swizzle/Negate in the IMC (which were unreliable when set from Python) while preserving correct directions and key-up behavior.
- **Axis accumulation:** `MovementForwardAxis` and `MovementRightAxis` updated on Triggered (+1 / -1) and Completed (-1 / +1), clamped to [-1, 1]. Diagonals (e.g. W+D) combine correctly.
- **Tick:** Each frame, direction is computed from control rotation and current axes, normalized, then `AddMovementInput(Direction, 1.0f)`. Movement stops when no keys are held because axes go to 0 on release.
- **Lyra:** Uses GAS + input tags and hero component for abilities; movement is ability-driven. For a single character with direct movement (no ability-based locomotion), our approach is the standard C++ pattern and is consistent with Epic’s “Configure Character Movement” and third-person template style.

## References

- Epic: [Setting Up Character Movement](https://dev.epicgames.com/documentation/en-us/unreal-engine/setting-up-character-movement), [AddMovementInput](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/GameFramework/APawn/AddMovementInput)
- Wirepair: [How (Third Person) Movement Works in UE5](https://wirepair.org/2023/09/22/how-third-person-movement-works-in-ue5/) (Triggered/Completed, ControlInputVector, ConsumeInputVector)
- Community: UE5 Enhanced Input C++ tutorials (Axis2D + modifiers for WASD; we use four Bool actions for reliability with our Python IMC setup)
