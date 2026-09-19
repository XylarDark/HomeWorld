import unreal, os, json
out = r"C:\dev\HomeWorld\Saved\PL_C_place.json"
labels = ["GP_Store_WOOD","GP_Store_FIBER","GP_Store_STONE","GP_Store_BERRY","GP_Store_HERB","GP_Store_SEED"]
found = {}
errs = []
for a in unreal.EditorLevelLibrary.get_all_level_actors():
    try:
        lab = a.get_actor_label()
    except Exception as e:
        continue
    if lab and "Store" in lab:
        found[lab] = a.get_class().get_name()
cls = unreal.load_class(None, "/Script/HomeWorld.HomeWorldStoreProp")
result = {"class_loaded": bool(cls), "store_like": found, "count": len(found)}
open(out,"w",encoding="utf-8").write(json.dumps(result, indent=2))
