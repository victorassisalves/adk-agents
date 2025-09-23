from google.adk.agents import LlmAgent, LoopAgent
from google.adk.tools import google_search, FunctionTool
from ..tools import save_blog_post_to_file, generate_image
from pydantic import BaseModel, Field
import os
import google.auth

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

class researchOutput(BaseModel):
    references: list[str] = Field(description="List of references for the research.")
    summary: str = Field(description="Summary of the research.")
    full_text: str = Field(description="Full text of the research.")
    post_theme: str = Field(description="Theme of the blog post.")


# 1. Planning agent: creates an outline based on best practices
planning_agent = LlmAgent(
    name="planning_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are a content planner. Extract from the user the theme of the post your team is working on, the theme, language, written style, tone and, target audience. (wait user input before continuing)\n"
        "Search online the best content structure for this type of post.\n"
        "Validate with the user if the post structure is the right one.\n"
        "Produce a clear outline with section headings for a blog post and a substack content."
        "Add clearly the theme of the post as 'post_theme' in your output.\n"
    ),
    output_key="outline"
)

# 3. Research agent: uses the built‑in Google Search tool to gather facts
research_agent = LlmAgent(
    name="research_agent",
    model="gemini-2.5-flash",
    instruction=(
        "Use the google search tool to find authoritative sources about the topic {outline} post_theme. "
        "Return a short summary, the full content and, include citation links."
    ),
    tools=[google_search],
    output_key="research_notes",
)

robust_post_researcher = LoopAgent(
    name="robust_blog_researcher",
    description="A robust blog researcher that retries if it fails.",
    sub_agents=[
        research_agent
    ],
    max_iterations=3,
)

# 3. Writing agent: writes the first draft
writing_agent = LlmAgent(
    name="writing_agent",
    model="gemini-2.5-flash",
    instruction=(
        "Write a blog post following this outline: {outline}. Use the research notes from {research_notes} "
        "to support your points and include quotes with citations."
    ),
    output_key="draft"
)

# 4. Editing agent: adapts the draft to my style
editing_agent = LlmAgent(
    name="editing_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are Victor Drakentide’s. Take the draft: {draft}. "
        "Rewrite it in the first person, using simple, reflective language and a forward‑thinking tone."
    ),
    output_key="final_post"
)

# 5 agent finishes the post by saving it to a file
finishing_agent = LlmAgent(
    name="finishing_agent",
    model="gemini-2.5-flash",
    instruction=(
        "You are a blog post finisher. Take the final post: {final_post}. "
        "Save it to a markdown file named 'blog_post.md'.\n"
        "Then, return formatted post to the user on chat."
    ),
    output_key="finished",
    tools=[FunctionTool(save_blog_post_to_file)]
)

image_generator = LlmAgent(
    name="Master_Image_Generator_Agent",
    model="gemini-2.5-flash",
    description=(
        "You are an expert in generating images using generative AI.\n"
        "You use the theme {outline} post_theme to help you create detailed prompts for generating images."
    ),
    instruction=(
        "You are a helpful assistant that generates images using generative AI.\n"
        "Create a detailed prompt for generating an image that complements the blog post theme {outline} post_theme and matches the post style.\n"
        "Use the tool 'generate_image' to generate the image.\n"
        "Display the image and the finished post {final_post} inside the chat."
    ),
    tools=[generate_image],
)