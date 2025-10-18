import { z } from "zod";

export const TriviaQuestionSchema = z.object({
  type: z.string(),
  difficulty: z.string(),
  category: z.string(),
  question: z.string(),
  correct_answer: z.string(),
  incorrect_answers: z.array(z.string()),
});

export const GameStateSchema = z.object({
  currentQuestion: TriviaQuestionSchema.nullable(),
  selectedAnswer: z.string().nullable(),
  isAnswered: z.boolean(),
  isCorrect: z.boolean().nullable(),
  isLoading: z.boolean(),
  error: z.string().nullable(),
});

export type TriviaQuestionType = z.infer<typeof TriviaQuestionSchema>;
export type GameStateType = z.infer<typeof GameStateSchema>;
