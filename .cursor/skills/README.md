# `.cursor/skills` — HomeWorld project skills

Cursor discovers `description` on every turn for each `SKILL.md` here. Keep this tree lean (EXIT SKILL_LOAD_BUDGET_V1).

## Live (discoverable)

A skill stored in both trees is advertised from **this** tree, so the trigger `description` lives here and the `.agents` copy is a short pointer (DEC-0041).

| Skill | Role |
|-------|------|
| `pcg-validate` | PCG validation / forest workflows |
| `automation-gap-solutions` | Automation-gap solutions; cite `docs/Automation/AUTOMATION_GAPS.md` |
| `ue-editor-ui` | Slate inspector for panels Python cannot write — fires on `editor_ui: NEED_SLATE` |

## Pointers and tombstones

`ue58-api-check` is **not** advertised from this tree: the file here is a short pointer with `disable-model-invocation: true`, and the body lives in `.agents/skills/ue58-api-check`.

The retired name `ue57-api-check` lives only in `.agents/skills/ue57-api-check`. Prefer `ue58-api-check`. UE57 docs stay under `docs/UE/UE57_*`.

**Retired (WAVE F):** `demo-map-setup`, `homestead-setup` — deleted; use VS_MVP + `Docs/04*`.

## Not here (by design)

- **Taste** → `.agents/skills/taste-gate` + `taste-profiler` only (no cursor dups).
- **Lean A/B** → `.agents/skills-extras/architecture-tradeoffs` + `design-complexity` only.
- **Full A–E** → `.agents/skills-extras/architecture-trade-offs-design-depth` cite/copy-in only — **never** copy onto this scan path.

See also `.agents/README.md` for the full discoverable vs extras catalog.
