"""Canonical PA-E shotlist capture entry — MRQ one-frame primary.

MCP / DESKTOP prove:
  execute_python_script("capture_shotlist.py")
  or execute_python_script("capture_shotlist_mrq.py")

Fallback diagnostic (AutomationLibrary pretick, not PASS path):
  capture_shotlist_viewport.py

See docs/Automation/CAPTURE_REDUNDANCY.md.
"""
from __future__ import annotations

from capture_shotlist_mrq import main

if __name__ == "__main__":
    main()
