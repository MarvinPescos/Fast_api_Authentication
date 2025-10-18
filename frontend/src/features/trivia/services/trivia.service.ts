import api from "../../../shared/services/api";
import type { TriviaQuestion } from "../types/trivia.types";

export class TriviaService {
  /**
   * Fetch a single random trivia question from the backend
   */
  async getQuestion(): Promise<TriviaQuestion> {
    try {
      const response = await api.get(
        "/fullstack_authentication/activities/trivia/question"
      );
      return response as unknown as TriviaQuestion;
    } catch (error: any) {
      console.error("Failed to fetch trivia question:", error);

      // Handle rate limiting specifically
      if (error.response?.status === 429) {
        throw new Error(
          "Too many requests to trivia service. Please wait a moment and try again."
        );
      }

      throw new Error("Failed to fetch trivia question");
    }
  }
}

export const triviaService = new TriviaService();
