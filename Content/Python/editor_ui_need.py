"""Signal that an editor panel has no Python write.

Does not import unreal. A normal pytest run can import this module.
"""

TOKEN = "editor_ui: NEED_SLATE"

_PANELS = (
    ("portal-level", ("leveltoopen",)),
    ("state-tree", ("state tree",)),
    ("pcg-details", ("by tag", "mesh list", "static mesh spawner")),
)


def report(panel, why):
    """Log the stable token and return that same line."""
    line = "%s panel=%s why=%s" % (TOKEN, panel, why)
    print(line)
    return line


def classify(text):
    """Return a panel id when text is a known no-Python-write failure."""
    if not text:
        return None
    folded = text.lower()
    for panel, needles in _PANELS:
        for needle in needles:
            if needle in folded:
                return panel
    return None
