# UE 5.7 Editor UI — Epic-sourced procedures

All steps below are taken from **Epic's Unreal Engine 5.7 documentation**. If your Editor does not show the same menus, options, or locations, open the cited doc and compare; UI can differ by build or setup.

**Policy:** For any Editor UI instructions, agents and docs must use only Epic UE 5.7 docs and cite them. See [.cursor/rules/ue57-editor-ui.mdc](.cursor/rules/ue57-editor-ui.mdc).

---

## Content Browser — opening and Settings

**Source:** [Content Browser in Unreal Engine (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/content-browser-in-unreal-engine)

You can open the Content Browser in three ways:

- From the **Window** menu in the top menu bar
- From the **Create** menu on the **Main Toolbar**
- By clicking the **Content Drawer** button on the **bottom toolbar**

The Content Drawer is a temporary instance that minimizes when it loses focus.

**Settings (UE 5.7):** [Content Browser Settings in Unreal Engine (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/content-browser-settings-in-unreal-engine)

- The **Settings** button is in the **top-right corner** of the Content Browser.
- Clicking it opens a **menu** (not a separate window).
- In that menu you can adjust: View type (Tiles, List, Columns), **Content to include or exclude**, and search options.

---

## Showing engine content (Engine Content folder)

**Source:** [Content Browser Settings — Content](https://dev.epicgames.com/documentation/en-us/unreal-engine/content-browser-settings-in-unreal-engine#content)

Under the **Content** section of the Settings menu:

| Option | Description (from Epic) |
|--------|-------------------------|
| **Show Engine Content** | If enabled, shows the **Engine Content** folder in the **Sources panel**. This folder contains Unreal Engine stock assets. |

Steps (exact wording from Epic 5.7):

1. Open the **Content Browser** (see above).
2. Click the **Settings** button in the **top-right corner** of the Content Browser.
3. In the menu that opens, find the **Content** section.
4. Enable **Show Engine Content**.
5. In the **Sources panel** (left side of the Content Browser), the **Engine Content** folder should appear. Expand it to browse engine assets. Folder structure may vary by engine build; use the Content Browser search box to search for asset names (e.g. "Cube", "Shape") while Engine content is visible.

**If you don’t see a Settings button or a "Content" / "Show Engine Content" option:** Open the [Content Browser Settings](https://dev.epicgames.com/documentation/en-us/unreal-engine/content-browser-settings-in-unreal-engine) doc and compare the screenshots and option names to your Editor. If your UI differs, note what you see (e.g. "I have a gear icon but no Content section") so we can update this doc.

---

## Placeholder / cube mesh for MEC or levels

Two approaches, both from Epic 5.7:

### A. Engine content (browse or search)

After enabling **Show Engine Content** (see above), in the **Sources panel** expand **Engine Content** and browse for static meshes. Engine folder structure may include a **BasicShapes** or similar folder; if not, use the Content Browser **search/filter** and search for **Cube** or **Shape** to find a primitive mesh. Assign that mesh where needed (e.g. MEC representation trait Static Mesh).

### B. Modeling Mode — create a Box (in-level)

**Source:** [Predefined Shapes in Unreal Engine (UE 5.7)](https://dev.epicgames.com/documentation/en-us/unreal-engine/predefined-shapes-in-unreal-engine)

- Create a new mesh via **Modeling Mode**: **Create** category → **Box** (or Sphere, Cylinder, etc.). Drag into the scene, adjust in **Tool Properties**, then **Accept**. Output can be Static Mesh. This creates an asset/actor in the level; you can then save or reference it as needed. For MEC representation, you typically need an **existing** Static Mesh asset (e.g. from Engine Content or your project), not only an in-level placement.

---

## If your UI doesn’t match

1. Open the Epic 5.7 doc linked for that step (same version as your engine: 5.7).
2. Compare the doc’s menu names, button positions, and option labels to your Editor.
3. If something is missing or named differently, report back what you see (e.g. "Settings opens a panel on the left" or "I see 'Include Engine Content' instead of 'Show Engine Content'") so we can update this doc and avoid wrong instructions.
