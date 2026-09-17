# Cloud agent packet — Conductor → Cursor cloud agent

**When to use:** Conductor assigns a **docs-only** or **C++-touching** task to a Cursor cloud agent (Linux VM, no UE/MCP). Fill this packet and attach paths from [HANDOFF_TEMPLATE.md](HANDOFF_TEMPLATE.md).

**Process authority:** [SWARM_OPS.md](SWARM_OPS.md) · **Windows follow-up:** [docs/Setup/WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md)

---

## Packet header

| Field | Value |
|-------|-------|
| **Packet ID** | HR-{phase}_{slug} or NP-{id}_{slug} |
| **Assigner** | CND (Conductor) |
| **Target** | Cursor cloud agent |
| **Branch** | `cursor/<descriptive-kebab-name>-b3a5` |
| **Base branch** | `main` (fetch before branch) |
| **Hard rules** | Docs/07 CLOSED · FALLBACK armed · no `.uasset`/`.umap` · docs/swarm only unless packet says otherwise |

---

## Branch naming (cloud agents)

```
cursor/<descriptive-name>-b3a5
```

- Prefix **`cursor/`** required for cloud-agent branches.
- Suffix **`-b3a5`** required (case-insensitive filesystem safety).
- Lowercase kebab-case only.
- One logical change per PR; push with `git push -u origin <branch>`.

---

## Evidence paths (required in PR)

| Evidence | Where |
|----------|--------|
| **PR URL** | GitHub PR link in handoff + PHASE_BOARD note |
| **Merge SHA** | Squash-merge commit on `main` after Lead/Conductor merge |
| **CI status** | `validate` + `python-lint` green (required for docs PRs) |
| **Optional `ci.yml`** | When `Source/` or `*.Build.cs` changed — self-hosted `windows`/`ue57` runner |
| **Windows validation** | DESKTOP-21CT3H0: Safe-Build → Editor → MCP — not on cloud VM |

List repo-relative paths for every deliverable (files created/changed). Gate claims without paths are invalid per SWARM_OPS.

---

## Cloud VM checklist — do NOT on cloud

Cloud agents run on **Linux without Unreal Engine**. Do **not** attempt:

- [ ] **MCP** / UnrealMCP tools (Editor not running)
- [ ] **`.\Tools\Safe-Build.ps1`** or any C++ build on the cloud VM
- [ ] **`execute_python_script`** / Editor Python (no Editor)
- [ ] **GUI automation** (`Content/Python/gui_automation/`) — Windows Editor only
- [ ] Commit **`.uasset`** / **`.umap`** — binary work stays on Windows

**Do on cloud:** docs, markdown, validate.yml-safe JSON, C++ source edits, Python scripts (untested in Editor until Windows handoff).

**Windows handoff:** After merge, Lead or Windows session follows [WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) for build, dress, PIE, MCP validation.

---

## Return handoff

On completion, Conductor files `Docs/handoffs/<packet_id>.md` using [HANDOFF_TEMPLATE.md](HANDOFF_TEMPLATE.md) § Cloud agent PR section.

**Gate:** Lead **`APPROVE HR-*`** per [Docs/11_SWARM_HARNESS_REFINE.md](../Docs/11_SWARM_HARNESS_REFINE.md).
