# Marketplace policy V1 (ProveOps B)

**Status:** ACTIVE  
**Owner:** Conductor proposes · Lead gates (`APPROVE TOOL SCOUT|BUILD`)  
**Tip measured:** HW `9b2747a` · pin HOLD `8c4442a`  
**Cite:** EXIT `MARKETPLACE_SCOUT_V1` · `swarm/SWARM_OPS.md` §14 · `docs/guides/mcp-hygiene.md` · `Docs/handoffs/U58F_F_MCP_DECISION.md` · `.cursor/mcp.json.example` · Co ops Marketplace row

Research and docs bites **do not install**. Live plugin/MCP start waits for a later Lead `APPROVE TOOL BUILD …` Act after `ACCEPT EXIT` + matching SCOUT string. Co seats must not self-install.

---

## Ban

- Install during Research (`/add-plugin`, plugin UI, OAuth click-ops by a seat)
- DESKTOP MCP trial as Research (new server, port, helper daemon)
- Duplicate memory plugins while file + Co memory exist
- Growing live `.cursor/mcp.json` or checking in secrets
- Treating GitHub Contents API as Editor/Python/DESKTOP
- Folding CAP-002 / EA Implement / pin bump into a scout

---

## Scout bar (SCOUT vs BUILD vs REJECT)

| Gate | Lead types | Evidence | Fail |
|------|------------|----------|------|
| **KEEP** | none | Path exists on tip (CE rule, pstack preference, UnrealMCP/Lab examples, §14) | Re-opening KEEP as a new plugin |
| **SCOUT** | `APPROVE TOOL SCOUT <Family> (<scope>; no mcp.json until BUILD)` | Named gap CE+pstack+files+UnrealMCP+Lab cannot cover; one host column; publisher + pin; dual-server empty; Context7/Linear need Phase Research one-pager; hygiene § Review | “Catalog looked useful”; wrong host; memory plugin; CAP/EA product |
| **BUILD** | `APPROVE TOOL BUILD <Family> (<pinned command; hygiene diff; host=…>)` | SCOUT already typed + ACCEPT evidence + version pin + example-only snippet | BUILD without SCOUT; live `mcp.json` in same Do as docs |
| **REJECT** | none (or `REJECT TOOL <Family>`) | Sprawl / wrong host / CAP theater / duplicate / dual MCP | Seats installing anyway |

**One line:** if CE + pstack + file memory + UnrealMCP (DESKTOP parent) + Lab Blender + Contents API degrade already cover the job → KEEP or REJECT — never a new row.

---

## Decision table

| Family | Rank | Lead string (if any) | Why |
|--------|------|----------------------|-----|
| Compound Engineering (EveryInc) | **KEEP** | — | Preferred installed skills |
| pstack | **KEEP** | — | Co ops preferred second row |
| UnrealMCP + sidecar (55557) | **KEEP** | — | U58F-F; DESKTOP parent only |
| Blender Lab MCP | **KEEP** | — | Official protocol; example stamped |
| GitHub Contents API | **KEEP** | — | §14 degrade; not a plugin |
| File / Co memory | **KEEP** | — | Only legal shared memory |
| MCP hygiene + mcp.json.**example** | **KEEP** | — | Review-as-code; example ≠ live growth |
| Context7 | **CANDIDATE** | `APPROVE TOOL SCOUT Context7 MCP (docs lookup only; no mcp.json until BUILD)` | Phase Research + Lead first |
| Linear | **CANDIDATE** | `APPROVE TOOL SCOUT Linear MCP (issues read; no mcp.json until BUILD)` | Phase Research + Lead first |
| Memory plugins (mem0…) | **REJECT** / **DUPLICATE** | — | Skip per Co ops |
| Epic ModelContextProtocol dual | **REJECT** | — | Never dual with UnrealMCP |
| Catalog sprawl (Composio, Playwright MCP, …) | **REJECT** | — | No named gap |
| New live mcp.json / new MCP processes | **REJECT** until BUILD | — | Hygiene + §14 |
| DESKTOP helper daemons as Research | **REJECT** | — | §14 ban |
| CAP-002 product Do | **PARK (#9)** | — | Do HELD |
| EA SCOUT | **PARK** | — | Only if Lead names bite |
| Pin / alwaysApply / AGENTS dump | **REJECT** | — | Pin stays `8c4442a` |

**Post-ACCEPT install gate:** after Conductor ACCEPT + Lead types the SCOUT string, a **separate** Act may request `APPROVE TOOL BUILD <Family> (…)`. Install / live mcp.json / OAuth / daemon start wait for **that** BUILD string.

---

## Fitness greps (before ACCEPT of any later tool Act)

```bash
# Policy names the two Lead-gated families and forbids install-without-gate
grep -nE 'APPROVE TOOL SCOUT|APPROVE TOOL BUILD' Docs/handoffs/MARKETPLACE_POLICY_V1.md
grep -nEi 'install without|no mcp.json until BUILD|Co seats must not self-install' Docs/handoffs/MARKETPLACE_POLICY_V1.md

# Live install artifacts must stay absent from a docs-only PR
git diff --name-only | grep -E '(^|/)mcp\.json$|Setup-MCP\.bat|Plugins/UnrealMCP' && echo FAIL live MCP surface

# Pin / A–E blob unchanged
python3 -c "import json; print(json.load(open('Config/userharness-pin.json'))['sha'])" | grep -q 8c4442a
git hash-object .agents/skills-extras/architecture-trade-offs-design-depth/SKILL.md | grep -q 107a5118c95c1bf0b1b3d1755796632bff41b535
```
