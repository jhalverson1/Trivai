import React from 'react';
import { useTrivia } from '../../hooks/useTrivia';
import { GameControls } from './GameControls';
import QuestionDisplay from './QuestionDisplay';
import GameOver from './GameOver';
import '../../styles/Game.css';

const DISCLAIMER = "Questions are generated using AI and focus on historical facts, science, and general knowledge.";

const Game = () => {
  const {
    game,
    config,
    isLoading,
    answered,
    selectedAnswer,
    updateConfig,
    handleAnswer,
    startGame,
    resetGame
  } = useTrivia();

  const currentQuestion = game && game.questions ? 
    game.questions[game.currentQuestionIndex] : null;

  return (
    <div className="game-container">
      {!game ? (
        <GameControls
          config={config}
          onConfigChange={updateConfig}
          onStartGame={startGame}
        />
      ) : (
        <>
          {isLoading ? (
            <div className="loading">Loading...</div>
          ) : game.status === 'completed' ? (
            <GameOver
              score={game.score}
              totalQuestions={game.questions.length}
              onRestart={resetGame}
            />
          ) : currentQuestion ? (
            <QuestionDisplay
              question={currentQuestion}
              score={game.score}
              answered={answered}
              selectedAnswer={selectedAnswer}
              onAnswer={handleAnswer}
            />
          ) : (
            <div>No questions available</div>
          )}
        </>
      )}
      <p className="disclaimer">{DISCLAIMER}</p>
    </div>
  );
};

export default Game;
