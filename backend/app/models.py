from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime
from .database import Base

class Research(Base):
    __tablename__ = "research"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    query = Column(Text, nullable=False)
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    research_data = Column(JSON, nullable=True)
    analysis_data = Column(JSON, nullable=True)
    code_outputs = Column(JSON, nullable=True)
    final_report = Column(Text, nullable=True)

    error_message = Column(Text, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Research(id={self.id}, query={self.query}, status={self.status})>"

    def to_dict(self):
        return {
            "id": self.id,
            "query": self.query,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "research_data": self.research_data,
            "analysis_data": self.analysis_data,
            "code_outputs": self.code_outputs,
            "final_report": self.final_report,
            "error_message": self.error_message,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        } 
