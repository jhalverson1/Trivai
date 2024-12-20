export interface Question {
  question: string;
  options: string[];
  correct_answer: string;
}

export interface AnswerResponse {
  correct: boolean;
  correct_answer: string;
}
