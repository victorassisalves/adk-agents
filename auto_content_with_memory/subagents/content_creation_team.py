from google.adk.agents import Agent, SequentialAgent, LoopAgent
from google.adk.tools import google_search
from crewai_tools import ScrapeWebsiteTool
from ..config import (
    text_model,
    text_model_lite
)


content_creation_team = SequentialAgent(

)
# CONTENT MEMORY
# V0 - Save content locally
# V1 - Save content online (RAG) Optimize

content_structure_agent = Agent(
    name="content_structure_creator",
    model=text_model_lite,
    description="You are responsible for creating the content structure to extract the most value from it."
)