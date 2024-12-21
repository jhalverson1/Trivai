from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from question_generator import QuestionGenerator
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db
import models
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",    # Local development
        "http://127.0.0.1:3000",    # Alternative local development
        "https://*.railway.app",    # Railway domains
        "http://backend:8000",      # Docker internal
        "http://frontend:3000",     # Docker internal
        "*"                         # Allow all origins for testing (remove in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the question generator
question_generator = QuestionGenerator()

class QuestionResponse(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

class AnswerRequest(BaseModel):
    answer: str
    correct_answer: str

@app.get("/api/question")
async def get_question(category: Optional[str] = None, db: Session = Depends(get_db)) -> QuestionResponse:
    try:
        print(f"Received question request with category: {category}")
        question_data = question_generator.generate_question(category)
        
        if not question_data:
            print("Failed to generate question")
            raise HTTPException(status_code=500, detail="Failed to generate question")
        
        print("Returning question:", question_data)
        
        # Save question to database
        db_question = models.Question(
            question_text=question_data['question'],
            correct_answer=question_data['correct_answer'],
            options=json.dumps(question_data['options'])
        )
        db.add(db_question)
        db.commit()
        
        return QuestionResponse(
            question=question_data['question'],
            options=question_data['options'],
            correct_answer=question_data['correct_answer']
        )
    except Exception as e:
        print(f"Error in get_question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/check-answer")
async def check_answer(answer_request: AnswerRequest) -> dict:
    user_answer = answer_request.answer.upper()
    correct_letter = answer_request.correct_answer
    
    # Extract just the letter if the answer contains full text
    if ')' in correct_letter:
        correct_letter = correct_letter.split(')')[0].strip()
    
    is_correct = user_answer == correct_letter
    return {
        "correct": is_correct,
        "correct_answer": answer_request.correct_answer
    } 

# Add after your existing FastAPI setup
app.mount("/", StaticFiles(directory="static", html=True))