from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    options = Column(String, nullable=False)  # Store as JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 