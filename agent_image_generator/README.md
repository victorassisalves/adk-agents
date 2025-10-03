# Agent Image Generator

Generates production-ready visual assets from natural language prompts. The root agent (`Master_Image_Prompt_Generator_Agent`) collaborates with an execution agent that calls the Gemini image model and returns both rendered images and descriptive text.

## How It Works
1. The root agent receives the user's creative brief and forwards it to the `Master_Image_Generator_Agent`.
2. `Master_Image_Generator_Agent` calls the async `generate_image` tool, which invokes `gemini-2.5-flash-image-preview`.
3. Artifacts are stored via the ADK artifact service and the chat response includes download handles plus any textual narration from the model.

## Agent Responsibilities
| Agent | Role | Notes |
| --- | --- | --- |
| `Master_Image_Prompt_Generator_Agent` (`root_agent`) | Captures prompt details and relays them downstream. | Set `output_key="image_details"` for caller reuse. |
| `Master_Image_Generator_Agent` | Uses the provided brief, optionally including a seed image path, to render assets. | Returns `generated_images` + `text_response`. |

## Tooling
- `generate_image(prompt, tool_context, filename_prefix)` uploads the resulting inline data as versioned artifacts and reports friendly filenames back to the user.
- Uses the default Gemini client; ensure `GOOGLE_API_KEY` or Vertex AI credentials are exported before invoking the agent.

## Quick Start
```bash
python - <<'PY'
from agent_image_generator.agent import root_agent
result = root_agent.run("Create neon cyberpunk cover art featuring a violinist under rain")
print(result.output["image_details"])
PY
```
The returned payload lists artifact handles such as `generated_image_0.png@v1` that ADK front-ends can render inline.

## Customize
- Add prompt engineering logic in the root agent before delegating to the generator for richer control.
- Accept user-supplied reference images by passing a path as the second argument when calling the tool.
- Adjust `filename_prefix` to keep artifacts organized by campaign or client.
