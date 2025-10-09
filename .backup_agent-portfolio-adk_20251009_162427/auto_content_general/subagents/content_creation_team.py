import datetime
from google.adk.agents import Agent, SequentialAgent, LoopAgent
from google.adk.tools import google_search
from crewai_tools import ScrapeWebsiteTool
from google.genai import types
from ..config import (
    text_model,
    text_model_lite
)
now = datetime.datetime.now()
# CONTENT MEMORY
# V0 - Save content locally
# V1 - Save content online (RAG) Optimize

# AGENT STRUCTURE
# Sequential Agent - Content Creation Team
    # Theme research definition
    # Theme Research (Google)
    # Research Scraping (Needed?)
    # Content Structure Creation (Post and topics)
    # Loop Agent - Content Creation and Review
        # Writer Agent
        # Review Agent
    # Content Validation Agent
    # Parallel Agent - Platform Specific Text Contents
        # Create text LinkedIn
        # Web - Blog
        # (COMMING SOON) X
        # (COMMING SOON) Reddit
    # (COMMING SOON) Parallel Agent - Platform Specific Multimedia Contents
        # Instragram
        # TikTok
        # Youtube
    # Generate Content Thumbnail

theme_research_definition = Agent(
    name="theme_research_definition_agent",
    model=text_model,
    description="You are responsible for defining the content theme, the best research topic and related topics to create the best content.",
    instruction=f"""
        You are responsible for establishing the content theme research definition.
        Get the theme and get the most updated information related to generate a couple of research topics to generate the deep content for the nest agent. Get the most updated info as of {now}.
        According with the theme and topis, do the best research and content gathering. If practical, serach for more practical examples, if insightful, get more insight, more actionable, get more actions and so on. Describe your chain of thought.
    """,
    tools=[google_search],
    output_key="theme_topics"
)

content_research_agent = Agent(
    name="content_research_specialst",
    model=text_model_lite,
    description="Expert in online research. You always find the best and more credible resourses.",
    instruction=f"""
        Getting the most updated information as of today {now}. Search online the topics theme_topics created by the theme_research_definition_agent and get deep valuable and insightful content. According with the theme, do the best research and content gathering. If practical, serach for more practical examples, if insightful, get more insight, more actionable, get more actions and so on. Describe your chain of thought.
    """,
    tools=[google_search],
    output_key="content_research"
)

content_structure_agent = Agent(
    name="content_structure_creator",
    model=text_model_lite,
    description="You are responsible for creating the content structure to extract the most value from it.",
    instruction=f"""
        You are responsible for establishing the content structure to be created.
        Make sure the content will follow best practices on how to present texts to the audience. In a sequential clear structured way. To better convey the information and the message.
        It should have an engaging structure to buildup the theme until climax and conclusion.
        Use the content_research to build the structure points.
    """,
    output_key="content_structure"
)

writing_agent = Agent(
    name="content_writer_agent",
    model=text_model,
    description="You are an exert in creating in depth valueable contents that will be easy to read and generate an insane amount of value to the reader.",
    instruction=f""""
        You need to generate content based in the guideline selected, the content_structure, and the full research content_research. Follow the guideline to the letter to make sure the content follow the user need.
        Create valueable content that's easy to read and scannable.
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5, # More deterministic output
    ),
    output_key="draft"
)

review_agent = Agent(
    name="content_review_agent",
    model=text_model,
    description="You are an expert content reviewer. Your job is to be critic on the draft provided by the writing_agent.",
    instruction=f"""
        Get the draft from the writing_agent and start reviewing.
        You need to evaluate the content according with the guidelines.
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5, # More deterministic output
    ),
)

content_review_team = LoopAgent(
    name="content_writing_team",
    description="You manage a team that writes content and refine until it's great and publishable",
    max_iterations=5,
    sub_agents=[review_agent]
)

content_creation_team = SequentialAgent(
    name="content_creation_team",
    description="You are the sequential coordinator of the content creation team.",
    sub_agents=[theme_research_definition, content_research_agent, content_structure_agent, writing_agent, content_review_team]
)

# AI Agent for lead generation
# Inform, create a how-to guide, and generate leads.
# I'm Victor Assis
# Audience: Entrepreneurs, marketing professionals
# How to, very thorough, and positioning myself as an expert and reference