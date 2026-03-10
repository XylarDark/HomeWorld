# batch_import_asset_creation.py
# Imports FBX/GLB from AssetCreation/Exports/ into /Game/HomeWorld/ by category.
# Run from Unreal Editor: Tools -> Execute Python Script, or via MCP execute_python_script("batch_import_asset_creation.py").
# Idempotent: set replace_existing=True to re-import and overwrite; False to skip files that already exist in Content.
# See AssetCreation/README.md and docs/ASSET_WORKFLOW_AND_STEAM_DEMO.md.

import os
import sys

try:
    import unreal
except ImportError:
    print("Batch import: Run this script inside Unreal Editor.")
    sys.exit(1)

PREFIX = "batch_import_asset_creation:"
EXPORTS_SUBFOLDERS = ("Characters", "Harvestables", "Homestead", "Dungeon", "Biomes")
CONTENT_PREFIX = "/Game/HomeWorld"
EXTENSIONS = (".fbx", ".FBX", ".glb", ".GLB")


def _log(msg):
    unreal.log(PREFIX + " " + str(msg))
    print(PREFIX, msg)


def _project_root():
    cwd = os.getcwd()
    if os.path.isdir(cwd) and "Content" in (os.listdir(cwd) or []):
        return cwd
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Content/Python -> project root
    return os.path.normpath(os.path.join(script_dir, "..", ".."))


def _exports_dir(project_root):
    return os.path.join(project_root, "AssetCreation", "Exports")


def _collect_files(exports_dir):
    """Return list of (category, absolute_path) for each FBX/GLB under exports_dir."""
    out = []
    if not os.path.isdir(exports_dir):
        return out
    for category in EXPORTS_SUBFOLDERS:
        sub = os.path.join(exports_dir, category)
        if not os.path.isdir(sub):
            continue
        for name in os.listdir(sub):
            if not name.endswith(EXTENSIONS):
                continue
            out.append((category, os.path.join(sub, name)))
    return out


def main():
    project_root = _project_root()
    exports_dir = _exports_dir(project_root)
    if not os.path.isdir(exports_dir):
        _log("Exports directory not found: %s. Create AssetCreation/Exports/ and add FBX/GLB by category." % exports_dir)
        return 0

    files = _collect_files(exports_dir)
    if not files:
        _log("No FBX/GLB files found under %s. Add assets to Exports/<Category>/ and re-run." % exports_dir)
        return 0

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    tasks = []
    for category, filepath in files:
        name_no_ext = os.path.splitext(os.path.basename(filepath))[0]
        dest_path = "%s/%s" % (CONTENT_PREFIX, category)
        task = unreal.AssetImportTask()
        task.filename = filepath
        task.destination_path = dest_path
        task.destination_name = name_no_ext
        task.automated = True
        task.save = True
        task.replace_existing = True
        tasks.append(task)

    _log("Importing %d file(s) into %s/..." % (len(tasks), CONTENT_PREFIX))
    result = asset_tools.import_asset_tasks(tasks)
    if result:
        _log("Import completed. Check Output Log for any errors.")
    else:
        _log("Import returned False; check Output Log for errors.")
    return 0 if result else 1


if __name__ == "__main__":
    sys.exit(main())
