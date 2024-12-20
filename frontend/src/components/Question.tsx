import React from 'react';
import { QuestionData } from '../types';

interface QuestionProps {
  question: QuestionData;
  onAnswer: (answer: string) => void;
  onQuit: () => void;
}

const Question: React.FC<QuestionProps> = ({ question, onAnswer, onQuit }) => {
  return (
    <div className="question-container">
      <h3>{question.question}</h3>
      <div className="options">
        {question.options.map((option, index) => (
          <button
            key={index}
            onClick={() => onAnswer(option.split(')')[0].trim())}
            className="option-button"
          >
            {option}
          </button>
        ))}
      </div>
      <button onClick={onQuit} className="quit-button">
        Quit Game
      </button>
    </div>
  );
};

export default Question; 