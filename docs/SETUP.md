# HomeWorld – Developer Setup Checklist

Do these steps once. Everything else for first-phase setup is already in the repo.

1. **Engine:** Install Unreal Engine 5.4+ (or confirm 5.7 used by this project).
2. **Project:** Open `HomeWorld.uproject`; allow first-time load/compile.
3. **Plugins:** In Editor, **Edit > Plugins** – confirm these six are enabled (all are in .uproject):
   - **PCG**, **Gameplay Abilities**, **Mass Entity** (in .uproject).
   - **Enhanced Input**, **Day Night Sequencer** (in .uproject).
   - **Steam Sockets** (replaces SteamCore for co-op; in .uproject).
   Optionally enable **Mass Gameplay** and **Mass AI** if the team wants them for Week 3–4 swarms. **Restart UE5 after enabling any new plugins.**
4. **Free assets:**
   - **FAB:** Survival character (or equivalent).
   - **Quixel:** Biomes/vegetation for forest.
   - *(Add exact asset names/links here as the team chooses.)*
5. **World:** Confirm the project uses Open World / World Partition (already set in `Config/DefaultEngine.ini`).
6. **Roles (optional):** Note Designer / Artist / Programmer / Tester and who leads Week 1.

After this, follow [WEEK1_TASKS.md](WEEK1_TASKS.md) in the Editor.
