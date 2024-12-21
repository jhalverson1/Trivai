from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class GameStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class Difficulty(Base):
    __tablename__ = "difficulties"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    number_of_questions = Column(Integer, nullable=False)
    difficulty_id = Column(Integer, ForeignKey("difficulties.id"), nullable=False)
    current_question_index = Column(Integer, default=0)
    score = Column(Integer, default=0)
    status = Column(Enum(GameStatus), default=GameStatus.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    difficulty = relationship("Difficulty")
    questions = relationship("Question", back_populates="game")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    options = Column(String, nullable=False)  # Store as JSON string
    difficulty_id = Column(Integer, ForeignKey("difficulties.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    difficulty = relationship("Difficulty")
    game = relationship("Game", back_populates="questions") 