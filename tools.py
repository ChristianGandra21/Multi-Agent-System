import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

#Cria a ferramenta de busca Tavily
search_tool = TavilySearchResults(max_results=2)

tools = [search_tool]