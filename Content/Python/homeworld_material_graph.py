# homeworld_material_graph.py
# Build HomeWorld master material node graphs in Unreal Editor (UE 5.7).

from __future__ import annotations

from typing import Any

try:
    import unreal
except ImportError:
    unreal = None  # type: ignore[assignment]

from homeworld_master_material_defs import MasterMaterialDef

GRAPH_MARKER_PARAM = "HomeWorldGraphVersion"
GRAPH_MARKER_VALUE = 1.0
MPC_PATH = "/Game/HomeWorld/Materials/MPC_HomeWorld_Time"
MPC_SCALAR_NAME = "NightMix"


def _enum_member(enum_cls: Any, *names: str) -> Any:
    for name in names:
        if hasattr(enum_cls, name):
            return getattr(enum_cls, name)
    raise AttributeError("None of %r found on %s" % (names, enum_cls))


def _mp(name: str) -> Any:
    return _enum_member(unreal.MaterialProperty, name)


def _create_expr(material: Any, expression_cls: Any, x: int, y: int) -> Any:
    return unreal.MaterialEditingLibrary.create_material_expression(
        material, expression_cls, x, y
    )


def _connect(from_expr: Any, from_output: str, to_expr: Any, to_input: str) -> None:
    unreal.MaterialEditingLibrary.connect_material_expressions(
        from_expr, from_output, to_expr, to_input
    )


def _connect_property(from_expr: Any, from_output: str, prop: Any) -> None:
    unreal.MaterialEditingLibrary.connect_material_property(from_expr, from_output, prop)


def _scalar_param(
    material: Any,
    name: str,
    default: float,
    x: int,
    y: int,
    group: str = "HomeWorld",
) -> Any:
    node = _create_expr(material, unreal.MaterialExpressionScalarParameter, x, y)
    node.set_editor_property("parameter_name", unreal.Name(name))
    node.set_editor_property("default_value", float(default))
    node.set_editor_property("group", unreal.Name(group))
    return node


def _vector_param(
    material: Any,
    name: str,
    default: tuple[float, float, float, float],
    x: int,
    y: int,
    group: str = "HomeWorld",
) -> Any:
    node = _create_expr(material, unreal.MaterialExpressionVectorParameter, x, y)
    node.set_editor_property("parameter_name", unreal.Name(name))
    color = unreal.LinearColor(default[0], default[1], default[2], default[3])
    node.set_editor_property("default_value", color)
    node.set_editor_property("group", unreal.Name(group))
    return node


def _constant(material: Any, value: float, x: int, y: int) -> Any:
    node = _create_expr(material, unreal.MaterialExpressionConstant, x, y)
    node.set_editor_property("r", float(value))
    return node


def _constant3(material: Any, rgb: tuple[float, float, float], x: int, y: int) -> Any:
    node = _create_expr(material, unreal.MaterialExpressionConstant3Vector, x, y)
    node.set_editor_property(
        "constant",
        unreal.LinearColor(rgb[0], rgb[1], rgb[2], 1.0),
    )
    return node


def _multiply(material: Any, x: int, y: int) -> Any:
    return _create_expr(material, unreal.MaterialExpressionMultiply, x, y)


def _lerp(material: Any, x: int, y: int) -> Any:
    return _create_expr(material, unreal.MaterialExpressionLinearInterpolate, x, y)


def _max_node(material: Any, x: int, y: int) -> Any:
    return _create_expr(material, unreal.MaterialExpressionMax, x, y)


def _add_node(material: Any, x: int, y: int) -> Any:
    return _create_expr(material, unreal.MaterialExpressionAdd, x, y)


def _desaturate(material: Any, x: int, y: int) -> Any:
    return _create_expr(material, unreal.MaterialExpressionDesaturation, x, y)


def material_has_homeworld_graph(material: Any) -> bool:
    if material is None:
        return False
    try:
        expressions = unreal.MaterialEditingLibrary.get_material_expressions(material)
    except Exception:
        return False
    for expr in expressions:
        try:
            if isinstance(expr, unreal.MaterialExpressionScalarParameter):
                if str(expr.get_editor_property("parameter_name")) == GRAPH_MARKER_PARAM:
                    return True
        except Exception:
            continue
    return False


def _effective_nightmix(material: Any, mpc: Any, local_default: float, x: int, y: int) -> Any:
    mpc_node = _create_expr(material, unreal.MaterialExpressionCollectionParameter, x, y)
    mpc_node.set_editor_property("collection", mpc)
    mpc_node.set_editor_property("parameter_name", unreal.Name(MPC_SCALAR_NAME))

    local_node = _scalar_param(material, "NightMix", local_default, x, y + 120)
    max_node = _max_node(material, x + 220, y + 60)
    _connect(mpc_node, "", max_node, "A")
    _connect(local_node, "", max_node, "B")
    return max_node


def _apply_night_overlay(
    material: Any,
    base_color_expr: Any,
    nightmix_expr: Any,
    overlay: Any,
    x: int,
    y: int,
) -> Any:
    desat_amt = _multiply(material, x + 200, y)
    _connect(
        nightmix_expr,
        "",
        desat_amt,
        "A",
    )
    desat_const = _constant(material, overlay.desaturate, x + 40, y + 80)
    _connect(desat_const, "", desat_amt, "B")

    desat_node = _desaturate(material, x + 420, y)
    _connect(base_color_expr, "", desat_node, "Input")
    _connect(desat_amt, "", desat_node, "Fraction")

    value_lerp = _lerp(material, x + 640, y)
    one = _constant(material, 1.0, x + 460, y + 120)
    value_const = _constant(material, overlay.value_mul, x + 460, y + 180)
    _connect(one, "", value_lerp, "A")
    _connect(value_const, "", value_lerp, "B")
    _connect(nightmix_expr, "", value_lerp, "Alpha")

    valued = _multiply(material, x + 860, y)
    _connect(desat_node, "", valued, "A")
    _connect(value_lerp, "", valued, "B")

    tint_lerp = _lerp(material, x + 1080, y)
    tint = _constant3(material, overlay.tint[:3], x + 860, y + 120)
    _connect(valued, "", tint_lerp, "A")
    _connect(tint, "", tint_lerp, "B")
    _connect(nightmix_expr, "", tint_lerp, "Alpha")
    return tint_lerp


def apply_material_settings(material: Any, master: MasterMaterialDef) -> None:
    if master.shading_model == "Unlit":
        material.set_editor_property(
            "shading_model",
            _enum_member(unreal.MaterialShadingModel, "MSM_UNLIT", "MSM_Unlit"),
        )
    else:
        material.set_editor_property(
            "shading_model",
            _enum_member(unreal.MaterialShadingModel, "MSM_DEFAULT_LIT", "MSM_DefaultLit"),
        )

    if master.opacity_masked:
        material.set_editor_property(
            "blend_mode",
            _enum_member(unreal.BlendMode, "BLEND_MASKED", "BLEND_Masked"),
        )
        material.set_editor_property("opacity_mask_clip_value", 0.5)
    else:
        material.set_editor_property(
            "blend_mode",
            _enum_member(unreal.BlendMode, "BLEND_OPAQUE", "BLEND_Opaque"),
        )


def build_master_graph(material: Any, master: MasterMaterialDef, mpc: Any) -> None:
    unreal.MaterialEditingLibrary.delete_all_material_expressions(material)

    base_param = _vector_param(material, "BaseColor", master.base_color, -1400, 0)
    rough_param = _scalar_param(material, "Roughness", master.roughness, -1400, 220)
    _scalar_param(material, "Variation", master.variation, -1400, 320)
    emissive_param = _vector_param(material, "Emissive", master.emissive, -1400, 420)

    nightmix = _effective_nightmix(material, mpc, master.night_mix_default, -1100, 0)
    overlay_color = _apply_night_overlay(
        material,
        base_param,
        nightmix,
        master.night_overlay,
        -900,
        0,
    )

    _scalar_param(
        material,
        GRAPH_MARKER_PARAM,
        GRAPH_MARKER_VALUE,
        -1400,
        520,
        group="HomeWorldInternal",
    )

    if master.shading_model == "Unlit":
        emissive_boost = _lerp(material, -500, 200)
        boost_one = _constant(material, 1.0, -740, 280)
        boost_night = _constant(
            material,
            master.night_overlay.emissive_mul_at_night or 1.0,
            -740,
            340,
        )
        _connect(boost_one, "", emissive_boost, "A")
        _connect(boost_night, "", emissive_boost, "B")
        _connect(nightmix, "", emissive_boost, "Alpha")

        emissive_mul = _multiply(material, -280, 120)
        _connect(emissive_param, "", emissive_mul, "A")
        _connect(emissive_boost, "", emissive_mul, "B")

        final_emissive = _add_node(material, -80, 80)
        _connect(overlay_color, "", final_emissive, "A")
        _connect(emissive_mul, "", final_emissive, "B")
        _connect_property(final_emissive, "", _mp("MP_EMISSIVE_COLOR"))
    else:
        _connect_property(overlay_color, "", _mp("MP_BASE_COLOR"))
        _connect_property(rough_param, "", _mp("MP_ROUGHNESS"))
        _connect_property(emissive_param, "", _mp("MP_EMISSIVE_COLOR"))

        if master.opacity_masked:
            opacity = _constant(material, 1.0, -500, 420)
            _connect_property(opacity, "", _mp("MP_OPACITY_MASK"))

    unreal.MaterialEditingLibrary.recompile_material(material)
