# AI Agent Enthusiast

**Agent name:** AI Agent Talkative Expert  
**Model:** `gemini-2.0-flash`  
**Purpose:** Friendly conversationalist that shares news, humor, and actionable insights about AI agents.

```python
from auto_content import root_agent
```

## Behavior

- Speaks in a lively, personable tone.
- Keeps information current (the prompt injects today’s date).
- Provides practical tips about AI agents, with a sprinkle of humor.
- Uses no external tools right now; replies come straight from the model.

## Environment

Set the required variables before importing the agent:

```bash
export GOOGLE_API_KEY="..."            # Gemini API key
export GOOGLE_GENAI_USE_VERTEXAI=FALSE # set TRUE if using Vertex AI
```

## Quick Start

```bash
pip install google-adk==1.8.0
python - <<'PY'
from auto_content import root_agent
print(root_agent.run("What should a beginner know about building AI agents?"))
PY
```

## Extending the Agent

- Add tools to `root_agent.tools` for API calls or custom logic.
- Adjust the `instruction` string to tune style and guardrails.
- Switch `model` to another Gemini family model if latency/cost/quality requirements change.

## Deployment

Use the ADK CLI when you’re ready:

```bash
adk deploy agent_engine \
  --project "<your-gcp-project>" \
  --region "us-central1" \
  --staging_bucket "gs://<your-bucket>" \
  --display_name "AI Agent Talkative Expert" \
  auto-content
```

After deployment, the agent is available through the ADK agent engine API.
