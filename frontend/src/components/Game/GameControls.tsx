import React from 'react';
import { GameConfig } from '../../types';

interface GameControlsProps {
  config: GameConfig;
  onConfigChange: (config: Partial<GameConfig>) => void;
  onStartGame: () => void;
}

export const GameControls: React.FC<GameControlsProps> = ({
  config,
  onConfigChange,
  onStartGame
}) => (
  <div className="game-setup">
    <input
      className="category-input"
      type="text"
      placeholder="Enter category (optional)"
      value={config.category}
      onChange={(e) => onConfigChange({ category: e.target.value })}
    />
    <select
      className="difficulty-select"
      value={config.difficultyId}
      onChange={(e) => onConfigChange({ difficultyId: parseInt(e.target.value, 10) })}
    >
      <option value={1}>Beginner</option>
      <option value={2}>Easy</option>
      <option value={3}>Medium</option>
      <option value={4}>Hard</option>
      <option value={5}>Expert</option>
    </select>
    <input
      className="questions-input"
      type="number"
      min="1"
      max="20"
      value={config.numberOfQuestions}
      onChange={(e) => onConfigChange({ numberOfQuestions: parseInt(e.target.value, 10) })}
    />
    <button className="start-button" onClick={onStartGame}>
      Start Game
    </button>
  </div>
);
