import datetime
from google.adk.agents import Agent, SequentialAgent, LoopAgent
from google.adk.tools import google_search
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from ..tools.tools import (
  generate_image
)
from ..config import (
    text_model,
    text_model_lite
)
# from crewai_tools import ScrapeWebsiteTool
now = datetime.datetime.now()

DRAFT = ""
# --- Tool Definition ---
def exit_loop(tool_context: ToolContext):
  """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
  print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
  tool_context.actions.escalate = True
  # Return empty dict as tools should typically return JSON-serializable output
  return {}
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
        When necessary, dive deep into technical aspects. Explain the 'how' and 'why' behind the content.
        If you think more info is necessary to write, use the google_search tool.
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5, # More deterministic output
    ),
    tools=[google_search],
    output_key=DRAFT
)

review_agent = Agent(
    name="content_review_agent",
    model=text_model_lite,
    description="You are an expert content reviewer. Your job is to be critic on the draft provided by the writing_agent.",
    instruction=f"""
        Get the draft from the writing_agent and start reviewing.
        You need to evaluate the content according with the guidelines. to make sure the content have high upstanding value.
        The content fufill it's purpose and will be the best way to deliver the message and achieve the goal.
        **Task:**
            Review the ```{DRAFT}``` for clarity, engagement, and basic coherence according to the initial topic (if known).

            IF you identify 1-2 *clear and actionable* ways the document could be improved to better capture the topic or enhance reader engagement (e.g., "Needs a stronger opening sentence", "Clarify the character's goal"):
            Provide these specific suggestions concisely. Output *only* the critique text.

            ELSE IF the document is coherent, addresses the topic adequately for its length, and has no glaring errors or obvious omissions:
            Respond *exactly* with the phrase "CONTENT APPROVED" and nothing else. It doesn't need to be perfect, just functionally complete for this stage. Avoid suggesting purely subjective stylistic preferences if the core is sound.

            Do not add explanations. Output only the critique OR the exact completion phrase.
    """,
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5, # More deterministic output
    ),
    output_key="review_suggestions"
)

edit_review = Agent(
    name="RefinerAgent",
    model=text_model,
    instruction=f"""You are a Creative Writing Assistant refining a document based on feedback OR exiting the process.
    **Current Document:**
    draft
    **Critique/Suggestions:**
    review_suggestions

    **Task:**
    Analyze the 'review_suggestions'.
    IF the critique is *exactly* "CONTENT APPROVED":
    Just handle to the next agent. Do not output any text.
    ELSE (the critique contains actionable feedback):
    Carefully apply the suggestions to improve the DRAFT. Output *only* the refined document text..
""",
    description="Refines the document based on critique, or calls exit_loop if critique indicates completion.",
    output_key=DRAFT # Overwrites state['current_document'] with the refined version
)

image_generator = Agent(
    name="Master_Image_Generator_Agent",
    model=text_model_lite,
    description=(
        "You are an expert in generating images using generative AI.\n"
        "You use the theme and content goals to help you create detailed prompts for generating images."
    ),
    instruction=(
        "You are a helpful assistant that generates images using generative AI.\n"
        "Create a detailed prompt for generating an image that complements the blog post theme and goals and matches the post style.\n"
        "Use the tool 'generate_image' to generate the image.\n"
        "Unless requested otherwise, generate 3 images matching the theme so the user can choose. Opt for images without text."
    ),
    tools=[generate_image],
)

# media_team = LoopAgent(
#     name="media_team",
#     description="You manage a team that generates images for the post",
#     max_iterations=3,
#     sub_agents=[image_generator]
# )


content_creation_team = SequentialAgent(
    name="content_creation_team",
    description="You are the sequential coordinator of the content creation team.",
    sub_agents=[theme_research_definition, content_research_agent, content_structure_agent, writing_agent, review_agent, edit_review, image_generator]
)

# AI Agent for lead generation
# Inform, create a how-to guide, and generate leads.
# I'm Victor Assis
# Audience: Entrepreneurs, marketing professionals
# How to, very thorough, and positioning myself as an expert and reference