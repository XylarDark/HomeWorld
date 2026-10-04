# HomeWorld route facts

Thin project file for the three-state working route. Facts only. It is not
the tutorial tests, not the Python scripts, and not a project survey. It does
not grow as the game grows. The state definitions and detection rule live in
the agnostic route file handed over with this one, and are not restated here.

## Tutorial offer

In the do state, the tutorial on offer is the generated one at
Docs/qa/HUMAN_TUTORIAL.md, kept current by research plus ongoing guidance.
Not filled further.

## Update rule

During a development session the agent may propose one fact the three states
need. It writes that fact only into this file, and only after the developer
says yes. It does not write into the agnostic route file, and the decide
state is not that writer.

## Recorded

- The gap under the lowest cloud, down to the ground, is 5 seconds of straight glide at the standard speed, with no slowdown in that gap. That height is 25 m, from the 75 m drop over the 15 second window. It is a placeholder until human testing.
- Clouds are 6-24 m across. It is a placeholder until human testing.
- Cloud spacing is top 3-4 times the diameter, middle 1.5-2.5, and bottom 4-6. It is a placeholder until human testing.
- The cloud layer above the 25 m gap is 50 m tall, the 75 m drop minus that gap. It is a placeholder until human testing.
- Any jump has more than one spirit-blue cloud, and there is no fixed count.
- The bottom of the cloud layer is the exit, and the landing stays in the existing field.
- The wisp is a bit of the signature spirit blue on a cloud, not one of the three wisps at the spirit wound.
- You collect the wisp on the way down, it stays with you, and you hold one per dung you will mix.
- There is more than one cloud layer, and there is no fixed count of layers. That is not a split of the 50 m layer.
- The descent is a steered glide, not a new flight mode.
- Polish gate rows are red only. A row is not allowed to pass as a warning.
- Farming lives on the homestead.
- In the zones, day and night, you collect and nurture so the place provides the plants and animals the homestead needs.
- Taming for now is one small barn that holds one big bull, and the fur is what that bull sheds.
- Gathering a pile takes one from a pool of piles. There is no cooldown.
- The stage name stays polish.
- An agent decision is never settled by what the developer seems to want: name the limitation, give the real options without pre-marking a default, say plainly when the evidence points against the choice in front of you, and ask a decision with the question tool rather than as prose.
- One dung and one wisp make one spirit fertilizer.
- It is mixed at the homestead, the spirit spreads it at night, and in the morning one herb pile appears per dung, at random in the field.
- Dawn alone does not bring a pile back.
- That night flight is not the locked first flight.
- The 75 m drop is how high the island sits above the plains, so every jump off the homestead drops that.

## Left empty on purpose

- Polish-gate ids and gate-chain order: (empty)
- Map paths: (empty)
- Editor steps: (empty)
