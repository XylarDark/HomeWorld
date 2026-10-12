"""Count editor-UI tokens against Slate clicks and MCP hangs.

Reads Saved/Logs/HomeWorld.log. Prints three counts. No editor required.
"""

import os
import sys

LOG = os.path.join(os.path.dirname(__file__), "..", "..", "Saved", "Logs", "HomeWorld.log")


def counts(text):
    need = text.count("editor_ui: NEED_SLATE")
    clicks = text.count("SlateInspectorToolset.SlateInspectorToolset.Click")
    hang_lines = 0
    for line in text.splitlines():
        folded = line.lower()
        if "recursionguard" in folded or "not responding" in folded or ("mcp" in folded and "timeout" in folded):
            hang_lines += 1
    return need, clicks, hang_lines


def main():
    path = os.path.abspath(LOG)
    if not os.path.isfile(path):
        print("count_mcp_editor_ui: no log at " + path)
        return 1
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        need, clicks, hangs = counts(handle.read())
    print("NEED_SLATE %d" % need)
    print("Slate Click %d" % clicks)
    print("MCP hang lines %d" % hangs)
    if need and clicks == 0:
        print("token without a click: the inspector was not used")
    return 0


if __name__ == "__main__":
    sys.exit(main())
