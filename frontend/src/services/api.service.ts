import axios from 'axios';
import { Question, AnswerResponse } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const triviaService = {
  async getQuestion(category?: string): Promise<Question> {
    const response = await axios.get(`${API_URL}/api/question`, {
      params: { category }
    });
    return response.data;
  },

  async checkAnswer(answer: string, correctAnswer: string): Promise<AnswerResponse> {
    const response = await axios.post(`${API_URL}/api/check-answer`, {
      answer,
      correct_answer: correctAnswer
    });
    return response.data;
  }
};