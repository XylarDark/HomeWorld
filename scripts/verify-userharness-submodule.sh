#!/usr/bin/env bash
# HR2-B: verify UserHarness gitlink matches documented pin; ensure checkout is usable.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PIN_FILE="Config/userharness-pin.json"
if [ ! -f "$PIN_FILE" ]; then
  echo "::error::Missing pin registry: $PIN_FILE"
  exit 1
fi

DOCUMENTED_SHA="$(python3 -c "import json; print(json.load(open('$PIN_FILE'))['sha'])")"
DOCUMENTED_SHORT="$(python3 -c "import json; print(json.load(open('$PIN_FILE'))['shortSha'])")"
DOCUMENTED_PATH="$(python3 -c "import json; print(json.load(open('$PIN_FILE')).get('path',''))")"
DOCUMENTED_REMOTE="$(python3 -c "import json; print(json.load(open('$PIN_FILE')).get('remote',''))")"
DOCUMENTED_BRANCH="$(python3 -c "import json; print(json.load(open('$PIN_FILE')).get('branch',''))")"

GITLINK_SHA="$(git ls-tree HEAD UserHarness | awk '{print $3}')"
if [ -z "$GITLINK_SHA" ]; then
  echo "::error::UserHarness gitlink not found at HEAD"
  exit 1
fi

if [ "$GITLINK_SHA" != "$DOCUMENTED_SHA" ]; then
  echo "::error::Gitlink SHA ($GITLINK_SHA) != documented pin ($DOCUMENTED_SHA)"
  echo "Update $PIN_FILE and docs/Setup/CURSOR_DEV.md (and Docs/13b if present) when bumping the submodule."
  exit 1
fi
echo "Gitlink matches documented pin: $DOCUMENTED_SHORT ($DOCUMENTED_SHA)"

# Three-name rule (Docs/handoffs/NAMING_CONTRACT.md): repo URL, path and
# productName must agree. Asserting the SHA alone is NOT enough — GitHub
# redirects renamed repos, so a stale .gitmodules URL still clones successfully
# while silently pointing at the old name. That is the redirect trap.
if [ ! -f .gitmodules ]; then
  echo "::error::.gitmodules missing but $PIN_FILE documents a submodule"
  exit 1
fi

if [ -z "$DOCUMENTED_REMOTE" ] || [ -z "$DOCUMENTED_PATH" ]; then
  echo "::error::$PIN_FILE must document both 'path' and 'remote' (three-name rule)"
  exit 1
fi

# Normalize away trailing slash and optional .git so a cosmetic difference
# cannot fail the gate while a genuine rename still does.
normalize_url() {
  printf '%s' "$1" | sed -e 's:/*$::' -e 's:\.git$::'
}

GITMOD_PATH="$(git config -f .gitmodules --get "submodule.$DOCUMENTED_PATH.path" || true)"
GITMOD_URL="$(git config -f .gitmodules --get "submodule.$DOCUMENTED_PATH.url" || true)"

if [ -z "$GITMOD_URL" ]; then
  echo "::error::.gitmodules has no submodule entry '$DOCUMENTED_PATH' (no URL)"
  exit 1
fi

if [ "$(normalize_url "$GITMOD_URL")" != "$(normalize_url "$DOCUMENTED_REMOTE")" ]; then
  echo "::error::Submodule URL mismatch"
  echo "  .gitmodules            : $GITMOD_URL"
  echo "  $PIN_FILE : $DOCUMENTED_REMOTE"
  echo "A renamed GitHub repo still clones via redirect, so a stale URL here fails"
  echo "silently rather than loudly. Update both, per NAMING_CONTRACT.md."
  exit 1
fi
echo "Submodule URL matches registry: $GITMOD_URL"

if [ -n "$GITMOD_PATH" ] && [ "$GITMOD_PATH" != "$DOCUMENTED_PATH" ]; then
  echo "::error::Submodule path mismatch: .gitmodules '$GITMOD_PATH' vs $PIN_FILE '$DOCUMENTED_PATH'"
  exit 1
fi
echo "Submodule path matches registry: $DOCUMENTED_PATH"

# PIN_SYNC_POLICY.md: never point the gitlink at DET 'main' while the registry
# documents 'master'. Class D PRs off main are the documented failure mode.
case "$DOCUMENTED_BRANCH" in
  main|master|"") ;;
  *)
    echo "::warning::$PIN_FILE documents branch '$DOCUMENTED_BRANCH' (expected master/main)"
    ;;
esac
if [ "$DOCUMENTED_BRANCH" = "main" ]; then
  echo "::error::$PIN_FILE documents branch 'main'. PIN_SYNC_POLICY forbids pointing the"
  echo "gitlink at DET 'main' — merge onto 'master' and record the master SHA instead."
  exit 1
fi

# CURSOR_DEV must cite the full SHA (pin hygiene)
if ! grep -q "$DOCUMENTED_SHA" docs/Setup/CURSOR_DEV.md; then
  echo "::error::docs/Setup/CURSOR_DEV.md missing full pin SHA $DOCUMENTED_SHA"
  exit 1
fi
echo "CURSOR_DEV.md cites documented pin"

# Cold clone: submodule dir may be empty until init
if [ ! -f UserHarness/package.json ]; then
  echo "UserHarness/ empty — running submodule init (cold-clone path)"
  git submodule update --init --recursive UserHarness
fi

if [ ! -f UserHarness/package.json ]; then
  echo "::error::UserHarness/ still empty after submodule init"
  exit 1
fi

CHECKED_OUT="$(git -C UserHarness rev-parse HEAD)"
if [ "$CHECKED_OUT" != "$DOCUMENTED_SHA" ]; then
  echo "::error::Checked-out submodule ($CHECKED_OUT) != documented pin ($DOCUMENTED_SHA)"
  exit 1
fi
echo "Submodule checkout matches pin: $CHECKED_OUT"

if [ ! -f UserHarness/dist/scripts/doctor/cli.js ]; then
  echo "::warning::Doctor CLI not built yet (run npm run doctor:build locally)"
else
  echo "Doctor CLI present: UserHarness/dist/scripts/doctor/cli.js"
fi

echo "UserHarness submodule verification OK"
