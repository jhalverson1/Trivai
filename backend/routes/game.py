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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
question_generator = QuestionGenerator()

@router.post("/games/", response_model=GameResponse)
async def create_game(game_config: GameCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new game with config: {game_config}")
    try:
        difficulty = db.query(Difficulty).filter(
            Difficulty.id == game_config.difficultyId
        ).first()
        if not difficulty:
            raise HTTPException(status_code=400, detail=f"Difficulty with ID {game_config.difficultyId} not found")

        new_game = Game(
            category=game_config.category,
            number_of_questions=game_config.numberOfQuestions,
            difficulty_id=game_config.difficultyId,
            status=GameStatus.in_progress
        )
        db.add(new_game)
        db.flush()

        questions = []
        logger.info(f"Generating {game_config.numberOfQuestions} questions")
        for i in range(game_config.numberOfQuestions):
            question_data = question_generator.generate_question(game_config.category)
            logger.info(f"Generated question {i+1}: {question_data}")
            question = Question(
                question_text=question_data["question"],
                correct_answer=question_data["correct_answer"],
                options=json.dumps(question_data["options"]),
                difficulty_id=game_config.difficultyId,
                game_id=new_game.id
            )
            questions.append(question)

        db.bulk_save_objects(questions)
        db.commit()
        db.refresh(new_game)

        # Convert to frontend format
        game_dict = {
            "id": str(new_game.id),
            "category": new_game.category,
            "numberOfQuestions": new_game.number_of_questions,
            "difficultyId": new_game.difficulty_id,
            "currentQuestionIndex": new_game.current_question_index,
            "score": new_game.score,
            "status": new_game.status.value,
            "createdAt": new_game.created_at,
            "updatedAt": new_game.updated_at,
            "questions": [{
                "id": str(q.id),
                "questionText": q.question_text,
                "correctAnswer": q.correct_answer,
                "options": json.loads(q.options),
                "difficultyId": q.difficulty_id,
                "gameId": str(q.game_id),
                "createdAt": q.created_at
            } for q in new_game.questions]
        }

        logger.info(f"Returning game with {len(game_dict['questions'])} questions")
        logger.info(f"Game data: {game_dict}")
        return game_dict

    except Exception as e:
        logger.error(f"Error creating game: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/games/{game_id}", response_model=GameResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
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