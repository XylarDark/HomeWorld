# create_master_materials_stub.py
# Back-compat entry point — delegates to create_master_materials.py (full graph builder).

from __future__ import annotations

import importlib
import sys

try:
    import unreal
except ImportError:
    print("create_master_materials_stub: Run inside Unreal Editor.")
    sys.exit(1)

PREFIX = "create_master_materials_stub:"


def _log(msg: str) -> None:
    unreal.log(PREFIX + " " + str(msg))
    print(PREFIX, msg)


def main() -> int:
    _log("Delegating to create_master_materials.py (post-audit wrap graph builder)")
    import create_master_materials

    importlib.reload(create_master_materials)
    return create_master_materials.main(force="--force" in sys.argv)


if __name__ == "__main__":
    code = main()
    if code != 0:
        unreal.log_error(PREFIX + " finished with code %s" % code)
