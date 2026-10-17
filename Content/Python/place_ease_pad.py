"""Ease pad placer check.

The pad and its focus belong on L_EasePad. They do not belong on L_SizeTest.
Saving the map in the editor is a separate step. This script does not write a map.
"""

from __future__ import annotations


PAD_MAP = "/Game/HomeWorld/Maps/EasePad/L_EasePad"
SIZE_TEST_MAP = "/Game/HomeWorld/Maps/SizeTest/L_SizeTest"

INTENDED_PAD = (
    ("EasePad", ("HomeWorldEasePad", "Focus")),
    ("EasePad_Focus", ("SceneComponent",)),
)

SIZE_TEST_STAYS = (
    ("PlayerStart", ("PlayerStart",)),
    ("SM_Size_Cottage", ("StaticMeshActor",)),
)


def _blob(label, class_names):
    parts = [label or ""]
    for name in class_names or ():
        parts.append(name or "")
    return " ".join(parts)


def _has(entries, needle):
    for label, class_names in entries:
        if needle in _blob(label, class_names):
            return True
    return False


def ease_pad_report(pad_level, size_test_level):
    """Report the pad, the focus, and that the pad is absent from L_SizeTest."""
    pad = _has(pad_level, "EasePad") or _has(pad_level, "HomeWorldEasePad")
    focus = _has(pad_level, "Focus")
    on_size_test = _has(size_test_level, "EasePad") or _has(size_test_level, "HomeWorldEasePad") or _has(
        size_test_level, "StrokeReport"
    )
    return {
        "map": PAD_MAP,
        "pad": pad,
        "focus": focus,
        "absent_from_L_SizeTest": not on_size_test,
        "size_test_map": SIZE_TEST_MAP,
    }


def main():
    report = ease_pad_report(INTENDED_PAD, SIZE_TEST_STAYS)
    print(
        "ease_pad: pad=%s focus=%s absent_from_L_SizeTest=%s map=%s"
        % (report["pad"], report["focus"], report["absent_from_L_SizeTest"], report["map"])
    )
    if not (report["pad"] and report["focus"] and report["absent_from_L_SizeTest"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
