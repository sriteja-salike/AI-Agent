from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from tools import search_tool, save_file

load_dotenv()

llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0.9)


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


system_prompt = """
You are a research assistant that will help generate a research paper and provides concise summaries of complex topics.
You will also provide a list of sources and tools used in the research process.
Answer the user query and use necessary tools to gather information and provide a comprehensive response.
"""

tools = [search_tool, save_file]
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt,
    response_format=ToolStrategy(ResearchResponse),
)

query = input("What can I help you research today? ")
raw_response = agent.invoke(
    {"messages": [{"role": "user", "content": query}]}
)

structured = raw_response["structured_response"]
print(structured.summary)


