"""
This module defines a multi‑agent system built with the Google
Agent Development Kit (ADK).  The system is designed to help a user
plan, research, design, implement, test and explain new ADK agents.

Each role in the development lifecycle is encapsulated in its own
``LlmAgent``.  These agents are orchestrated by a ``SequentialAgent``
which runs them in a fixed order.  The stub functions defined in
``tools`` demonstrate how you could integrate custom functionality
(e.g. searching documentation, executing code or running tests) as
ADK tools.  Replace these stubs with actual implementations when
available.

Example usage::

    from agent_builder.agent import root_agent
    from google.adk.runners import InMemoryRunner

    runner = InMemoryRunner(app_name="agent_helper_app", root_agent=root_agent)
    session = runner.start_session(user_id="user123")
    response = runner.send_message(session=session, content="Build me an agent that greets users")
    print(response)

"""

from typing import Any, Dict

from google.adk.agents import LlmAgent, SequentialAgent


# ---------------------------------------------------------------------------
# Tool stubs
#
# Tools extend an agent's capabilities beyond the underlying language
# model.  Each tool should return a JSON‑serialisable dict.  In a
# production system you would replace these stubs with real search APIs,
# code execution environments or test runners.

def search_adk_docs(query: str) -> Dict[str, Any]:
    """Return search results for the ADK documentation.

    Args:
        query: The user's search query.

    Returns:
        A dict containing a status and a result string.  This stub
        always succeeds and echoes the query.  Replace with a real
        search integration (e.g. Google Search tool from ADK) as needed.
    """
    # In a real implementation you would call the ADK search tool or
    # another API here.  For now we just return a placeholder.
    return {
        "status": "success",
        "results": f"Search results for '{query}' (stub)"
    }


def execute_code(code: str) -> Dict[str, Any]:
    """Execute a code snippet and return its output.

    This stub does not actually execute code for safety reasons.  It
    simply returns a success message.  In a real system, you could
    integrate with a sandboxed execution environment or ADK's built‑in
    Code Execution tool.
    """
    return {
        "status": "success",
        "output": f"Executed code: {code[:30]}... (stub)"
    }


def run_unit_tests(code: str) -> Dict[str, Any]:
    """Run unit tests against generated code and report results.

    This stub always reports that tests pass.  Replace with logic
    that invokes your test suite using the ADK evaluation framework or
    an external test runner.
    """
    return {
        "status": "success",
        "result": "All tests passed (stub)"
    }


# ---------------------------------------------------------------------------
# Agent definitions
#
# Each LLM agent encapsulates a single role in the agent development
# workflow.  Agents store their outputs in the session state using
# ``output_key`` so that subsequent agents can access prior results.


# 1. Planner Agent
planner_agent = LlmAgent(
    name="PlannerAgent",
    model="gemini-2.0-flash",
    description=(
        "Creates a high‑level plan for building an ADK agent based on the "
        "user's project specification."
    ),
    instruction=(
        "You are a planning agent.  Given a specification for a new agent, "
        "produce a structured plan with clear, numbered steps.  The plan "
        "should outline what information needs to be gathered (e.g. ADK docs "
        "pages to read), which tools or sub‑agents will be needed, and the "
        "overall workflow.  Use concise language and avoid unnecessary prose."
    ),
    # The planner does not require tools; it relies on the LLM for reasoning.
    tools=[],
    # Store the plan in the session state so the architect can access it.
    output_key="project_plan",
)


# 2. Researcher Agent
researcher_agent = LlmAgent(
    name="ResearcherAgent",
    model="gemini-2.0-flash",
    description=(
        "Gathers information from the ADK documentation and other sources "
        "needed to fulfil the project plan."
    ),
    instruction=(
        "You are a researcher.  Given a plan and a project specification, "
        "identify which topics or questions need answers.  Use the "
        "`search_adk_docs` tool to retrieve information from the ADK docs.  "
        "Summarise the findings in a concise format.  Focus only on the "
        "content relevant to the current project."
    ),
    tools=[search_adk_docs],
    # Save the research summary so other agents can reference it.
    output_key="research_summary",
)


# 3. Architect Agent
architect_agent = LlmAgent(
    name="ArchitectAgent",
    model="gemini-2.0-flash",
    description=(
        "Designs a multi‑agent architecture based on the project plan and research."
    ),
    instruction=(
        "You are a software architect.  Using the plan (`{project_plan}`) and "
        "research summary (`{research_summary}`) from previous agents, propose "
        "an ADK architecture.  Specify the names, descriptions and models for "
        "each sub‑agent (planner, researcher, architect, developer, tester, "
        "explainer).  Indicate whether any workflow agents (SequentialAgent, "
        "LoopAgent, ParallelAgent) are required.  Describe how data flows "
        "between agents using `output_key`.  Respond with a bullet list of "
        "components and their responsibilities."
    ),
    tools=[],
    output_key="architecture_spec",
)


# 4. Developer Agent
developer_agent = LlmAgent(
    name="DeveloperAgent",
    model="gemini-2.0-flash",
    description=(
        "Writes the actual Python code for the agents defined in the architecture."
    ),
    instruction=(
        "You are an expert ADK developer.  Based on the architecture (`{architecture_spec}`) "
        "and project plan (`{project_plan}`), write the Python code required to implement "
        "all agents.  Follow best practices: define tool functions, LLM agents with clear "
        "names/instructions, workflow agents as needed, and a `root_agent` to orchestrate them. "
        "Return only the Python code enclosed in triple backticks (```python ... ```).  Do not "
        "include explanatory text."
    ),
    tools=[execute_code],
    output_key="generated_code",
)


# 5. Tester Agent
tester_agent = LlmAgent(
    name="TesterAgent",
    model="gemini-2.0-flash",
    description=(
        "Runs a suite of tests on the generated code and reports results."
    ),
    instruction=(
        "You are a tester.  Given the generated code (`{generated_code}`), "
        "run unit tests to ensure the code compiles and the agents interact "
        "correctly.  Use the `run_unit_tests` tool.  Summarise the results, "
        "highlighting any failures or areas for improvement."
    ),
    tools=[run_unit_tests],
    output_key="test_report",
)


# 6. Explainer Agent
explainer_agent = LlmAgent(
    name="ExplainerAgent",
    model="gemini-2.0-flash",
    description=(
        "Explains the architecture, code and test results in plain language."
    ),
    instruction=(
        "You are an explainer.  Using the architecture (`{architecture_spec}`), the "
        "generated code (`{generated_code}`) and the test report (`{test_report}`), "
        "write a clear explanation of how the multi‑agent system works.  Summarise the "
        "purpose of each agent, how they coordinate via ADK workflows, and interpret "
        "the test results.  Present the explanation in a friendly, concise way."
    ),
    tools=[],
    output_key="explanation",
)


# ---------------------------------------------------------------------------
# Root agent orchestrating the pipeline
#
# The root agent uses a SequentialAgent to ensure that the planner runs first,
# followed by the researcher, architect, developer, tester and explainer.

root_agent = SequentialAgent(
    name="AgentBuilderPipeline",
    sub_agents=[
        planner_agent,
        researcher_agent,
        architect_agent,
        developer_agent,
        tester_agent,
        explainer_agent,
    ],
    description=(
        "Orchestrates the process of planning, researching, designing, coding, "
        "testing and explaining a new ADK agent.  Sub‑agents are executed in "
        "the order they appear in the list."
    ),
)


__all__ = [
    "root_agent",
    "planner_agent",
    "researcher_agent",
    "architect_agent",
    "developer_agent",
    "tester_agent",
    "explainer_agent",
    "search_adk_docs",
    "execute_code",
    "run_unit_tests",
]