# init_unreal.py
# Runs automatically when the Unreal Editor loads (Content/Python/ is a standard startup location).
# Ensures Enhanced Input assets (IA_Move, IA_Look, IMC_Default, etc.) exist so movement works
# without manually running setup_enhanced_input.py. Idempotent: safe to run every load.

import sys
import os

try:
    import unreal
except ImportError:
    # Not in Editor (e.g. standalone Python); skip
    sys.exit(0)

_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

try:
    import setup_enhanced_input
    setup_enhanced_input.main()
except Exception as e:
    unreal.log_warning("InitUnreal: Enhanced Input setup failed: " + str(e))
