# HomeWorld – Git and GitHub Setup Verification

Use this checklist to confirm that the four setup steps (GitHub repo, Git LFS, terminal commands, team clone) have been accomplished.

---

## Step 1 – GitHub

- [ ] **Repo exists:** HomeWorld repo is created and accessible (e.g. `github.com/homeworld460-cmyk/HomeWorld`).
- [ ] **Visibility:** Settings → General → Danger Zone confirms Private (or Public if intended).
- [ ] **.gitignore:** Repo root `.gitignore` contains standard UE5 entries (Binaries/, Intermediate/, Saved/, DerivedDataCache/, IDE/OS entries).

---

## Step 2 – Git LFS

- [ ] **Installed:** In terminal, `git lfs version` returns a version string (e.g. "Git LFS: 3.x.x").
- [ ] **Tracking:** Repo root `.gitattributes` exists and contains LFS rules for `*.uasset` and `*.umap`.

---

## Step 3 – Terminal (project root)

- [ ] **Initialized:** Project has been initialized with `git init` (`.git` exists on disk).
- [ ] **LFS tracked:** `git lfs track ".uasset" ".umap"` has been run; `.gitattributes` has the LFS lines.
- [ ] **Committed:** `git add .` and `git commit -m "Week1 Setup"` (or equivalent) completed.
- [ ] **Remote:** `git remote -v` shows `origin` pointing to the correct HomeWorld repo URL.
- [ ] **Branch:** `git branch` shows `main` (or `master`).
- [ ] **Pushed:** `git log -1` shows the expected commit; the same commit appears on GitHub.

---

## Step 4 – Team (all others)

- [ ] **Clone:** Each team member has run `git clone [REPO]` and can open the project.
- [ ] **GenerateProjectFiles.bat:** Run `GenerateProjectFiles.bat` (VS2022) from the Engine folder or project root so the .sln is generated; then open `HomeWorld.uproject` or the solution.

---

## Next step

When all above are checked, Git setup is complete. For full developer setup (Engine, Plugins, assets, etc.), see [SETUP.md](SETUP.md).
