# vp2_b_one_shot_success.py — careful success-path provocations (no mega hang)
import unreal

def pie_world():
    try:
        worlds = unreal.EditorLevelLibrary.get_pie_worlds(False)
        return worlds[0] if worlds else None
    except Exception:
        return None

def pawn():
    w = pie_world()
    if not w:
        return None
    pc = unreal.GameplayStatics.get_player_controller(w, 0)
    return pc.get_controlled_pawn() if pc else None

def find_label(label):
    w = pie_world()
    if not w:
        return None
    for a in unreal.GameplayStatics.get_all_actors_of_class(w, unreal.Actor):
        try:
            if a.get_actor_label() == label:
                return a
        except Exception:
            pass
        try:
            if a.get_name() == label or label in a.get_name():
                return a
        except Exception:
            pass
    return None

def teleport_near(target, dist=120.0):
    p = pawn()
    if not p or not target:
        unreal.log_warning("teleport: missing pawn/target")
        return False
    loc = target.get_actor_location()
    # stand slightly offset so facing toward target
    fwd = target.get_actor_forward_vector()
    # use world X offset instead if zero
    offset = unreal.Vector(dist, 0.0, 0.0)
    new_loc = unreal.Vector(loc.x - dist, loc.y, loc.z + 50.0)
    p.set_actor_location(new_loc, False, False)
    # face target
    to = unreal.Vector(loc.x - new_loc.x, loc.y - new_loc.y, 0.0)
    if to.length() > 1.0:
        rot = to.rotator()
        p.set_actor_rotation(rot, False)
    unreal.log("teleport_near ok -> %s at %s" % (target.get_actor_label(), new_loc))
    return True

def call_try(method_name):
    p = pawn()
    if not p:
        unreal.log_warning("no pawn for %s" % method_name)
        return False
    # UE Python: snake_case
    fn = getattr(p, method_name, None)
    if fn is None:
        unreal.log_warning("missing method %s on %s" % (method_name, p.get_class().get_name()))
        return False
    try:
        r = fn()
        unreal.log("%s -> %s" % (method_name, r))
        return bool(r)
    except Exception as e:
        unreal.log_warning("%s exception: %s" % (method_name, e))
        return False

def grant_via_cheat(cmd):
    unreal.SystemLibrary.execute_console_command(pie_world(), cmd, None)

def main():
    p = pawn()
    if not p:
        unreal.log_warning("vp2_b: no PIE pawn")
        return
    unreal.log("vp2_b: pawn=%s" % p.get_class().get_name())

    # DAY / BODY — gather wood from pile, store stone (cheat), tame herb
    grant_via_cheat("hw.TimeOfDay.SetPhase 0")
    # ensure day body - phase 0 should be day

    wood = find_label("GP_Gather_WOOD")
    if wood:
        teleport_near(wood, 150)
        call_try("try_harvest_in_front")
    else:
        unreal.log_warning("no GP_Gather_WOOD")
        grant_via_cheat("hw.GrantBossReward 3")

    store = find_label("GP_Store_STONE")
    grant_via_cheat("hw.Gather.Ore 2")
    if store:
        teleport_near(store, 150)
        call_try("try_store_transfer_in_front")
    else:
        unreal.log_warning("no GP_Store_STONE")

    beast = find_label("GP_BeastPad")
    grant_via_cheat("hw.Gather.Flowers 2")
    if beast:
        teleport_near(beast, 150)
        call_try("try_tame_beast_in_front")

    glide = find_label("GP_GlideStart")
    if not glide:
        glide = find_label("CRUMB_Depart_Lookout")
    if glide:
        teleport_near(glide, 80)
        call_try("try_start_fallback_glide")

    # NIGHT / SPIRIT — heal + nurture
    grant_via_cheat("hw.TimeOfDay.SetPhase 2")
    # form may auto-switch with phase; if not, interact ability still gates

    heal = find_label("GP_SpiritWisp_A")
    grant_via_cheat("hw.Gather.Flowers 2")
    if heal:
        teleport_near(heal, 150)
        call_try("try_heal_spirit_in_front")

    # N2 needs wood; N1 needs seed — try N2 with boss wood; also try grant seed via inventory if exposed
    grant_via_cheat("hw.GrantBossReward 5")
    n2 = find_label("GP_N2_Stored")
    if n2:
        teleport_near(n2, 150)
        call_try("try_nurture_in_front")
    n1 = find_label("GP_N1_Crop")
    if n1:
        # try add seed via component if possible
        teleport_near(n1, 150)
        call_try("try_nurture_in_front")

    grant_via_cheat("hw.Inventory.Dump")
    # DAWN
    grant_via_cheat("hw.TimeOfDay.SetPhase 3")
    unreal.log("vp2_b: one-shot done")

if __name__ == "__main__":
    main()
else:
    main()
