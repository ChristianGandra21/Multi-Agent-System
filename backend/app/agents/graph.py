from langgraph.graph import StateGraph, START, END
from typing import Literal

from app.agents.state import ResearchState
from app.agents.research_node import research_node

def create_graph():
    workflow = StateGraph(ResearchState)

    workflow.add_node("research_node", research_node)

    workflow.set_entry_point("research_node")
    workflow.add_edge("research_node", END)

    app = workflow.compile()

    return app

def run_research(query: str) -> dict:
    graph = create_graph()
    initial_state: ResearchState = {
        "query": query,
        "research_results": [],
        "research_summary": "",
        "extracted_data": {},
        "data_analysis": "",
        "visualizations": [],
        "code_outputs": {},
        "final_report": "",
        "messages": [],
        "current_step": "start",
        "erros": []
    }
    try:
        final_state = graph.invoke(initial_state)
        return {
            "success": True,
            "query": query,
            "research_results": final_state.get("research_results", []),
            "research_summary": final_state.get("research_summary", ""),
            "final_report": final_state.get("final_report", ""),
            "errors": final_state.get("erros", [])
        }
    except Exception as e:
        return {
            "success": False,
            "query": query,
            "error": str(e)
        }
    
