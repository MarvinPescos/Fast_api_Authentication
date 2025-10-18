import { decodeHtmlEntities } from "../../../shared/utils/htmlEntities";

interface AnswerButtonProps {
  answer: string;
  isSelected: boolean;
  isCorrect: boolean | null;
  isAnswered: boolean;
  onClick: () => void;
}

export function AnswerButton({
  answer,
  isSelected,
  isCorrect,
  isAnswered,
  onClick,
}: AnswerButtonProps) {
  const getButtonStyles = () => {
    if (!isAnswered) {
      return isSelected
        ? "bg-amber-500 text-white border-amber-500"
        : "bg-white text-gray-700 border-gray-300 hover:border-gray-400";
    }

    // After answering
    if (answer === "correct") {
      return "bg-green-500 text-white border-green-500";
    }
    if (isSelected && !isCorrect) {
      return "bg-red-500 text-white border-red-500";
    }
    return "bg-gray-100 text-gray-500 border-gray-200";
  };

  return (
    <button
      onClick={onClick}
      disabled={isAnswered}
      className={`w-full p-4 text-left border rounded-lg transition-all ${getButtonStyles()} ${
        !isAnswered ? "hover:shadow-md" : ""
      } disabled:cursor-not-allowed`}
    >
      <div className="flex items-center justify-between">
        <span className="font-medium">{decodeHtmlEntities(answer)}</span>
        {isAnswered && answer === "correct" && (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
              clipRule="evenodd"
            />
          </svg>
        )}
        {isAnswered && isSelected && !isCorrect && (
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clipRule="evenodd"
            />
          </svg>
        )}
      </div>
    </button>
  );
}
