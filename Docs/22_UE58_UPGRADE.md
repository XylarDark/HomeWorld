# Docs/22 — UE 5.8 Upgrade (U58)

| Field | Value |
|-------|-------|
| **Status** | **CLOSED / COMPLETE** — Lead implement-plan 2026-09-19 ET · Safe-Build green · MCP + RS PIE smoke on DESKTOP-21CT3H0 |
| **Date** | 2026-09-19 |
| **Author** | Conductor (HomeWorld) |
| **Prior** | Docs/21 Reap & Sow **CLOSED** — Lead **`APPROVE RS-E`**, 2026-09-19 ET |
| **Prefix** | **U58** |
| **Engine** | Epic Launcher `C:\Program Files\Epic Games\UE_5.8` (5.8.2-56702186) |
| **Branch** | `chore/ue-5.8-upgrade` |

---

## Gate

Lead unlocked cutover from UE **5.7** to **5.8** by approving the upgrade implementation plan. Platform remains **PC + Steam Early Access**.

---

## Goal

Ship HomeWorld on **Unreal Engine 5.8**: `EngineAssociation` 5.8, tooling/CI defaults, compile green, MCP/automation re-verified, VS_MVP smoke, docs/rules sourced to 5.8 only.

---

## Phases

| Phase | Focus | Host | Status |
|-------|--------|------|--------|
| **U58-A** | Strategy + EngineAssociation + lock docs | CLOUD | **APPROVED** |
| **U58-B** | Tools/CI/env path retarget | CLOUD | **APPROVED** |
| **U58-C** | First open + Safe-Build | DESKTOP | **APPROVED** — MassEntity removed; DLL OK |
| **U58-D** | UnrealMCP + automation access | DESKTOP | **APPROVED** — port 55557 Listen after shader compile |
| **U58-E** | VS_MVP content / PIE smoke | DESKTOP | **APPROVED** — RS placement + `hw.RS.*` LogTemp PASS |
| **U58-F** | UE58_TECH + ue58-sources; close + PR | CLOUD+Lead | **APPROVED** |

---

## Evidence (DESKTOP)

- Engine: `5.8.2-56702186+++UE5+Release-5.8` (`Saved/Logs/HomeWorld.log`)
- Safe-Build: exit 0; `UnrealEditor-HomeWorld.dll` ~1.4 MB
- MCP: `execute_python_script` success; UnrealMCP DLL rebuilt with project
- RS: `hw.RS.CollectDayBonus` → `day_bonus collected`; `CrossBonusStatus`; `CollectNightBonus` → `night_bonus collected`
- Placement: `place_vs_mvp_rs_*` scripts ok (KEEP-LOCAL map save)

---

## Env (host)

```text
UE_ENGINE=C:\Program Files\Epic Games\UE_5.8
UE_EDITOR=C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe
```

CI runner label: **`ue58`** (was `ue57`).

---

## Key fix

**MassEntity** plugin entry removed from `HomeWorld.uproject` — stub absent in Launcher 5.8. See [KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md).

---

## Non-goals (unchanged)

Console/mobile unlock; source-built engine; reopen Docs/07; Mannequins git commit; dual 5.7+5.8 forever.

---

## References

- [docs/UE/UE58_TECH.md](../docs/UE/UE58_TECH.md)
- [.cursor/rules/ue58-sources.mdc](../.cursor/rules/ue58-sources.mdc)
- [.cursor/skills/ue58-api-check/SKILL.md](../.cursor/skills/ue58-api-check/SKILL.md)
