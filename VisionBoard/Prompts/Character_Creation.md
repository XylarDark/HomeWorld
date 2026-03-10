# Character Creation — Vision Board

Use this when generating prompts or design for the player character, family, child creation, and customization. Source: [../Character/CHARACTER_GENERATION_AND_CUSTOMIZATION.md](../Character/CHARACTER_GENERATION_AND_CUSTOMIZATION.md), [../Core/VISION.md](../Core/VISION.md), [docs/TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md](../../docs/TaskLists/TaskSpecs/MILADY_IMPORT_ROADMAP.md).

---

## Opening: start with a family

- **Player starts with a family** (partner and homestead). The tutorial covers resource collection, home building, magic, and combat.
- **You do not start with a child.** You **create your child** by playing a **mini-game**: press the **same sequence of keys in a song-like pattern** (e.g. a short rhythm or melody of key presses). When you complete the pattern, the **child spawns** and joins the household. Then the homestead is attacked and the family is taken; the player sets out to get them back.
- **MVP:** Simple version of the child-creation mini-game (short key sequence, song-like timing).

---

## Child-creation mini-game (vision)

- **Input:** Press a **sequence of keys in a song-like pattern** (rhythm or melody of key presses).
- **Success:** When you **match the pattern**, the **child spawns** and joins the household.
- **After:** Take care of them (play with them, keep them safe). Day goal includes building up love through child care → bonuses for the night.

---

## Generated vs static characters

- **Static:** Default pawn (e.g. BP_HomeWorldCharacter), family/NPCs. Mesh and skeleton from project content; same C++ pawn class.
- **Generated:** Player-supplied art (e.g. image) → pipeline (e.g. Meshy 2D→3D, VRM4U) → rigged mesh → same pawn class with different Skeletal Mesh. **Body types are standardized** (one target skeleton); **face/head varies**. Stylized pipeline: see Milady import roadmap.
- **In game:** Character source is `Static` or `Generated`. Spawn uses the same pawn class; for generated players the mesh (and optional material) come from the generated asset. Store which generated character is selected in SaveGame or profile.

---

## Main menu and character screen (flow)

- **Main menu:** Play, Character, Options, Quit. **Play** loads the game map (e.g. DemoMap). **Character** opens the character customization screen (WBP_CharacterCreate).
- **Character screen:** Placeholder Upload/Scan, face sliders (or “Face customization” area), **Confirm**, **Back**. **Confirm** saves profile (e.g. to Saved/CharacterCustomization.json) and closes the screen. **Back** closes without save. Full “image → character” and face-param backend can be deferred (Phase C/E).
- **First-launch flow:** Game starts on MainMenu → Play opens playable level; Character opens character screen; Confirm persists customization and closes.

---

## Face generation (stylized pipeline)

- **Input:** Any artwork (upload/URL or image). Generic “download image for character” or reuse existing download pipeline.
- **Body standardized:** One target skeleton; all generated characters retargeted to it so only head/face geometry differs. Optionally “face only” generation step attached to a standard body.
- **Output:** Same pawn class with different Skeletal Mesh (and optional material); store in profile/SaveGame for spawn.

---

## Family roles (by day/night)

- **Partner:** Present at opening; resurrection by partner if player dies outside at night. Love task with partner during the day (one task type for MVP).
- **Child:** Created via mini-game; then play games with them, keep them safe. Contributes to “love” and day buffs.
- **Protector / healer / caretaker:** By day, cooking and meals (caretaker); by night, family can have Defend role (defend homestead). Roles support casual (healer/home) and hardcore (protector) playstyles.

---

## Succession

- When the player character dies (in contexts where resurrection does not apply), that character becomes a **spirit** and is no longer playable. The player continues as one of their **children** (or another heir).
- **Final boss beat:** The player’s **child** takes over, defeats or seals the villain, returns to the homestead, and starts their own family. Succession: the next generation carries on.
