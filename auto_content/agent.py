
from google.adk.agents import SequentialAgent, LlmAgent
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
        writing_agent,
        editing_agent,
        finishing_agent,
        image_generator
    ],
    description="Executes a sequence of agents to create a technical blog post."

)

post_theme_extractor = LlmAgent(
    model="gemini-2.5-flash",
    name="Post_Theme_Extractor",
    description="""An agent that will get the theme for a blog post from the user and suggest a post structures to the end user. Accepting user feedback.""",
    instruction="""
        1. Ask the user for the theme of the blog post.
        2. Suggest a blog post tone, writing style, language, size, audiences and other relevant information based on the theme.
        3. Ask the user for feedback and adjust the suggestions accordingly.
        4. Once the user is satisfied with the suggestions, output the final theme and structure.
        5. Call the pipeline agent to start the blog post creation process.
        6. On the writing agent, the user needs to approve the editing draft before moving to the next step.
        7. Return the final blog post and generated image to the user.
    """,
    output_key="post_theme",
    sub_agents=[pipeline_agent]
)

# The root agent must be named `root_agent` for CLI compatibility
root_agent = post_theme_extractor