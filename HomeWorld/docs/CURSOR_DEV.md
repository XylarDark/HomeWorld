# Development with Cursor

HomeWorld is set up so that AI agents and humans follow the same conventions when working in Cursor.

- **Agent context:** [AGENTS.md](../AGENTS.md) at the repo root gives a short project summary, the **programmatic-by-default** policy, and where code and docs live. Use it to onboard agents and tools.
- **Cursor rules:** Under [.cursor/rules/](../.cursor/rules/), file-specific rules apply when you work with:
  - **Unreal C++** (`**/*.cpp`, `**/*.h`): naming, UPROPERTY/UFUNCTION, module boundaries, include order.
  - **Unreal Blueprint** (`**/*.uasset`): when to use Blueprint vs C++, naming, and that core movement/input/camera are in C++.
  - **Unreal project/config** (`**/*.uproject`, `**/Config/*.ini`): project layout, game module, plugins, default pawn and game mode.
- **Building:** Generate Visual Studio project files from the `.uproject`, then build the **HomeWorld** and **HomeWorldEditor** targets. See the **Building (C++)** section in [SETUP.md](SETUP.md). To build from the command line, use MSBuild or the IDE after generating the solution once.

When asking Cursor to change C++ or Blueprint behavior, the rules ensure suggestions align with programmatic-by-default and the existing HomeWorld layout.
