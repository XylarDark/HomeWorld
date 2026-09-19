# Docs/23 U58F-F — MCP landscape decision

| Field | Value |
|-------|-------|
| **Date** | 2026-09-19 |
| **Phase** | U58F-F |
| **Decision** | **Keep UnrealMCP as primary** — do **not** enable Epic `ModelContextProtocol` alongside it |

---

## Compared

| | **UnrealMCP** (project) | **ModelContextProtocol** (Epic Experimental, UE 5.8) |
|--|-------------------------|------------------------------------------------------|
| Location | `Plugins/UnrealMCP/` (gitignored; Setup-MCP.bat) | Engine `Plugins/Experimental/ModelContextProtocol` |
| Port / bridge | Cursor MCP → 55557 (proven Docs/22) | Epic LLM assistant tooling (Blueprint/asset automation) |
| HomeWorld automation | `execute_python_script`, PIE cheats, placement scripts | Not wired into our Conductor / Windows bridge |
| Risk if dual-enabled | Port/tool collision; two transaction models (5.8.1 MCP notes) | Experimental; Assistant Blueprint crashes fixed in 5.8.1 |

---

## Stamp

1. **Primary:** UnrealMCP remains the only MCP server HomeWorld automation depends on.
2. **Epic MCP:** Leave **disabled** in `HomeWorld.uproject`. Revisit only if Lead opens a dedicated track and UnrealMCP cannot cover a required tool surface.
3. **No dual servers** on DESKTOP-21CT3H0.

See [Docs/23_UE58_FEATURE_ADOPTION.md](../23_UE58_FEATURE_ADOPTION.md) · [docs/Setup/MCP_SETUP.md](../../docs/Setup/MCP_SETUP.md).
