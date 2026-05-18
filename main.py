from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

load_dotenv()

llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0.9)

response = llm.invoke("What's the current job market scenario for international students in the US?")
print(response)

