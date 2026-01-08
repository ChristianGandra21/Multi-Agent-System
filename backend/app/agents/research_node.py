from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import os
import json
from tavily import TavilyClient

from app.agents.state import ResearchState
from app.agents.llm_config import get_llm

def web_search(query: str) -> str:
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
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
        return json.dumps(formatted_results)
    except Exception as e:
        return json.dumps({
            "error": str(e)
        })

def research_node(state: ResearchState) -> ResearchState:
    query  = state["query"]

    try:
        llm = get_llm(tools=[web_search])

        results = web_search(query)

        system_message = SystemMessage(content=(
            "Você é um agente de pesquisa especializado em buscar informações na web. "
            "Use as ferramentas disponíveis para encontrar informações relevantes e atualizadas sobre o tópico solicitado."
        ))

        human_message = HumanMessage(content=(
            f"Realize uma pesquisa na web sobre o seguinte tópico: {query}\n\n"
            f"Use os seguintes resultados da pesquisa para formular sua resposta:\n{results}\n\n"
            "Forneça um resumo claro e organizado das informações encontradas, citando as fontes (URLs)."
        ))

        response = llm.invoke([system_message, human_message])
        summary = response.content
        
        # Parse results to list of dicts
        results_list = json.loads(results) if isinstance(results, str) else results

        return {
            **state,
            "research_results": results_list,
            "research_summary": summary,
            "current_step": "research_completed",
            "messages": state.get("messages", []) + [f"Pesquisa concluída para: {query}"]
        }
    except Exception as e:
        return {
            **state,
            "erros": state.get("erros", []) + [str(e)],
            "current_step": "error"
        }