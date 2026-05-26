
'''
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

load_dotenv()

llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0.9)


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

parser = PydanticOutputParser(pydantic_object=ResearchResponse)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", 
            """
            You are a research assistant that will help generate a research paper and provides concise summaries of complex topics.
            You will also provide a list of sources and tools used in the research process.
            Answer the user query and use necessary tools to gather information and provide a comprehensive response.
            Wrap the output in this format and provide no other text \n{format_instructions}
            """
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial_format_instructions(parser.get_format_instructions())

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools = [],
    output_parser=parser
)

agent_executor = AgentExecutor(agent=agent, tools=[], verbose = True)
raw_response = agent_executor.invoke({"query": "What the current stock price of Google?"})
print(raw_response)














'''



######## -------------------------------------------- 



from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

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

agent = create_agent(
    model=llm,
    tools=[],
    system_prompt=system_prompt,
    response_format=ToolStrategy(ResearchResponse),
)

query = input("What can I help you research today? ")
raw_response = agent.invoke(
    {"messages": [{"role": "user", "content": query}]}
)

structured = raw_response["structured_response"]
print(structured.summary)


