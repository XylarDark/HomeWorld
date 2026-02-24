# test_character.py
# PythonAutomationTest: validates character Blueprint configuration.

import unreal

BP_PATH = "/Game/HomeWorld/Characters/BP_HomeWorldCharacter"
ABP_PATH = "/Game/HomeWorld/Characters/ABP_HomeWorldCharacter"


def _load_character_cdo():
    bp = unreal.load_asset(BP_PATH)
    assert bp, "Could not load BP_HomeWorldCharacter"
    gen_class = None
    try:
        gen_class = bp.generated_class()
    except Exception:
        gen_class = bp.get_editor_property("generated_class")
    assert gen_class, "No generated class"
    cdo = unreal.get_default_object(gen_class)
    assert cdo, "No CDO"
    return cdo


def test_character_has_skeletal_mesh():
    """Character Blueprint has a skeletal mesh assigned."""
    cdo = _load_character_cdo()
    mesh_comp = None
    try:
        mesh_comp = cdo.get_editor_property("mesh")
    except Exception:
        pass
    assert mesh_comp, "No Mesh component on character CDO"

    sk = None
    try:
        sk = mesh_comp.get_editor_property("skeletal_mesh_asset")
    except Exception:
        sk = getattr(mesh_comp, "skeletal_mesh", None)
    assert sk, "No skeletal mesh assigned on character mesh component"


def test_character_has_anim_blueprint():
    """Character Blueprint has an Animation Blueprint assigned."""
    cdo = _load_character_cdo()
    mesh_comp = None
    try:
        mesh_comp = cdo.get_editor_property("mesh")
    except Exception:
        pass
    assert mesh_comp, "No Mesh component on character CDO"

    anim_class = None
    try:
        anim_class = mesh_comp.get_editor_property("anim_class")
    except Exception:
        pass
    assert anim_class, "No anim_class assigned on character mesh component"

    name = anim_class.get_name()
    assert "HomeWorld" in name or "ABP" in name, \
        "AnimBP class '%s' doesn't look like the HomeWorld AnimBP" % name


def test_capsule_dimensions():
    """Character has reasonable capsule dimensions."""
    cdo = _load_character_cdo()
    radius = cdo.get_editor_property("capsule_radius") if hasattr(cdo, "get_editor_property") else 42.0
    half_height = cdo.get_editor_property("capsule_half_height") if hasattr(cdo, "get_editor_property") else 88.0
    assert radius > 0, "Capsule radius is 0"
    assert half_height > 0, "Capsule half-height is 0"
