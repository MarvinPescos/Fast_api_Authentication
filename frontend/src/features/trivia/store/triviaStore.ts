import { create } from "zustand";
import type { GameState } from "../types/trivia.types";
import { triviaService } from "../services/trivia.service";

interface TriviaStore extends GameState {
  // Actions
  fetchQuestion: () => Promise<void>;
  selectAnswer: (answer: string) => void;
  submitAnswer: () => void;
  nextQuestion: () => Promise<void>;
  resetGame: () => void;
}

const initialState: GameState = {
  currentQuestion: null,
  selectedAnswer: null,
  isAnswered: false,
  isCorrect: null,
  isLoading: false,
  error: null,
};

export const useTriviaStore = create<TriviaStore>((set, get) => ({
  ...initialState,

  fetchQuestion: async () => {
    set({ isLoading: true, error: null });
    try {
      const question = await triviaService.getQuestion();
      set({
        currentQuestion: question,
        selectedAnswer: null,
        isAnswered: false,
        isCorrect: null,
        isLoading: false,
      });
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Failed to fetch question",
        isLoading: false,
      });
    }
  },

  selectAnswer: (answer: string) => {
    if (get().isAnswered) return;
    set({ selectedAnswer: answer });
  },

  submitAnswer: () => {
    const { selectedAnswer, currentQuestion, isAnswered } = get();
    if (!selectedAnswer || !currentQuestion || isAnswered) return;

    const isCorrect = selectedAnswer === currentQuestion.correct_answer;

    set({
      isAnswered: true,
      isCorrect,
    });
  },

  nextQuestion: async () => {
    await get().fetchQuestion();
  },

  resetGame: () => {
    set(initialState);
  },
}));
