import axios from 'axios';
import { Question, Game, GameConfig, AnswerResponse } from '../types';

// Ensure URL has protocol and no trailing slashes
const API_URL = process.env.REACT_APP_API_URL?.startsWith('http') 
  ? process.env.REACT_APP_API_URL.replace(/\/+$/, '')
  : `https://${process.env.REACT_APP_API_URL}`.replace(/\/+$/, '') || 'http://localhost:8080';

console.log('API_URL:', API_URL); // Debug log

export const triviaService = {
  async createGame(config: GameConfig): Promise<Game> {
    console.log('Making request to:', `${API_URL}/api/games`);  // Debug log
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