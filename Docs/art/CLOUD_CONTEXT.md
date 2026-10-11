# Cloud context

Playtest context for the descent clouds. Meters and spacing stay in `Docs/context/HOMEWORLD_ROUTE.md`. The kept wisp-cloud picture is `Docs/art/field/SM_Cloud_Wisp_sheet.jpg`.

## Two clouds

Developer design, 2026-10-11. Clouds are not the rugged facet look.

- Ambient. Not collected. Well-defined and fluffy, with fog. No kept picture yet.
- Wisp cloud. Larger and easier to read. A gap shows a bright wisp inside. The kept picture uses cyan. The cloud can take a wisp color.

The wisp on a cloud is the descent collect. It is not one of the three wisps at the spirit wound.

## How games usually build them

The playtest mesh is one solid sample. The other methods are the later choices.

- Painted sky or a skydome. Cheap, and good for clouds the player never enters. Horizon’s earlier games used domes and cards for a fixed time of day, then moved to a raymarched volume so the sky could change. That talk is Schneider, “The Real-time Volumetric Cloudscapes of Horizon: Zero Dawn” (SIGGRAPH 2015).
- Billboard cards. One card per cloud in older flight games, or a handful of cards, or many small particles. Artist-placed cards stay directable. A stylized sky in Unreal is usually cards or a mesh, because a volume is costly and hard to keep fluffy-on-purpose.
- A mesh, sometimes with cards stuck on it. Painterly stylized clouds are often a base mesh plus planes. That is the family of this sample.
- A volume, raymarched. Right for a huge changing sky. Wrong for the first playtest, where one cloud has to read as “the wisp is in this one.”

Ambient fog can be a fog volume around a mesh. It does not have to be the same mesh as the wisp cloud.

## Sample size

The route placeholder is 36–144 m across. `AHomeWorldCloudField` defaults to 72 m and clamps to that same range. At the 30 m/s glide, 72 m is about two and a half seconds inside the cloud, long enough to see the wisp and short enough that the 300 m layer can hold more than one. The sample mesh uses that 72 m. It is the field default, not a new lock.
