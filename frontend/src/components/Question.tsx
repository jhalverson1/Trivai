import React from 'react';
import type { Question as QuestionType } from '../types';

interface QuestionProps {
  question: QuestionType;
  onAnswer: (answer: string) => void;
}

const Question: React.FC<QuestionProps> = ({ question, onAnswer }) => {
  return (
    <div>
      <h3>{question.question}</h3>
      <div className="options">
        {question.options.map((option: string, index: number) => (
          <button
            key={index}
            onClick={() => onAnswer(option.split(')')[0].trim())}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Question; 