"""Shared PA-E shotlist constants and helpers (paths, validation, level/camera).

Used by capture_shotlist_mrq.py (primary) and capture_shotlist_viewport.py (diagnostic).
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import struct
import subprocess
import zlib
from typing import Any, Optional

try:
    import unreal
except ImportError:
    unreal = None  # type: ignore

LEVEL_PATH = "/Game/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers"
CINEMATICS_PA_E_DIR = "/Game/HomeWorld/Cinematics/PA_E"
RES_X, RES_Y = 1920, 1080
MIN_BYTES = 50 * 1024
MIN_MEAN_LUMINANCE = 8.0
# Global mean alone passes ~6% edge speckles on ~93% black (post-#170 DESKTOP) — require coverage + center read.
MIN_CENTER_CROP_MEAN_LUMINANCE = 12.0
MIN_FRACTION_L_GT_1 = 0.18
MIN_FRACTION_L_GT_8 = 0.10
MIN_FRACTION_PURE_BLACK_L0 = 0.85
SHOT_PAIR_COMPARE_SIZE = 48
SHOT_PAIR_MAX_MSE = 4.0
DESKTOP_PA_E = r"C:\Users\User\Desktop\HomeWorld_PA_E"
ONE_FRAME_START = 0
ONE_FRAME_END = 1
# MRQ warm-up (Epic MoviePipelineAntiAliasingSetting — engine + GPU discard frames)
MRQ_ENGINE_WARMUP_COUNT = 32
MRQ_RENDER_WARMUP_COUNT = 8
MRQ_CAMERA_CUT_PREROLL_FRAME = -32

_PHASE_2_ALONE_INSUFFICIENT = (
    "hw.TimeOfDay.Phase 2 sets gameplay night phase only. Readable thematic night requires "
    "PRESET_Homestead_Night tune (sky/moon/stars ambient, fog SSS, warm cabin emissives) — "
    "apply_homestead_night_tune() + verify moon/skylight/cabin stack before capture."
)

# Lead hard rule — required loop before any failure claim (docs + report).
LEAD_PROVE_LOOP = (
    {
        "step": 1,
        "id": "inventory",
        "action": "Confirm homestead dress/mesh actors are IN the loaded level (DRESS_*, SM_Cabin, island kit).",
    },
    {
        "step": 2,
        "id": "aim",
        "action": "Aim viewport/shot cameras AT confirmed actor bounds centroids (not void); re-aim CAM_* or bounds-offset if needed.",
    },
    {
        "step": 3,
        "id": "capture_inspect",
        "action": "Capture + inspect luminance/content; near-black = loop continues, not closed FAIL.",
    },
    {
        "step": 4,
        "id": "bugfix",
        "action": "Fix pose / lighting / game-view / buffer / MRQ binding until stills show intended homestead.",
    },
)

# Universal testing preconditions (Lead lock-in) — verify before trusting pass/fail.
UNIVERSAL_TESTING_PRECONDITIONS = (
    {
        "step": 1,
        "id": "content_in_level",
        "action": "Required content/actors exist in the loaded level (not assumed from asset path alone).",
    },
    {
        "step": 2,
        "id": "camera_aim",
        "action": "Cameras/viewport aimed at that content (bounds centroids), not void or wrong pilot.",
    },
    {
        "step": 3,
        "id": "lighting_tod_view",
        "action": (
            "Lighting, time-of-day, and PRESET tune match shot intent (PA-E: Phase 2 + "
            "PRESET_Homestead_Night tune — Phase 2 alone insufficient); record in report."
        ),
    },
    {
        "step": 4,
        "id": "capture_inspect",
        "action": "Capture or run harness, then inspect output (luminance, logs, artifacts) before PASS/FAIL claims.",
    },
)

# PA-E Shot 1–2: homestead **night** per Docs/00_SHOTLIST.md (not day unless shotlist changes).
PA_E_SHOTLIST_TIME_OF_DAY = {
    "phase": 2,
    "phase_name": "Night",
    "console_command": "hw.TimeOfDay.Phase 2",
    "shotlist_doc": "Docs/00_SHOTLIST.md",
    "preset_canon": "Lib/07_Night_SpiritLayer/PRESET_Homestead_Night.md",
    "night_tune_module": "Content/Python/vnp_night_tune_and_evidence.py",
    "shotlist_intent": "Shot 1 homestead night lookout; Shot 2 cabin+garden close at night (warm windows vs moonlight).",
    "phase_2_alone_insufficient": (
        "hw.TimeOfDay.Phase 2 sets gameplay night phase only. Readable thematic night requires "
        "PRESET_Homestead_Night tune (sky/moon/stars ambient, fog SSS, warm cabin emissives) — "
        "apply_homestead_night_tune() + verify moon/skylight/cabin stack before capture."
    ),
    "do_not_switch_to_day": (
        "Do not switch shotlist capture to day phase to dodge black stills — fix night lighting stack."
    ),
    "note": (
        "Use explicit phase + night tune in code/report. Day phase (0) only when shotlist requires day (e.g. Shot 4)."
    ),
}

PROVE_CRITERIA = {
    "requires_lit_homestead_visible": True,
    "min_bytes": MIN_BYTES,
    "min_mean_luminance": MIN_MEAN_LUMINANCE,
    "min_center_crop_mean_luminance": MIN_CENTER_CROP_MEAN_LUMINANCE,
    "min_fraction_l_gt_1": MIN_FRACTION_L_GT_1,
    "min_fraction_l_gt_8": MIN_FRACTION_L_GT_8,
    "max_fraction_pure_black_l0": MIN_FRACTION_PURE_BLACK_L0,
    "shot_pair_max_mse_at_compare_size": SHOT_PAIR_MAX_MSE,
    "file_exists_alone_is_not_pass": True,
    "black_stills_not_closed_fail": True,
    "night_readable_requires_preset_tune": True,
    "preset_canon": "Lib/07_Night_SpiritLayer/PRESET_Homestead_Night.md",
    "phase_2_alone_insufficient": _PHASE_2_ALONE_INSUFFICIENT,
    "do_not_switch_to_day": PA_E_SHOTLIST_TIME_OF_DAY["do_not_switch_to_day"],
    "note": (
        "Near-black PNGs start the prove loop (in progress), not a closed FAIL. "
        "Lead-visible lit geometry when rotating viewport means wrong aim/buffer — fix pose/lighting/capture. "
        "Night must be readable (moon/sky/cabin emissives), not pitch black — Phase 2 + PRESET tune."
    ),
}

# Actors that must be present for step 1 (any match counts toward inventory).
HOMESTEAD_INVENTORY_NEEDLES = (
    "DRESS_",
    "SM_Cabin",
    "SM_Island",
    "SM_Lookout",
    "VS_MVP/Dress",
)

# Per-shot framing targets (union bounds centroid used for look-at).
SHOT_FRAMING_NEEDLES: dict[str, tuple[str, ...]] = {
    "shot1": (
        "DRESS_SM_Island",
        "SM_Island",
        "SM_Lookout",
        "Lookout",
        "DRESS_SM_Cabin",
        "SM_Cabin",
        "Cabin",
    ),
    "shot2": (
        "DRESS_SM_Cabin",
        "SM_Cabin",
        "Cabin",
        "Garden",
        "Planter",
        "Path",
    ),
}

# Aim / look-at centroid: dress + hero mass — excludes edge Fence/Rock that pull framing off-shot.
SHOT_AIM_PRIMARY_NEEDLES: dict[str, tuple[str, ...]] = {
    "shot1": (
        "DRESS_SM_Island",
        "SM_Island",
        "DRESS_SM_Lookout",
        "SM_Lookout",
        "Lookout",
        "DRESS_SM_Cabin",
        "SM_Cabin",
    ),
    "shot2": (
        "DRESS_SM_Cabin",
        "SM_Cabin",
        "Cabin",
        "Garden",
        "Planter",
        "Path",
    ),
}

SHOT_FRAMING_EXCLUDE: dict[str, tuple[str, ...]] = {
    "shot1": ("Fence", "Rock", "Planter", "Path"),
    "shot2": ("Fence", "Rock", "Lookout", "SM_Lookout"),
}

DRESS_LABEL_PREFIX = "DRESS_"

MRQ_PIE_LIGHTING_NOTE = (
    "MoviePipelinePIEExecutor renders a PIE world. Editor-session TMP lights under VS_MVP/TMP_PA_E_Arrange "
    "may not match MRQ exposure until reseed_pa_e_tmp_night_fixtures() + apply_homestead_night_tune() run "
    "after load and again immediately before each MRQ job. If stack_ok in Editor but MRQ stills are dark, "
    "verify deferred lit pass, warm-up counts, and Epic MRQ PIE / exposure settings (do not switch to day). "
    "Refs: Movie Render Queue overview (UE 5.8), MoviePipelineDeferredPass, MoviePipelinePIEExecutor."
)

SHOTS = (
    {
        "id": "shot1",
        "filename": "Shot1_lookout.png",
        "sequence_name": "LS_PA_E_Shot1_lookout",
        "camera_labels": ("CAM_Hero", "Shot1", "Lookout", "Hero"),
        "fallback_location_m": (-9.0, -4.0, 5.8),
        "fallback_rotation_deg": (41.61, 0.0, -108.43),
        "fallback_source": "Docs/handoffs/P6_FIX_shot1.md + AssetCreation CAM_Hero",
    },
    {
        "id": "shot2",
        "filename": "Shot2_cabin_garden.png",
        "sequence_name": "LS_PA_E_Shot2_cabin_garden",
        "camera_labels": ("CAM_CabinClose", "Shot2", "Cabin", "Garden", "CAM_CabinGarden"),
        "fallback_location_m": (-4.0, -2.5, 1.6),
        "fallback_rotation_deg": (81.08, 0.0, -26.56),
        "fallback_source": "Lib/00_Core/GRAYBOX_LAYOUT.md CAM_CabinClose (blender euler from JSON)",
    },
)


def log(prefix: str, msg: str, data: Optional[dict] = None) -> None:
    line = prefix + " " + msg
    if data:
        line += " " + json.dumps(data, default=str)
    if unreal is not None:
        # Editor mirrors stdout into LogPython — print() duplicates unreal.log (post-#169).
        unreal.log(line)
        return
    print(line)


def abs_path(path: str) -> str:
    return os.path.abspath(os.path.normpath(path))


def project_dir() -> str:
    if unreal is None:
        return abs_path(os.getcwd())
    raw = unreal.Paths.project_dir()
    if raw:
        return abs_path(raw)
    return abs_path(os.getcwd())


def saved_pa_e_dir() -> str:
    path = abs_path(os.path.join(project_dir(), "Saved", "Screenshots", "PA_E"))
    os.makedirs(path, exist_ok=True)
    return path


def shot_dest_abs(filename: str) -> str:
    return abs_path(os.path.join(saved_pa_e_dir(), filename))


def mrq_staging_dir(shot_id: str) -> str:
    path = abs_path(os.path.join(project_dir(), "Saved", "Screenshots", "PA_E", "mrq_staging", shot_id))
    os.makedirs(path, exist_ok=True)
    return path


def report_path() -> str:
    return abs_path(os.path.join(project_dir(), "Saved", "pa_e_capture_report.json"))


def sequence_asset_path(sequence_name: str) -> str:
    return f"{CINEMATICS_PA_E_DIR}/{sequence_name}"


def pil_available() -> bool:
    try:
        from PIL import Image  # noqa: F401
        return True
    except ImportError:
        return False


def meters_to_ue(loc_m: tuple[float, float, float]) -> "unreal.Vector":
    x, y, z = loc_m
    return unreal.Vector(x * 100.0, -y * 100.0, z * 100.0)


def euler_deg_to_rotator(pitch: float, yaw: float, roll: float) -> "unreal.Rotator":
    return unreal.Rotator(pitch=pitch, yaw=yaw, roll=roll)


def actor_label(actor) -> str:
    try:
        return actor.get_actor_label() or actor.get_name()
    except Exception:
        return actor.get_name() if actor else ""


def find_camera(needles: tuple[str, ...]):
    cams = []
    for a in unreal.EditorLevelLibrary.get_all_level_actors():
        if not a:
            continue
        cls = a.get_class().get_name() if a.get_class() else ""
        if "Camera" not in cls:
            continue
        cams.append(a)
    needle_l = [n.lower() for n in needles]
    for needle in needle_l:
        for a in cams:
            label = actor_label(a).lower()
            name = a.get_name().lower()
            if label == needle or name == needle:
                return a
    for a in cams:
        label = actor_label(a).lower()
        name = a.get_name().lower()
        if any(n in label or n in name for n in needle_l):
            return a
    return None


def load_level(log_prefix: str) -> bool:
    log(log_prefix, "load_level start", {"path": LEVEL_PATH})
    try:
        subsys = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
        if subsys and hasattr(subsys, "load_level"):
            subsys.load_level(LEVEL_PATH)
            log(log_prefix, "load_level via LevelEditorSubsystem", {"ok": True})
            return True
    except Exception as e:
        log(log_prefix, "load_level LevelEditorSubsystem failed", {"error": str(e)})
    try:
        ok = unreal.EditorLevelLibrary.load_level(LEVEL_PATH)
        log(log_prefix, "load_level via EditorLevelLibrary", {"ok": bool(ok)})
        return bool(ok)
    except Exception as e:
        log(log_prefix, "load_level failed", {"error": str(e)})
        return False


def purge_stale_shot_pngs(dest_abs: str) -> dict[str, Any]:
    basename = os.path.basename(dest_abs)
    candidates: set[str] = {abs_path(dest_abs)}
    candidates.add(abs_path(os.path.join(DESKTOP_PA_E, basename)))
    removed: list[str] = []
    errors: list[dict[str, str]] = []
    for p in sorted(candidates):
        if not os.path.isfile(p):
            continue
        try:
            os.remove(p)
            removed.append(p)
        except OSError as e:
            errors.append({"path": p, "error": str(e)})
    return {"basename": basename, "removed": removed, "remove_errors": errors}


def _mean_luminance_pil(path: str) -> Optional[float]:
    try:
        from PIL import Image
    except ImportError:
        return None
    try:
        with Image.open(path) as im:
            im = im.convert("L")
            hist = im.histogram()
            total = sum(hist) or 1
            mean = sum(i * hist[i] for i in range(256)) / total
            return float(mean)
    except Exception:
        return None


def _paeth(a: int, b: int, c: int) -> int:
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        return a
    if pb <= pc:
        return b
    return c


def _png_unfilter_scanlines(
    raw: bytes, width: int, height: int, bpp: int
) -> Optional[bytes]:
    stride = width * bpp
    if stride <= 0 or height <= 0:
        return None
    out = bytearray(height * stride)
    prev = bytearray(stride)
    pos = 0
    for _row in range(height):
        if pos >= len(raw):
            return None
        filt = raw[pos]
        pos += 1
        row = raw[pos : pos + stride]
        pos += stride
        if len(row) != stride:
            return None
        cur = bytearray(stride)
        for i in range(stride):
            x = row[i]
            a = cur[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if filt == 0:
                v = x
            elif filt == 1:
                v = (x + a) & 0xFF
            elif filt == 2:
                v = (x + b) & 0xFF
            elif filt == 3:
                v = (x + ((a + b) // 2)) & 0xFF
            elif filt == 4:
                v = (x + _paeth(a, b, c)) & 0xFF
            else:
                return None
            cur[i] = v
        out[_row * stride : (_row + 1) * stride] = cur
        prev = cur
    return bytes(out)


def _mean_luminance_stdlib_png(path: str) -> Optional[float]:
    """8-bit RGB/RGBA PNG mean luminance without Pillow (MRQ deferred PNG)."""
    try:
        with open(path, "rb") as f:
            sig = f.read(8)
        if sig != b"\x89PNG\r\n\x1a\n":
            return None
        width = height = 0
        bit_depth = color_type = 0
        idat = bytearray()
        with open(path, "rb") as f:
            f.read(8)
            while True:
                hdr = f.read(8)
                if len(hdr) < 8:
                    break
                length, ctype = struct.unpack(">I4s", hdr)
                data = f.read(length)
                f.read(4)
                if ctype == b"IHDR" and len(data) >= 13:
                    width, height, bit_depth, color_type = struct.unpack(">IIBB", data[:10])
                elif ctype == b"IDAT":
                    idat.extend(data)
                elif ctype == b"IEND":
                    break
        if bit_depth != 8 or color_type not in (2, 6):
            return None
        bpp = 3 if color_type == 2 else 4
        try:
            raw = zlib.decompress(bytes(idat))
        except zlib.error:
            return None
        pixels = _png_unfilter_scanlines(raw, width, height, bpp)
        if not pixels:
            return None
        total_pixels = width * height
        step = max(1, total_pixels // 250_000)
        total = 0.0
        count = 0
        for idx_px in range(0, total_pixels, step):
            o = idx_px * bpp
            if o + 2 >= len(pixels):
                break
            r, g, b = pixels[o], pixels[o + 1], pixels[o + 2]
            total += 0.2126 * r + 0.7152 * g + 0.0722 * b
            count += 1
        return float(total / count) if count else None
    except OSError:
        return None


def _mean_luminance_host_python(path: str) -> Optional[float]:
    """Fallback: host ``py``/``python`` with Pillow when Editor Python has no PIL."""
    abs_png = os.path.abspath(path)
    code = (
        "import sys\n"
        "from PIL import Image\n"
        "im = Image.open(sys.argv[1]).convert('L')\n"
        "h = im.histogram()\n"
        "t = sum(h) or 1\n"
        "print(sum(i * h[i] for i in range(256)) / t)\n"
    )
    candidates: list[list[str]] = []
    env_py = os.environ.get("HOMEWORLD_HOST_PYTHON")
    if env_py:
        candidates.append([env_py, "-c", code, abs_png])
    candidates.append(["py", "-3", "-c", code, abs_png])
    for name in ("python3", "python"):
        candidates.append([name, "-c", code, abs_png])
    for cmd in candidates:
        exe = cmd[0]
        if os.path.sep not in exe and shutil.which(exe) is None:
            continue
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=45,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if proc.returncode != 0 or not proc.stdout.strip():
            continue
        try:
            return float(proc.stdout.strip().splitlines()[-1])
        except ValueError:
            continue
    return None


def mean_luminance(path: str) -> tuple[Optional[float], str]:
    """Return (mean 0–255, source tag). Order: Editor PIL → stdlib PNG → host Python PIL."""
    lum = _mean_luminance_pil(path)
    if lum is not None:
        return lum, "pil"
    lum = _mean_luminance_stdlib_png(path)
    if lum is not None:
        return lum, "stdlib_png"
    lum = _mean_luminance_host_python(path)
    if lum is not None:
        return lum, "host_python_pil"
    return None, "none"


def _luminance_from_rgb(r: int, g: int, b: int) -> int:
    return int(0.2126 * r + 0.7152 * g + 0.0722 * b)


def _decode_png_l_grid(path: str) -> tuple[Optional[list[int]], int, int, str]:
    """Return (luminance grid row-major, width, height, source)."""
    try:
        from PIL import Image
    except ImportError:
        pass
    else:
        try:
            with Image.open(path) as im:
                im = im.convert("RGB")
                width, height = im.size
                pixels = list(im.getdata())
                grid = [_luminance_from_rgb(r, g, b) for r, g, b in pixels]
                return grid, width, height, "pil"
        except Exception:
            pass
    try:
        with open(path, "rb") as f:
            sig = f.read(8)
        if sig != b"\x89PNG\r\n\x1a\n":
            return None, 0, 0, "none"
        width = height = 0
        bit_depth = color_type = 0
        idat = bytearray()
        with open(path, "rb") as f:
            f.read(8)
            while True:
                hdr = f.read(8)
                if len(hdr) < 8:
                    break
                length, ctype = struct.unpack(">I4s", hdr)
                data = f.read(length)
                f.read(4)
                if ctype == b"IHDR" and len(data) >= 13:
                    width, height, bit_depth, color_type = struct.unpack(">IIBB", data[:10])
                elif ctype == b"IDAT":
                    idat.extend(data)
                elif ctype == b"IEND":
                    break
        if bit_depth != 8 or color_type not in (2, 6) or width <= 0 or height <= 0:
            return None, 0, 0, "none"
        bpp = 3 if color_type == 2 else 4
        raw = zlib.decompress(bytes(idat))
        rgb_bytes = _png_unfilter_scanlines(raw, width, height, bpp)
        if not rgb_bytes:
            return None, 0, 0, "none"
        grid: list[int] = []
        total = width * height
        for idx in range(total):
            o = idx * bpp
            grid.append(_luminance_from_rgb(rgb_bytes[o], rgb_bytes[o + 1], rgb_bytes[o + 2]))
        return grid, width, height, "stdlib_png"
    except (OSError, zlib.error):
        return None, 0, 0, "none"


def analyze_png_luminance_content(path: str) -> dict[str, Any]:
    """Coverage + center-crop metrics — blocks global-mean false PASS on sparse speckles."""
    grid, width, height, source = _decode_png_l_grid(path)
    out: dict[str, Any] = {"luminance_source": source, "width": width, "height": height}
    if not grid or width <= 0 or height <= 0:
        out["error"] = "luminance_decode_failed"
        return out
    total = len(grid)
    hist = [0] * 256
    for lv in grid:
        hist[min(255, max(0, lv))] += 1
    mean = sum(i * hist[i] for i in range(256)) / total
    out["mean_luminance"] = float(mean)
    out["fraction_l_eq_0"] = hist[0] / total
    out["fraction_l_gt_1"] = sum(hist[i] for i in range(2, 256)) / total
    out["fraction_l_gt_8"] = sum(hist[i] for i in range(9, 256)) / total
    x0, x1 = width // 4, (width * 3) // 4
    y0, y1 = height // 4, (height * 3) // 4
    center_vals: list[int] = []
    for y in range(y0, y1):
        row = y * width
        for x in range(x0, x1):
            center_vals.append(grid[row + x])
    center_total = len(center_vals) or 1
    out["center_crop_mean_luminance"] = float(sum(center_vals) / center_total)
    out["center_crop_fraction"] = 0.5
    try:
        with open(path, "rb") as f:
            out["sha256"] = hashlib.sha256(f.read()).hexdigest()
    except OSError:
        out["sha256"] = None
    return out


def _downsample_l_grid(grid: list[int], width: int, height: int, size: int) -> list[float]:
    if width <= 0 or height <= 0:
        return []
    out: list[float] = []
    for sy in range(size):
        y = min(height - 1, int((sy + 0.5) * height / size))
        row = y * width
        for sx in range(size):
            x = min(width - 1, int((sx + 0.5) * width / size))
            out.append(float(grid[row + x]))
    return out


def _mse(a: list[float], b: list[float]) -> Optional[float]:
    if len(a) != len(b) or not a:
        return None
    return sum((x - y) ** 2 for x, y in zip(a, b)) / len(a)


def validate_shot_pair_diversity(paths: list[tuple[str, Optional[str]]]) -> dict[str, Any]:
    """When both shots exist, reject near-identical mostly-black scrap (post-#170)."""
    out: dict[str, Any] = {"pass": True, "compare_size": SHOT_PAIR_COMPARE_SIZE}
    existing = [(sid, p) for sid, p in paths if p and os.path.isfile(p)]
    if len(existing) < 2:
        out["skipped"] = "need_two_files"
        return out
    metrics: list[dict[str, Any]] = []
    samples: list[list[float]] = []
    hashes: list[str] = []
    for sid, path in existing:
        content = analyze_png_luminance_content(path)
        content["shot_id"] = sid
        metrics.append(content)
        grid, w, h, _src = _decode_png_l_grid(path)
        if grid:
            samples.append(_downsample_l_grid(grid, w, h, SHOT_PAIR_COMPARE_SIZE))
        sha = content.get("sha256")
        if sha:
            hashes.append(sha)
    out["shots"] = metrics
    if len(hashes) == 2 and hashes[0] == hashes[1]:
        out["pass"] = False
        out["error"] = "shots_identical_hash"
        out["prove_loop_status"] = "in_progress"
        out["closed_fail"] = False
        return out
    if len(samples) == 2:
        mse = _mse(samples[0], samples[1])
        out["mse_downsampled"] = mse
        if mse is not None and mse <= SHOT_PAIR_MAX_MSE:
            out["pass"] = False
            out["error"] = "shots_near_identical"
            out["prove_loop_status"] = "in_progress"
            out["closed_fail"] = False
    return out


def _mark_prove_loop_in_progress(out: dict[str, Any], error: str) -> None:
    out["error"] = error
    out["pass"] = False
    out["prove_loop_status"] = "in_progress"
    out["closed_fail"] = False
    out["lead_rule"] = (
        "Near-black / wrong framing / sparse speckle is not a closed FAIL — "
        "complete LEAD_PROVE_LOOP (fix Arrange setup before claiming success)."
    )
    out["prove_loop"] = list(LEAD_PROVE_LOOP)


def validate_png(path: Optional[str]) -> dict:
    out: dict[str, Any] = {"path": path, "pass": False}
    if not path or not os.path.isfile(path):
        out["error"] = "file_missing"
        return out
    size = os.path.getsize(path)
    out["bytes"] = size
    if size < MIN_BYTES:
        out["error"] = "file_too_small"
        return out
    content = analyze_png_luminance_content(path)
    out.update(content)
    out["pil_available"] = pil_available()
    lum = content.get("mean_luminance")
    lum_source = content.get("luminance_source", "none")
    out["luminance_source"] = lum_source
    if lum is None or content.get("error") == "luminance_decode_failed":
        out["error"] = "luminance_unavailable"
        out["install_note"] = (
            "Editor Pillow missing; stdlib PNG decode failed. "
            "Optional: HOMEWORLD_HOST_PYTHON or install Pillow in Editor Python."
        )
        return out
    if lum < MIN_MEAN_LUMINANCE:
        _mark_prove_loop_in_progress(out, "near_black")
        return out
    center_mean = content.get("center_crop_mean_luminance")
    if center_mean is None or center_mean < MIN_CENTER_CROP_MEAN_LUMINANCE:
        _mark_prove_loop_in_progress(out, "center_crop_near_black")
        return out
    frac_gt_8 = content.get("fraction_l_gt_8")
    frac_gt_1 = content.get("fraction_l_gt_1")
    frac_black = content.get("fraction_l_eq_0")
    if frac_gt_8 is not None and frac_gt_8 < MIN_FRACTION_L_GT_8:
        _mark_prove_loop_in_progress(out, "sparse_speckle_insufficient_l_gt_8")
        return out
    if frac_gt_1 is not None and frac_gt_1 < MIN_FRACTION_L_GT_1:
        _mark_prove_loop_in_progress(out, "sparse_speckle_insufficient_l_gt_1")
        return out
    if frac_black is not None and frac_black > MIN_FRACTION_PURE_BLACK_L0:
        _mark_prove_loop_in_progress(out, "mostly_pure_black")
        return out
    out["pass"] = True
    out["prove_loop_status"] = "complete"
    return out


def copy_to_desktop(local_path: str, filename: str) -> dict:
    dest_dir = DESKTOP_PA_E
    dest = os.path.join(dest_dir, filename)
    try:
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(local_path, dest)
        return {"copied": True, "desktop_path": dest}
    except Exception as e:
        return {"copied": False, "desktop_path": dest, "error": str(e)}


def homestead_diagnostic_path() -> str:
    return abs_path(os.path.join(project_dir(), "Saved", "pa_e_homestead_capture_diagnostic.json"))


def _actor_folder(actor) -> str:
    try:
        return str(actor.get_folder_path() or "")
    except Exception:
        return ""


def _actor_matches_needles(actor, needles: tuple[str, ...]) -> bool:
    label = actor_label(actor)
    folder = _actor_folder(actor).replace("\\", "/")
    label_l = label.lower()
    for n in needles:
        nl = n.lower()
        if nl in label_l or nl in folder.lower():
            return True
    return False


def _bounds_dict(actor) -> dict[str, Any]:
    origin, extent = actor.get_actor_bounds(False)
    return {
        "label": actor_label(actor),
        "class": actor.get_class().get_name() if actor.get_class() else "",
        "folder": _actor_folder(actor),
        "origin": [origin.x, origin.y, origin.z],
        "extent": [extent.x, extent.y, extent.z],
        "centroid": [origin.x, origin.y, origin.z],
    }


def _actor_excluded_for_shot(actor, shot_id: str) -> bool:
    exclude = SHOT_FRAMING_EXCLUDE.get(shot_id or "", ())
    if not exclude:
        return False
    label = actor_label(actor)
    folder = _actor_folder(actor).replace("\\", "/")
    label_l = label.lower()
    for n in exclude:
        nl = n.lower()
        if nl in label_l or nl in folder.lower():
            return True
    return False


def inventory_homestead_in_level(shot_id: Optional[str] = None) -> dict[str, Any]:
    """Step 1: actors in loaded level matching homestead / shot framing needles."""
    needles = HOMESTEAD_INVENTORY_NEEDLES
    framing = SHOT_FRAMING_NEEDLES.get(shot_id or "", ())
    aim_primary = SHOT_AIM_PRIMARY_NEEDLES.get(shot_id or "", ())
    actors_all: list = []
    actors_framing: list = []
    actors_aim: list = []
    for a in unreal.EditorLevelLibrary.get_all_level_actors():
        if not a:
            continue
        if _actor_matches_needles(a, needles):
            actors_all.append(a)
        if framing and _actor_matches_needles(a, framing) and not _actor_excluded_for_shot(a, shot_id or ""):
            actors_framing.append(a)
        if aim_primary and _actor_matches_needles(a, aim_primary) and not _actor_excluded_for_shot(a, shot_id or ""):
            actors_aim.append(a)
    combined_all = combined_bounds_from_actors(actors_all)
    combined_framing = combined_bounds_from_actors(actors_framing) if actors_framing else combined_all
    combined_aim = combined_bounds_from_actors(actors_aim) if actors_aim else combined_framing
    return {
        "level_path": LEVEL_PATH,
        "shot_id": shot_id,
        "homestead_actor_count": len(actors_all),
        "framing_actor_count": len(actors_framing),
        "aim_primary_actor_count": len(actors_aim),
        "homestead_actors_sample": [_bounds_dict(a) for a in actors_all[:40]],
        "framing_actors_sample": [_bounds_dict(a) for a in actors_framing[:40]],
        "aim_primary_actors_sample": [_bounds_dict(a) for a in actors_aim[:40]],
        "homestead_bounds": combined_all,
        "framing_bounds": combined_framing,
        "aim_bounds": combined_aim,
        "inventory_ok": len(actors_all) > 0,
        "framing_ok": combined_framing is not None,
        "aim_bounds_ok": combined_aim is not None,
    }


def combined_bounds_from_actors(actors: list) -> Optional[dict[str, Any]]:
    if not actors:
        return None
    min_x = min_y = min_z = float("inf")
    max_x = max_y = max_z = float("-inf")
    labels: list[str] = []
    for a in actors:
        try:
            origin, extent = a.get_actor_bounds(False)
        except Exception:
            continue
        labels.append(actor_label(a))
        for sx in (-1, 1):
            for sy in (-1, 1):
                for sz in (-1, 1):
                    x = origin.x + extent.x * sx
                    y = origin.y + extent.y * sy
                    z = origin.z + extent.z * sz
                    min_x, max_x = min(min_x, x), max(max_x, x)
                    min_y, max_y = min(min_y, y), max(max_y, y)
                    min_z, max_z = min(min_z, z), max(max_z, z)
    if min_x == float("inf"):
        return None
    cx = (min_x + max_x) * 0.5
    cy = (min_y + max_y) * 0.5
    cz = (min_z + max_z) * 0.5
    return {
        "centroid": [cx, cy, cz],
        "extent": [(max_x - min_x) * 0.5, (max_y - min_y) * 0.5, (max_z - min_z) * 0.5],
        "min": [min_x, min_y, min_z],
        "max": [max_x, max_y, max_z],
        "actor_labels": labels[:50],
        "actor_count": len(labels),
    }


def _vector_from_list(values: list[float]) -> "unreal.Vector":
    return unreal.Vector(values[0], values[1], values[2])


def look_at_rotation(from_loc: "unreal.Vector", to_loc: "unreal.Vector") -> "unreal.Rotator":
    try:
        return unreal.MathLibrary.find_look_at_rotation(from_loc, to_loc)
    except Exception:
        pass
    dx = to_loc.x - from_loc.x
    dy = to_loc.y - from_loc.y
    dz = to_loc.z - from_loc.z
    yaw = unreal.MathLibrary.deg_atan2(dy, dx) if hasattr(unreal.MathLibrary, "deg_atan2") else 0.0
    horiz = (dx * dx + dy * dy) ** 0.5
    pitch = -unreal.MathLibrary.deg_atan2(dz, horiz) if hasattr(unreal.MathLibrary, "deg_atan2") else -15.0
    return unreal.Rotator(pitch=pitch, yaw=yaw, roll=0.0)


def _ray_intersects_aabb(
    origin: tuple[float, float, float],
    direction: tuple[float, float, float],
    bmin: tuple[float, float, float],
    bmax: tuple[float, float, float],
    max_t: float = 500000.0,
) -> bool:
    tmin = 0.0
    tmax = max_t
    for i in range(3):
        o, d, mn, mx = origin[i], direction[i], bmin[i], bmax[i]
        if abs(d) < 1e-8:
            if o < mn or o > mx:
                return False
            continue
        inv = 1.0 / d
        t1 = (mn - o) * inv
        t2 = (mx - o) * inv
        if t1 > t2:
            t1, t2 = t2, t1
        tmin = max(tmin, t1)
        tmax = min(tmax, t2)
        if tmax < tmin:
            return False
    return tmax >= tmin


def camera_forward_alignment(
    from_loc: "unreal.Vector",
    rot: "unreal.Rotator",
    target: "unreal.Vector",
    *,
    dress_bounds: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Diagnostic: forward dot to target + optional ray hit on dress AABB."""
    fwd = unreal.MathLibrary.get_forward_vector(rot)
    delta = target - from_loc
    dist = delta.length()
    if dist < 1.0:
        return {"distance_uu": dist, "forward_dot_to_target": None, "aim_ok": False}
    delta_n = unreal.Vector(delta.x / dist, delta.y / dist, delta.z / dist)
    dot = fwd.x * delta_n.x + fwd.y * delta_n.y + fwd.z * delta_n.z
    ray_hits = None
    if dress_bounds and dress_bounds.get("min") and dress_bounds.get("max"):
        bmin = tuple(dress_bounds["min"])
        bmax = tuple(dress_bounds["max"])
        ray_hits = _ray_intersects_aabb(
            (from_loc.x, from_loc.y, from_loc.z),
            (fwd.x, fwd.y, fwd.z),
            bmin,
            bmax,
        )
    aim_ok = dot > 0.3 and (ray_hits is not False)
    return {
        "distance_uu": round(dist, 2),
        "forward_dot_to_target": round(dot, 4),
        "forward_ray_hits_dress_aabb": ray_hits,
        "aim_ok": aim_ok,
    }


def _camera_pose_from_bounds(shot_id: str, bounds: dict[str, Any]) -> tuple[Any, Any, dict[str, Any]]:
    meta: dict[str, Any] = {"pose_source": "homestead_bounds"}
    c = bounds["centroid"]
    ext = bounds["extent"]
    target = _vector_from_list(c)
    if shot_id == "shot1":
        loc = unreal.Vector(
            target.x - ext[0] * 1.2,
            target.y - ext[1] * 0.9,
            target.z + ext[2] + 250.0,
        )
    else:
        loc = unreal.Vector(
            target.x + ext[0] * 0.45,
            target.y - ext[1] * 1.0,
            target.z + ext[2] * 0.35 + 120.0,
        )
    rot = look_at_rotation(loc, target)
    meta["target_centroid"] = c
    meta["camera_location"] = [loc.x, loc.y, loc.z]
    meta["camera_rotation"] = [rot.pitch, rot.yaw, rot.roll]
    return loc, rot, meta


def resolve_camera_transform(shot: dict, cam) -> tuple[Any, Any, dict[str, Any]]:
    """Step 2: prefer in-level CAM; aim at homestead framing bounds; avoid void-pointing hardcoded pose."""
    shot_id = shot.get("id", "")
    inventory = inventory_homestead_in_level(shot_id)
    meta: dict[str, Any] = {
        "used_camera_actor": bool(cam),
        "prove_loop_step1_inventory": inventory,
    }
    bounds = (
        inventory.get("aim_bounds")
        or inventory.get("framing_bounds")
        or inventory.get("homestead_bounds")
    )
    target: Optional[unreal.Vector] = None
    if bounds and bounds.get("centroid"):
        target = _vector_from_list(bounds["centroid"])
        meta["framing_target_centroid"] = bounds["centroid"]
        meta["expected_framing"] = {
            "aim_bounds_centroid": bounds["centroid"],
            "aim_bounds_min": bounds.get("min"),
            "aim_bounds_max": bounds.get("max"),
            "aim_bounds_actor_count": bounds.get("actor_count"),
            "aim_bounds_labels_sample": (bounds.get("actor_labels") or [])[:12],
        }

    if cam:
        loc = cam.get_actor_location()
        meta["camera_label"] = actor_label(cam)
        rot = cam.get_actor_rotation()
        if target is not None:
            align_before = camera_forward_alignment(loc, rot, target, dress_bounds=bounds)
            meta["aim_before"] = align_before
            if not align_before.get("aim_ok"):
                rot = look_at_rotation(loc, target)
                try:
                    cam.set_actor_rotation(rot, False)
                    meta["camera_reaimed_at_homestead"] = True
                except Exception as e:
                    meta["camera_reaim_error"] = str(e)
                meta["aim_after"] = camera_forward_alignment(loc, rot, target, dress_bounds=bounds)
            meta["pose_source"] = "in_level_camera_aim_at_bounds"
        else:
            meta["pose_source"] = "in_level_camera_no_bounds"
            meta["warning"] = "inventory empty — camera may point at void; run place_vs_mvp_dress.py"
        meta["location"] = [loc.x, loc.y, loc.z]
        meta["rotation"] = [rot.pitch, rot.yaw, rot.roll]
        return loc, rot, meta

    if bounds:
        loc, rot, pose_meta = _camera_pose_from_bounds(shot_id, bounds)
        meta.update(pose_meta)
        return loc, rot, meta

    loc = meters_to_ue(tuple(shot["fallback_location_m"]))
    rot = euler_deg_to_rotator(*tuple(shot["fallback_rotation_deg"]))
    meta["pose_source"] = "hardcoded_fallback_last_resort"
    meta["fallback_location_m"] = list(shot["fallback_location_m"])
    meta["fallback_rotation_deg"] = list(shot["fallback_rotation_deg"])
    meta["warning"] = "No homestead inventory and no CAM — hardcoded pose may point into void"
    return loc, rot, meta


def write_homestead_capture_diagnostic(
    log_prefix: str = "pa_e_homestead_capture_diagnostic:",
    *,
    level_loaded: Optional[bool] = None,
    homestead_night_environment: Optional[dict[str, Any]] = None,
    arrange_gate: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Steps 1–2 snapshot: inventory + camera vs homestead centroids → Saved JSON (single write)."""
    payload: dict[str, Any] = {
        "lead_prove_loop": list(LEAD_PROVE_LOOP),
        "universal_testing_preconditions": list(UNIVERSAL_TESTING_PRECONDITIONS),
        "prove_criteria": dict(PROVE_CRITERIA),
        "level_path": LEVEL_PATH,
        "shots": [build_shot_diagnostic(shot) for shot in SHOTS],
        "diagnostic_script": "pa_e_homestead_capture_diagnostic.py",
        "note": (
            "Near-black captures are prove-loop in progress, not a closed FAIL. "
            "Use framing_bounds centroids to aim CAM_* before MRQ/AL capture."
        ),
    }
    if level_loaded is not None:
        payload["level_loaded"] = level_loaded
    if homestead_night_environment is not None:
        payload["homestead_night_environment"] = homestead_night_environment
    if arrange_gate is not None:
        payload["arrange_gate"] = arrange_gate
        payload["arrange_gate_path"] = arrange_gate.get("written_path") or arrange_gate_path()
    path = homestead_diagnostic_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        payload["written_path"] = path
        log(log_prefix, "diagnostic written", {"path": path})
    except OSError as e:
        payload["write_error"] = str(e)
        log(log_prefix, "diagnostic write failed", {"error": str(e)})
    return payload


def summarize_capture_report(shots: list[dict[str, Any]]) -> dict[str, Any]:
    """Report-level status: ok = capture PASS; near-black / speckle is not closed_fail."""
    capture_pass = bool(shots) and all(r.get("pass") for r in shots)
    closed_fail = False
    setup_quality_errors = (
        "near_black",
        "center_crop_near_black",
        "sparse_speckle_insufficient_l_gt_8",
        "sparse_speckle_insufficient_l_gt_1",
        "mostly_pure_black",
        "global_mean_false_pass_speckle",
        "shots_identical_hash",
        "shots_near_identical",
    )
    setup_only = True
    for r in shots:
        validation = r.get("validation") or {}
        if validation.get("closed_fail") is True:
            closed_fail = True
            setup_only = False
            break
        err = validation.get("error") or r.get("error")
        if err in setup_quality_errors:
            continue
        if not r.get("pass"):
            setup_only = False
            if err not in (None, *setup_quality_errors):
                closed_fail = True

    pair_paths = [(r.get("id", ""), (r.get("validation") or {}).get("path") or r.get("saved_path")) for r in shots]
    shot_pair = validate_shot_pair_diversity(pair_paths)
    if not shot_pair.get("pass"):
        capture_pass = False
        for r in shots:
            r["pass"] = False
            validation = r.setdefault("validation", {})
            if validation.get("pass"):
                validation["pass"] = False
            if not validation.get("error"):
                validation["error"] = shot_pair.get("error")
                validation["prove_loop_status"] = "in_progress"
                validation["closed_fail"] = False
        setup_only = setup_only and shot_pair.get("error") in setup_quality_errors

    if capture_pass:
        prove_loop_status = "complete"
    elif setup_only and not closed_fail:
        prove_loop_status = "in_progress"
    elif closed_fail:
        prove_loop_status = "blocked"
    else:
        prove_loop_status = "in_progress"
    return {
        "ok": capture_pass,
        "capture_pass": capture_pass,
        "closed_fail": closed_fail,
        "prove_loop_status": prove_loop_status,
        "shot_pair_validation": shot_pair,
        "black_stills_not_closed_fail": True,
        "lead_rule": (
            "Do not treat near-black / speckle / identical wrong stills as closed FAIL — "
            "complete LEAD_PROVE_LOOP (inventory → aim → lighting → capture/inspect → bug-fix) "
            "before claiming success."
        ),
    }


def build_shot_diagnostic(shot: dict) -> dict[str, Any]:
    """Camera vs homestead centroids for DESKTOP (MCP execute_python_script diagnostic helper)."""
    shot_id = shot["id"]
    inv = inventory_homestead_in_level(shot_id)
    cam = find_camera(shot["camera_labels"])
    entry: dict[str, Any] = {
        "shot_id": shot_id,
        "inventory": inv,
        "camera_labels": shot["camera_labels"],
        "camera_found": actor_label(cam) if cam else None,
    }
    bounds = inv.get("aim_bounds") or inv.get("framing_bounds") or inv.get("homestead_bounds")
    if cam and bounds and bounds.get("centroid"):
        loc = cam.get_actor_location()
        rot = cam.get_actor_rotation()
        target = _vector_from_list(bounds["centroid"])
        entry["camera_location"] = [loc.x, loc.y, loc.z]
        entry["target_centroid"] = bounds["centroid"]
        entry["expected_framing"] = {
            "aim_bounds_centroid": bounds["centroid"],
            "aim_bounds_min": bounds.get("min"),
            "aim_bounds_max": bounds.get("max"),
        }
        entry["alignment"] = camera_forward_alignment(loc, rot, target, dress_bounds=bounds)
    return entry


def ensure_cinematics_folder() -> None:
    if not unreal.EditorAssetLibrary.does_directory_exist(CINEMATICS_PA_E_DIR):
        unreal.EditorAssetLibrary.make_directory(CINEMATICS_PA_E_DIR)


def desktop_conductor_checklist() -> list[str]:
    """Checks Conductor runs on DESKTOP when capture fails or MRQ plugins block."""
    return [
        "Lead prove loop: (1) inventory homestead in level, (2) aim cameras at bounds centroids, "
        "(3) capture+inspect luminance, (4) bug-fix until lit — near-black is NOT closed FAIL.",
        "Run execute_python_script('pa_e_homestead_capture_diagnostic.py') → Saved/pa_e_homestead_capture_diagnostic.json",
        "Confirm report homestead_night_environment: Phase 2 + night tune + lighting_stack_verify.stack_ok "
        "(PRESET_Homestead_Night.md; Phase 2 alone insufficient — do not switch to day for black stills)",
        "Safe-Build after MovieRenderPipeline plugins; confirm MRQ Python types import.",
        "If inventory_ok false: run place_vs_mvp_dress.py + batch_import on DESKTOP.",
        "Run execute_python_script('capture_shotlist.py'); read Saved/pa_e_capture_report.json prove_loop fields.",
        "Until framing/lighting fixed: expect capture_pass false on mostly-black MRQ stills (~93% L=0, global mean ~8.7).",
        "PASS only when both PNGs pass bytes + mean + center-crop + bright-pixel fraction + shot-pair diversity "
        "(not file-exists-only or global-mean speckle PASS).",
    ]


def finish_loading_before_capture() -> dict[str, Any]:
    meta: dict[str, Any] = {"called": False}
    try:
        fn = getattr(unreal.AutomationLibrary, "finish_loading_before_screenshot", None)
        if callable(fn):
            fn()
            meta["called"] = True
    except Exception as e:
        meta["error"] = str(e)
    return meta


def apply_time_of_day_phase(phase: int, log_prefix: str = "") -> dict[str, Any]:
    """Apply hw.TimeOfDay.Phase N; return metadata for reports (testing precondition step 3)."""
    cmd = f"hw.TimeOfDay.Phase {int(phase)}"
    names = {0: "Day", 1: "Dusk", 2: "Night", 3: "Dawn"}
    meta: dict[str, Any] = {
        "phase": int(phase),
        "phase_name": names.get(int(phase), "Unknown"),
        "console_command": cmd,
        "applied": False,
    }
    try:
        unreal.SystemLibrary.execute_console_command(None, cmd)
        meta["applied"] = True
        if log_prefix:
            log(log_prefix, "time_of_day applied", {"phase": meta["phase"], "name": meta["phase_name"]})
    except Exception as e:
        meta["error"] = str(e)
        if log_prefix:
            log(log_prefix, "time_of_day failed", {"error": str(e)})
    return meta


def apply_pa_e_shotlist_time_of_day(log_prefix: str = "") -> dict[str, Any]:
    """Shotlist-aligned TOD for PA-E stills (night for shots 1–2). Phase 2 alone is insufficient."""
    block = dict(PA_E_SHOTLIST_TIME_OF_DAY)
    applied = apply_time_of_day_phase(block["phase"], log_prefix)
    block["apply_result"] = applied
    block["applied"] = applied.get("applied", False)
    return block


def apply_pa_e_homestead_night_environment(
    log_prefix: str = "",
    *,
    reseed_tmp_fixtures: bool = True,
    homestead_centroid: Optional[list[float]] = None,
) -> dict[str, Any]:
    """Phase 2 + PRESET tune + lighting stack verify before PA-E/MRQ capture."""
    import vnp_night_tune_and_evidence as vnp

    block: dict[str, Any] = {
        "preset_canon": PA_E_SHOTLIST_TIME_OF_DAY["preset_canon"],
        "night_tune_module": PA_E_SHOTLIST_TIME_OF_DAY["night_tune_module"],
        "phase_2_alone_insufficient": PA_E_SHOTLIST_TIME_OF_DAY["phase_2_alone_insufficient"],
        "do_not_switch_to_day": PA_E_SHOTLIST_TIME_OF_DAY["do_not_switch_to_day"],
        "mrq_pie_lighting_note": MRQ_PIE_LIGHTING_NOTE,
    }
    block["time_of_day"] = apply_pa_e_shotlist_time_of_day(log_prefix)
    tune = vnp.apply_homestead_night_tune()
    verify = vnp.verify_homestead_night_lighting_stack()
    reseed_meta: Optional[dict[str, Any]] = None
    if reseed_tmp_fixtures and not verify.get("stack_ok"):
        if homestead_centroid is None:
            inv = inventory_homestead_in_level()
            bounds = inv.get("homestead_bounds") or inv.get("framing_bounds")
            if bounds and bounds.get("centroid"):
                homestead_centroid = bounds["centroid"]
        reseed_meta = vnp.reseed_pa_e_tmp_night_fixtures(homestead_centroid)
        block["tmp_fixture_reseed"] = reseed_meta
        if reseed_meta.get("stack_ok_after_reseed"):
            tune = vnp.apply_homestead_night_tune()
            verify = vnp.verify_homestead_night_lighting_stack()
    block["night_tune"] = tune
    block["lighting_stack_verify"] = verify
    block["environment_preconditions_ok"] = bool(
        block["time_of_day"].get("applied")
        and tune.get("ok")
        and verify.get("stack_ok")
    )
    if not verify.get("stack_ok"):
        block["warning"] = (
            "Homestead night stack incomplete (moon/skylight/cabin warm) — pitch-black risk; "
            "dress LIT actors per PRESET_Homestead_Night.md then re-run diagnostic."
        )
        log(log_prefix, "night stack verify failed", {"verify": verify})
    elif log_prefix:
        log(log_prefix, "homestead night environment applied", {"stack_ok": True})
    return block


def apply_lit_game_view_for_capture() -> dict[str, Any]:
    """Align editor with lit + game view before MRQ/AL (same intent as viewport script)."""
    applied: dict[str, Any] = {}
    lit_method: Optional[str] = None
    try:
        set_vm = getattr(unreal.AutomationLibrary, "set_editor_viewport_view_mode", None)
        if callable(set_vm):
            mode = getattr(unreal, "ViewModeIndex", None)
            if mode is not None and hasattr(mode, "VMI_LIT"):
                set_vm(mode.VMI_LIT)
                lit_method = "AutomationLibrary.set_editor_viewport_view_mode(VMI_LIT)"
    except Exception as e:
        applied["automation_view_mode_error"] = str(e)
    if not lit_method:
        try:
            unreal.SystemLibrary.execute_console_command(None, "viewmode lit")
            lit_method = "console_viewmode_lit"
        except Exception as e:
            applied["viewmode_error"] = str(e)
    applied["viewmode"] = lit_method or "unknown"

    game_view = False
    try:
        ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
        if ues and hasattr(ues, "editor_set_game_view"):
            ues.editor_set_game_view(True)
            game_view = True
            applied["game_view_method"] = "UnrealEditorSubsystem.editor_set_game_view"
    except Exception as e:
        applied["game_view_error"] = str(e)
    if not game_view:
        try:
            unreal.SystemLibrary.execute_console_command(None, "gameview")
            game_view = True
            applied["game_view_method"] = "console_gameview"
        except Exception:
            pass
    applied["game_view"] = game_view
    return applied


def sync_editor_viewport_to_camera(cam, loc, rot) -> dict[str, Any]:
    """Pose editor viewport to shot camera (diagnostic — Lead-visible framing check)."""
    meta: dict[str, Any] = {"viewport_set": False, "pilot": False}
    try:
        ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
        if ues and hasattr(ues, "set_level_viewport_camera_info"):
            ues.set_level_viewport_camera_info(loc, rot)
            meta["viewport_set"] = True
            meta["viewport_api"] = "UnrealEditorSubsystem.set_level_viewport_camera_info"
    except Exception as e:
        meta["viewport_ues_error"] = str(e)
    if not meta["viewport_set"]:
        try:
            unreal.EditorLevelLibrary.set_level_viewport_camera_info(loc, rot)
            meta["viewport_set"] = True
            meta["viewport_api"] = "EditorLevelLibrary.set_level_viewport_camera_info"
        except Exception as e:
            meta["viewport_error"] = str(e)
    if cam:
        try:
            unreal.EditorLevelLibrary.pilot_level_actor(cam)
            meta["pilot"] = True
            meta["pilot_label"] = actor_label(cam)
        except Exception as e:
            meta["pilot_error"] = str(e)
    meta["location"] = [loc.x, loc.y, loc.z]
    meta["rotation"] = [rot.pitch, rot.yaw, rot.roll]
    return meta


def arrange_gate_path() -> str:
    return abs_path(os.path.join(project_dir(), "Saved", "pa_e_arrange_gate.json"))


def probe_mrq_tool_readiness() -> dict[str, Any]:
    """MRQ Python types + queue subsystem — blocked with editor_restart_required if plugins stale."""
    if unreal is None:
        return {"available": False, "error": "not_in_editor"}
    probe: dict[str, Any] = {"available": False}
    required = (
        "MoviePipelineQueueSubsystem",
        "MoviePipelineExecutorJob",
        "MoviePipelinePIEExecutor",
        "MoviePipelineOutputSetting",
        "MoviePipelineImageSequenceOutput_PNG",
    )
    missing = [n for n in required if not hasattr(unreal, n)]
    probe["missing_types"] = missing
    if missing:
        probe["error"] = "missing_unreal_types: " + ", ".join(missing)
        probe["blocked_reason"] = "mrq_unavailable"
        probe["plugin_hint"] = [
            "MovieRenderPipeline",
            "MovieRenderPipelineEditor",
            "SequencerScripting",
        ]
        probe["remediation"] = "Enable plugins in HomeWorld.uproject, Safe-Build, restart Editor"
        return probe
    try:
        subsys = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
        probe["subsystem"] = subsys is not None
        if subsys is None:
            probe["error"] = "MoviePipelineQueueSubsystem get_editor_subsystem returned None"
            probe["blocked_reason"] = "editor_restart_required"
            probe["remediation"] = (
                "Plugins may be enabled on disk but Python session stale — restart Editor after Safe-Build"
            )
            return probe
    except Exception as e:
        probe["error"] = str(e)
        probe["blocked_reason"] = "mrq_unavailable"
        return probe
    probe["available"] = True
    return probe


def aim_shot_cameras_for_capture(log_prefix: str = "") -> dict[str, Any]:
    """Step 2: re-aim CAM_* at per-shot aim_bounds centroids (find_look_at_rotation)."""
    shots_aim: list[dict[str, Any]] = []
    all_aim_ok = True
    for shot in SHOTS:
        cam = find_camera(shot["camera_labels"])
        loc, rot, pose_meta = resolve_camera_transform(shot, cam)
        inv = pose_meta.get("prove_loop_step1_inventory") or inventory_homestead_in_level(shot["id"])
        bounds = inv.get("aim_bounds") or inv.get("framing_bounds") or inv.get("homestead_bounds")
        aim_meta = pose_meta.get("aim_after") or pose_meta.get("aim_before")
        aim_ok = False
        if bounds and bounds.get("centroid"):
            target = _vector_from_list(bounds["centroid"])
            aim_meta = camera_forward_alignment(loc, rot, target, dress_bounds=bounds)
            aim_ok = bool(aim_meta.get("aim_ok"))
        elif aim_meta is not None:
            aim_ok = bool(aim_meta.get("aim_ok"))
        elif pose_meta.get("warning"):
            aim_ok = False
        else:
            aim_ok = pose_meta.get("pose_source") != "hardcoded_fallback_last_resort"
        if not aim_ok:
            all_aim_ok = False
        shots_aim.append(
            {
                "shot_id": shot["id"],
                "camera_labels": shot["camera_labels"],
                "camera_label": pose_meta.get("camera_label"),
                "pose_source": pose_meta.get("pose_source"),
                "expected_framing": pose_meta.get("expected_framing"),
                "aim_ok": aim_ok,
                "aim": aim_meta,
                "inventory_ok": inv.get("inventory_ok"),
                "aim_bounds_ok": inv.get("aim_bounds_ok"),
            }
        )
    out = {"shots": shots_aim, "aim_ok": all_aim_ok}
    if log_prefix:
        log(log_prefix, "aim_shot_cameras", {"aim_ok": all_aim_ok})
    return out


def reapply_night_environment_for_mrq_shot(shot_id: str, log_prefix: str = "") -> dict[str, Any]:
    """Re-apply Phase 2 + PRESET tune before each MRQ PIE job (Editor TMP ≠ PIE world)."""
    inv = inventory_homestead_in_level(shot_id)
    bounds = inv.get("aim_bounds") or inv.get("framing_bounds") or inv.get("homestead_bounds")
    centroid = bounds.get("centroid") if bounds else None
    block = apply_pa_e_homestead_night_environment(
        log_prefix,
        reseed_tmp_fixtures=True,
        homestead_centroid=centroid,
    )
    block["shot_id"] = shot_id
    block["mrq_pie_lighting_note"] = MRQ_PIE_LIGHTING_NOTE
    return block


def arrange_pa_e_shotlist(
    log_prefix: str = "",
    *,
    level_loaded: bool = True,
    require_mrq: bool = False,
    mrq_probe: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """P0 Arrange gate — inventory, aim, night stack, lit/game view. Blocks capture when not ready."""
    blocked_reasons: list[str] = []
    if not level_loaded:
        blocked_reasons.append("level_load_failed")

    per_shot_inventory: list[dict[str, Any]] = []
    for shot in SHOTS:
        inv = inventory_homestead_in_level(shot["id"])
        per_shot_inventory.append({"shot_id": shot["id"], "inventory": inv})
        if not inv.get("inventory_ok"):
            blocked_reasons.append(f"inventory_empty_{shot['id']}")
        if not inv.get("aim_bounds_ok"):
            blocked_reasons.append(f"aim_bounds_missing_{shot['id']}")

    inventory = inventory_homestead_in_level()
    if not inventory.get("inventory_ok"):
        blocked_reasons.append("inventory_empty")

    centroid = None
    bounds = inventory.get("homestead_bounds") or inventory.get("framing_bounds")
    if bounds and bounds.get("centroid"):
        centroid = bounds["centroid"]

    aim = aim_shot_cameras_for_capture(log_prefix)
    if not aim.get("aim_ok"):
        blocked_reasons.append("camera_aim_not_at_homestead")
    for shot_aim in aim.get("shots") or []:
        alignment = shot_aim.get("aim") or {}
        if alignment.get("forward_ray_hits_dress_aabb") is False:
            blocked_reasons.append(f"camera_ray_misses_dress_bounds_{shot_aim.get('shot_id')}")

    finish_loading = finish_loading_before_capture()
    lighting = apply_pa_e_homestead_night_environment(
        log_prefix, reseed_tmp_fixtures=True, homestead_centroid=centroid
    )
    view = apply_lit_game_view_for_capture()

    tool_readiness: dict[str, Any] = {"mrq": None}
    if require_mrq:
        tool_readiness["mrq"] = mrq_probe if mrq_probe is not None else probe_mrq_tool_readiness()
        mrq = tool_readiness["mrq"] or {}
        if not mrq.get("available"):
            reason = mrq.get("blocked_reason") or "mrq_unavailable"
            blocked_reasons.append(reason)

    if not lighting.get("environment_preconditions_ok"):
        blocked_reasons.append("night_lighting_stack_incomplete")

    ready = len(blocked_reasons) == 0
    gate: dict[str, Any] = {
        "ready": ready,
        "blocked_reasons": blocked_reasons,
        "level_loaded": level_loaded,
        "inventory": inventory,
        "per_shot_inventory": per_shot_inventory,
        "aim": aim,
        "lighting": lighting,
        "mrq_pie_lighting_note": MRQ_PIE_LIGHTING_NOTE,
        "view": view,
        "finish_loading": finish_loading,
        "tool_readiness": tool_readiness,
        "lead_prove_loop": list(LEAD_PROVE_LOOP),
        "universal_testing_preconditions": list(UNIVERSAL_TESTING_PRECONDITIONS),
        "level_path": LEVEL_PATH,
    }
    path = arrange_gate_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(gate, f, indent=2, default=str)
        gate["written_path"] = path
        if log_prefix:
            log(log_prefix, "arrange_gate written", {"ready": ready, "path": path, "blocked": blocked_reasons})
    except OSError as e:
        gate["write_error"] = str(e)
        if log_prefix:
            log(log_prefix, "arrange_gate write failed", {"error": str(e)})
    return gate


def write_blocked_capture_report(
    *,
    prefix: str,
    primary_path: str,
    arrange_gate: dict[str, Any],
    level_loaded: bool,
    keep_python_script_alive: bool = False,
    mrq_probe: Optional[dict[str, Any]] = None,
    extra: Optional[dict[str, Any]] = None,
) -> str:
    """No capture attempted — prove-loop blocked, not closed FAIL."""
    report: dict[str, Any] = {
        "ok": False,
        "capture_pass": False,
        "closed_fail": False,
        "prove_loop_status": "blocked",
        "arrange_gate": arrange_gate,
        "arrange_gate_path": arrange_gate.get("written_path") or arrange_gate_path(),
        "blocked_reasons": arrange_gate.get("blocked_reasons") or [],
        "lead_prove_loop": list(LEAD_PROVE_LOOP),
        "universal_testing_preconditions": list(UNIVERSAL_TESTING_PRECONDITIONS),
        "homestead_diagnostic_path": homestead_diagnostic_path(),
        "prefix": prefix.strip(":"),
        "primary_path": primary_path,
        "level_path": LEVEL_PATH,
        "level_loaded": level_loaded,
        "keep_python_script_alive": keep_python_script_alive,
        "prove_criteria": PROVE_CRITERIA,
        "desktop_conductor_checklist": desktop_conductor_checklist(),
        "shots": [],
        "policy": (
            "P0 Arrange gate — no MRQ/AL job until ready. "
            "Blocked is not closed FAIL; complete LEAD_PROVE_LOOP (inventory→aim→lighting→capture)."
        ),
    }
    if mrq_probe is not None:
        report["mrq_probe"] = mrq_probe
        report["mrq_available"] = bool(mrq_probe.get("available"))
    if extra:
        report.update(extra)
    out_path = report_path()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, default=str)
    log(prefix, "capture blocked by arrange gate", {"reasons": report["blocked_reasons"], "path": out_path})
    return out_path


# Lead-facing alias (Arrange before Act/Assert).
assert_environment_ready = arrange_pa_e_shotlist
