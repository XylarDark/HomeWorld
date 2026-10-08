# T0 shape plan

Lead lock, 2026-10-07. Shape only. No meshes. No prove. Open when placing the wake yard.

## This chat can finish

1. Wake yard names and order.
2. Homestead markers for the wound, the garden slot, the rune, and the shrine.
3. Camp clearing size and its shrine waypoint.
4. The bull ride named as a verb, not a mount system.

## Wake yard

First minute: cabin, partner and child present, safe.

| Order | Actor | Job |
|---|---|---|
| 1 | `NODE_BED` | Sleep gate. Wake starts here. |
| 2 | `NPC_PARTNER` | Present at wake. Not a dialogue tree. |
| 3 | `NPC_CHILD` | Present at wake. Not a dialogue tree. |
| 4 | `NODE_GARDEN` | Plant slot reads as garden, not heal. |
| 5 | `NODE_WOUND` | Spirit wound. On the homestead. |
| 6 | `NODE_SHRINE` | Waypoint and its own activator. The rune is removed. |

The shrine does not wait on a rune. Sleep is the form change. At night the shrine can be traversed only in spirit form.

## Shrine

Twice player height. A standing stone. No meter is written. Each zone gets one of the same kind, named `NODE_SHRINE_<zone>`, and it waypoints home. The night shrine is that same kind of thing.

## Camp

Clearing is 40 m across. One shrine waypoint on that clearing. Guard sightline stays readable from outside. No HUD marker.

## Bull

T0 riding is the barn bull. One barn, one bull. Not a separate mount. The shrine waypoint carries the player and the bull home.

## Not this chat

Desktop Wake prove. Placing actors in the level. Promoting art into `Content/`. A meter for the shrine. A second portal system.

## Later locks

- `NPC_PARTNER` is taken at the camp. `NPC_CHILD` stays home.
- `NODE_SHRINE` returns home. It does not carry you to a zone. Day out is the glide. Night out is the spirit glide.
- Bull ride is field only.
- `NODE_WOUND` is seen by day and healed at night.
- Sleep is `NODE_BED` only.
