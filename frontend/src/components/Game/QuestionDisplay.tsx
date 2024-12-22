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
}) => {
  const handleAnswerClick = (option: string) => {
    const answer = option.match(/[A-D]/)?.[0] || '';
    console.log('Selected answer:', answer);
    console.log('Correct answer:', question.correctAnswer);
    onAnswer(answer);
  };

  return (
    <>
      <h2 className="score">Score: {score}</h2>
      <div>
        <h3 className="question">{question.questionText}</h3>
        <div className="options">
          {question.options.map((option, index) => (
            <button
              className={`option-button ${
                answered
                  ? selectedAnswer === option.match(/[A-D]/)?.[0]
                    ? selectedAnswer === question.correctAnswer.toUpperCase()
                      ? 'correct'
                      : 'wrong'
                    : option.match(/[A-D]/)?.[0] === question.correctAnswer.toUpperCase()
                      ? 'correct'
                      : ''
                  : ''
              }`}
              key={index}
              onClick={() => handleAnswerClick(option)}
              disabled={answered}
            >
              {option}
            </button>
          ))}
        </div>
      </div>
    </>
  );
};

export default QuestionDisplay; 