from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from question_generator import QuestionGenerator
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://*.railway.app",  # Railway domains
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
async def get_question(category: Optional[str] = None) -> QuestionResponse:
    question_data = question_generator.generate_question(category)
    
    if not question_data:
        raise HTTPException(status_code=500, detail="Failed to generate question")
    
    return QuestionResponse(
        question=question_data['question'],
        options=question_data['options'],
        correct_answer=question_data['correct_answer']
    )

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