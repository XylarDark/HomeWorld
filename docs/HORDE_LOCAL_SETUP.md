# Horde local setup (optional)

Use [Epic Horde](https://dev.epicgames.com/documentation/en-us/unreal-engine/horde-build-automation-for-unreal-engine) for distributed builds and automated tests. This doc gives minimal steps to get a local agent and register this project.

## 1. Install Horde Server (optional; for local cluster)

- Run **Engine\\Extras\\Horde\\UnrealHordeServer.msi** from your UE 5.7 engine install (e.g. `C:\Program Files\Epic Games\UE_5.7\Engine\Extras\Horde\`).
- Server listens on HTTP 13340 and 13342. Use the dashboard (e.g. `http://localhost:13340`) to manage agents and jobs.
- For production, configure **Server.json** and host MongoDB/Redis separately (see [Horde Server for Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/horde-server-for-unreal-engine)).

## 2. Install Horde Agent (Windows)

- In the Horde Server dashboard: **Tools > Downloads** — download the **Horde Agent Windows Installer**.
- Run the installer; set **server address** (e.g. `http://localhost:13340`) and a **working directory** (e.g. `D:\HordeWork`) with at least 100GB free for C++ builds.
- Enroll the agent in the dashboard so it is authorized.

## 3. Unreal Build Accelerator (UBA)

- UBA can be enabled for faster incremental builds. Configure per [Epic Horde docs](https://dev.epicgames.com/documentation/en-us/unreal-engine/horde-build-automation-for-unreal-engine); optional for a single local agent.

## 4. Register this project for CI

- In Horde you declare **job templates** (BuildGraph + parameters), **agent types**, and **streams/projects** (see [Horde Build Automation](https://dev.epicgames.com/documentation/en-us/unreal-engine/horde-build-automation-for-unreal-engine)).
- Use **Tools/horde_job_templates.json** in this repo as an example: an Editor automation test job you can import or adapt in the Horde dashboard.
- Ensure the project path (and engine path) are visible to the agent (e.g. same drive or mapped path).

## 5. Editor automation tests

- To run Editor automation tests via Horde, your job template should invoke RunUAT (or your BuildGraph) with steps that run `Automation RunTest` and export the report (e.g. `-ReportExportPath`). See [Run Automation Tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine).

## References

- [Horde Build Automation (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/horde-build-automation-for-unreal-engine)
- [Horde Installation Tutorial](https://dev.epicgames.com/documentation/en-us/unreal-engine/horde-installation-tutorial-for-unreal-engine)
- [Horde Agents](https://dev.epicgames.com/documentation/en-us/unreal-engine/horde-agents-for-unreal-engine)
