# homeworld_master_material_defs.py
# Pure-Python loaders for Lib/06_Materials_Master/*.json (no unreal import).

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

MASTER_NAMES = (
    "M_StylizedGrass",
    "M_CliffRock",
    "M_WoodCabin",
    "M_WoodWild",
    "M_FoliageCard",
    "M_PathStone",
    "M_GatherHerb",
    "M_BeastStylized",
    "M_SpiritUnlit",
    "M_Nurtured",
)

JSON_DIR_REL = os.path.join("Lib", "06_Materials_Master")


@dataclass(frozen=True)
class NightOverlayDef:
    tint: tuple[float, float, float, float]
    desaturate: float
    value_mul: float
    emissive_mul_at_night: float


@dataclass(frozen=True)
class MasterMaterialDef:
    name: str
    shading_model: str
    base_color: tuple[float, float, float, float]
    roughness: float
    variation: float
    night_mix_default: float
    emissive: tuple[float, float, float, float]
    night_overlay: NightOverlayDef
    opacity_masked: bool


def _project_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, "..", ".."))


def json_dir() -> str:
    return os.path.join(_project_root(), JSON_DIR_REL)


def load_master_json(name: str) -> dict[str, Any]:
    path = os.path.join(json_dir(), "%s.json" % name)
    if not os.path.isfile(path):
        raise FileNotFoundError("Master JSON not found: %s" % path)
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def parse_master_def(raw: dict[str, Any]) -> MasterMaterialDef:
    params = raw.get("parameters") or {}
    overlay = raw.get("night_overlay") or {}

    def _color(key: str, default: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
        value = (params.get(key) or {}).get("default", list(default))
        rgba = tuple(float(v) for v in value[:4])
        if len(rgba) == 3:
            rgba = (rgba[0], rgba[1], rgba[2], 1.0)
        return rgba

    def _float(key: str, default: float) -> float:
        return float((params.get(key) or {}).get("default", default))

    tint_raw = overlay.get("tint", [0.12, 0.18, 0.28, 1.0])
    tint = tuple(float(v) for v in tint_raw[:4])
    if len(tint) == 3:
        tint = (tint[0], tint[1], tint[2], 1.0)

    shading = str(raw.get("shading_model", "DefaultLit"))
    opacity_masked = "Masked" in shading or str(raw.get("opacity", "")).lower().startswith("alpha")

    return MasterMaterialDef(
        name=str(raw.get("id") or raw.get("ue_material") or "M_Unknown"),
        shading_model=shading,
        base_color=_color("BaseColor", (0.5, 0.5, 0.5, 1.0)),
        roughness=_float("Roughness", 0.8),
        variation=_float("Variation", 0.3),
        night_mix_default=_float("NightMix", 0.0),
        emissive=_color("Emissive", (0.0, 0.0, 0.0, 1.0)),
        night_overlay=NightOverlayDef(
            tint=tint,
            desaturate=float(overlay.get("desaturate", 0.2)),
            value_mul=float(overlay.get("value_mul", 0.55)),
            emissive_mul_at_night=float(overlay.get("emissive_mul_at_night", 1.0)),
        ),
        opacity_masked=opacity_masked,
    )


def load_all_master_defs() -> list[MasterMaterialDef]:
    return [parse_master_def(load_master_json(name)) for name in MASTER_NAMES]
