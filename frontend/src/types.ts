export interface Difficulty {
  id: number;
  name: string;
  description: string;
}

export interface Game {
  id: string;
  category: string;
  numberOfQuestions: number;
  difficultyId: number;
  difficulty: Difficulty;
  currentQuestionIndex: number;
  score: number;
  status: 'pending' | 'in_progress' | 'completed';
  questions: Question[];
  createdAt: Date;
  updatedAt: Date;
}

export interface Question {
  id: string;
  questionText: string;
  options: string[];
  correctAnswer: string;
  difficultyId: number;
  difficulty: Difficulty;
  gameId: string;
}

export interface GameConfig {
  category: string;
  numberOfQuestions: number;
  difficultyId: number;
}

export interface AnswerResponse {
  correct: boolean;
  correct_answer: string;
}
