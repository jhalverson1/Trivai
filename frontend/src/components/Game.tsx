import React, { useState } from 'react';
import axios from 'axios';
import { Question, AnswerResponse } from '../types';
import './Game.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const DISCLAIMER = "Questions are generated using AI and focus on historical facts, science, and general knowledge.";

const Game = () => {
  const [question, setQuestion] = useState<Question | null>(null);
  const [score, setScore] = useState(0);
  const [category, setCategory] = useState('');
  const [isGameStarted, setIsGameStarted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const fetchQuestion = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get(`${API_URL}/api/question`, {
        params: { category: category || undefined }
      });
      setQuestion(response.data);
    } catch (error) {
      console.error('Error fetching question:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnswer = async (answer: string) => {
    if (!question || isLoading) return;
    setIsLoading(true);

    try {
      const response = await axios.post<AnswerResponse>(`${API_URL}/api/check-answer`, {
        answer,
        correct_answer: question.correct_answer
      });

      if (response.data.correct) {
        setScore(prev => prev + 1);
      }
      
      await fetchQuestion();
    } catch (error) {
      console.error('Error checking answer:', error);
      setIsLoading(false);
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
            className="category-input"
            type="text"
            placeholder="Enter category (optional)"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
          />
          <button className="start-button" onClick={startGame}>
            Start Game
          </button>
        </div>
      ) : (
        <>
          <h2 className="score">Score: {score}</h2>
          {isLoading ? (
            <div className="loading">Loading...</div>
          ) : question ? (
            <div>
              <h3 className="question">{question.question}</h3>
              <div className="options">
                {question.options.map((option, index) => (
                  <button
                    className="option-button"
                    key={index}
                    onClick={() => handleAnswer(option.split(')')[0].trim())}
                    disabled={isLoading}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>
          ) : null}
        </>
      )}
      <p className="disclaimer">{DISCLAIMER}</p>
    </div>
  );
};

export default Game; 