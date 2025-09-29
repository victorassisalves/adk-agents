import datetime
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
import os
import google.auth

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_REGION", "us-central1")

audio_model_native_audio = "gemini-live-2.5-flash-preview-native-audio"
audio_model = "gemini-live-2.5-flash-preview"
text_model_lite = "gemini-2.5-flash-lite"
text_model = "gemini-2.5-flash"
image_model = "gemini-2.5-flash-image-preview"
now = datetime.datetime.now()

podcast_theme_researcher = LlmAgent(
    name="Podcast_Theme_Researcher_Agent",
    model=text_model,
    description=(
        "You are an expert in researching podcast themes and topics using online search tools."
    ),
    instruction=f"You are a helpful assistant that researches deep and relevant information about a theme using the most updated content as of today {now}. Use the google_search tool to gather information about the podcast theme provided by the user. Summarize your findings and provide a list of references.\n",
    tools=[google_search],
    output_key="research_details",
)

podcast_script_creator = Agent(
    name="Podcast_Script_Creator_Agent",
    model=text_model,
    description=(
        "You are an expert in creating engaging podcast episodes based on researched themes and topics."
    ),
    instruction=(
        "You are a helpful assistant that creates engaging podcast episodes based on researched themes and topics. Use the research details provided by the Podcast_Theme_Researcher_Agent {research_details} to create a compelling podcast script. Ensure the script is well-structured, informative, and engaging for listeners.\n"
    ),
    output_key="podcast_script",
)

root_agent = Agent(
    name="Podcast_Creation_Agent",
    model=text_model,
    description=(
        "You are an expert in creating podcasts from theme research to script writing."
    ),
    instruction=(
        "You are a helpful assistant that creates podcasts from theme research to script writing. First, use the Podcast_Theme_Researcher_Agent to research the podcast theme provided by the user. Then, use the Podcast_Script_Creator_Agent to create a compelling podcast script based on the research findings. Ensure the final podcast script is well-structured, informative, and engaging for listeners.\n"
    ),
    sub_agents=[podcast_theme_researcher, podcast_script_creator],
    output_key="podcast",
)