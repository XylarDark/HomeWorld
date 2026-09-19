import unreal, os, math

def logf(m):
    path = os.path.join(unreal.Paths.project_saved_dir(), "d19_probe.txt")
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
    unreal.SystemLibrary.execute_console_command(pie_world(), cmd, None)
    logf("console %s" % cmd)

def aim_at(target, dist=100.0):
    w, pc, p = pawn_pc()
    if not p or not target or not pc:
        logf("aim fail t=%s" % target)
        return False
    sl = target.get_actor_location()
    new = unreal.Vector(sl.x - dist, sl.y, sl.z + 30.0)
    p.set_actor_location(new, False, True)
    yaw = math.degrees(math.atan2(sl.y - new.y, sl.x - new.x))
    rot = unreal.Rotator(0.0, yaw, 0.0)
    p.set_actor_rotation(rot, True)
    pc.set_control_rotation(rot)
    logf("aimed %s yaw=%.1f" % (target.get_actor_label(), yaw))
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
console("hw.TimeOfDay.SetPhase 0")

# D19-A: harvest from pile label
g = find_label("GP_Gather_WOOD")
logf("GP_Gather_WOOD=%s" % g)
if g:
    aim_at(g)
    call_try("try_harvest_in_front")
else:
    logf("MISSING pile label")

# D19-B: seed cheat + N1 nurture at night
console("hw.Gather.Seed 2")
console("hw.TimeOfDay.SetPhase 2")
n1 = find_label("GP_N1_Crop")
logf("GP_N1_Crop=%s" % n1)
if n1:
    aim_at(n1)
    call_try("try_nurture_in_front")

console("hw.Inventory.Dump")
logf("d19 batch done")
