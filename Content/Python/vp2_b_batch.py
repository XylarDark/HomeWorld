import unreal
import os
import math

def logf(m):
    path = os.path.join(unreal.Paths.project_saved_dir(), "vp2_b_probe.txt")
    with open(path, "a", encoding="utf-8") as f:
        f.write(m + "\n")
    unreal.log(m)

def pie_world():
    worlds = unreal.EditorLevelLibrary.get_pie_worlds(include_dedicated_server=False)
    return worlds[0] if worlds else None

def pawn_pc():
    w = pie_world()
    pc = unreal.GameplayStatics.get_player_controller(w, 0)
    return w, pc, pc.get_controlled_pawn() if pc else None

def find_label(label):
    w = pie_world()
    for a in unreal.GameplayStatics.get_all_actors_of_class(w, unreal.Actor):
        try:
            if a.get_actor_label() == label:
                return a
        except Exception:
            pass
    return None

def console(cmd):
    w = pie_world()
    unreal.SystemLibrary.execute_console_command(w, cmd, None)
    logf("console %s" % cmd)

def aim_at(target, dist=100.0):
    w, pc, p = pawn_pc()
    if not p or not target or not pc:
        logf("aim fail")
        return False
    sl = target.get_actor_location()
    new = unreal.Vector(sl.x - dist, sl.y, sl.z + 30.0)
    p.set_actor_location(new, False, True)
    yaw = math.degrees(math.atan2(sl.y - new.y, sl.x - new.x))
    rot = unreal.Rotator(0.0, yaw, 0.0)
    p.set_actor_rotation(rot, True)
    pc.set_control_rotation(rot)
    logf("aimed %s dist=%s yaw=%.1f loc=%s" % (target.get_actor_label(), dist, yaw, p.get_actor_location()))
    return True

def call_try(name):
    _, _, p = pawn_pc()
    fn = getattr(p, name, None)
    if not fn:
        logf("missing %s" % name)
        return False
    r = fn()
    logf("%s -> %s" % (name, r))
    return bool(r)

console("log LogTemp Log")

# DAY body verbs
console("hw.TimeOfDay.SetPhase 0")
g = find_label("GP_Gather_WOOD")
if g:
    aim_at(g)
    call_try("try_harvest_in_front")
else:
    logf("NO GP_Gather_WOOD")
    console("hw.GrantBossReward 3")

console("hw.Gather.Ore 2")
aim_at(find_label("GP_Store_STONE"))
call_try("try_store_transfer_in_front")

console("hw.Gather.Flowers 2")
aim_at(find_label("GP_BeastPad"))
call_try("try_tame_beast_in_front")

# NIGHT spirit
console("hw.TimeOfDay.SetPhase 2")
console("hw.Gather.Flowers 2")
aim_at(find_label("GP_SpiritWisp_A"))
call_try("try_heal_spirit_in_front")

console("hw.GrantBossReward 5")
aim_at(find_label("GP_N2_Stored"))
call_try("try_nurture_in_front")

# DAWN (skip FALLBACK this pass — crashed editor last time)
console("hw.Inventory.Dump")
console("hw.TimeOfDay.SetPhase 3")
logf("done success-path batch")
