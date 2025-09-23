from google.adk.agents import SequentialAgent
from .sub_agents.sub_agents import (
    planning_agent,
    robust_post_researcher,
    # researcher_organizer,
    writing_agent,
    editing_agent,
    finishing_agent,
    image_generator
)
pipeline_agent = SequentialAgent(
    name="Content_Creation_Pipeline",
    sub_agents=[
        planning_agent,
        robust_post_researcher,
        # researcher_organizer,
        writing_agent,
        editing_agent,
        finishing_agent,
        image_generator
    ],
    description="Executes a sequence of agents to create a technical blog post."
)

# The root agent must be named `root_agent` for CLI compatibility
root_agent = pipeline_agent