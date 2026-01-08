import os
from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq
from tools import tools
from langgraph.prebuilt import ToolNode

load_dotenv()

class Estado(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatGroq(model_name='llama-3.3-70b-versatile').bind_tools(tools)

def pesquisador(state: Estado):
    resposta = llm.invoke(state['messages'])
    return {'messages': [resposta]}

def analista_dados(state: Estado):
    mensagens = state['messages']
    
    prompt_analista = (
        "Você é um Analista de Dados sênior. Sua única função é extrair informações "
        "quantitativas e estruturadas do texto fornecido.\n\n"
        "REGRAS DE OURO:\n"
        "1. Se houver valores monetários, organize-os em uma tabela.\n"
        "2. Identifique métricas como datas, porcentagens e nomes de empresas.\n"
        "3. Se houver dados conflitantes, aponte a discrepância.\n"
        "4. Responda APENAS com a tabela Markdown e um breve parágrafo de 'Insight do Analista'."
    )
    
    resposta = llm.invoke(mensagens + [("system", prompt_analista)])
    return {"messages": [resposta]}

def auditor(state: Estado):
    mensagens = state['messages']
    ultima_mensagem = mensagens[-1]

    if "não foi possível encontrar" in ultima_mensagem.content.lower() or "nenhum resultado" in ultima_mensagem.content.lower() or "não encontrei" in ultima_mensagem.content.lower():
        prompt_critica = (
                    "Você é um Auditor de Qualidade. O relatório acima está incompleto. "
                    "Dê uma ordem clara para o pesquisador voltar e buscar especificamente esses dados."
                )
        return {'messages': [( "system", prompt_critica)]}
    
    return {'messages': [( "system", "Relatório aprovado. Nenhuma ação adicional é necessária.")]}

ferramentas_node = ToolNode(tools)

workflow = StateGraph(Estado)
workflow.add_node("agente_pesquisador", pesquisador)
workflow.add_node("analista_dados", analista_dados)
workflow.add_node("auditor", auditor)
workflow.add_node("ferramentas", ferramentas_node)

workflow.set_entry_point("agente_pesquisador")

def have_to_continue(state: Estado):
    mensagens = state['messages']
    ultima_mensagem = mensagens[-1]

    if ultima_mensagem.tool_calls:
        return "ferramentas"
    
    return "analista_dados"

workflow.add_conditional_edges(
    "agente_pesquisador",
    have_to_continue,
)

def decide_end(state: Estado):
    if "Relatório aprovado" in state['messages'][-1].content:
        return END
    return "agente_pesquisador"

workflow.add_conditional_edges(
    "auditor",
    decide_end,
)

workflow.add_edge("ferramentas", "agente_pesquisador")
workflow.add_edge("analista_dados", "auditor")
workflow.add_edge("auditor", END)

app = workflow.compile()

# Tente perguntar sobre algo que aconteceu nas últimas 24 horas
result = app.invoke({"messages": [("user", "Compare o preço e a autonomia dos 3 carros elétricos mais vendidos no Brasil em 2025.")]})

# Vamos imprimir de um jeito mais bonito para ver a conversa
for msg in result["messages"]:
    print(f"--- \n {msg.type.upper()}: {msg.content}")