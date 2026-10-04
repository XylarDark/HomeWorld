"""Raise a notification when a session ends, on any harness.

The problem this solves, in the Lead's words on 2026-10-04: *"if I have specified
I am on my phone using grok bot, that you alert the bot when you are finished a
task and with a question."* Today the only way to find out what an agent is doing
is to ask a bot to screenshot the desktop.

Two channels, and the split is not a preference - it is what the apps actually
expose.

**Windows toast.** Verified on this host: `Windows.UI.Notifications` via WinRT
works under PowerShell 5.1, with no BurntToast module installed. Reaches the
desktop, including a phone linked to this machine.

**`grokbot://`.** Grok Bot 0.66.0 is an Electron app installed at
`%LOCALAPPDATA%\\Programs\\Grok Bot` and registers the `grokbot` URL scheme.
Measured from its own bundle on 2026-10-04 (`dist/electron-main/main-core.cjs`):

    schemes: ["grokbot", "sand"]   authority: "app"   maxUrlLength: 2048

    agent            /v1/agent?id=<agentId>
    marketplace      /v1/marketplace?tab=plugins|bots&id=<slug>
    plugin-add       /v1/plugin/add?id=<numeric>
    open             /v1/open                 <- NO parameters
    create-team-bot  /v1/create-team-bot
    settings         /v1/settings?id=<...>
    task             /v1/task?id=<10 hex chars>
    sidebar          /v1/sidebar?target=webhook-url|webhook-key|webhook-header
                                       &automation=<...>&agent=<...>
                                       &tab=overview|routines|media|computer
                                            |meetings|members

**`grokbot://` CANNOT CARRY A MESSAGE.** Every parameter in that schema is an ID
or a closed enum, and `open` - the route a "show me the app" link would use -
takes none at all. The bare `grokbot://` in the app's own CTA copy resolves to
`/v1/open` and raises the window. That is the whole capability: focus, not
transmit.

This is why the toast carries the question and the protocol handler only raises
the window. The alternative - assuming a payload parameter exists and building on
it - would produce a notification that silently drops the one thing that matters.
`KNOWING_WHY` below records that this was measured rather than assumed, because
the obvious guess is wrong and a future session will make it again.

The phone case is not solved by either channel. A Windows toast reaches a linked
phone; `grokbot://` reaches a desktop app. A toast carrying the full question is
the closest available thing, and it needs no network, no allowlist change, and no
new dependency.

HARNESS-AGNOSTIC BY CONSTRUCTION. Nothing here imports an agent, reads a cursor
config, or knows which IDE a session runs in. It is a script that raises a
notification, so `session_close.py` can call it from opencode, from cursor, or
from a cron job at 3am, and the behaviour is identical.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Grok Bot, measured not guessed
# --------------------------------------------------------------------------

#: The URL schemes the app registers. `grokbot` is the product; `sand` is the
#: internal Cursor surface and is deliberately not used.
GROKBOT_SCHEME = "grokbot"
GROKBOT_AUTHORITY = "app"
GROKBOT_SCHEMES = ("grokbot", "sand")

#: Routes recovered from the app bundle, with the parameters each accepts.
#:
#: WHY THIS TABLE IS THE POINT OF THE MODULE. `open` is the only route that can
#: be built without knowing an ID, and it takes no parameters - which is exactly
#: why the question cannot travel this way. Written out rather than left implicit
#: so the next session does not "discover" a payload parameter that does not
#: exist and build on it.
GROKBOT_ROUTES: dict[str, tuple[str, tuple[str, ...]]] = {
    "open": ("/v1/open", ()),
    "agent": ("/v1/agent", ("id",)),
    "marketplace": ("/v1/marketplace", ("tab", "id")),
    "plugin-add": ("/v1/plugin/add", ("id",)),
    "create-team-bot": ("/v1/create-team-bot", ()),
    "settings": ("/v1/settings", ("id",)),
    "task": ("/v1/task", ("id",)),
    "sidebar": ("/v1/sidebar", ("target", "automation", "agent", "tab")),
}

#: Schemes that could plausibly carry free text, had the app any. Empty on
#: purpose - this is a measurement, and it measured nothing.
GROKBOT_TEXT_ROUTES: frozenset[str] = frozenset()

KNOWING_WHY = (
    "grokbot:// is a window-raise, not a message channel. Measured from "
    "Grok Bot 0.66.0's own bundle on 2026-10-04: every parameter on every "
    "route is an ID or a closed enum, and the `open` route takes none. The "
    "question therefore travels in the toast, and the protocol handler is "
    "used only to bring the app forward. If a future Grok Bot adds a text "
    "parameter, add it to GROKBOT_TEXT_ROUTES and re-test - do not assume one."
)


def grokbot_url(route: str = "open", **params: str) -> str:
    """Build a `grokbot://` URL. Raises on an unknown route or bad param name.

    Validated rather than assembled. The app rejects unknown routes and
    ill-typed parameters at parse time, and a malformed URL is indistinguishable
    from no notification at all - it opens nothing and reports nothing.
    """
    if route not in GROKBOT_ROUTES:
        raise KeyError(f"unknown grokbot route {route!r}; known: "
                       + ", ".join(sorted(GROKBOT_ROUTES)))
    path, allowed = GROKBOT_ROUTES[route]
    bad = [k for k in params if k not in allowed]
    if bad:
        raise KeyError(f"route {route!r} takes {allowed or 'no parameters'}; "
                       f"got {bad}")
    url = f"{GROKBOT_SCHEME}://{GROKBOT_AUTHORITY}{path}"
    if params:
        from urllib.parse import urlencode
        url += "?" + urlencode(params)
    return url


def grokbot_installed() -> bool:
    """True when this host has Grok Bot and it registered the URL scheme."""
    if not sys.platform.startswith("win"):
        return False
    try:
        import winreg
    except ImportError:
        return False
    for root in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        for scheme in GROKBOT_SCHEMES:
            try:
                with winreg.OpenKey(root, rf"Software\Classes\{scheme}") as k:
                    winreg.QueryValueEx(k, "")
                    return True
            except OSError:
                continue
    return False


# --------------------------------------------------------------------------
# Windows toast
# --------------------------------------------------------------------------

# PowerShell that raises a ToastGeneric notification. Kept as a single line
# sequence because PowerShell 5.1 has no -Command quoting rules worth relying
# on from Python; the script is passed as -EncodedCommand to avoid quoting
# entirely.
_TOAST_PS = r"""
$ErrorActionPreference = 'Stop'
[void][Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType=WindowsRuntime]
[void][Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType=WindowsRuntime]
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$esc = { param($s) [System.Security.SecurityElement]::Escape([string]$s) }
$xml.LoadXml(("<toast><visual><binding template='ToastGeneric'>" +
  "<text id='1'>" + (& $esc $env:HW_TOAST_TITLE) + "</text>" +
  "<text id='2'>" + (& $esc $env:HW_TOAST_BODY)  + "</text>" +
  "</binding></visual></toast>"))
$toast = New-Object Windows.UI.Notifications.ToastNotification $xml
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('HomeWorld').Show($toast)
Write-Output 'ok'
"""


def _ps_encoded(script: str) -> list[str]:
    import base64
    return [
        "powershell", "-NoProfile", "-NonInteractive",
        "-ExecutionPolicy", "Bypass",
        "-EncodedCommand",
        base64.b64encode(script.encode("utf-16-le")).decode("ascii"),
    ]


def notify_toast(title: str, body: str, timeout_ms: int = 20000) -> tuple[bool, str]:
    """Raise a Windows toast. Returns (ok, detail) and never raises.

    Env vars carry the text rather than interpolated literals: a session
    question contains apostrophes, quotes, arrows and newlines, and building a
    PowerShell string literal out of those is how a notification silently
    becomes a syntax error.
    """
    if not sys.platform.startswith("win"):
        return False, "not Windows; no toast channel"
    if len(body) > 320:
        body = body[:317] + "..."
    env = dict(os.environ)
    env["HW_TOAST_TITLE"] = title
    env["HW_TOAST_BODY"] = body
    try:
        r = subprocess.run(_ps_encoded(_TOAST_PS), capture_output=True,
                           text=True, timeout=30, env=env)
    except (OSError, subprocess.SubprocessError) as e:
        return False, f"{type(e).__name__}: {e}"
    if r.returncode != 0:
        return False, (r.stderr or r.stdout or "unknown").strip()[:200]
    return "ok" in (r.stdout or ""), (r.stdout or "").strip()[:80]


def notify_grokbot(route: str = "open", **params: str) -> tuple[bool, str]:
    """Raise the Grok Bot window. Returns (ok, detail) and never raises.

    Uses the shell so the OS protocol handler runs, which is what focuses an
    already-running instance. `rundll32 url.dll,FileProtocolHandler` is the
    documented way to do this from a non-shell context and does not need a
    `file://` association.
    """
    try:
        url = grokbot_url(route, **params)
    except KeyError as e:
        return False, str(e)
    launcher = shutil.which("rundll32")
    if not launcher:
        return False, "rundll32 not on PATH"
    try:
        subprocess.Popen([launcher, "url.dll,FileProtocolHandler", url],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError as e:
        return False, f"{type(e).__name__}: {e}"
    return True, url


def notify(title: str, body: str, grokbot: bool = True) -> dict:
    """Both channels. Always returns a report; never raises.

    The toast is the channel that carries the question, so it is attempted
    first and its result is the one that decides whether the notification
    happened. `grokbot` raising the app is a bonus: it is useful when you are at
    the desk and useless when you are on a phone, which is why the toast is not
    treated as a fallback.

    WHY THE TRY/EXCEPT IS HERE AND NOT ONLY IN THE CALLER. This function's
    docstring claimed it never raised while it called `notify_toast` with no
    guard, and a mutation-free unit test caught it: raising a fake that threw
    `RuntimeError` propagated straight through. `session_close.py` also wraps the
    call, which is why the bug never reached a session - but two callers do not
    make a documented guarantee true, and the next caller would inherit it. The
    guarantee is enforced here now.
    """
    try:
        toast_ok, toast_detail = notify_toast(title, body)
    except Exception as e:
        toast_ok, toast_detail = False, f"{type(e).__name__}: {e}"
    try:
        installed = grokbot_installed()
    except Exception as e:
        installed, toast_detail = False, f"{toast_detail} (registry: {type(e).__name__})"
    report = {
        "title": title,
        "body": body,
        "toast": {"ok": toast_ok, "detail": toast_detail},
        "grokbot": {"ok": False, "detail": "not attempted"},
        "grokbot_installed": installed,
        "channel_that_carries_the_question": "toast" if toast_ok else "none",
    }
    if grokbot and installed:
        try:
            report["grokbot"] = dict(zip(("ok", "detail"), notify_grokbot("open")))
        except Exception as e:
            report["grokbot"] = {"ok": False, "detail": f"{type(e).__name__}: {e}"}
    elif grokbot:
        report["grokbot"]["detail"] = "grokbot:// scheme not registered on this host"
    return report


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Raise a desktop notification, optionally raising Grok Bot too.")
    ap.add_argument("--title", default="HomeWorld")
    ap.add_argument("--body", default="")
    ap.add_argument("--no-grokbot", action="store_true",
                    help="toast only; do not raise the Grok Bot window")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if not args.body:
        print("nothing to say: --body is empty", file=sys.stderr)
        return 2

    report = notify(args.title, args.body, grokbot=not args.no_grokbot)
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"toast   : {'ok' if report['toast']['ok'] else 'FAILED'} "
              f"({report['toast']['detail']})")
        print(f"grokbot : {'ok' if report['grokbot']['ok'] else 'skipped'} "
              f"({report['grokbot']['detail']})")
        print(f"carries the question: {report['channel_that_carries_the_question']}")
    # 0 when at least one channel worked. A notification that could not be
    # delivered is worth a non-zero exit so a caller can notice, but a missing
    # Grok Bot is not an error - it is a host without that app.
    return 0 if report["toast"]["ok"] or report["grokbot"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())