#!/usr/bin/env bash
# HR2-B: verify DevEnvTemplate gitlink matches documented pin; ensure checkout is usable.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PIN_FILE="config/devenv-template-pin.json"
if [ ! -f "$PIN_FILE" ]; then
  echo "::error::Missing pin registry: $PIN_FILE"
  exit 1
fi

DOCUMENTED_SHA="$(python3 -c "import json; print(json.load(open('$PIN_FILE'))['sha'])")"
DOCUMENTED_SHORT="$(python3 -c "import json; print(json.load(open('$PIN_FILE'))['shortSha'])")"

GITLINK_SHA="$(git ls-tree HEAD DevEnvTemplate | awk '{print $3}')"
if [ -z "$GITLINK_SHA" ]; then
  echo "::error::DevEnvTemplate gitlink not found at HEAD"
  exit 1
fi

if [ "$GITLINK_SHA" != "$DOCUMENTED_SHA" ]; then
  echo "::error::Gitlink SHA ($GITLINK_SHA) != documented pin ($DOCUMENTED_SHA)"
  echo "Update $PIN_FILE and docs/Setup/CURSOR_DEV.md (and Docs/13b if present) when bumping the submodule."
  exit 1
fi
echo "Gitlink matches documented pin: $DOCUMENTED_SHORT ($DOCUMENTED_SHA)"

# CURSOR_DEV must cite the full SHA (pin hygiene)
if ! grep -q "$DOCUMENTED_SHA" docs/Setup/CURSOR_DEV.md; then
  echo "::error::docs/Setup/CURSOR_DEV.md missing full pin SHA $DOCUMENTED_SHA"
  exit 1
fi
echo "CURSOR_DEV.md cites documented pin"

# Cold clone: submodule dir may be empty until init
if [ ! -f DevEnvTemplate/package.json ]; then
  echo "DevEnvTemplate/ empty — running submodule init (cold-clone path)"
  git submodule update --init --recursive DevEnvTemplate
fi

if [ ! -f DevEnvTemplate/package.json ]; then
  echo "::error::DevEnvTemplate/ still empty after submodule init"
  exit 1
fi

CHECKED_OUT="$(git -C DevEnvTemplate rev-parse HEAD)"
if [ "$CHECKED_OUT" != "$DOCUMENTED_SHA" ]; then
  echo "::error::Checked-out submodule ($CHECKED_OUT) != documented pin ($DOCUMENTED_SHA)"
  exit 1
fi
echo "Submodule checkout matches pin: $CHECKED_OUT"

if [ ! -f DevEnvTemplate/dist/scripts/doctor/cli.js ]; then
  echo "::warning::Doctor CLI not built yet (run npm run doctor:build locally)"
else
  echo "Doctor CLI present: DevEnvTemplate/dist/scripts/doctor/cli.js"
fi

echo "DevEnvTemplate submodule verification OK"
