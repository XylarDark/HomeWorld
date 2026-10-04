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

## Left empty on purpose

- Polish-gate ids and gate-chain order: (empty)
- Map paths: (empty)
- Editor steps: (empty)
