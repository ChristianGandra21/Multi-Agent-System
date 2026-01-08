from langchain_core.tools import Tool
from tavily import TavilyClient
import os
import json

# Carrega as variáveis de ambiente do arquivo .env
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def search_web(query: str) -> str:
    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(query, max_results=5)
        results = response.get("results", [])
        formatted_results = []

        for result in results:
            formatted_results.append({
                "title": result.get("title"),
                "url": result.get("url"),
                "content": result.get("content"),
                "score": result.get("score")
            })
        return json.dumps({
            "success": True,
            "query": query,
            "results": formatted_results
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        })

def get_search_tool() -> Tool:
    return Tool(
        name="Tavily Web Search",
        func=search_web,
        description="Use this tool to search the web for relevant information. Input should be a search query string."
    )