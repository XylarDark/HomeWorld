# Rune drawing

How a shown rune is drawn. Not pathing. Not collision.

## 2026-10-17

Ask: how published games draw a shown shape, and how to keep that interaction from failing for the wrong reason.

Already covered: nothing. This file is the first entry for this body.

### Sources

- Okami: Great Brushwork. Game Design Reviews. http://gamedesignreviews.com/reviews/okami-great-brushwork/ Retrieved 2026-10-17.
- Recognizing runes drawn by user. GameDev StackExchange, Stephane Hockenhull. https://gamedev.stackexchange.com/questions/120413/recognizing-runes-drawn-by-user Retrieved 2026-10-17.

Hogwarts Legacy shows a spell path and asks the player to follow it. When that path is strict, players miss. The gestures that feel fair reduce to a few directions. Arx Fatalis is the caution named in the StackExchange thread: drawing with no guide fails too often.

### Reuse

KEEP

- Show the shape. Score a few big pieces. A heart is 10 segments for a drag, one tenth each. Ten tenths are one herb.
- The easy heart is three ordered clicks: 3 chunks, 3 chunks, then 4, so three successes are 10. A missed click ends the encounter. Chunks already earned are kept.
- Leaving a drag segment skips only that segment.
- The air heart stands upright beside the collectible and yaws to the camera. It does not pitch with the camera. The ground heart stays fixed beside the bed.

PARK

- Freehand recognition with no guide.
- A screen-only drawing mode.
