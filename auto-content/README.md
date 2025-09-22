# Agent Portfolio (Google ADK)

This repository collects lightweight demos for agents built with the Google Agent Developer Kit (ADK).  
Each agent lives in its own folder and exposes a `root_agent` object that can be deployed with the ADK CLI or imported into other apps.

## Repository Structure

```
auto-content/     # AI Agent Talkative Expert (demo agent definition)
env.example       # Copy to .env and fill in credentials
```

## Prerequisites

- Python 3.10 – 3.12
- A Google Generative AI API key with Gemini access
- `pip` or another Python package manager

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install google-adk
```

Copy environment variables and fill them in:

```bash
cp env.example .env
# set GOOGLE_API_KEY=...
# set GOOGLE_GENAI_USE_VERTEXAI=FALSE  # or TRUE if you use Vertex AI
```

Export the variables before running anything:

```bash
export $(grep -v '^#' .env | xargs)               # macOS/Linux
set -a; source .env; set +a                       # alternative shell-safe form
```

## Running the Demo Agent

You can exercise the agent locally with a quick Python snippet:

```bash
adk web
from auto_content import root_agent
response = root_agent.run("Give me a fun fact about AI agent frameworks.")
print(response)
PY
```

To deploy with the ADK CLI:

```bash
adk deploy agent_engine \
  --project "<your-gcp-project>" \
  --region "us-central1" \
  --staging_bucket "gs://<your-bucket>" \
  --display_name "Agent Portfolio Demo" \
  auto-content
```

## Development Notes

- Keep each agent self-contained (its own dependencies, doc, README).
- Wrap new agent folders with an `__init__.py` that re-exports `root_agent`.
- Add sample conversations or test scripts where helpful.
