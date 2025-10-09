from google.adk.agents import Agent
from .config import (
    text_model
)
from .subagents import (
    overall_workflow
)

root_agent = Agent(
    name="prd_new_ideas",
    model=text_model,
    description=f"You are an expert Product Manager that orchestrates a team of product managers and extracts user requirements.",
    instruction=f"""Orchestrate your team of product managers in creating a top notch, helpful and through Product Requirement Document for a new system. Assign the product_researcher agent for deep research o a theme.
    Your jobs are:
        1 - Extract from the user what you can about the business idea and product. Making sure you lapidate the idea to come up with a refined product idea before handling to your team.
        2 - Use the overall_workflow angent (sequential agent) to manage the researches and syntetization of results.
        3 - Present the final PRD to the user and answer questions.
    """,
    # tools=[product_reseacher_tool],
    sub_agents=[overall_workflow]
)



# Refined Product Idea: AI-Powered Podcast Co-creation Platform

# This platform empowers users (producers, content creators) to generate dynamic, engaging podcasts featuring multiple AI agents. It leverages a hybrid human-AI workflow for content creation, allowing for highly customized AI agent personalities, contextual awareness, and spontaneous, yet bounded, conversations delivered through real-time, human-like speech. The core value lies in providing tools for users to craft diverse podcast experiences, from deep dives to entertaining discussions, with AI agents acting as configurable, integral co-hosts or characters.

# Key differentiators include:

# Hybrid Scripting & Research: A collaborative environment where AI assists with research and initial script generation, which humans then refine and edit.
# Rich Agent Configuration: Users can define intricate details for each AI agent, including name, role, specific goals, background, conversational context (spanning episodes and current discussions), and proprietary material inputs. This enables agents to develop distinct "souls" and consistent personas.
# Dynamic, Bounded Conversation: Agents engage in real-time, spontaneous dialogue, ensuring natural flow within the user-defined script and contextual parameters.
# Real-time, Expressive Speech Generation: High-quality, human-like voices with configurable emotional ranges are generated live, enhancing listener engagement.
# Agent Reusability: The ability to save and reuse configured AI agents across episodes fosters continuity and simplifies content production.
# User-Driven Content Diversity: The platform is designed to be flexible, allowing users to create a wide spectrum of content, from educational and analytical to purely entertaining.
# This is a well-defined product concept that addresses a clear need for efficient, creative, and scalable podcast production with a unique AI-driven approach.