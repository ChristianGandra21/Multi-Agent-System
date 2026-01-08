from pydantic import BaseModel
from typing import Dict, Optional, Any
from datetime import datetime

class ResearchBase(BaseModel):
    query: str

class ResearchCreate(ResearchBase):
    pass

class ResearchResponse(ResearchBase):
    id: int
    status: str
    created_at: datetime

    research_data: Optional[Dict[str, Any]] = None  # Research Agent
    analysis_data: Optional[Dict[str, Any]] = None  # Data Agent
    code_outputs: Optional[Dict[str, Any]] = None   # Code Agent
    final_report: Optional[str] = None              # Writer Agent
    
    error_message: Optional[str] = None             # Error messages
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
