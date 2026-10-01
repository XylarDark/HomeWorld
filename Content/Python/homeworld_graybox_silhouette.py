"""Silhouette-collision assertion: two volumes from different mechanic families
may not share a scale band.

This is the machine form of the Lead's criterion 4 -- *"is it distinct in its
rudimentary form"* -- made mechanical by TG-ZONE-FAMILY, whose locked rule is:

    "A mechanic family that cannot be told apart by shape from 20 m away has
    failed its section. No HUD is permitted to rescue it."

The seven signature silhouettes are LOCKED TASTE (TG-GRAYBOX-SILHOUETTE,
2026-10-01). How they are measured is an architecture decision, recorded as
DEC-0022. The honest caveat below is carried from Docs/34 research §7.

WHAT IS AND IS NOT A CITED STANDARD
-----------------------------------
There is **no published industry standard** for a greybox acceptance checklist
and **no source shows anyone running a programmatic silhouette-distinctness
check**. David Shaver's method is a manual squint test. This module is a **house
standard**. It is not evidence of industry practice and must not be cited as
such.

WHY NOT JUST ASPECT RATIO
-------------------------
The upstream handoff proposed "two volumes from different families may not share
an aspect ratio within the same scale band". Aspect ratio is a *proxy for*
silhouette, not a measure of it, and it fails in both directions:

  * **False negative** -- a 1:1:1 pyramid and a 1:1:1 cube share aspect ratio
    1.00 and are not the same silhouette. This is exactly the measured defect:
    SM_Cabin (5.5x4.5x5.5) and SM_PineValley_Block_A (10x8x10) both resolve to
    1.00 while being obviously different objects.
  * **False positive** -- two flat wide pads at aspect 0.05 and 0.06 collide on
    a ratio band while being unmistakably different in outline.

So this module computes a **silhouette descriptor** and uses aspect ratio only
as one cheap input to it:

  * ``profile`` -- normalized height / width / depth, the raw proportions
  * ``band``    -- verticality class (flat / low / mid / tall / spire)
  * ``footprint_aspect`` -- plan-view aspect (square / oblong / strip)
  * ``openness`` -- estimated sky visibility, from plan-view area vs silhouette

``openness`` exists because one locked signature is *"tall thin vertical with a
see-through gap"* (spirit). Two volumes can share every proportion and still be
told apart if one is open and the other is solid, and a pure proportion metric
cannot see that at all.
"""

from __future__ import annotations

from dataclasses import dataclass

from homeworld_graybox_spec import (
    FAMILY_BUILD_PLACE,
    FAMILY_COMBAT,
    FAMILY_GATHER,
    FAMILY_HEAL,
    FAMILY_NURTURE_TAME,
    FAMILY_SPIRIT,
    FAMILY_STEALTH,
    Volume,
)

# --------------------------------------------------------------------------
# Verticality bands. Cut from the locked silhouettes:
#   gather        "low wide soft mound"        -> flat
#   nurture_tame  "broad low pad"              -> flat
#   stealth       "low broken horizontal"      -> low
#   build_place   "flat square plate"          -> flat
#   heal          "narrow upright"             -> mid
#   spirit        "tall thin vertical"         -> tall/spire
#   combat        "tallest in frame"           -> tall/spire
#
# Two different families in the SAME band are the ones at risk of colliding,
# so bands are the primary axis. Width/height tolerance within a band is the
# secondary axis.
# --------------------------------------------------------------------------

BAND_FLAT = "flat"
BAND_LOW = "low"
BAND_MID = "mid"
BAND_TALL = "tall"

#: band -> (min aspect, max aspect) inclusive. Outside these bounds is the next band.
BAND_BOUNDS: tuple[tuple[str, float, float], ...] = (
    (BAND_FLAT, 0.00, 0.35),
    (BAND_LOW, 0.35, 0.75),
    (BAND_MID, 0.75, 1.80),
    (BAND_TALL, 1.80, 99.0),
)

#: Bands a family is allowed to occupy, from its locked signature silhouette.
#: Agent-owned derivation (DEC-0022) of the Lead's words.
FAMILY_BANDS: dict[str, tuple[str, ...]] = {
    FAMILY_GATHER: (BAND_FLAT,),
    FAMILY_NURTURE_TAME: (BAND_FLAT,),
    FAMILY_STEALTH: (BAND_LOW, BAND_FLAT),
    FAMILY_BUILD_PLACE: (BAND_FLAT,),
    FAMILY_HEAL: (BAND_MID, BAND_TALL),
    FAMILY_SPIRIT: (BAND_TALL,),
    FAMILY_COMBAT: (BAND_TALL, BAND_MID),
}

#: A family's signature, quoted from the taste gate for error messages. This is
#: taste text, not a rule -- the rule is FAMILY_BANDS above.
FAMILY_SIGNATURE: dict[str, str] = {
    FAMILY_GATHER: "low wide soft mound, reads as a spreading patch",
    FAMILY_NURTURE_TAME: "broad low pad with a raised rim you can see over",
    FAMILY_HEAL: "narrow upright, single soft column",
    FAMILY_SPIRIT: "tall thin vertical with a see-through gap",
    FAMILY_STEALTH: "low broken horizontal, never a closed mass",
    FAMILY_BUILD_PLACE: "flat square plate, deliberately dull",
    FAMILY_COMBAT: "jagged asymmetric wedge, tallest in frame",
}

#: Two assertable volumes whose aspect ratios differ by less than this are
#: treated as the same proportions. Not a tight number: it is a change
#: detector, and the tolerance that matters is the one the eye accepts, which
#: nobody has measured for our camera. Flagged in the report as a house value.
ASPECT_TOLERANCE = 0.15


@dataclass(frozen=True)
class Silhouette:
    """Measured shape descriptor for one volume."""

    name: str
    family: str
    size_m: tuple[float, float, float]
    band: str
    aspect: float
    footprint_aspect: float
    openness: float
    is_thin: bool

    def describe(self) -> str:
        return "%s %s band=%s aspect=%.2f plan=%.2f open=%.2f" % (
            self.name,
            self.family,
            self.band,
            self.aspect,
            self.footprint_aspect,
            self.openness,
        )


@dataclass(frozen=True)
class Collision:
    """Two volumes from different families that read too alike."""

    a: Silhouette
    b: Silhouette
    reason: str
    severity: str  # "blocking" | "warn"

    def describe(self) -> str:
        return "%s: %s  vs  %s" % (self.severity.upper(), self.a.describe(), self.b.describe())


def band_for(aspect: float) -> str:
    """Map an aspect ratio (height / largest footprint dimension) to a band."""
    for band, low, high in BAND_BOUNDS:
        if low <= aspect <= high:
            return band
    return BAND_TALL


def openness_for(size_m: tuple[float, float, float]) -> float:
    """Estimated sky visibility, 0.0 (solid) .. 1.0 (see-through).

    A greybox box's plan area versus its bounding-box area is the only openness
    signal available without authored topology. A plate scores high because most
    of its silhouette is empty; a solid mass scores low. This is a proxy and is
    labelled as one -- see the module docstring.
    """
    x, y, z = size_m
    if x <= 0.0 or y <= 0.0 or z <= 0.0:
        return 0.0
    # A cube is 1.0 volume / 1.0 bbox-volume-ish; a thin plate is mostly air
    # above it. Use solidity against the smallest sensible bounding solid.
    solidity = (x * y * z) / max(x * y * z, 1e-9)
    thinness = min(x, y, z) / max(x, y, z)
    return max(0.0, min(1.0, 1.0 - solidity * (1.0 - thinness) * 0.5))


def measure(volume: Volume) -> Silhouette:
    """Build the silhouette descriptor for a spec'd volume."""
    x, y, z = volume.size_m
    plan = x / y if y > 0.0 else 0.0
    return Silhouette(
        name=volume.name,
        family=volume.family,
        size_m=volume.size_m,
        band=band_for(volume.aspect),
        aspect=volume.aspect,
        footprint_aspect=plan,
        openness=openness_for(volume.size_m),
        is_thin=volume.is_thin,
    )


def family_conformance(volumes: list[Volume]) -> list[tuple[Volume, str]]:
    """Volumes whose measured band does not match their family's locked signature.

    This is the assertion that catches "the gather zone reads tall", which is a
    direct violation of TG-ZONE-FAMILY fork G.
    """
    out: list[tuple[Volume, str]] = []
    for volume in volumes:
        if not volume.is_assertable:
            continue
        allowed = FAMILY_BANDS.get(volume.family)
        if not allowed:
            out.append(
                (
                    volume,
                    "family '%s' has no band rule; add one or drop the assertion"
                    % volume.family,
                )
            )
            continue
        measured = measure(volume).band
        if measured not in allowed:
            out.append(
                (
                    volume,
                    "measures %s but the locked signature for '%s' is %s"
                    % (measured, volume.family, FAMILY_SIGNATURE.get(volume.family, "?")),
                )
            )
    return out


def find_collisions(volumes: list[Volume]) -> list[Collision]:
    """Every pair of assertable volumes from *different* families that collide.

    Collision means: same verticality band AND aspect within ASPECT_TOLERANCE.
    Openness is used to downgrade rather than to trigger, because a gap is a
    secondary cue and a real geometry difference, not a proportion one.
    """
    assertable = [volume for volume in volumes if volume.is_assertable]
    measured = [(volume, measure(volume)) for volume in assertable]
    collisions: list[Collision] = []

    for i, (vol_a, sil_a) in enumerate(measured):
        for vol_b, sil_b in measured[i + 1 :]:
            if vol_a.family == vol_b.family:
                continue  # same family is *supposed* to share a silhouette
            if sil_a.band != sil_b.band:
                continue
            delta = abs(sil_a.aspect - sil_b.aspect)
            if delta > ASPECT_TOLERANCE:
                continue

            # Same band and same proportions. Openness can still separate them.
            if abs(sil_a.openness - sil_b.openness) > 0.25:
                collisions.append(
                    Collision(
                        a=sil_a,
                        b=sil_b,
                        reason="same band and proportion, only openness separates them",
                        severity="warn",
                    )
                )
                continue

            collisions.append(
                Collision(
                    a=sil_a,
                    b=sil_b,
                    reason="different families share band '%s' and aspect within %.2f"
                    % (sil_a.band, ASPECT_TOLERANCE),
                    severity="blocking",
                )
            )

    collisions.sort(key=lambda c: (c.severity != "blocking", c.a.name, c.b.name))
    return collisions
