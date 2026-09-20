# Docs/CAMERA_BIBLE.md

**Status:** LOCKED (Lead paste 2026-09-20 ET)  
**Pointers:** `Docs/canon/PILLARS.md`, `Docs/canon/FEEL.md`, `Docs/02_ART_BIBLE.md`, `Docs/03_GAMEPLAY_MVP.md`

---

HOMEWORLD CAMERA BIBLE — IDENTITY + SYSTEMS + INTIMACY

Project: HomeWorld. Wholesome family co-op ARPG survival. Floating-island homestead hub + playable planet-below slice. Day body: gather, tame, glide down. Night spirit: heal, shrine portals. Art/asset pipeline: Blender first, UE5 second.

CORE RULE
Do not treat first person, third person, and isometric as equal always-on views.
One identity camera. One systems camera. One intimacy camera.
Build character, animation, and world for third person first. Isometric and first person are derived from that.

LAYER SEPARATION
Look ≠ control.
- LOOK / DEFAULT FRAMING: Super Mario Galaxy. Slightly high, slightly far, character readable in a big toy-like space. Show the island, the drop, the other player. Not shooter over-the-shoulder. Not cinematic rails as the default.
- CONTROL / FUNCTION: World of Warcraft orbit camera. Player can freely orbit around the character (yaw + pitch), zoom boom in/out, look from behind/side/front. Movement is camera-relative. Optional facing-lock. Collision pull-in with return to preferred distance. Mild lag.
Galaxy is the rest pose. WoW is the input model.
Do not copy Galaxy’s authored camera theft (gravity rails, forced swings) except as short scripted beats, then hand control back.

CAMERA ROLES
1) Identity camera (default): Galaxy-framed WoW orbit third person.
   Use for: homestead walking/chores, exploration, co-op presence, taming out of combat, glide, shrine arrival spectacle.
2) Systems camera: Path of Exile-style isometric (true ortho OR distant low-FOV “fake iso”).
   Use for: ARPG combat, loot/telegraphs, homestead layout/building/pens/crops, co-op tactical shared picture, night-spirit area control if it plays like radii/fields.
   Isometric is a mode switch, not a zoom stop on the orbit camera.
3) Intimacy camera: first person, opt-in and short.
   Use for: close gather/inspect, shrine/heal close-ups, tight interiors, wonder shots.
   Never required for travel or core combat.

ACTIVITY TABLE
- Hub life / walk / co-op presence → Galaxy-framed orbit TP
- Glide down / shrine arrival → same TP, temporarily bias/soft-lock behind, then release
- Planet combat / loot / fight-tame → isometric
- Building / pen / crop planning → isometric
- Pick / inspect / spirit close-up → first person hold or toggle

DEFAULTS FOR THE ORBIT RIG (Galaxy rest pose)
- Farther than typical action TP
- Slight downward pitch, not spine-level
- Mild lag
- Pitch clamp so the camera cannot easily go under the character
- Collision: pull in on obstruction, restore preferred boom when clear
- Zoom range may go near-TP / almost-FP and far homestead overview, but REST distance is Galaxy
- Co-op: each player has their own orbit camera. Never share one.

GLIDE / ISLANDS
- Mid-glide: bias or soft-lock behind so orbit cannot swing into the horizon
- On land: restore free orbit
- Floating islands: collision probes must handle thin floors and undersides. Do not clip under platforms.

FIRST PERSON IMPLEMENTATION
Prefer a dedicated FP camera (head socket, hide or fade body, optional simple view-arms) over boom-zoom-to-zero on a full body mesh.
Zoom-to-head on a full body is allowed only as a prototype.

ART / LOOK-GOOD RULE
Stylized readable forms over photoreal close-up detail.
Third-person full body and animations must work from behind and 3/4.
Isometric uses that same body; prioritize silhouette and VFX readability from high angle.
First person does not dictate the asset pipeline.

ENGINE NOTE (UE5)
One camera manager. Presets:
- Orbit TP (Spring Arm + Camera, Galaxy defaults)
- Iso rig (separate locked high angle)
- FP rig
Blend or hard-swap by activity. Do not fight one camera into all three jobs.

ONE-LINE LOCK
Galaxy third person is the identity camera. Isometric is the systems camera. First person is the intimacy camera. Control is WoW orbit. Framing is Galaxy.
