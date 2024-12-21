import axios from 'axios';
import { Question, Game, GameConfig, AnswerResponse } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

export const triviaService = {
  async createGame(config: GameConfig): Promise<Game> {
    const response = await axios.post(`${API_URL}/api/games`, config);
    return response.data;
  },

  async getGame(gameId: string): Promise<Game> {
    const response = await axios.get(`${API_URL}/api/games/${gameId}`);
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