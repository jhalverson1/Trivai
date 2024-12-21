from pydantic import BaseModel, Field, model_validator
from typing import List, Optional
from datetime import datetime
import json

class GameCreate(BaseModel):
    category: str = Field(..., description="The category of questions")
    numberOfQuestions: int = Field(default=5, ge=1, le=50, description="Number of questions (1-50)")
    difficultyId: int = Field(default=3, ge=1, le=5, description="Difficulty level (1-5)")

class QuestionResponse(BaseModel):
    id: str
    questionText: str
    correctAnswer: str
    options: List[str]
    difficultyId: int
    gameId: str
    createdAt: datetime

    @model_validator(mode='before')
    @classmethod
    def parse_data(cls, values):
        if isinstance(values, dict):
            # Convert IDs to strings
            if 'id' in values:
                values['id'] = str(values['id'])
            if 'game_id' in values:
                values['gameId'] = str(values.pop('game_id'))
            # Convert field names
            if 'question_text' in values:
                values['questionText'] = values.pop('question_text')
            if 'correct_answer' in values:
                values['correctAnswer'] = values.pop('correct_answer')
            if 'difficulty_id' in values:
                values['difficultyId'] = values.pop('difficulty_id')
            if 'created_at' in values:
                values['createdAt'] = values.pop('created_at')
            # Parse options if they're a JSON string
            if isinstance(values.get('options'), str):
                values['options'] = json.loads(values['options'])
        return values

    class Config:
        from_attributes = True
        populate_by_name = True

class GameResponse(BaseModel):
    id: str
    category: str
    numberOfQuestions: int
    difficultyId: int
    currentQuestionIndex: int
    score: int
    status: str
    createdAt: datetime
    updatedAt: Optional[datetime]
    questions: List[QuestionResponse]

    @model_validator(mode='before')
    @classmethod
    def parse_data(cls, values):
        if isinstance(values, dict):
            # Convert ID to string
            if 'id' in values:
                values['id'] = str(values['id'])
            # Convert field names
            if 'number_of_questions' in values:
                values['numberOfQuestions'] = values.pop('number_of_questions')
            if 'difficulty_id' in values:
                values['difficultyId'] = values.pop('difficulty_id')
            if 'current_question_index' in values:
                values['currentQuestionIndex'] = values.pop('current_question_index')
            if 'created_at' in values:
                values['createdAt'] = values.pop('created_at')
            if 'updated_at' in values:
                values['updatedAt'] = values.pop('updated_at')
        return values

    class Config:
        from_attributes = True
        populate_by_name = True 