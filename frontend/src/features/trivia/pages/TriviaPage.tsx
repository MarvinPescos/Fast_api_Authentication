import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTriviaStore } from "../store/triviaStore";
import { QuestionCard } from "../components/QuestionCard";
import { AnswerButton } from "../components/AnswerButton";
import { LoadingSpinner } from "../../../shared/components/LoadingSpinner";
import { ActivityLayout } from "../../../shared/components/ActivityLayout";
import { decodeHtmlEntities } from "../../../shared/utils/htmlEntities";

export function TriviaPage() {
  const navigate = useNavigate();
  const {
    currentQuestion,
    selectedAnswer,
    isAnswered,
    isCorrect,
    isLoading,
    error,
    fetchQuestion,
    selectAnswer,
    submitAnswer,
    nextQuestion,
    resetGame,
  } = useTriviaStore();

  const [shuffledAnswers, setShuffledAnswers] = useState<string[]>([]);

  useEffect(() => {
    fetchQuestion();
  }, [fetchQuestion]);

  useEffect(() => {
    if (currentQuestion) {
      const answers = [
        currentQuestion.correct_answer,
        ...currentQuestion.incorrect_answers,
      ];
      setShuffledAnswers(answers.sort(() => Math.random() - 0.5));
    }
  }, [currentQuestion]);

  const handleAnswerSelect = (answer: string) => {
    selectAnswer(answer);
  };

  const handleSubmitAnswer = () => {
    submitAnswer();
  };

  const handleNextQuestion = () => {
    nextQuestion();
  };

  const handleResetGame = () => {
    resetGame();
    fetchQuestion();
  };

  const handleBackToDashboard = () => {
    navigate("/home");
  };

  if (isLoading && !currentQuestion) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner size="lg" text="Loading trivia question..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md mx-auto text-center">
          <div className="bg-white border border-red-200 rounded-lg p-6">
            <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg
                className="w-6 h-6 text-red-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Error Loading Question
            </h3>
            <p className="text-gray-600 mb-4">{error}</p>
            <div className="flex space-x-3">
              <button
                onClick={handleResetGame}
                className="px-4 py-2 bg-amber-500 text-white rounded-lg hover:bg-amber-600 transition-colors"
              >
                Try Again
              </button>
              <button
                onClick={handleBackToDashboard}
                className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                Back to Dashboard
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <ActivityLayout
      title="Trivia Game"
      description="Test your knowledge with random trivia questions"
      currentPath="/activities/trivia"
    >
      {/* Question Card */}
      {currentQuestion && (
        <QuestionCard question={currentQuestion} questionNumber={1} />
      )}

      {/* Answer Options */}
      {currentQuestion && (
        <div className="space-y-3 mb-6">
          {shuffledAnswers.map((answer, index) => (
            <AnswerButton
              key={index}
              answer={answer}
              isSelected={selectedAnswer === answer}
              isCorrect={isCorrect}
              isAnswered={isAnswered}
              onClick={() => handleAnswerSelect(answer)}
            />
          ))}
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4">
        {!isAnswered ? (
          <button
            onClick={handleSubmitAnswer}
            disabled={!selectedAnswer}
            className="px-6 py-3 bg-amber-500 text-white font-medium rounded-lg hover:bg-amber-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            Submit Answer
          </button>
        ) : (
          <button
            onClick={handleNextQuestion}
            disabled={isLoading}
            className="px-6 py-3 bg-amber-500 text-white font-medium rounded-lg hover:bg-amber-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            {isLoading ? "Loading..." : "Next Question"}
          </button>
        )}

        <button
          onClick={handleResetGame}
          className="px-6 py-3 bg-gray-500 text-white font-medium rounded-lg hover:bg-gray-600 transition-colors"
        >
          Reset Game
        </button>
      </div>

      {/* Answer Feedback */}
      {isAnswered && (
        <div className="mt-6 p-4 rounded-lg text-center">
          {isCorrect ? (
            <div className="text-green-600 bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center justify-center space-x-2">
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                    clipRule="evenodd"
                  />
                </svg>
                <span className="font-medium">Correct! Well done!</span>
              </div>
            </div>
          ) : (
            <div className="text-red-600 bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center justify-center space-x-2">
                <svg
                  className="w-5 h-5"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
                <span className="font-medium">
                  Incorrect. The correct answer was:{" "}
                  {currentQuestion &&
                    decodeHtmlEntities(currentQuestion.correct_answer)}
                </span>
              </div>
            </div>
          )}
        </div>
      )}
    </ActivityLayout>
  );
}
