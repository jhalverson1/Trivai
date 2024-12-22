import { useState } from 'react';
import { Question, Game, GameConfig } from '../types';
import { triviaService } from '../services/api.service';

export const useTrivia = () => {
  const [game, setGame] = useState<Game | null>(null);
  const [config, setConfig] = useState<GameConfig>({
    category: '',
    numberOfQuestions: 1,
    difficultyId: 3  // Medium difficulty
  });
  const [isLoading, setIsLoading] = useState(false);
  const [answered, setAnswered] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);

  const updateConfig = (updates: Partial<GameConfig>) => {
    setConfig(prev => ({ ...prev, ...updates }));
  };

  const startGame = async () => {
    setIsLoading(true);
    try {
      const newGame = await triviaService.createGame(config);
      setGame(newGame);
    } catch (error) {
      console.error('Error starting game:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnswer = async (answer: string) => {
    if (!game || isLoading) return;
    setSelectedAnswer(answer);
    setAnswered(true);
    
    try {
      const currentQuestion = game.questions[game.currentQuestionIndex];
      const response = await triviaService.checkAnswer(answer, currentQuestion.correctAnswer);
      
      if (response.correct) {
        setGame(prev => prev ? { ...prev, score: prev.score + 1 } : null);
      }
      
      // Move to next question after 1.5 seconds
      setTimeout(() => {
        setGame(prev => {
          if (!prev) return null;
          const nextIndex = prev.currentQuestionIndex + 1;
          return {
            ...prev,
            currentQuestionIndex: nextIndex,
            status: nextIndex >= prev.questions.length ? 'completed' : 'in_progress'
          };
        });
        setAnswered(false);
        setSelectedAnswer(null);
      }, 1500);
    } catch (error) {
      console.error('Error checking answer:', error);
      // Still move to next question even if there's an error
      setTimeout(() => {
        setGame(prev => {
          if (!prev) return null;
          const nextIndex = prev.currentQuestionIndex + 1;
          return {
            ...prev,
            currentQuestionIndex: nextIndex,
            status: nextIndex >= prev.questions.length ? 'completed' : 'in_progress'
          };
        });
        setAnswered(false);
        setSelectedAnswer(null);
      }, 1500);
    }
  };

  const resetGame = () => {
    setGame(null);
    setAnswered(false);
    setSelectedAnswer(null);
    setIsLoading(false);
  };

  return {
    game,
    config,
    isLoading,
    answered,
    selectedAnswer,
    updateConfig,
    handleAnswer,
    startGame,
    resetGame
  };
};