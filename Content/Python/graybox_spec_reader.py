"""Blender-side reader: measure the live scene against the Lib/01 specs and emit
a machine-checked report.

Runs inside Blender via the official Blender Lab MCP
(``execute_blender_code``) or the Scripting workspace. It does three things:

  1. MEASURE every spec'd volume out of the live scene -- name, world origin,
     bbox, pivot Z, poly count, material binding. Nothing is assumed.
  2. VERIFY against the spec on the Lead's criteria 1-3, plus the DEC-0018
     master-binding check.
  3. REPORT to a dict and to Markdown on disk.

It is deliberately **read-only by default**. ``--place`` is available and is
check-before-create: it never overwrites authored geometry. The blend already
holds a 1680-tri cabin, 864/648/540-tri cliff assemblies and 472-tri pines; a
reader that "emits placed primitives" would destroy authored work that took a
human modeler. See DEC-0019.

Usage from the MCP bridge -- the code is pre-seeded with a ``result`` dict:

    import sys; sys.path.insert(0, r"C:\\dev\\HomeWorld\\Content\\Python")
    import graybox_spec_reader as r
    result = r.run()

Or place missing volumes (check-before-create, never overwrites):

    result = r.run(place=True)
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any

try:
    import bpy  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover - only when run outside Blender
    bpy = None  # type: ignore[assignment]

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import homeworld_graybox_silhouette as silhouette  # noqa: E402
from homeworld_graybox_spec import (  # noqa: E402
    ALLOWED_MATERIAL_INSTANCES,
    MASTER_NAMES,
    Volume,
    all_spec_ids,
    load_all_specs,
    load_all_zone_specs,
    resolve_alias,
)

#: Per-class poly budget, asserted not assumed (DEC-0018). From
#: MVP_EXPORT_MANIFEST.md and the PA-C tranche handoffs.
POLY_BUDGET: dict[str, int] = {
    "SM_Cabin": 1680,
    "SM_Cliff_LookoutFace": 864,
    "SM_Cliff_CabinFace": 648,
    "SM_Cliff_Rear": 540,
    "SM_Pine_Homestead_S": 472,
    "SM_Pine_Homestead_M": 472,
    "SM_Pine_Homestead_L": 472,
    "SM_Glider_Perch": 132,
    "SM_Planter_A": 240,
    "SM_Planter_B": 336,
    "SM_Planter_C": 240,
    "SM_Garden_Fence_Seg": 100,
    "SM_PathStone_A": 24,
    "SM_PathStone_B": 20,
    "SM_PathStone_C": 28,
}

#: Per-class bbox height tolerance in meters. Generous at greybox tier -- these
#: catch a wrong scale, not a hand-tune.
HEIGHT_TOLERANCE_M: dict[str, float] = {
    "default": 0.5,
    "SM_IslandTop": 0.2,
    "SM_Path_Homestead": 0.1,
    "SM_Path_Planet_SegA": 0.1,
    "SM_Path_Planet_SegB": 0.1,
    "SM_Path_Planet_SegC": 0.1,
}

POSITION_TOLERANCE_M = 0.25

#: Footprint half-extents (x, y) of assembly roots, used only to check that a
#: child module sits inside its parent assembly. From GRAYBOX_LAYOUT.md and the
#: specs' own overall_size_m.
ASSEMBLY_FOOTPRINTS: dict[str, tuple[float, float]] = {
    "SM_Cabin": (5.5, 4.5),
    "SM_Garden_Beds": (4.0, 2.5),
    "SM_Island_Hero": (21.0, 14.0),
}


# --------------------------------------------------------------------------
# Measurement
# --------------------------------------------------------------------------


def measure_object(name: str) -> dict[str, Any] | None:
    """Measure one object out of the live scene. Read-only.

    Returns None when the object is absent, which is itself a finding: the
    verifier distinguishes 'missing' from 'wrong'.
    """
    if bpy is None:
        raise RuntimeError("measure_object requires bpy; run inside Blender")

    obj = bpy.data.objects.get(name)
    if obj is None:
        return None

    row: dict[str, Any] = {
        "name": obj.name,
        "type": obj.type,
        "world_origin": [round(v, 4) for v in obj.matrix_world.translation],
        "scale": [round(v, 4) for v in obj.scale],
        "parent": obj.parent.name if obj.parent else None,
    }

    if obj.type != "MESH":
        return row

    dims = obj.dimensions
    row["bbox"] = [round(v, 4) for v in dims]
    row["tris"] = sum(len(poly.vertices) - 2 for poly in obj.data.polygons)
    row["polys"] = len(obj.data.polygons)
    row["materials"] = [
        slot.material.name if slot.material else None for slot in obj.material_slots
    ]

    # Pivot Z is measured as the world Z of the origin, and separately as the
    # lowest vertex in world space. Ground-contact pivot means the second.
    matrix = obj.matrix_world
    zs = [(matrix @ vert.co).z for vert in obj.data.vertices]
    row["origin_z_world"] = round(matrix.translation.z, 4)
    row["lowest_vert_z_world"] = round(min(zs), 4) if zs else None
    row["pivot_is_ground_contact"] = bool(zs) and abs(min(zs)) <= 0.05
    row["scale_applied"] = all(abs(s - 1.0) <= 1e-4 for s in obj.scale)
    return row


def measure_scene(names: list[str]) -> dict[str, dict[str, Any] | None]:
    """Measure each name, plus every alias any name resolves to."""
    wanted: set[str] = set()
    for name in names:
        wanted.update(resolve_alias(name))
    return {name: measure_object(name) for name in sorted(wanted)}


# --------------------------------------------------------------------------
# Verification, criteria 1-3
# --------------------------------------------------------------------------


def verify(volume: Volume, measured: dict[str, Any] | None) -> list[dict[str, Any]]:
    """Compare one spec'd volume against its measurement. Returns findings."""
    findings: list[dict[str, Any]] = []

    if measured is None:
        findings.append(
            {
                "criterion": "1_location",
                "severity": "blocking",
                "volume": volume.name,
                "detail": "object not present in the blend",
            }
        )
        return findings

    if measured.get("type") != "MESH":
        # An Empty root is legitimate for an assembly; the children carry the
        # geometry. Reported as info, not a failure.
        findings.append(
            {
                "criterion": "1_location",
                "severity": "info",
                "volume": volume.name,
                "detail": "assembly root (%s); geometry on children"
                % measured.get("type"),
            }
        )
        return findings

    # --- criterion 1: right location -------------------------------------
    # A child module inherits its assembly's origin (CABIN_MODULES names 14
    # sub-modules without restating positions; they sit at offsets inside the
    # assembly). Comparing such a module's *world* origin against a spec origin
    # of (0,0,0) would report every cabin wall as 6 m out of place, which is how
    # the first pass produced 45 false blocking findings. For those the check is
    # containment: the module must sit inside its assembly's footprint.
    actual_origin = measured.get("world_origin") or [0.0, 0.0, 0.0]

    if volume.origin_is_explicit:
        for axis, index in (("x", 0), ("y", 1), ("z", 2)):
            delta = abs(actual_origin[index] - volume.origin[index])
            if delta > POSITION_TOLERANCE_M:
                findings.append(
                    {
                        "criterion": "1_location",
                        "severity": "blocking",
                        "volume": volume.name,
                        "detail": "%s origin off by %.3f m (spec %.3f, actual %.3f)"
                        % (axis, delta, volume.origin[index], actual_origin[index]),
                    }
                )
    elif volume.assembly_origin is not None:
        parent = measured.get("parent")
        if parent is not None and parent != volume.assembly:
            findings.append(
                {
                    "criterion": "1_location",
                    "severity": "warn",
                    "volume": volume.name,
                    "detail": "parented to '%s', spec assembly is '%s'"
                    % (parent, volume.assembly),
                }
            )
        ax, ay, _az = volume.assembly_origin
        half_x = ASSEMBLY_FOOTPRINTS.get(volume.assembly, (4.0, 4.0))[0] * 0.5
        half_y = ASSEMBLY_FOOTPRINTS.get(volume.assembly, (4.0, 4.0))[1] * 0.5
        outside_x = abs(actual_origin[0] - ax) > half_x + POSITION_TOLERANCE_M
        outside_y = abs(actual_origin[1] - ay) > half_y + POSITION_TOLERANCE_M
        if outside_x or outside_y:
            findings.append(
                {
                    "criterion": "1_location",
                    "severity": "blocking",
                    "volume": volume.name,
                    "detail": "child module sits outside assembly '%s' footprint "
                    "(module at %.3f, %.3f; assembly centre %.3f, %.3f)"
                    % (
                        volume.assembly,
                        actual_origin[0],
                        actual_origin[1],
                        ax,
                        ay,
                    ),
                }
            )

    # --- criterion 2: sized right ----------------------------------------
    bbox = measured.get("bbox") or [0.0, 0.0, 0.0]
    tol = HEIGHT_TOLERANCE_M.get(volume.name, HEIGHT_TOLERANCE_M["default"])
    for axis, index in (("x", 0), ("y", 1), ("z", 2)):
        expected = volume.size_m[index]
        if expected <= 0.0:
            continue  # spec names no size for this module
        delta = abs(bbox[index] - expected)
        threshold = tol if axis == "z" else max(tol, expected * 0.10)
        if delta > threshold:
            findings.append(
                {
                    "criterion": "2_sized",
                    "severity": "blocking",
                    "volume": volume.name,
                    "detail": "%s bbox %.3f vs spec %.3f (off by %.3f, tolerance %.3f)"
                    % (axis, bbox[index], expected, delta, threshold),
                }
            )

    if not measured.get("scale_applied", True):
        findings.append(
            {
                "criterion": "2_sized",
                "severity": "blocking",
                "volume": volume.name,
                "detail": "object scale is not applied (%.3f, %.3f, %.3f); art bible S10"
                % tuple(measured.get("scale", [1.0, 1.0, 1.0])),
            }
        )

    if volume.pivot_is_ground_contact and not measured.get("pivot_is_ground_contact"):
        findings.append(
            {
                "criterion": "2_sized",
                "severity": "blocking",
                "volume": volume.name,
                "detail": "origin is not at ground contact (lowest vertex at Z %.3f)"
                % (measured.get("lowest_vert_z_world") or 0.0),
            }
        )

    # --- DEC-0018: poly budget, asserted not assumed ---------------------
    budget = POLY_BUDGET.get(volume.name)
    tris = measured.get("tris") or 0
    if budget is not None and tris > budget:
        findings.append(
            {
                "criterion": "poly_budget",
                "severity": "blocking",
                "volume": volume.name,
                "detail": "%d tris exceeds the %d budget from MVP_EXPORT_MANIFEST.md"
                % (tris, budget),
            }
        )

    # --- DEC-0018(e): one of the ten masters, generated textures banned ---
    for material in measured.get("materials") or []:
        if material is None:
            continue
        if material in MASTER_NAMES or material in ALLOWED_MATERIAL_INSTANCES:
            continue
        findings.append(
            {
                "criterion": "master_binding",
                "severity": "blocking",
                "volume": volume.name,
                "detail": "material '%s' is not one of the ten masters and not an "
                "allowed instance; this is an 11th family" % material,
            }
        )

    return findings


def check_materials_in_blend() -> list[dict[str, Any]]:
    """DEC-0018(e) across the whole blend, not just spec'd volumes."""
    findings = []
    if bpy is None:
        return findings
    for material in bpy.data.materials:
        name = material.name
        if name in MASTER_NAMES or name in ALLOWED_MATERIAL_INSTANCES:
            continue
        findings.append(
            {
                "criterion": "master_binding",
                "severity": "blocking",
                "volume": name,
                "detail": "material in the blend is neither one of the ten masters nor "
                "an allowed instance (art bible S10)",
            }
        )
    return findings


# --------------------------------------------------------------------------
# Place: check-before-create, never overwrite
# --------------------------------------------------------------------------


def place(volume: Volume) -> str:
    """Create a volume if absent. Never overwrites authored geometry.

    Returns 'created', 'exists' or 'skipped'.

    A child module is placed at its ASSEMBLY's origin, not at (0,0,0). The first
    version read volume.origin directly, and for every module that inherits its
    assembly origin that is the zero vector -- so placing a kettle put its body and
    handle at world zero while the spec said (-4.5, 3.2, 0). The verifier then
    correctly reported them as outside the assembly footprint, which is how the bug
    surfaced. See DEC-0025.
    """
    if bpy is None:
        raise RuntimeError("place requires bpy; run inside Blender")

    # Check every alias, not just the spec name. SM_Island_Hero resolves to SM_IslandTop
    # because the blend already holds the plateau under that name; testing only the spec
    # name created a second 21x14 box beside the first, which is the "rival object"
    # failure the spirit work is told to avoid.
    for candidate in resolve_alias(volume.name):
        if bpy.data.objects.get(candidate) is not None:
            return "exists"

    if volume.size_m == (0.0, 0.0, 0.0):
        return "skipped"  # spec names the module without a size

    # An assembly read is a SYNTHESIS - the union of its parts' boxes, computed so the
    # collision check has a zone-level unit. It is not geometry. Placing it grew a
    # duplicate object per beat state, which is the "rival object" failure the spirit
    # work is explicitly told to avoid, so it is refused here rather than cleaned up
    # afterwards. See DEC-0026.
    if volume.is_assembly_read:
        return "synthesis"

    # Where this part actually goes.
    if volume.origin_is_explicit:
        location = volume.origin
    elif volume.assembly_origin is not None:
        location = volume.assembly_origin
    else:
        location = volume.origin

    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = volume.name
    obj.data.name = volume.name
    obj.scale = volume.size_m
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.location = location

    # Move the lowest vertex to ground contact if the spec asserts it.
    if volume.pivot_is_ground_contact:
        zs = [vert.co.z for vert in obj.data.vertices]
        if zs:
            obj.location.z += -min(zs)

    return "created"


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------


def _all_volumes() -> list[Volume]:
    """Every volume across every spec: Lib/01 homestead and Lib/02 zone kits.

    Both sources feed one verification pass. They are kept separate in the repo
    (DEC-0020) because the 39-volume layout table is cited elsewhere, but the
    report has to cover both or it would read PASS while a zone prop is missing.
    """
    volumes: list[Volume] = []
    for spec in load_all_specs():
        volumes.extend(spec.volumes)
    for spec in load_all_zone_specs():
        volumes.extend(spec.volumes)
    return volumes


def run(place_missing: bool = False, **kwargs: Any) -> dict[str, Any]:
    """Full pass: measure, verify, and return a machine-checked report dict.

    ``place=True`` is an alias for ``place_missing=True`` (docstring / MCP callers).
    When both are set, either true enables place-missing (check-before-create).
    """
    if bpy is None:
        raise RuntimeError("run() requires bpy; run inside Blender")

    if "place" in kwargs:
        place_missing = bool(place_missing) or bool(kwargs.pop("place"))
    if kwargs:
        raise TypeError("run() got unexpected keyword argument(s): %s" % ", ".join(sorted(kwargs)))

    bpy.context.view_layer.update()

    volumes = _all_volumes()
    names = [volume.name for volume in volumes]

    placed: dict[str, str] = {}
    if place_missing:
        for volume in volumes:
            placed[volume.name] = place(volume)

    measured = measure_scene(names)

    findings: list[dict[str, Any]] = []
    for volume in volumes:
        # Resolve through the alias table so a spec module authored as a
        # mirrored pair is verified against what is actually in the blend.
        row: dict[str, Any] | None = None
        matched_as: str | None = None
        for candidate in resolve_alias(volume.name):
            row = measured.get(candidate)
            if row is not None:
                matched_as = candidate
                break
        # An assembly read is a SYNTHESIS: the union of its parts' bounding boxes,
        # computed so the collision check has a zone-level unit to measure. It is not
        # a real object and must never be demanded in the scene -- the first version
        # that placed it created a duplicate object per beat state, which is exactly
        # the "rival object" failure the spirit work is told to avoid.
        if volume.is_assembly_read and row is None:
            continue
        findings.extend(verify(volume, row))
        if matched_as and matched_as != volume.name:
            findings.append(
                {
                    "criterion": "1_location",
                    "severity": "info",
                    "volume": volume.name,
                    "detail": "spec module resolved to authored object '%s'" % matched_as,
                }
            )
    findings.extend(check_materials_in_blend())

    assertable = [volume for volume in volumes if volume.is_assertable]
    collisions = silhouette.find_collisions(assertable)
    conformance = silhouette.family_conformance(assertable)

    for volume, message in conformance:
        findings.append(
            {
                "criterion": "4_distinct",
                "severity": "blocking",
                "volume": volume.name,
                "detail": message,
            }
        )

    for collision in collisions:
        findings.append(
            {
                "criterion": "4_distinct",
                "severity": collision.severity,
                "volume": "%s vs %s" % (collision.a.name, collision.b.name),
                "detail": collision.reason,
            }
        )

    unassigned = [
        volume.name
        for volume in volumes
        if volume.family_status not in ("assigned", "helper")
    ]

    blocking = [f for f in findings if f["severity"] == "blocking"]
    by_criterion: dict[str, int] = {}
    for finding in findings:
        key = finding["criterion"]
        by_criterion[key] = by_criterion.get(key, 0) + 1

    families_present = sorted({v.family for v in assertable})

    return {
        "blender": bpy.app.version_string,
        "blend_file": bpy.data.filepath,
        "spec_ids": list(all_spec_ids()),
        "volumes_measured": len(measured),
        "volumes_present": sum(1 for m in measured.values() if m is not None),
        "volumes_assertable": len(assertable),
        "families_present": families_present,
        "unassigned": unassigned,
        "placed": placed,
        "measurements": measured,
        "collisions": [collision.describe() for collision in collisions],
        "family_conformance": [
            {"volume": volume.name, "detail": message} for volume, message in conformance
        ],
        "findings": findings,
        "blocking_count": len(blocking),
        "by_criterion": by_criterion,
        "passed": not blocking,
    }


def to_markdown(report: dict[str, Any]) -> str:
    """Render the report dict as Markdown for review."""
    lines = [
        "# Graybox spec verification report",
        "",
        "Generated by `Content/Python/graybox_spec_reader.py` from "
        "`Lib/01_Homestead/*.json` against the live blend.",
        "",
        "| Field | Value |",
        "|---|---|",
        "| Blender | %s |" % report.get("blender"),
        "| Blend | `%s` |" % report.get("blend_file"),
        "| Specs read | %s |" % ", ".join(report.get("spec_ids", [])),
        "| Volumes measured | %s |" % report.get("volumes_measured"),
        "| Volumes present | %s |" % report.get("volumes_present"),
        "| Volumes assertable | %s |" % report.get("volumes_assertable"),
        "| Families represented | %s |" % ", ".join(report.get("families_present", [])),
        "| **Blocking findings** | **%s** |" % report.get("blocking_count"),
        "| Result | %s |" % ("PASS" if report.get("passed") else "FAIL"),
        "",
    ]

    lines += [
        "",
        "## Measured bbox",
        "",
        "| Name | Bbox xyz (m) | World origin |",
        "|---|---|---|",
    ]
    measurements = report.get("measurements") or {}
    for name in sorted(measurements.keys()):
        row = measurements.get(name)
        if row is None:
            lines.append("| `%s` | *(absent)* | — |" % name)
            continue
        bbox = row.get("bbox")
        origin = row.get("world_origin")
        if bbox is None:
            bbox_s = "*(non-mesh)*"
        else:
            bbox_s = "%.4f × %.4f × %.4f" % (bbox[0], bbox[1], bbox[2])
        if origin is None:
            origin_s = "—"
        else:
            origin_s = "%.4f, %.4f, %.4f" % (origin[0], origin[1], origin[2])
        lines.append("| `%s` | %s | %s |" % (name, bbox_s, origin_s))

    lines += ["", "## Findings by criterion", "", "| Criterion | Count |", "|---|---|"]
    for criterion, count in sorted(report.get("by_criterion", {}).items()):
        lines.append("| `%s` | %d |" % (criterion, count))

    findings = report.get("findings", [])
    if findings:
        lines += ["", "## Blocking", "", "| Criterion | Volume | Detail |", "|---|---|---|"]
        for finding in findings:
            if finding["severity"] != "blocking":
                continue
            lines.append(
                "| `%s` | `%s` | %s |"
                % (finding["criterion"], finding["volume"], finding["detail"])
            )

    lines += [
        "",
        "## Caveat",
        "",
        "Criterion 4 is a **house standard**. There is no published industry standard "
        "for a greybox silhouette-distinctness check, and no source shows anyone "
        "running one programmatically -- Shaver's method is a manual squint test. "
        "`ASPECT_TOLERANCE` is a change detector with no measured eye threshold behind "
        "it. Report a collision as a prompt to look, never as proof.",
        "",
    ]
    return "\n".join(lines)


def write_report(report: dict[str, Any], directory: str) -> tuple[str, str]:
    """Write JSON + Markdown. Returns the two paths."""
    os.makedirs(directory, exist_ok=True)
    json_path = os.path.join(directory, "graybox_spec_report.json")
    md_path = os.path.join(directory, "GRAYBOX_SPEC_REPORT.md")
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
    with open(md_path, "w", encoding="utf-8") as handle:
        handle.write(to_markdown(report))
    return json_path, md_path
