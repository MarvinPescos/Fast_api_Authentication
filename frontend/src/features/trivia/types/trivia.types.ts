export interface TriviaQuestion {
  type: string;
  difficulty: string;
  category: string;
  question: string;
  correct_answer: string;
  incorrect_answers: string[];
}

export interface GameState {
  currentQuestion: TriviaQuestion | null;
  selectedAnswer: string | null;
  isAnswered: boolean;
  isCorrect: boolean | null;
  isLoading: boolean;
  error: string | null;
}

export type Difficulty = "easy" | "medium" | "hard";
export type GameStatus = "idle" | "playing" | "answered" | "finished";
