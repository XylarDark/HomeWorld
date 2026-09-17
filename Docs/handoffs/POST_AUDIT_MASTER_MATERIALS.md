# Handoff — Post-audit master materials (Windows Editor)

| Field | Value |
|-------|-------|
| **Date** | 2026-09-17 |
| **Script** | `Content/Python/create_master_materials.py` |
| **Canon** | `Docs/02_MATERIAL_SHEET.md`, `Lib/06_Materials_Master/*.json` |

## Prerequisites

- Unreal Editor **5.7** on Windows (DESKTOP host with UE installed)
- Project open; Python Editor Script Plugin enabled
- `MPC_HomeWorld_Time` at `/Game/HomeWorld/Materials/MPC_HomeWorld_Time` (run `place_vs_mvp_markers.py` once if missing)

## Run

```text
Tools → Execute Python Script → Content/Python/create_master_materials.py
```

Or from MCP (Editor connected):

```text
execute_python_script("create_master_materials.py")
```

Force rebuild existing graphs:

```text
execute_python_script("create_master_materials.py --force")
```

## Expected log

Prefix `create_master_materials:` — summary line `created=N upgraded=N skipped=N failed=0`.

## Verify

- Content Browser: `/Game/HomeWorld/Materials/Masters/` — ten `M_*` materials
- Open any master: **NightMix** CollectionParameter → `MPC_HomeWorld_Time` / scalar **NightMix**
- PIE on VS_MVP: C++ logs `HomeWorld: NightMix=…` on phase change

## Notes

- `M_FoliageCard`: masked blend with constant opacity 1 until card textures exist
- No binary commit — assets live in local Content only
- Closeout: [Docs/10_POST_AUDIT_WRAP.md](../10_POST_AUDIT_WRAP.md)
