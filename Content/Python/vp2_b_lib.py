import unreal, os, math
def logf(msg):
    p = os.path.join(unreal.Paths.project_saved_dir(), "vp2_b_probe.txt")
    with open(p, "a", encoding="utf-8") as f: f.write(msg+"\n")
    unreal.log(msg)
def pie_world():
    worlds = unreal.EditorLevelLibrary.get_pie_worlds(include_dedicated_server=False)
    return worlds[0] if worlds else None
def pawn():
    w = pie_world()
    if not w: return None
    pc = unreal.GameplayStatics.get_player_controller(w, 0)
    return pc.get_controlled_pawn() if pc else None
def find_label(label):
    w = pie_world()
    if not w: return None
    for a in unreal.GameplayStatics.get_all_actors_of_class(w, unreal.Actor):
        try:
            if a.get_actor_label() == label: return a
        except Exception: pass
    return None
def teleport_near(target, dist=140.0):
    p = pawn()
    if not p or not target:
        logf("teleport fail p=%s t=%s" % (p, target)); return False
    loc = target.get_actor_location()
    new_loc = unreal.Vector(loc.x - dist, loc.y, loc.z + 40.0)
    ok = p.set_actor_location(new_loc, False, False)
    dx = loc.x - new_loc.x; dy = loc.y - new_loc.y
    yaw = math.degrees(math.atan2(dy, dx))
    p.set_actor_rotation(unreal.Rotator(0.0, yaw, 0.0), False)
    logf("teleport ok=%s to %s yaw=%.1f" % (ok, new_loc, yaw))
    return True
def console(cmd):
    w = pie_world()
    unreal.SystemLibrary.execute_console_command(w, cmd, None)
    logf("console %s" % cmd)
def call_try(name):
    p = pawn()
    fn = getattr(p, name, None) if p else None
    if not fn:
        logf("missing %s" % name); return False
    try:
        r = fn(); logf("%s -> %s" % (name, r)); return bool(r)
    except Exception as e:
        logf("%s EXC %s" % (name, e)); return False
