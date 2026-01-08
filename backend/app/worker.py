import os
from celery import Celery

from app.agents.graph import run_graph
from app.database import SessionLocal
from app.models import Research

celery_app = Celery(
    "research_tasks", 
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task(name="execute_research_flow")
def execute_research_flow(research_id: int, query: str):
    db = SessionLocal()
    
    try:
        research = db.query(Research).filter(Research.id == research_id).first()
        research.status = "in_progress"
        db.commit()

        result = run_graph(query)

        if result["success"]:
            research.status = "completed"
            research.research_data = result.get("research_results")
            research.analysis_data = result.get("data_analysis")
            research.final_report = result.get("final_report")
        else:
            research.status = "failed"
            research.error_message = str(result.get("error"))

        db.commit()
    except Exception as e:
        db.rollback
        db.query(Research).filter(Research.id == research_id).update({
            "status": "failed", 
            "error_message": str(e)
        })
        db.commit()
    finally:
        db.close()