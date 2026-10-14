# L_Field context

Open with `Docs/context/SCENE_SETUP.md` before moving this map. Placement numbers are in `Docs/level/L_Field_METRICS.md`. `Content/Python/place_field_greybox.py` applies that file. `Content/Python/verify_field_greybox.py` measures it and does not save.

Map: `/Game/HomeWorld/Maps/Field/L_Field`.

## What this mass is

Texture-off greybox of the field zone in `Lib/02_Zones/gather/FIELD.json`. The arrival is the meadow centre. There is no path and no landing ring. The north lip is three cliff faces and a lower shelf. The east edge is the river channel. The south and west edges are one pine sequence, so they read the same from inside the meadow. Herb centres follow the scatter rule on the sheet. The camp is not in this zone.

A few pines stand in the meadow, far apart. Bulls match the herb-centre count. Half stand beside a herb. Not in this mass: beast pads, a landing circle, a path, clouds, and the camp. The authored module offsets in the zone file are the old field and are not placed. The plain under `L_SizeTest` is not this zone.

## Pass

`field_greybox: CHECK PASS` and `field_greybox: forests identical` from `Content/Python/verify_field_greybox.py`, in the open editor, after the save.
