# Session start flow

The door as written in `Docs/context/SESSION_START.md`, redrawn 2026-10-20. This picture is not a second door. When the two differ, the door wins.

```mermaid
flowchart TD
  msg[Message] --> mode["Mode line: solo or co, state (first match: decide, do, agent)"]
  mode --> kind0{What does it name}

  kind0 -->|Log line, screenshot, lock, or beat| playtest[Playtest reply]
  playtest --> questCheck["RunTests.ps1 -QuestCheck"]
  questCheck --> beat["FastForward row + one queue section"]
  beat --> pie["Fresh PIE on L_SizeTest, FastForward plus the words"]
  pie --> closeNode

  kind0 -->|Handoff, queue section, or file| owner[Read that owner and stop]
  owner --> afterReads

  kind0 -->|Otherwise| routeIndex[ROUTE_INDEX]
  routeIndex --> taskRow{Task row}
  taskRow -->|What next or critical path| pick[Pick the task: vision Shape, three status lines, one room]
  taskRow -->|Fix| knownErrors[KNOWN_ERRORS symptom only]
  taskRow -->|Level option, packet, or level fix| doorRules[DOOR_RULES and LEVEL_RULES]
  taskRow -->|Other row| rowOwner[The file that row names]
  taskRow -->|No row| afterReads

  pick --> room{Room}
  room -->|Look| artDoor[PHASES Now line, then ART_ASSET_DOOR]
  room -->|Play| playLock[The named lock]
  room -->|Prove| prove[The named prove]

  knownErrors --> afterReads
  doorRules --> afterReads
  rowOwner --> afterReads
  artDoor --> closeNode
  playLock --> closeNode
  prove --> closeNode

  afterReads{Kind} -->|Named task| work[One-line plan, then work]
  afterReads -->|Queue| queue[Run until decide, do, or second fail]
  afterReads -->|Unknown| oneRun[One change, one run, stop]
  afterReads -->|Topic| clarifier[One typed clarifier, then one room]
  afterReads -->|Dream| dream[Ask or draft, wait for yes]

  work --> closeNode
  queue --> closeNode
  oneRun --> closeNode
  clarifier --> closeNode
  dream --> closeNode

  closeNode[Close] --> drain[Finish agent work]
  drain --> ask[Ask if an answer unblocks more]
  ask --> hands{Needs hands}
  hands -->|Yes| nameStep[Name the next manual step]
  hands -->|No| done[Stop]
```

Look is art and asset. Play and Prove are the other two rooms. There is no fourth craft room.
