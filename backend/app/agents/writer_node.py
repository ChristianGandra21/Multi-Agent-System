from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from app.agents.state import ResearchState
from app.agents.llm_config import get_llm

import os

def writer_node(state: ResearchState) -> ResearchState:
    summary = state.get("research_summary")
    analysis = state.get("data_analysis")

    llm = get_llm()

    prompt = (
            f"Você é um Escritor Técnico. Crie um relatório executivo final em Markdown.\n"
            f"Use o resumo da pesquisa: {summary}\n"
            f"E a análise de dados: {analysis}\n"
            "Inclua uma introdução, seções com tabelas e uma conclusão estratégica."
        )

    response = llm.invoke([HumanMessage(content=prompt)])

    return {
        **state,
        "final_report": response.content,
        "current_step": "report_written"
    }