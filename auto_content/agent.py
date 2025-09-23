from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search
from pydantic import BaseModel, Field

class researchOutput(BaseModel):
    references: list[str] = Field(description="List of references for the research.")
    summary: str = Field(description="Summary of the research.")
    full_text: str = Field(description="Full text of the research.")

# 1. Research agent: uses the built‑in Google Search tool to gather facts
research_agent = LlmAgent(
    name="ResearchAgent",
    model="gemini-2.5-flash",
    instruction=(
        "Use the google search tool to find authoritative sources about the topic. "
        "Return a short summary and include citation links."
    ),
    tools=[google_search],
    output_key="research_notes",
    output_schema=researchOutput
)

# 2. Planning agent: creates an outline based on the research
planning_agent = LlmAgent(
    name="PlanningAgent",
    model="gemini-2.5-flash",
    instruction=(
        "You are a content planner. Read the research notes from {research_notes} and "
        "produce a clear outline with section headings for a blog post and a substack content."
    ),
    output_key="outline"
)

# 3. Writing agent: writes the first draft
writing_agent = LlmAgent(
    name="WritingAgent",
    model="gemini-2.5-flash",
    instruction=(
        "Write a blog post following this outline: {outline}. Use the research notes from {research_notes} "
        "to support your points and include quotes with citations."
    ),
    output_key="draft"
)

# 4. Editing agent: adapts the draft to my style
editing_agent = LlmAgent(
    name="EditingAgent",
    model="gemini-2.5-flash",
    instruction=(
        "You are Victor Drakentide’s. Take the draft: {draft}. "
        "Rewrite it in the first person, using simple, reflective language and a forward‑thinking tone."
    ),
    output_key="final_post"
)

# 5. Design agent (custom): generates a thumbnail or selects an image
from google.adk.agents import BaseAgent

class DesignAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="DesignAgent", description="Creates a thumbnail image")

    async def run_async(self, context):
        # In a real implementation, call an image API or tool here.
        # For demonstration, we just return a placeholder path.
        image_path = "/path/to/thumbnail.jpg"
        context.state["thumbnail"] = image_path
        return image_path

design_agent = DesignAgent()

pipeline_agent = SequentialAgent(
    name="ContentPipelineAgent",
    sub_agents=[
        research_agent,
        planning_agent,
        writing_agent,
        editing_agent,
        design_agent
    ],
    description="Generates a researched, structured and styled blog post with an image"
)

# The root agent must be named `root_agent` for CLI compatibility
root_agent = pipeline_agent