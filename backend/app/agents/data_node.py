from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import os
import json

from app.agents.state import ResearchState
from app.agents.llm_config import get_llm

def data_node(state: ResearchState) -> ResearchState:
    summary = state.get("research_summary", "")

    llm = get_llm(temperature=0)

    system_prompt = (
            "Você é um Especialista em Extração de Dados. Sua tarefa é identificar todos os valores numéricos, "
            "estatísticas, porcentagens e métricas do texto fornecido. "
            "Você deve retornar APENAS um objeto JSON puro com os dados extraídos, sem explicações."
        )

    human_prompt = f"Extraia os dados estruturados do seguinte resumo de pesquisa: {summary}"

    try:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ])
        
        content = response.content.strip()
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()

        extracted_data = json.loads(content)

        return {
            **state,
            "extracted_data": extracted_data,
            "data_analysis": "Dados extraídos com sucesso.",
            "current_step": "data_extracted" 
        }
    except Exception as e:
        return {
            **state,
            "extracted_data": {},
            "data_analysis": f"Erro ao extrair dados: {str(e)}",
            "current_step": "data_extraction_failed"
        }