import type { TriviaQuestion } from "../types/trivia.types";
import { decodeHtmlEntities } from "../../../shared/utils/htmlEntities";

interface QuestionCardProps {
  question: TriviaQuestion;
  questionNumber: number;
}

export function QuestionCard({ question, questionNumber }: QuestionCardProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
      {/* Question Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <span className="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-100 rounded-full">
            Question {questionNumber}
          </span>
          <span className="px-3 py-1 text-xs font-medium text-amber-700 bg-amber-50 rounded-full">
            {question.difficulty}
          </span>
        </div>
        <span className="text-sm text-gray-500">
          {decodeHtmlEntities(question.category)}
        </span>
      </div>

      {/* Question Text */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-gray-900 leading-relaxed">
          {decodeHtmlEntities(question.question)}
        </h2>
      </div>
    </div>
  );
}
