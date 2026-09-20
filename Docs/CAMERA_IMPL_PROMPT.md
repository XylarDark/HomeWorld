# Camera implementation prompt (agent / UE Copilot)

Copy-paste for implementers. Source of truth: `Docs/CAMERA_BIBLE.md`.

```
Implement HomeWorld camera per Docs/CAMERA_BIBLE.md. Change only the camera manager / spring-arm / iso preset files you must touch. Do not add features not listed.

LOCKED
- Identity: Galaxy-framed WoW orbit third person (Spring Arm + Camera). Rest boom farther + slight down pitch. Mild lag. Pitch clamp (no under-character). Collision pull-in then restore preferred distance. Camera-relative move. Per-player cameras in co-op.
- Systems: separate isometric preset (true ortho OR distant low-FOV fake iso). Mode switch — not an orbit zoom stop.
- Glide: mid-glide soft-lock/bias behind; on land restore free orbit. Island collision must not clip under thin floors.
- NO dedicated FP camera, FP component, head-socket FP, view-arms, or body-hide FP mode. Near “intimacy” = WoW-style boom zoom only on the same orbit rig.
- Do not fight one camera into both orbit and iso jobs — two presets, blend or hard-swap by activity.

ACTIVITY → PRESET
- Hub walk / chores / explore / co-op / out-of-combat tame / shrine spectacle → Orbit TP
- Glide / shrine arrival → Orbit TP + temporary behind bias, then release
- Planet combat / loot / fight-tame / building / pens / crops → Iso
- Close pick/inspect → Orbit TP near-zoom (same rig)

DONE WHEN
- Orbit rest reads Galaxy (far + slight high); player can orbit yaw/pitch and zoom near↔far
- Iso is a distinct mode, not max zoom-out
- No FP class/component in the change
- PLAYTEST: walk homestead orbit; zoom near; toggle iso; start glide and confirm behind bias then release on land
```
