import React from 'react';
import { Question } from '../../types';

interface QuestionDisplayProps {
  question: Question;
  score: number;
  answered: boolean;
  selectedAnswer: string | null;
  onAnswer: (answer: string) => void;
}

const QuestionDisplay: React.FC<QuestionDisplayProps> = ({
  question,
  score,
  answered,
  selectedAnswer,
  onAnswer
}) => (
  <>
    <h2 className="score">Score: {score}</h2>
    <div>
      <h3 className="question">{question.questionText}</h3>
      <div className="options">
        {question.options.map((option, index) => (
          <button
            className={`option-button ${
              answered
                ? option.startsWith(question.correctAnswer)
                  ? 'correct'
                  : selectedAnswer === option.split(')')[0].trim()
                  ? 'wrong'
                  : ''
                : ''
            }`}
            key={index}
            onClick={() => onAnswer(option.split(')')[0].trim())}
            disabled={answered}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  </>
);

export default QuestionDisplay; 