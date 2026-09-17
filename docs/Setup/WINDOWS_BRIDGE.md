# Windows bridge — cloud agent → CI → local Editor/MCP

**When to use this:** A Cursor **cloud agent** (Linux VM, no UE/MCP) ships a PR that needs Windows Unreal validation, dress/material scripts, or PIE.

---

## Host roles

| Host | OS | UE 5.7 | MCP | Typical work |
|------|-----|--------|-----|--------------|
| **Cursor cloud agent** | Linux | No | No | Docs, C++ edits, Python scripts, PRs |
| **GitHub self-hosted runner** | Windows (`DESKTOP-21CT3H0`) | Yes | Optional | `ci.yml` Win64 build, automation tests |
| **Lead Windows dev machine** | Windows | Yes | Yes | Safe-Build, Editor, MCP, `.uasset` dress/material, PIE |

---

## Flow (canonical)

```
Cloud agent PR (GitHub)
    │
    ├─ docs-only ──► validate.yml (Ubuntu) ──► merge when green
    │
    └─ C++ / needs PIE ──► validate.yml ──► ci.yml (self-hosted ue57)
                                    │
                                    └─► DESKTOP-21CT3H0: build + optional tests
                                              │
                                              └─► Open Editor + MCP for dress/PIE
                                                    (Lead or Windows Cursor session)
```

---

## Step-by-step

### 1. Cloud agent opens PR

- Branch: `cursor/<descriptive-name>-<suffix>` per cloud agent policy
- No `.uasset` / `.umap` in repo — binary work stays on Windows
- Evidence paths in PR body (scripts, docs, log expectations)

### 2. GitHub Actions — validate (always)

Runs on Ubuntu — no UE install:

- JSON, required docs ([DOCS_LAYOUT.md](../DOCS_LAYOUT.md) paths), python-lint
- See [CI_POLICY.md](CI_POLICY.md)

### 3. GitHub Actions — ci.yml (when C++ touched)

Requires runner labels: `self-hosted`, `windows`, `ue57`.

- Checkout + LFS
- `RunFullBuild.ps1` / `Build-HomeWorld.bat`
- Optional Smoke tests if `UE_EDITOR` set on runner

Setup: [CI_SETUP.md](CI_SETUP.md)

### 4. Windows Editor + MCP (dress, materials, PIE)

Cloud agents **cannot** run this step. On **DESKTOP-21CT3H0** (or Lead machine):

1. Pull PR branch
2. **`.\Tools\Safe-Build.ps1`** if C++ changed — [BUILD_POLICY.md](BUILD_POLICY.md)
3. Open **`HomeWorld.uproject`**
4. Restart Cursor → MCP green dot (port **55557**) — [MCP_SETUP.md](MCP_SETUP.md)
5. Run Editor scripts via MCP `execute_python_script` or Tools → Execute Python Script
6. PIE / dress validation; capture logs under `Saved/Logs/` as evidence

---

## Agent vs human build entry

| Actor | Build command |
|-------|---------------|
| **Agents / automation** | `.\Tools\Safe-Build.ps1` only |
| **Humans (Editor closed)** | `Build-HomeWorld.bat` OK |
| **ci.yml** | `Build-HomeWorld.bat` / `RunFullBuild.ps1` on runner |

Single path for agents: [AGENTS.md](../../AGENTS.md) § Build → Editor → MCP.

---

## Related

- [CURSOR_DEV.md](CURSOR_DEV.md) — DevEnvTemplate init on any host
- [Docs/11b_HR_B_HANDOFF.md](../../Docs/11b_HR_B_HANDOFF.md) — HR-B checklist
- [swarm/SWARM_OPS.md](../../swarm/SWARM_OPS.md) — Conductor / evidence gates
