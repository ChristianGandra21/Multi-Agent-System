from langchain_experimental.utilities import PythonREPL
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.state import ResearchState
from app.agents.llm_config import get_llm
import os

def code_node(state: ResearchState) -> ResearchState:
    data = state.get("extracted_data", {})

    llm = get_llm()

    prompt = (
        f"Com base nos seguintes dados JSON: {data}, escreva um código Python usando matplotlib "
        "para criar um gráfico de barras comparativo. Salve o gráfico como 'chart.png'. "
        "Retorne APENAS o código Python, sem blocos de texto ou markdown."
    )

    try:
        code_response = llm.invoke([HumanMessage(content=prompt)])

        code = code_response.content.replace("```python", "").replace("```", "").strip()

        repl = PythonREPL()
        output = repl.run(code)

        return {
            **state,
            "code_outputs": {"logs": output, "code": code},
            "visualizations": [{"path": "chart.png", "type": "plot"}],
            "current_step": "code_executed"
        }
    except Exception as e:
        return {
            **state,
            "code_outputs": {"logs": f"Erro ao executar o código: {str(e)}", "code": ""},
            "visualizations": [],
            "current_step": "code_execution_failed"
        }