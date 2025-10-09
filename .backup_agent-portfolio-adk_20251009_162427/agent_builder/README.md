# Agent Builder

A multi-agent pipeline that plans, researches, architects, implements, tests, and explains new Google ADK agents. Use this project when you want to go from a product idea to production-ready agent code with minimal manual coordination.

## Highlights
- Runs a six-stage SequentialAgent that mirrors a real software delivery lifecycle.
- Captures intermediate outputs (`project_plan`, `research_summary`, …) so later agents can build on earlier work.
- Includes stubbed tools you can swap for live integrations (documentation search, code execution, test runner).

## Workflow Overview
| Order | Agent | Responsibility | Key Output |
| --- | --- | --- | --- |
| 1 | `PlannerAgent` | Breaks the user request into a numbered delivery plan. | `project_plan` |
| 2 | `ResearcherAgent` | Queries references via `search_adk_docs` and summarizes findings. | `research_summary` |
| 3 | `ArchitectAgent` | Designs the agent topology and data flow. | `architecture_spec` |
| 4 | `DeveloperAgent` | Emits Python implementations for the designed agents. | `generated_code` |
| 5 | `TesterAgent` | Validates generated code with `run_unit_tests`. | `test_report` |
| 6 | `ExplainerAgent` | Produces a user-facing recap of the full build. | `explanation` |

`root_agent` (`AgentBuilderPipeline`) orchestrates them sequentially so each stage receives the context it needs.

## Tools
- `search_adk_docs(query)` → replace with your preferred documentation or web search endpoint.
- `execute_code(code)` → integrate with a secure sandbox when you want real execution.
- `run_unit_tests(code)` → hook this into your CI or ADK evaluation harness.

## Run It Locally
```bash
python - <<'PY'
from agent_builder import root_agent
print(root_agent.run("Design an agent that audits data privacy policies"))
PY
```

Ensure `GOOGLE_API_KEY` (or Vertex AI credentials) is exported so the underlying Gemini models can run.

## Customize
- Swap any agent’s `model` for latency/price trade-offs.
- Extend the planner or researcher with new tools (e.g., Stack Overflow search) and add their return payloads to later instructions.
- Add optional branches by wrapping sub-lists in `ParallelAgent` or `LoopAgent` before or after the sequential pipeline.
