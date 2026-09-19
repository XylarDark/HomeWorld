import unreal, json, os
out = r"C:\dev\HomeWorld\Saved\PL_D_cam_inventory.json"
actors = []
for a in unreal.EditorLevelLibrary.get_all_level_actors():
    try:
        lab = a.get_actor_label() or ""
        cls = a.get_class().get_name()
    except Exception:
        continue
    if any(x in lab.upper() for x in ("CAM", "SHOT", "LOOKOUT", "HERO", "VS_MARKER")) or "Camera" in cls or "CineCamera" in cls:
        loc = a.get_actor_location()
        actors.append({"label": lab, "class": cls, "loc": [loc.x, loc.y, loc.z]})
# also any TargetPoint
tps = []
for a in unreal.EditorLevelLibrary.get_all_level_actors():
    try:
        lab = a.get_actor_label() or ""
        cls = a.get_class().get_name()
    except Exception:
        continue
    if "TargetPoint" in cls or lab.startswith("CAM_") or lab.startswith("VS_"):
        loc = a.get_actor_location()
        tps.append({"label": lab, "class": cls, "loc": [round(loc.x,1), round(loc.y,1), round(loc.z,1)]})
world = unreal.EditorLevelLibrary.get_editor_world()
result = {
    "editor_world": str(world.get_path_name() if world else None),
    "cam_like": actors[:40],
    "target_or_cam_labels": tps[:60],
    "counts": {"cam_like": len(actors), "target_or_cam": len(tps)},
}
open(out, "w", encoding="utf-8").write(json.dumps(result, indent=2))
print("wrote", out, "cam_like", len(actors), "tps", len(tps))
