# HomeWorld

**Co-op ARPG survival with family sim.** Players build and protect a life worth fighting for—explore, fight, build, then nurture bonds and defend together. Roles for casual (healer/home) and hardcore (protector) players. Target: 8–12h campaign + endgame; PC, Steam Early Access.

---

## Start here (MVP canon)

| Path | Role |
|------|------|
| **[START_HERE.md](START_HERE.md)** | Boot the MVP lookdev swarm (Conductor, phase gates) |
| **[Docs/](Docs/README.md)** | **Signed MVP product canon** — GDD, art bible, export/UE handoff, audit WAVEs |
| **[swarm/SWARM_OPS.md](swarm/SWARM_OPS.md)** | Swarm process — Human Use, evidence gates |
| **[AGENTS.md](AGENTS.md)** | Agent / Cursor context (UE 5.7, MCP, build policy) |
| **[docs/](docs/README.md)** | UE engineering docs — setup, PCG, automation, known errors |

**Quarantine (history only):** [VisionBoard/MVP/](VisionBoard/MVP/README.md) · [docs/Automation/AGENT_COMPANY.md](docs/Automation/AGENT_COMPANY.md)

---

## Getting started (UE 5.7)

- **Project layout:** Repository root contains `HomeWorld.uproject`, `Source/`, `Config/`, and `Content/`.
- **Engine:** Unreal Engine 5.7 (recommended).
- **Clone** this repo, then open `HomeWorld.uproject` in the Editor (first load may compile).
- **MCP setup:** Run `Setup-MCP.bat` to enable Cursor control of the Editor. Then **`.\Tools\Safe-Build.ps1`**, open the Editor, restart Cursor. See [docs/Setup/MCP_SETUP.md](docs/Setup/MCP_SETUP.md).
- **Build policy:** Agents use [Safe-Build](docs/Setup/BUILD_POLICY.md) (wraps `Build-HomeWorld.bat`).
- Full setup: [docs/SETUP.md](docs/SETUP.md).

---

## Docs split

| Tree | Purpose |
|------|---------|
| **`Docs/`** (capital) | MVP swarm canon — do not merge with lowercase tree |
| **`docs/`** (lowercase) | Unreal project documentation — session ops, PCG, setup |

Session task boards live under `docs/TaskLists/` and `docs/workflow/` — they are **not** the signed MVP GDD (see **`Docs/`**).

---

## Team

Home team (3). See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute.
