# GAS 3 Survivor Skills (Day 2)

**Goal:** Three gameplay abilities for Act 1 (explore → fight → build): Primary Attack, Dodge/Sprint, Interact. Grant them to the character, bind input, and make them triggerable in PIE.

**Status:** Implemented. Run `Content/Python/setup_gas_abilities.py` in the Editor to create ability Blueprints, input actions, and assign them to BP_HomeWorldCharacter. Build C++ with Editor closed if needed.

---

## Abilities

| Skill | Input | Purpose (Act 1) | Cost (optional) |
|-------|--------|------------------|------------------|
| **GA_PrimaryAttack** | Left Mouse Button | Melee or short-range attack | Stamina (add GameplayEffect in Blueprint) |
| **GA_Dodge** | Left Shift | Dodge or sprint | Stamina |
| **GA_Interact** | E | Pickup, open, or "claim" (precursor to build) | None |

All three are Blueprint assets; **Interact** is parented to `HomeWorldInteractAbility` (C++) so harvest logic lives in code with no Blueprint graph. Primary Attack and Dodge remain parented to `HomeWorldGameplayAbility`; for new abilities, prefer a C++ ability subclass and reparent the Blueprint so logic stays programmatic (see [CONVENTIONS.md](../CONVENTIONS.md) "Programmatic by default").

---

## Setup (one-time)

1. **Build C++** with the Editor closed (or disable Live Coding): `Build-HomeWorld.bat`.
2. **Open the project** in the Editor.
3. **Run the setup script:** Tools → Execute Python Script → `Content/Python/setup_gas_abilities.py` (or via MCP: `execute_python_script("setup_gas_abilities.py")`).
4. The script creates:
   - `/Game/HomeWorld/Abilities/GA_PrimaryAttack`, `GA_Dodge`, `GA_Interact` (Blueprint, parent `HomeWorldGameplayAbility`)
   - `/Game/HomeWorld/Input/IA_PrimaryAttack`, `IA_Dodge`, `IA_Interact` (Boolean) and adds mappings to IMC_Default (Left Mouse Button, Left Shift, E)
   - Assigns `DefaultAbilities` and the three ability-class + input-action properties on BP_HomeWorldCharacter.

---

## Input binding (C++)

`AHomeWorldCharacter` has:

- **PrimaryAttackAction**, **DodgeAction**, **InteractAction** (UInputAction*) — optional; fallback load from `/Game/HomeWorld/Input/IA_*`.
- **PrimaryAttackAbilityClass**, **DodgeAbilityClass**, **InteractAbilityClass** (TSubclassOf<UGameplayAbility>) — set by the setup script on the character Blueprint CDO.

When the player triggers the input, the character calls `AbilitySystemComponent->TryActivateAbilityByClass(...)` for the corresponding class. Abilities are granted in `PossessedBy` from `DefaultAbilities`.

---

## Adding cost or effects

1. Open each GA_* Blueprint (e.g. Content → HomeWorld → Abilities → GA_PrimaryAttack).
2. Override **Activate Ability**: add your logic (e.g. Apply Gameplay Effect for Stamina cost, play montage, apply damage), then call **End Ability**.
3. Optional: create a **GameplayEffect** Blueprint that modifies `HomeWorldAttributeSet` (Stamina) and add it as a cost or cooldown.

---

## Verification

- **PIE on DemoMap:** Confirm movement (WASD), look (mouse), and that Left Mouse, Shift, and E trigger the three abilities (base implementation commits and ends with no visible effect; add Blueprint logic for feedback).
- **Optional:** Run `Content/Python/pie_test_runner.py` for ground, character, and animation checks.

---

## Day 2 verification checklist (in Editor)

Use this to confirm Day 2 work is complete without relying only on logs.

**1. Assets exist (Content Browser)**  
- **Content → HomeWorld → Abilities:** `GA_PrimaryAttack`, `GA_Dodge`, `GA_Interact` (each opens as a Blueprint with parent `HomeWorldGameplayAbility`).  
- **Content → HomeWorld → Input:** `IA_PrimaryAttack`, `IA_Dodge`, `IA_Interact` (Input Action assets).

**2. Input mappings**  
- Open **IMC_Default** (Content → HomeWorld → Input).  
- In **Mappings**, confirm: **Left Mouse Button** → IA_PrimaryAttack, **Left Shift** → IA_Dodge, **E** → IA_Interact.

**3. Character Blueprint**  
- Open **BP_HomeWorldCharacter** (Content → HomeWorld → Characters).  
- In **Details** (with Class Defaults selected):  
  - **Default Abilities:** array of 3 entries (the three GA_* classes).  
  - **Primary Attack Ability Class** = GA_PrimaryAttack (or equivalent).  
  - **Dodge Ability Class** = GA_Dodge.  
  - **Interact Ability Class** = GA_Interact.  
  - **Primary Attack Action**, **Dodge Action**, **Interact Action** = the three IA_* assets.

**4. PIE (Play in Editor)**  
- Set **DemoMap** (or Homestead) as the editor level; press **Play**.  
- **WASD:** character moves. **Mouse:** look.  
- **Left Mouse:** primary attack (no visible effect is OK; ability should commit/end).  
- **Left Shift:** dodge (same). **E:** interact (same).  
- No repeated errors in **Output Log** about missing abilities or input.

**5. Optional automated check**  
- Run **Tools → Execute Python Script** → `Content/Python/pie_test_runner.py` (or via MCP).  
- Open `Saved/pie_test_results.json`: confirm character spawn, ground contact, and animation checks pass if implemented.

---

## References

- [STACK_PLAN.md](../STACK_PLAN.md) Layer 3 — GAS, 3 survivor skills
- [30_DAY_SCHEDULE.md](../workflow/30_DAY_SCHEDULE.md) Day 2
- [.cursor/rules/unreal-gas.mdc](../../.cursor/rules/unreal-gas.mdc) — base classes, Blueprint content
