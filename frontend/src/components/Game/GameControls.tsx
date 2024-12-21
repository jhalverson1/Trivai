interface GameControlsProps {
  category: string;
  onCategoryChange: (value: string) => void;
  onStartGame: () => void;
}

export const GameControls: React.FC<GameControlsProps> = ({
  category,
  onCategoryChange,
  onStartGame
}) => (
  <div>
    <input
      className="category-input"
      type="text"
      placeholder="Enter category (optional)"
      value={category}
      onChange={(e) => onCategoryChange(e.target.value)}
    />
    <button className="start-button" onClick={onStartGame}>
      Start Game
    </button>
  </div>
);
