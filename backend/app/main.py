from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .database import get_db, engine, Base
from .models import Research
from .schemas import ResearchCreate, ResearchResponse
from .worker import execute_research_flow

app = FastAPI(
    title="Multi-Agent Research System",
    description="An API for managing multi-agent research tasks.",
    version="1.0.0",
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine) # Cria as tabelas do banco de dados na inicialização

# Rota index
@app.get("/")
def root():
    return {"message": "Welcome to the Multi-Agent Research System API", "version": "1.0.0", "status": "running"}

# Rota para criar uma nova tarefa de pesquisa
@app.post("/research/", response_model=ResearchResponse)
def create_research(research: ResearchCreate, db: Session = Depends(get_db)):
    new_research = Research(query=research.query, status="pending")
    db.add(new_research)
    db.commit()
    db.refresh(new_research)

    # Executar pesquisa de forma assíncrona
    execute_research_flow.delay(new_research.id, new_research.query)
def get_research(research_id: int, db: Session = Depends(get_db)):
    research = db.query(Research).filter(Research.id == research_id).first()
    if not research:
        raise HTTPException(status_code=404, detail="Research task not found")
    return research

# Rota para listar todas as tarefas de pesquisa
@app.get("/research/", response_model=List[ResearchResponse])
def list_research(db: Session = Depends(get_db)):
    researches = db.query(Research).order_by(Research.created_at.desc()).all()
    return researches