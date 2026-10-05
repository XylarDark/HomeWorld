# Cloud and glider route handoff

Provider-, model-, IDE-, and runner-agnostic handoff for a development session
that has been explicitly started by the developer. Use `Docs/context/ROUTE_START.md`
for the route handoff; this file is supporting status, not a replacement start
protocol. During discovery, do not open this handoff unless the developer names
it as an extra file.

## Current route state

Read `Docs/context/HOMEWORLD_ROUTE.md` from the current `main` commit before
using any route facts. If the checkout may be on another branch or have local
edits, inspect `git show main:Docs/context/HOMEWORLD_ROUTE.md` (or the host's
equivalent read of the named `main` revision), not the working copy. The current
route facts include a steered glide, a 15-second homestead-to-field window,
placeholders for cloud dimensions and spacing, and the existing field landing.
Treat each fact's qualification as part of the fact. Do not promote a
placeholder or conditional target to a settled value.

The route facts file is the source of truth; this handoff intentionally does not
copy its numeric details. Do not infer that a current clean working tree makes
old handoff text current.

## Scope boundary

This is preparation for a developer-named cloud and glider task. It does not
authorize choosing the design bite, accepting a taste call, or starting a build
without the required packet and human decisions. Use the project ownership and
test rules for any missing scope, feel, or acceptance bar. If no packet or next
sentence has been named, ask the developer what they want to test next; do not
invent one.

Do not use prior OpenCode-only instructions, stale commit pins, or stale claims
that route files are dirty. Provider identity is optional test metadata, never a
workflow precondition.
