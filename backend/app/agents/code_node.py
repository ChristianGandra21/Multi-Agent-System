from langchain_experimental.utilities import PythonREPL
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.state import ResearchState
from app.agents.llm_config import get_llm
import os
import base64

def code_node(state: ResearchState) -> ResearchState:
    data = state.get("extracted_data", {})

    # Se não há dados extraídos, pula a geração de gráficos
    if not data or data == {}:
        return {
            **state,
            "code_outputs": {"logs": "Sem dados estruturados para visualização", "code": "", "chart_base64": None},
            "visualizations": [],
            "current_step": "code_skipped"
        }

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

        # Tentar ler a imagem gerada e converter para base64
        chart_base64 = None
        try:
            if os.path.exists("chart.png"):
                with open("chart.png", "rb") as img_file:
                    chart_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                os.remove("chart.png")  # Limpar o arquivo após leitura
        except Exception as img_error:
            print(f"Erro ao processar imagem: {str(img_error)}")

        return {
            **state,
            "code_outputs": {"logs": output, "code": code, "chart_base64": chart_base64},
            "visualizations": [{"type": "plot", "available": chart_base64 is not None}] if chart_base64 else [],
            "current_step": "code_executed"
        }
    except Exception as e:
        return {
            **state,
            "code_outputs": {"logs": f"Erro ao executar o código: {str(e)}", "code": "", "chart_base64": None},
            "visualizations": [],
            "current_step": "code_execution_failed"
        }