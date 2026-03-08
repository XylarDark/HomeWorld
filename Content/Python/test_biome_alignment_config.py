# test_biome_alignment_config.py
# Loads resource_nodes_per_biome.json and planetoid_alignments.json and logs one entry per
# biome and per alignment. Use to validate configs without PIE (e.g. via MCP execute_python_script).
# See docs/PLANETOID_BIOMES.md "How to test biome/alignment" and docs/CONSOLE_COMMANDS.md.

import json
import os

# Resolve Content/Python so we can load JSONs next to this script
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_BIOME_CONFIG = os.path.join(_SCRIPT_DIR, "resource_nodes_per_biome.json")
_ALIGNMENT_CONFIG = os.path.join(_SCRIPT_DIR, "planetoid_alignments.json")

_PREFIX = "HomeWorld biome/alignment test: "


def _log(msg: str) -> None:
    try:
        import unreal
        unreal.log(_PREFIX + msg)
    except Exception:
        print(_PREFIX + msg)


def run() -> bool:
    ok = True
    # resource_nodes_per_biome.json — one log line per biome
    if not os.path.isfile(_BIOME_CONFIG):
        _log(f"Missing {_BIOME_CONFIG}")
        ok = False
    else:
        with open(_BIOME_CONFIG, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, value in data.items():
            if key.startswith("_"):
                continue
            if isinstance(value, list):
                _log(f"biome {key}: {len(value)} node type(s)")
            else:
                _log(f"biome {key}: {value}")
    # planetoid_alignments.json — one log line per alignment
    if not os.path.isfile(_ALIGNMENT_CONFIG):
        _log(f"Missing {_ALIGNMENT_CONFIG}")
        ok = False
    else:
        with open(_ALIGNMENT_CONFIG, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, value in data.items():
            if key.startswith("_"):
                continue
            if isinstance(value, dict):
                focus = value.get("activity_focus", "?")
                _log(f"alignment {key}: activity_focus={focus}")
            else:
                _log(f"alignment {key}: {value}")
    return ok


if __name__ == "__main__":
    run()
