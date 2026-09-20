# Docs/CAMERA_BIBLE.md

**Status:** LOCKED (Lead paste 2026-09-20 ET; FP amendment 2026-09-20 ET)  
**Pointers:** `Docs/canon/PILLARS.md`, `Docs/canon/FEEL.md`, `Docs/02_ART_BIBLE.md`, `Docs/03_GAMEPLAY_MVP.md`

---

HOMEWORLD CAMERA BIBLE — IDENTITY + SYSTEMS (NO DEDICATED FP)

Project: HomeWorld. Wholesome family co-op ARPG survival. Floating-island homestead hub + playable planet-below slice. Day body: gather, tame, glide down. Night spirit: heal, shrine portals. Art/asset pipeline: Blender first, UE5 second.

CORE RULE
Do not treat first person, third person, and isometric as equal always-on views.
One identity camera. One systems camera.
**No dedicated first-person camera / FP component.** Near-head framing is only the orbit boom zoomed in (WoW-style). Do not optimize art, animation, or gameplay for true FP.
Build character, animation, and world for third person first. Isometric is derived from that.

LAYER SEPARATION
Look ≠ control.
- LOOK / DEFAULT FRAMING: Super Mario Galaxy. Slightly high, slightly far, character readable in a big toy-like space. Show the island, the drop, the other player. Not shooter over-the-shoulder. Not cinematic rails as the default.
- CONTROL / FUNCTION: World of Warcraft orbit camera. Player can freely orbit around the character (yaw + pitch), zoom boom in/out, look from behind/side/front. Movement is camera-relative. Optional facing-lock. Collision pull-in with return to preferred distance. Mild lag.
Galaxy is the rest pose. WoW is the input model.
Do not copy Galaxy’s authored camera theft (gravity rails, forced swings) except as short scripted beats, then hand control back.

CAMERA ROLES
1) Identity camera (default): Galaxy-framed WoW orbit third person.
   Use for: homestead walking/chores, exploration, co-op presence, taming out of combat, glide, shrine arrival spectacle.
   Close gather/inspect / wonder: **zoom the orbit boom near** (may feel almost-FP). Body may clip; that is acceptable — do not ship a separate FP mode.
2) Systems camera: Path of Exile-style isometric (true ortho OR distant low-FOV “fake iso”).
   Use for: ARPG combat, loot/telegraphs, homestead layout/building/pens/crops, co-op tactical shared picture, night-spirit area control if it plays like radii/fields.
   Isometric is a mode switch, not a zoom stop on the orbit camera.

ACTIVITY TABLE
- Hub life / walk / co-op presence → Galaxy-framed orbit TP
- Glide down / shrine arrival → same TP, temporarily bias/soft-lock behind, then release
- Planet combat / loot / fight-tame → isometric
- Building / pen / crop planning → isometric
- Pick / inspect / spirit close-up → same orbit TP, boom zoomed near (not a FP camera swap)

DEFAULTS FOR THE ORBIT RIG (Galaxy rest pose)
- Farther than typical action TP
- Slight downward pitch, not spine-level
- Mild lag
- Pitch clamp so the camera cannot easily go under the character
- Collision: pull in on obstruction, restore preferred boom when clear
- Zoom range: near (almost-FP feel, WoW-style) ↔ far homestead overview; **REST distance is Galaxy**
- Do not hide body / swap to head socket / view-arms for “true FP”
- Co-op: each player has their own orbit camera. Never share one.

GLIDE / ISLANDS
- Mid-glide: bias or soft-lock behind so orbit cannot swing into the horizon
- On land: restore free orbit
- Floating islands: collision probes must handle thin floors and undersides. Do not clip under platforms.

NEAR-ZOOM (NOT FIRST PERSON)
Allowed: boom TargetArmLength → small / near-zero while keeping the same Spring Arm + Camera and full body mesh (WoW zoom-in).
Forbidden: dedicated FP camera component, head-socket FP rig, viewmodel arms, fade-body FP mode, optimizing meshes/anims for FP-only.

ART / LOOK-GOOD RULE
Stylized readable forms over photoreal close-up detail.
Third-person full body and animations must work from behind and 3/4.
Isometric uses that same body; prioritize silhouette and VFX readability from high angle.
Near-zoom does not dictate the asset pipeline.

ENGINE NOTE (UE5)
One camera manager. Presets:
- Orbit TP (Spring Arm + Camera, Galaxy defaults; zoom includes near)
- Iso rig (separate locked high angle)
Blend or hard-swap Orbit ↔ Iso by activity. **Do not add an FP preset.**

ONE-LINE LOCK
Galaxy third person is the identity camera. Isometric is the systems camera. Control is WoW orbit (including near-zoom). Framing is Galaxy. No dedicated first person.
