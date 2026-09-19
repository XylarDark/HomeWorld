import unreal
import os

def pie_world():
    try:
        worlds = unreal.EditorLevelLibrary.get_pie_worlds(include_dedicated_server=False)
        return worlds[0] if worlds else None
    except Exception as e:
        return "ERR:%s" % e

def out(msg):
    path = os.path.join(unreal.Paths.project_saved_dir(), "vp2_b_probe.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    unreal.log(msg)

out("--- probe ---")
w = pie_world()
out("world=%s type=%s" % (w, type(w).__name__))
if w is None or isinstance(w, str):
    out("NO WORLD")
else:
    pc = unreal.GameplayStatics.get_player_controller(w, 0)
    out("pc=%s" % pc)
    p = pc.get_controlled_pawn() if pc else None
    out("pawn=%s cls=%s" % (p, p.get_class().get_name() if p else None))
    # list labels containing GP_
    labels = []
    for a in unreal.GameplayStatics.get_all_actors_of_class(w, unreal.Actor):
        try:
            lab = a.get_actor_label()
        except Exception:
            lab = ""
        if lab and ("GP_" in lab or "Store" in lab or "Beast" in lab or "Spirit" in lab or "N1" in lab or "N2" in lab or "Gather" in lab):
            labels.append(lab)
    out("labels=%s" % sorted(set(labels))[:40])
    # try console
    try:
        unreal.SystemLibrary.execute_console_command(w, "hw.Gather.Ore 1", None)
        out("console ore ok")
    except Exception as e:
        out("console err %s" % e)
    # methods on pawn
    if p:
        for n in ("try_store_transfer_in_front","try_harvest_in_front","try_nurture_in_front","try_heal_spirit_in_front","try_tame_beast_in_front"):
            out("%s=%s" % (n, hasattr(p, n)))
