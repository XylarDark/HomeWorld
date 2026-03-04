# AnimGraph automation — spike (Solution 4)

**Purpose:** Document options for automating Animation Blueprint AnimGraph setup (e.g. add Locomotion state machine, Idle/Walk states, Speed-driven transitions) so the 30-day loop does not require manual AnimGraph editing per ABP.

**Status:** Deferred. Use one-time manual setup per [CHARACTER_ANIMATION.md](CHARACTER_ANIMATION.md) or Editor + auto-clicker (Section 2 of rare-intervention plan).

---

## Findings

1. **Python/MCP:** AnimGraph visual graph API is not exposed. [09-mcp-workflow.mdc](../../.cursor/rules/09-mcp-workflow.mdc): "Animation Blueprint state machine editing (AnimGraph visual graph API is not exposed)."

2. **C++:** The engine uses `UAnimBlueprint`, `FAnimNode_StateMachine`, and related editor types in `Engine/Source/Editor/AnimationEditor` and the Animation module. Building a state machine (add states, set transitions, wire Speed) from a commandlet or Editor Utility would require:
   - Access to the AnimBlueprint's graph (often editor-internal or not fully exposed for programmatic construction).
   - Creating and connecting graph nodes (state machine node, state nodes, transition rules). Engine APIs for this are not documented as a stable public commandlet workflow.

3. **Editor + auto-clicker:** Ref-based PyAutoGUI (or SikuliX) can drive the Editor: open ABP → AnimGraph tab → add state machine → add states → wire Speed. Same pattern as PCG: capture refs once (or use capture script), then run host-side click script. See plan "Editor-driven GUI automation" and [AUTOMATION_READINESS.md](../AUTOMATION_READINESS.md).

---

## Recommendation

- **Default:** One-time manual per ABP per [CHARACTER_ANIMATION.md](CHARACTER_ANIMATION.md). Document as acceptable rare intervention in [AUTOMATION_READINESS.md](../AUTOMATION_READINESS.md).
- **If automation required:** Prefer Editor + auto-clicker (ref-based flow for ABP); only invest in C++ commandlet if engine API is confirmed and the 30-day loop frequently introduces new ABPs.

---

## References

- [CHARACTER_ANIMATION.md](CHARACTER_ANIMATION.md) — manual AnimGraph steps (state machine, Idle/Walk, Speed).
- [.cursor/rules/09-mcp-workflow.mdc](../../.cursor/rules/09-mcp-workflow.mdc) — what MCP cannot do (AnimGraph).
- Rare human intervention plan — Solution 4 (AnimGraph), Section 2 (Editor-driven GUI automation).
