# CONSTRAINTS.md

**Status:** LOCKED (harness + engine)  
**Sources:** swarm/HS docs; `Docs/20_UASSET_AI_POLICY.md`; Lead Game Dev Partner rules

## Engine / platform

- Unreal Engine **5.7** target for product; Blender library first for art.
- Phaser only for cheap loop prototypes — not product path.
- Primary prove host: DESKTOP-21CT3H0 (Conductor parent for MCP/PIE).
- No extra backend / multiplayer netcode unless Lead specifies.

## Performance / content

- Exactly **10** master materials (`Docs/00_CANON.md` §6).
- `.uasset` / `.umap` only via `config/uasset-allowlist.json` + Git LFS (`Docs/20`).
- Mannequins **KEEP-LOCAL** — do not bulk-commit Marketplace mannequin trees.
- Generated assets: log tool/prompt/edit in `Docs/AI_ASSET_LOG.md`; stay hand-replaceable.

## Module / file ownership

- Constants live at the **top** of the owning file.
- One owner per system: GP (walk/form/glide/portal/time), SYS (inventory/tame/heal/nurture).
- Before adding movement, time, or hub logic: **read existing** `HomeWorldCharacter`, `HomeWorldFallbackGlideComponent`, time/TOD, shrine/portal code — do **not** add a parallel system.
- Do not two agents write the same file in one phase.

## Agent / harness

- No silent refactors. No deleting working files without Lead.
- No duplicate PlayerController / movement component.
- “Done” = compiles or runs + `Docs/canon/PLAYTEST.md` test passes + matching canon file updated.
- Lead stamps phase gates in chat (`APPROVE …`); workers do not self-approve.
- Prefer `evidence:grep -- --success-path` for prove; soft-reject alone is not PASS.
