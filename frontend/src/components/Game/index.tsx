import React from 'react';
import { useTrivia } from '../../hooks/useTrivia';
import { GameControls } from './GameControls';
import QuestionDisplay from './QuestionDisplay';
import '../../styles/Game.css';

const DISCLAIMER = "Questions are generated using AI and focus on historical facts, science, and general knowledge.";

const Game = () => {
  const {
    question,
    score,
    category,
    isLoading,
    isGameStarted,
    answered,
    selectedAnswer,
    setCategory,
    handleAnswer,
    startGame
  } = useTrivia();

  return (
    <div className="game-container">
      {!isGameStarted ? (
        <GameControls
          category={category}
          onCategoryChange={setCategory}
          onStartGame={startGame}
        />
      ) : (
        <>
          {isLoading ? (
            <div className="loading">Loading...</div>
          ) : question ? (
            <QuestionDisplay
              question={question}
              score={score}
              answered={answered}
              selectedAnswer={selectedAnswer}
              onAnswer={handleAnswer}
            />
          ) : null}
        </>
      )}
      <p className="disclaimer">{DISCLAIMER}</p>
    </div>
  );
};

export default Game;
