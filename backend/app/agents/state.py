from typing import TypedDict, List, Dict, Any, Annotated
from langgraph.graph.message import add_messages

class ResearchState(TypedDict):
    query: str

    research_results: List[Dict[str, Any]]
    research_summary: str

    extracted_data: Dict[str, Any]
    data_analysis: str

    visualizations: List[Dict[str, Any]]
    code_outputs: Dict[str, Any]

    final_report: str

    messages: Annotated[List, add_messages]
    current_step: str
    erros: List[str]