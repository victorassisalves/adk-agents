from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search
from ..config import (text_model,text_model_lite)
from ..tools.tools import (
    save_prd_file
)
import datetime

now = datetime.datetime.now()


#  DISCOVERY & RESEARCH TEAM

# Objective: To understand the problem space, the user, and the market. This team answers the questions: "Why are we doing this?" and "What is the opportunity?"

# Market & Competitive Analyst Agent

# Role: (Merges your Product Research and Market research agents). Conducts a deep analysis of the market landscape, identifies competitors, analyzes their products (features, pricing, weaknesses), and reports on market size and trends.

# Inputs: Initial product concept from CPO Agent.

# Outputs: A detailed Market & Competitive Landscape report.

market_and_competitive_analysis = Agent(
    name="market_and_competitive_analysis",
    model=text_model_lite,
    description="You are an expert in doing market reserach and analysis for products.",
    instruction=f"""
        Using the google_search tool, conducts a research to get deep analysis of the market landscape, identifies competitors, analyzes their products (features, pricing, weaknesses), and reports on market size and trends.
    """,
    tools=[google_search],
    output_key="market_research"
)

# User Insights & Persona Agent

# Role: (Refines your User Persona Architect Agent). Focuses entirely on the user. It can analyze user feedback, conduct research on forums, and then synthesizes this into detailed user personas, including their goals, pain points, and motivations.

# Inputs: Initial product concept and Market report.

# Outputs: A set of 2-3 detailed User Personas.

persona_researcher = Agent(
    name="persona_researcher",
    model=text_model_lite,
    description="You are an expert in researching and building personas",
    instruction=f"""
        Focuses entirely on the user. It can analyze user feedback and then synthesizes this into detailed user personas, including their goals, pain points, and motivations.
    """,
    output_key="persona_research"
)

# Technology Trends & Feasibility Agent

# Role: (A more focused version of your Technical research agent). Scans for relevant technologies, platforms, and APIs that could be used. It provides a high-level assessment of technical possibilities and potential challenges without designing the solution.

# Inputs: Initial product concept.

# Outputs: A Technology Opportunities & Risks brief.

technology_researcher = Agent(
    name="technology_researcher",
    model=text_model_lite,
    description="You are an expert in researching and building personas",
    instruction=f"""
        Scans for relevant technologies, platforms, and APIs that could be used. It provides a high-level assessment of technical possibilities and potential challenges without designing the solution. Give preference on Flutter and Flutterflow to make building the frontend then it looks at the back for compatible.
        Research flutterflow to make sure is doable and viable. And how to do it.
    """,
    tools=[google_search],
    output_key="tech_research"
)

# Research Lead Agent (Team Orchestrator)

# Role: Manages the research process, ensures agents are not duplicating work, and synthesizes their findings into a single "Discovery Brief."

research_and_dicovery_team = ParallelAgent(
    name="research_and_dicovery_team",
    description=""""
        Agent responsible for orchestrating the research and discovery team of agents.
        The agents are market_and_competitive_analysis for market analysis, persona_researcher for persona building, and technology_researcher for building a technology research.
    """,
    sub_agents=[market_and_competitive_analysis, persona_researcher, technology_researcher],
)

synthesizer = Agent(
    name="Synthesizer",
    model=text_model,
    description="Expert im building combined reports from researches",
    instruction="Combine results from {persona_research}, {tech_research} and {market_research}. and save research into an markdown file using save file tool. The tool need two paramenters (file_name, content) for file name use PRD_research_ name_of_the_PRD (the actual name not the literal text). Instead of spaces, use _ between words.",
    tools=[save_prd_file],
    output_key="combined_reasearch"
)

overall_workflow = SequentialAgent(
    name="research_and_synthesize",
    sub_agents=[research_and_dicovery_team, synthesizer] # Run parallel fetch, then synthesize
)