from langchain_groq import ChatGroq
import os
from typing import Optional, List

def get_llm(temperature: float = 0.1, model: str = "llama-3.3-70b-versatile", tools: Optional[List] = None):
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model=model,
        temperature=temperature    
    )

    if tools:
        return llm.bind_tools(tools)
    return llm    