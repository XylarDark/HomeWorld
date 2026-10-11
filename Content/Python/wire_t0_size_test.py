"""Tag the size-test map so the existing T0 verbs can be walked.

Loads L_SizeTest. Does not rebuild meshes. Re-running updates labels and does not duplicate them.
"""

import os
import sys

try:
    import unreal
except ImportError:
    print("wire_t0_size_test: run inside Unreal Editor")
    sys.exit(1)

MAP_PATH = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"
PREFIX = "wire_t0_size_test:"
M = 100.0


def log(message):
    unreal.log(PREFIX + " " + str(message))
    print(PREFIX, message)


def actors():
    return unreal.get_editor_subsystem(unreal.EditorActorSubsystem).get_all_level_actors()


def find_label(label):
    for actor in actors():
        try:
            if actor.get_actor_label() == label:
                return actor
        except Exception:
            continue
    return None


def add_tag(actor, tag_name):
    tag = unreal.Name(tag_name)
    current = list(actor.tags)
    if tag not in current:
        current.append(tag)
        actor.tags = current


def tag_existing(label, tag_name):
    actor = find_label(label)
    if actor is None:
        log("missing " + label)
        return None
    add_tag(actor, tag_name)
    log("tagged %s %s" % (label, tag_name))
    return actor


def load_class(class_name):
    try:
        return unreal.load_class(None, "/Script/HomeWorld." + class_name)
    except Exception:
        return getattr(unreal, class_name, None)


def spawn_once(label, cls, location, rotation=None):
    actor = find_label(label)
    if actor is not None:
        actor.set_actor_location(location, False, False)
        return actor
    if rotation is None:
        rotation = unreal.Rotator(0.0, 0.0, 0.0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(cls, location, rotation)
    if actor is None:
        log("FAILED spawn " + label)
        return None
    actor.set_actor_label(label)
    log("spawned " + label)
    return actor


def vec(x_m, y_m, z_m):
    return unreal.Vector(x_m * M, y_m * M, z_m * M)


def main():
    if not unreal.EditorAssetLibrary.does_asset_exist(MAP_PATH):
        log("missing map " + MAP_PATH)
        return 1
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).load_level(MAP_PATH)

    tag_existing("SM_Size_Bed", "NODE_BED")
    tag_existing("SM_Size_Kettle", "NODE_KETTLE")
    tag_existing("SM_Size_HerbBed", "NODE_GARDEN")
    tag_existing("SM_Size_Herb", "NODE_FIELD_GATHER")
    tag_existing("SM_Size_Stump", "NODE_MIX")
    tag_existing("SM_Size_Fire", "NODE_DAY_CAMP")
    tag_existing("SK_Size_Partner", "NPC_PARTNER")
    tag_existing("SK_Size_Child", "NPC_CHILD")
    tag_existing("SK_Size_Bull", "NODE_BULL")

    mesh_rock = unreal.EditorAssetLibrary.load_asset("/Game/HomeWorld/Meshes/SizeTest/SM_Size_Rock")
    mesh_fence = unreal.EditorAssetLibrary.load_asset("/Game/HomeWorld/Meshes/SizeTest/SM_Size_Fence")
    mesh_crystal = unreal.EditorAssetLibrary.load_asset("/Game/HomeWorld/Meshes/SizeTest/SM_Size_Crystal")

    def place_mesh(label, mesh, location, tag_name):
        actor = find_label(label)
        if actor is None and mesh is not None:
            actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
                unreal.StaticMeshActor, location, unreal.Rotator(0.0, 0.0, 0.0)
            )
            if actor is not None:
                actor.get_component_by_class(unreal.StaticMeshComponent).set_static_mesh(mesh)
                actor.set_actor_label(label)
        if actor is not None:
            actor.set_actor_location(location, False, False)
            add_tag(actor, tag_name)
            log("placed %s" % label)
        return actor

    place_mesh("NODE_WOUND", mesh_crystal, vec(-4, -2, 451), "NODE_WOUND")
    place_mesh("NODE_DUNG", mesh_rock, vec(850, 8, 0), "NODE_DUNG")
    place_mesh("NODE_BARN", mesh_fence, vec(-14, -2, 451), "NODE_BARN")

    pile_class = load_class("HomeWorldResourcePile")
    if pile_class is not None:
        for label, location in (
            ("PILE_WOOD", vec(870, 10, 0)),
            ("PILE_BERRY", vec(890, -16, 0)),
        ):
            spawn_once(label, pile_class, location)
            log("pile %s stays on the class resource (ResourceType is not per instance)" % label)

    camp_class = load_class("HomeWorldCampActor")
    if camp_class is not None:
        role = unreal.HomeWorldCampRole
        for label, guard_role, location in (
            ("NODE_GUARD", role.GUARD, vec(1054, 2, 0)),
            ("NODE_GUARD_1", role.GUARD, vec(1066, 2, 0)),
            ("NODE_GUARD_2", role.GUARD, vec(1060, -4, 0)),
            ("NODE_CAPTIVE", role.CAPTIVE, vec(1060, 6, 0)),
        ):
            actor = spawn_once(label, camp_class, location)
            if actor is None:
                continue
            actor.set_editor_property("CampRole", guard_role)
            actor.set_actor_label(label)
            if hasattr(actor, "refresh_camp_identity"):
                actor.refresh_camp_identity()

    portal_class = load_class("HomeWorldShrinePortalTrigger")
    if portal_class is not None:
        home = spawn_once("NODE_SHRINE", portal_class, vec(-16, -6, 451))
        camp = spawn_once("NODE_SHRINE_CAMP", portal_class, vec(1072, 0, 0))
        for actor, destination in ((home, "NODE_SHRINE_CAMP"), (camp, "NODE_SHRINE")):
            if actor is None:
                continue
            component = actor.get_component_by_class(unreal.HomeWorldShrinePortalComponent)
            if component is not None:
                component.set_editor_property("DestinationLabel", unreal.Name(destination))
                component.set_editor_property("bRequireNight", False)

    wisp_class = load_class("HomeWorldCloudWisp")
    if wisp_class is not None:
        spawn_once("CLOUD_WISP_A", wisp_class, vec(400, 0, 250))
        spawn_once("CLOUD_WISP_B", wisp_class, vec(650, 0, 150))

    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
    log("saved " + MAP_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
