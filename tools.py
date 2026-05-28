from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
from datetime import datetime

search = DuckDuckGoSearchRun()

@tool
def search_tool(query: str) -> str:
    "use this tool to answer questions about current events or " \
    "to find information that may not be in the model's training data. " \
    "The input to this tool should be a search query."
    return search.run(query)

@tool
def save_file(data: str, filename: str = "research_output.txt") -> str:
    "Use this tool to save data to a file. The input to this tool should be the data to save and the filename."
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"---- Research Output ----\nTimestamp: {timestamp}\n\n{data}\n"
        
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}."
        

