"""Regenerate the greybox spec report from the LIB blend. Run inside Blender.

    blender --background blender/floating_island_homestead_LIB.blend \
            --python Content/Python/graybox_report_driver.py

WHY THIS FILE EXISTS
``graybox_spec_reader.py`` measures the live scene and can write its report, but it
has no ``__main__`` block -- it is a library meant to be driven from the MCP bridge
or the Scripting workspace. That left the report with no *committed* way to be
regenerated, so it silently went stale: it carried a 1.4 m y-mismatch against a
21 x 14 spec long after the Lead locked 180 x 100, and nothing failed. A stale gate
that still looks authoritative is worse than no gate.

This is that missing entry point, and nothing more. It is read-only: it calls
``run()`` with ``place_missing=False`` and never saves the blend, so authored
geometry is untouched. The one thing it does write is the report itself.

Output goes to Docs/qa/graybox_spec_report.json and Docs/qa/GRAYBOX_SPEC_REPORT.md.
"""

import os
import sys

import bpy

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(REPO, "Content", "Python"))

import graybox_spec_reader as reader  # noqa: E402


def main() -> int:
    if not bpy.data.filepath:
        print("GGBLEND_REFUSING: no blend is open. Open the LIB blend first -- the "
              "report measures the live scene, so running this against an empty "
              "file would report 0 objects and 0 findings and look like a pass.")
        return 2

    print("GGBLEND:", bpy.data.filepath)
    print("GGVER:", bpy.app.version_string)

    report = reader.run()                      # read-only: place_missing defaults False
    json_path, md_path = reader.write_report(report, os.path.join(REPO, "Docs", "qa"))

    print("GGWROTE:", json_path)
    print("GGWROTE:", md_path)
    print("GGOBJECTS:", len(bpy.data.objects))
    print("GGPASSED:", report.get("passed"))
    print("GGBLOCKING:", report.get("blocking_count"))
    print("GGCRITERIA:", report.get("by_criterion"))

    # Surface the island measurement explicitly. It is the number the Lead's
    # 180 x 100 lock is judged against and the one that has moved before.
    for key, value in (report.get("measurements") or {}).items():
        if key == "SM_IslandTop":
            print("GGMEAS", key, "bbox=", value.get("bbox"),
                  "top_vert_z_world=", value.get("top_vert_z_world"),
                  "lowest_vert_z_world=", value.get("lowest_vert_z_world"))

    for finding in report.get("findings") or []:
        if finding.get("criterion") != "1_location":
            print("GGFINDING", finding.get("criterion"), "|",
                  finding.get("volume"), "|", str(finding.get("detail"))[:110])

    print("GGDONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())