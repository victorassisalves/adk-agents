from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool
from ..config import (
    text_model_lite
)
import datetime

now = datetime.datetime.now()

product_reseacher = Agent(
    name="product_reseacher",
    model=text_model_lite,
    description=f"You are a product research expert. Tasked with doing deep researches on a product theme to uncover the best information possible for creating a Product Requirement Document.",
    instruction=f"""
        Always using the google_search toll and get the most updated info as of today {now}, Your step by step method is:
        1 - Understanding the product environment. Doing online searches on the product space. Understanding what is important.
        2 - You now reasearch online the specifics of such product. The necessary requirements of the product that are more important.
        3 - You research the market for competidors and the landscape for this type of products.
        4 - Return the raw research in md format
    """,
    tools=[google_search],
    output_key="product_research"
)

product_reseacher_tool = AgentTool(agent=product_reseacher)
