import { useState } from 'react';
import { Question } from '../types';
import { triviaService } from '../services/api.service';

export const useTrivia = () => {
  const [question, setQuestion] = useState<Question | null>(null);
  const [nextQuestion, setNextQuestion] = useState<Question | null>(null);
  const [score, setScore] = useState(0);
  const [category, setCategory] = useState('');
  const [isGameStarted, setIsGameStarted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingNext, setLoadingNext] = useState(false);
  const [answered, setAnswered] = useState(false);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);

  const fetchNextQuestion = async () => {
    setLoadingNext(true);
    try {
      const data = await triviaService.getQuestion(category);
      setNextQuestion(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoadingNext(false);
    }
  };

  const handleAnswer = async (answer: string) => {
    if (!question || isLoading) return;
    setSelectedAnswer(answer);
    setAnswered(true);
    
    try {
      const response = await triviaService.checkAnswer(answer, question.correct_answer);
      if (response.correct) {
        setScore(prev => prev + 1);
      }
      
      if (!nextQuestion && !loadingNext) {
        await fetchNextQuestion();
      }
      
      setTimeout(() => {
        if (nextQuestion) {
          setQuestion(nextQuestion);
          setNextQuestion(null);
          setAnswered(false);
          setSelectedAnswer(null);
          fetchNextQuestion();
        }
      }, 1500);
    } catch (error) {
      console.error(error);
      setAnswered(false);
      setSelectedAnswer(null);
    }
  };

  const startGame = async () => {
    setIsGameStarted(true);
    setIsLoading(true);
    try {
      const data = await triviaService.getQuestion(category);
      setQuestion(data);
      fetchNextQuestion();
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return {
    question,
    nextQuestion,
    score,
    category,
    isLoading,
    isGameStarted,
    answered,
    selectedAnswer,
    setCategory,
    handleAnswer,
    startGame
  };
};