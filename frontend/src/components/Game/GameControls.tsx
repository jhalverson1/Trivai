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
    <div className="input-group">
      <label htmlFor="category">Category</label>
      <input
        id="category"
        className="category-input"
        type="text"
        placeholder="Enter category (e.g., History, Science)"
        value={config.category}
        onChange={(e) => onConfigChange({ category: e.target.value })}
      />
    </div>
    
    <div className="input-group">
      <label htmlFor="difficulty">Difficulty</label>
      <select
        id="difficulty"
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
    </div>
    
    <div className="input-group">
      <label htmlFor="questions">Questions</label>
      <input
        id="questions"
        className="questions-input"
        type="number"
        min="1"
        max="20"
        value={config.numberOfQuestions}
        onChange={(e) => onConfigChange({ numberOfQuestions: parseInt(e.target.value, 10) })}
      />
    </div>
    
    <button className="start-button" onClick={onStartGame}>
      Start Game
    </button>
  </div>
);
