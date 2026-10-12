"""Measure the homestead. Do not move actors and do not save."""

import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import cabin_shell
import scene_placement

importlib.reload(cabin_shell)
importlib.reload(scene_placement)
sys.exit(scene_placement.check())
