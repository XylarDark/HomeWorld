# Accessibility checklist (research deliverable)

**Source:** Phase 6 research (R-6-1), 2026-10-17.  
**Status:** Draft — pending Lead adoption (interview Q4).  
**Canon impact:** none yet. Would become a new `Docs/` accessibility doc if adopted.

## P0 (MVP — low cost, high impact)

- [ ] **Remappable controls.** Full button remapping for keyboard+mouse and gamepad. Baseline expectation in 2026.
- [ ] **Subtitles + closed captions.** Dialogue subtitles plus closed captions for non-dialogue audio (footsteps, spirit hum, bonk, wind-up). Large, high-contrast, opaque background, adjustable size/font, speaker names, directional indicators.
- [ ] **Motion-sickness toggles.** FOV slider, motion-blur toggle (off by default recommended), camera sensitivity slider, head-bob toggle (off by default), high-FPS target. Third-person is safer than first-person but cloud descent + floating island is a hotspot.
- [ ] **Colorblind non-color cues.** Blue=danger stealth must have a non-color cue (shape, icon, or sound). Manual per-color tweaks > blanket filters. Test with colorblind simulation.
- [ ] **"No number, no bar" optional aid.** Spirit-sickness stacks read via body/shoulder-spirit light. Offer an optional numeric/visual aid for cognitive accessibility. Default off (preserves design intent).

## P1 (EA — medium cost)

- [ ] **UI scaling.** Adjustable UI/menu/subtitle size. Low-vision + small screens.
- [ ] **Difficulty/assist options.** Celeste-style assist (speed, stamina, dashes) adapted to HomeWorld: slower spirit-sickness timer, longer wind-up window, reduced bonk penalty. Does not remove the core verb.
- [ ] **Toggle vs. hold inputs.** All hold interactions (gather, ease) should have a toggle option.
- [ ] **Invert axis + sensitivity sliders.** Standard for camera.

## P2 (post-EA — higher cost)

- [ ] **Full WCAG-for-games audit.** Screen reader support, full keyboard navigation, one-switch/voice control compatibility.
- [ ] **Audio descriptions** for key visual events.
- [ ] **Cognitive accessibility review** of the virtue bench (place/turn/commit) and spirit-sickness readability.

## Notes

- HomeWorld's design intent ("no number, no bar," "blue = danger") is preserved by making aids *optional* and default-off. The design is not compromised; it is made available to more players.
- Motion-sickness mitigations are especially important for the cloud descent (V2) and the floating-island context. Test with motion-sensitive players during Phase 1 playtest.