# HomeWorld route facts

Thin project file for the three-state working route. Facts only. It is not
the tutorial tests, not the Python scripts, and not a project survey. It does
not grow as the game grows. The state definitions and detection rule live in
the agnostic route file handed over with this one, and are not restated here.

## Tutorial offer

In the do state, the generated tutorial at Docs/qa/HUMAN_TUTORIAL.md is offered
only once it is committed and its check passes; until then, name the next
manual step in one line.
Not filled further.

## Update rule

One fact proposed at a time, one yes from Luke, one write into this file only — the rule itself lives in route-context `## Updating facts`, not restated here.

## Recorded

- The gap under the lowest cloud, down to the ground, is 150 m, which is 10 seconds of straight glide at the 15 m/s sink that keeps the 450 m drop at 30 seconds to ground, with no slowdown in that gap. It is a placeholder until human testing. (6× world-scale pass, Lead 2026-10-07.)
- Clouds are 36-144 m across. It is a placeholder until human testing. (6× pass 2026-10-07.)
- Cloud spacing is top 3-4 times the diameter, middle 1.5-2.5, and bottom 4-6. It is a placeholder until human testing. (Ratios unchanged by the 6× pass.)
- The cloud layer above the 150 m gap is 300 m tall, the 450 m drop minus that gap. It is a placeholder until human testing. (6× pass 2026-10-07.)
- Any jump has more than one spirit-blue cloud, and there is no fixed count.
- The bottom of the cloud layer is the exit, and the landing stays in the existing field.
- The wisp is a bit of the signature spirit blue on a cloud, not one of the three wisps at the spirit wound.
- You collect the wisp on the way down, it stays with you, and you hold one per dung you will mix.
- There is more than one cloud layer, and there is no fixed count of layers. That is not a split of the 300 m layer. (×6 world-scale pass 2026-10-07.)
- Steering is unrestricted by rails, corridors, or artificial bounds throughout the descent. It remains a glider descent, not a new flight mode.
- Lead 2026-10-07 scale change: the WORLD grows by about **6×** — island, field,
  camp, descent space. Props, characters, and trigger radii stay human-scale.
  bulls rideable: bull max speed = **3× player sprint**, fast in a single
  direction, hard to turn at max speed, must slow down for better turning.
  (All size rows in `WORLD_METRICS.md` carry the old scale; they need a
  re-derivation pass before use.)
- Farming lives on the homestead.
- In the zones, day and night, you collect and nurture so the place provides the plants and animals the homestead needs.
- Taming for now is one small barn that holds one big bull, and the fur is what that bull sheds.
- Lead 2026-10-07: a bull boots you back to the homestead on a charge if you get
  too close or fill its threat meter without leaving its area. Walking toward it
  carrying an herb suppresses the boot; sudden movement builds threat, standing
  still lets it approach, eat the herb, and it is tamed. Tamed, the bull is
  rideable, and the rune stone transports you and the bull to the homestead as a
  pet. Bull turning is like a real animal (Lead 2026-10-07): turn rate is
  inversely related to travel speed — near-zero turn authority at 3× sprint,
  full turn authority at walking or stopped speed. The player steers by managing
  momentum, not by steering at speed. Homestead herbs are few (morning tea, tending wounded spirits); the same
  plant/nurture/collect mechanic runs uncapped in the field for other uses later
  (e.g. feeding collected bulls).
- Gathering a pile takes one from a pool of piles. There is no cooldown.
- The stage name stays polish.
- An agent decision is never settled by what the developer seems to want: name the limitation, give the real options with one recommended pick marked, say plainly when the evidence points against the choice in front of you, and ask a decision with the question tool rather than as prose.
- Lead 2026-10-07: the three wound wisps, once healed, each become a spirit
  companion that follows the player (Ni No Kuni style) rather than staying a
  soft-emissive prop in place. The heal verb's result is a following wisp.
- Lead 2026-10-07 field-scatter rule (×6 pass): no clustering, no grid; a common herb node is ~30 m from its nearest kind; 25% of that density is dual herbs (2 nodes, 1 m apart); 5% of that density is triple herbs (3 nodes, 1 m apart between them). Clump counts grow with the 420×420 field (was 70×70); the 5 m min-separation and same-type-adjacent bans are superseded.
- One dung and one wisp make one spirit fertilizer.
- Lead 2026-10-07 (revises the line above's spread agent): the herbs have their
  own use — the kettle, tea, and the day sprint buff. Dung + wisp is what the
  spirit carries. Herbs collected, combined with a wisp from a cloud, are *given
  to the spirit wisps*; the payoff for those given wisps is the spirit flight
  buff at night. The player uses that night flight buff to disperse dung + wisp
  over the herb sites in the field. The homestead-fertilizer morning-pile line
  above is superseded: spreading is a spirit-flight verb of the player, not an
  automatic homestead morning spawn.
- It is mixed at the homestead, the spirit spreads it at night, and in the morning one herb pile appears per dung, at random in the field.
- Dawn alone does not bring a pile back.
- That night flight is not the locked first flight.
- The 450 m drop is how high the island sits above the plains, so every jump off the homestead drops that. (6× pass 2026-10-07.)
- The 1560 m line is the plains edge on that straight glide only. (6× pass.)
- Other directions have no edge.
- A cloud ring does not draw that line around the island.
- Height is one and a half times the first jump's 450 m drop. It is a placeholder until human testing.
- Neutral glide speed is two thirds of the first jump's neutral glide speed. It is a placeholder until human testing.
- No meter height is written for the night flight.

- Lead 2026-10-07: the art bible owns how the island top looks. This file owns the meters. A look change does not move the drop. A route change does not pick the materials.
- Lead 2026-10-07: T0 riding is the barn bull. It is not a separate mount.

- Lead 2026-10-07: the rune is removed. Each zone has a shrine, and that shrine is the waypoint home and its own activator. The night shrine and the zone shrine are the same kind of thing.

- Lead 2026-10-07: sleep is the form change. It is what lets the player become spirit. At night the shrine can be traversed only in spirit form.

## Left empty on purpose

- Polish-gate ids and gate-chain order: (empty)
- Map paths: (empty)
- Editor steps: (empty)
