import React from 'react';

interface GameOverProps {
  score: number;
  totalQuestions: number;
  onRestart: () => void;
}

const GameOver: React.FC<GameOverProps> = ({ score, totalQuestions, onRestart }) => (
  <div className="game-over">
    <h2>Game Over!</h2>
    <div className="stats">
      <p>Final Score: {score}/{totalQuestions}</p>
      <p>Accuracy: {((score / totalQuestions) * 100).toFixed(1)}%</p>
    </div>
    <button className="restart-button" onClick={onRestart}>
      Play Again
    </button>
  </div>
);

export default GameOver; 