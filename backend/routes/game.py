from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json
import logging
from database import get_db
import models
from models import Game, Question, GameStatus, Difficulty
from schemas import GameCreate, GameResponse
from question_generator import QuestionGenerator
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
question_generator = QuestionGenerator()

@router.post("/games")
async def create_game(game_data: GameCreate, db: Session = Depends(get_db)):
    logger.info(f"Received game creation request: {game_data}")
    try:
        # Verify OpenAI API key is set
        api_key = os.getenv('OPENAI_API_KEY')
        logger.info(f"API Key present: {bool(api_key)}")
        if not api_key:
            logger.error("OPENAI_API_KEY not found in environment")
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")

        # Verify difficulty exists
        difficulty = db.query(Difficulty).filter(Difficulty.id == game_data.difficultyId).first()
        if not difficulty:
            logger.error(f"Difficulty {game_data.difficultyId} not found")
            raise HTTPException(status_code=400, detail=f"Difficulty {game_data.difficultyId} not found")

        # Create new game
        logger.info("Creating new game")
        new_game = Game(
            category=game_data.category,
            number_of_questions=game_data.numberOfQuestions,
            difficulty_id=game_data.difficultyId,
            status=GameStatus.in_progress
        )
        db.add(new_game)
        db.commit()
        db.refresh(new_game)
        logger.info(f"Created game with ID: {new_game.id}")

        # Generate questions for the game
        questions = []
        for i in range(game_data.numberOfQuestions):
            logger.info(f"Generating question {i+1}/{game_data.numberOfQuestions}")
            try:
                question_data = question_generator.generate_question(game_data.category)
                logger.info(f"Generated question data: {question_data is not None}")
                if not question_data:
                    logger.error("Question generator returned None")
                    continue
                
                logger.info("Creating question in database")
                question = Question(
                    question_text=question_data['question'],
                    correct_answer=question_data['correct_answer'],
                    options=json.dumps(question_data['options']),
                    difficulty_id=game_data.difficultyId,
                    game_id=new_game.id
                )
                questions.append(question)
            except Exception as e:
                logger.error(f"Error generating question: {str(e)}")
                logger.exception("Full traceback:")
                continue

        if not questions:
            logger.error("No questions were generated successfully")
            db.delete(new_game)
            db.commit()
            raise HTTPException(status_code=500, detail="Failed to generate questions")

        logger.info(f"Adding {len(questions)} questions to database")
        db.add_all(questions)
        db.commit()

        # Return game with questions
        return {
            "id": str(new_game.id),
            "category": new_game.category,
            "numberOfQuestions": new_game.number_of_questions,
            "difficultyId": new_game.difficulty_id,
            "currentQuestionIndex": new_game.current_question_index,
            "score": new_game.score,
            "status": new_game.status.value,
            "questions": [{
                "id": str(q.id),
                "questionText": q.question_text,
                "correctAnswer": q.correct_answer,
                "options": json.loads(q.options),
                "difficultyId": q.difficulty_id,
                "gameId": str(q.game_id),
                "createdAt": q.created_at
            } for q in questions]
        }

    except Exception as e:
        logger.error(f"Error creating game: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/games/{game_id}")
async def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.post("/check-answer")
async def check_answer(answer_data: dict):
    user_answer = answer_data.get('answer', '').upper()
    correct_answer = answer_data.get('correct_answer', '')
    
    # Extract just the letter if the answer contains full text
    if ')' in correct_answer:
        correct_answer = correct_answer.split(')')[0].strip()
    
    is_correct = user_answer == correct_answer.upper()  # Make sure both are uppercase
    return {
        "correct": is_correct,
        "correct_answer": correct_answer
    }