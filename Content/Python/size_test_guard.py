"""Refuse a stroke or an ease pad on L_SizeTest.

The size-test map is a walk, a stop, and a hop. This check is pure so a host
test can run it without the Editor.
"""


def is_stroke_or_ease(label, class_names):
    parts = [label or ""]
    for name in class_names or []:
        parts.append(name or "")
    blob = " ".join(parts)
    return "StrokeReport" in blob or "EasePad" in blob


def size_test_stroke_errors(entries):
    """entries is a sequence of (label, class_names)."""
    errors = []
    for label, class_names in entries:
        if is_stroke_or_ease(label, class_names):
            errors.append("stroke or ease pad on L_SizeTest: %s" % (label or "unnamed"))
    return errors
