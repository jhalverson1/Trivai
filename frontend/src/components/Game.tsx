import React, { useState } from 'react';
import axios from 'axios';
import { Question, AnswerResponse } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const Game = () => {
  const [question, setQuestion] = useState<Question | null>(null);
  const [score, setScore] = useState(0);
  const [category, setCategory] = useState('');
  const [isGameStarted, setIsGameStarted] = useState(false);

  const fetchQuestion = async () => {
    try {
      console.log('Fetching from:', `${API_URL}/api/question`);
      const response = await axios.get(`${API_URL}/api/question`, {
        params: {
          category: category || undefined
        }
      });
      setQuestion(response.data);
    } catch (error) {
      console.error('Error fetching question:', error);
    }
  };

  const handleAnswer = async (answer: string) => {
    if (!question) return;

    try {
      const response = await axios.post<AnswerResponse>(`${API_URL}/api/check-answer`, {
        answer,
        correct_answer: question.correct_answer
      });

      if (response.data.correct) {
        setScore(prev => prev + 1);
        alert('Correct! 🎉');
      } else {
        alert(`Wrong! The correct answer was ${response.data.correct_answer}`);
      }

      fetchQuestion();
    } catch (error) {
      console.error('Error checking answer:', error);
    }
  };

  const startGame = () => {
    setIsGameStarted(true);
    fetchQuestion();
  };

  return (
    <div className="game-container">
      {!isGameStarted ? (
        <div>
          <input
            type="text"
            placeholder="Enter category (optional)"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          />
          <button onClick={startGame}>Start Game</button>
        </div>
      ) : (
        <>
          <h2>Score: {score}</h2>
          {question && (
            <div>
              <h3>{question.question}</h3>
              <div className="options">
                {question.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => handleAnswer(option.split(')')[0].trim())}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default Game; 