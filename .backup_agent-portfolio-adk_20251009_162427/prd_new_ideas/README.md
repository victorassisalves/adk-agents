# PRD New Ideas Workspace

Generates end-to-end Product Requirement Documents (PRDs) by orchestrating a guild of specialized product management agents. The system interviews stakeholders, commissions focused research, synthesizes findings, and ships a polished PRD ready for review.

## System Goals
- Refine ambiguous business ideas into a clear, validated product vision.
- Delegate market, user, and technology research to dedicated ADK agents with live search capabilities.
- Synthesize research into a unified discovery brief and persist the final PRD to disk.

## Architecture Snapshot
```
root_agent ("prd_new_ideas")
  └─ overall_workflow (SequentialAgent)
       ├─ research_and_dicovery_team (ParallelAgent)
       │    ├─ market_and_competitive_analysis → `market_research`
       │    ├─ persona_researcher             → `persona_research`
       │    └─ technology_researcher          → `tech_research`
       └─ synthesizer                         → `combined_reasearch` + PRD file
```
A standalone `product_reseacher` agent (with `AgentTool` wrapper) is also available when you want bespoke deep dives outside the core workflow—simply add it to the root agent’s `tools` list.

## Agent Lineup
- **Root Product Manager (`prd_new_ideas`)** – Interviews the user, shapes the product framing, and coordinates the workflow.
- **Market & Competitive Analyst** – Uses `google_search` to benchmark competitors, surface market trends, and size the opportunity.
- **Persona Researcher** – Distills likely personas, goals, and pain points from qualitative signals.
- **Technology Researcher** – Evaluates enabling tech stacks with emphasis on Flutter/FlutterFlow feasibility and backend considerations.
- **Research & Discovery Team** – A `ParallelAgent` that runs the three research tracks simultaneously for speed.
- **Synthesizer** – Combines `{persona_research}`, `{tech_research}`, and `{market_research}` into a cohesive narrative and writes the Markdown artifact through `save_prd_file`.

## Tools & Outputs
- `google_search` (ADK) keeps each research track current as of run time.
- `save_prd_file(file_name, content)` stores Markdown files under `prd_new_ideas/prds/` using the PRD title.
- The sequential workflow exposes `combined_reasearch` for downstream consumption (e.g., presentation agents).

## Usage
```bash
python - <<'PY'
from prd_new_ideas.agent import root_agent
response = root_agent.run("Help me scope an AI-powered virtual sales tax analyst for SMBs")
print(response.output["combined_reasearch"])
PY
```
Generated PRDs are saved alongside the chat in `prd_new_ideas/prds/PRD_<Title>.md`.

## Extending the Workspace
1. Add compliance, UX, or analytics sub-agents by appending to `research_and_dicovery_team.sub_agents`.
2. Register new output keys in the synthesizer instruction and template the final PRD accordingly.
3. Wire `product_reseacher_tool` into the root agent’s `tools` list when you need ad-hoc research on user demand before kicking off the main workflow.
