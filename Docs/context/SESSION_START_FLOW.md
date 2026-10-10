# Session start flow

The door as written in `Docs/context/SESSION_START.md`. This picture is not a second door. Production is `## Pick the task`: vision Shape, then the three critical-path status lines, then one room.

```mermaid
flowchart TD
  startNode[Message] --> modeNode[Mode solo unless Co]
  modeNode --> stateNode["State: agent, decide, or do"]
  stateNode --> doorRules[DOOR_RULES]
  doorRules --> routeContext[route-context through detect state]
  routeContext --> routeIndex[ROUTE_INDEX]
  routeIndex --> taskMatch{Task row}

  taskMatch -->|What next or critical path| threeLists[Three task lists]
  taskMatch -->|Stills Tripo Meshy Mixar| artDoor[ART_ASSET_DOOR]
  taskMatch -->|Fix| knownErrors[KNOWN_ERRORS symptom only]
  taskMatch -->|Homestead route| homeRoute[HOMEWORLD_ROUTE]
  taskMatch -->|Level| levelRules[LEVEL_RULES]
  taskMatch -->|T0 or first loop| t0Lock[T0 lock and shape plan]
  taskMatch -->|Interview or boss| bossLock[BOSS_LAIR_LOCK]
  taskMatch -->|Hand back| handback[HANDBACK]
  taskMatch -->|No row| afterReads[Classify the message]

  threeLists --> nextItem[First critical path item not kept]
  nextItem --> artDoor

  knownErrors --> afterReads
  homeRoute --> afterReads
  levelRules --> afterReads
  t0Lock --> afterReads
  bossLock --> afterReads
  handback --> afterReads

  afterReads --> kind{Kind}
  kind -->|Named task| workNode[One-line plan then work]
  kind -->|Queue| queueNode[Run until decide do or second fail]
  kind -->|Unknown| oneRun[One change one run then stop]
  kind -->|Topic| clarifier[One clarifier]
  kind -->|Dream| dreamNode[Ask or draft then wait for yes]

  clarifier --> room{One room}
  room -->|Look| lookCard[FORK_LOOK]
  room -->|Play| playCard[FORK_GAMEPLAY]
  room -->|Prove| proveCard[FORK_TESTING]

  artDoor --> bibleHead[Art bible north stars only]
  bibleHead --> sittingQueue[Sitting queue status line]
  sittingQueue --> oneSitting[That sitting only]
  oneSitting --> keepReject{Keep or reject}
  keepReject -->|Keep| fileStill[File the still]
  keepReject -->|Reject| oneSitting
  fileStill --> meshReady{Stills kept}
  meshReady -->|Yes| nameTool[Name Tripo Meshy or hand mesh]
  nameTool --> mixarNode[Mixar cleans and exports]

  workNode --> closeNode[Close]
  queueNode --> closeNode
  oneRun --> closeNode
  lookCard --> closeNode
  playCard --> closeNode
  proveCard --> closeNode
  mixarNode --> closeNode

  closeNode --> drain[Finish agent work]
  drain --> askNode[Ask if an answer unblocks more]
  askNode --> humanHands{Needs hands}
  humanHands -->|Yes| nameStep[Name the next manual step]
  humanHands -->|No| doneNode[Stop]
```

Look is art and asset. Play and Prove are the other two rooms. There is no fourth craft room.
