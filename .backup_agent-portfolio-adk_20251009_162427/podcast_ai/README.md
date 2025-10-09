# Podcast AI Lab

Researches podcast themes and drafts episode scripts using Gemini models and the Google ADK orchestration framework. Point it at a topic and receive concise research notes plus a ready-to-record narrative.

## Flow
1. `Podcast_Theme_Researcher_Agent` queries the latest sources with `google_search`, summarizes the opportunity, and surfaces references (`research_details`).
2. `Podcast_Script_Creator_Agent` turns those findings into a structured episode script (`podcast_script`).
3. `root_agent` (`podcast_ai`) orchestrates the process so users can request an episode in a single call, while still giving direct access to each specialized agent if you want to reuse them elsewhere.

> Note: In this repo the root agent explicitly lists the researcher as a sub-agent; invoke `podcast_script_creator` manually or chain the agents in your runner if you want script generation as part of the default pass.

## Models & Environment
All agents use Gemini via `LiteLlm` wrappers. Export a valid `GOOGLE_API_KEY` (or set Vertex AI defaults) before running:
```bash
export GOOGLE_API_KEY="..."
```

## Quick Start
```bash
python - <<'PY'
from podcast_ai.agent import root_agent, podcast_script_creator
session = root_agent.run("Create an episode about cities building digital twins")
print(session.output["research_details"])
print(podcast_script_creator.run(context=session.output).output["podcast_script"])
PY
```

## Customize
- Swap the research model to `gemini-2.5-flash-lite` when latency matters more than depth.
- Expand `podcast_script_creator.instruction` to include host persona beats, ad breaks, or interview sections.
- Compose additional agents (e.g., audio narration, show notes writer) and add them to the `sub_agents` list for a complete production stack.
