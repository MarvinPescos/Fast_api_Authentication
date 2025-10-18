import { useEffect, useState } from "react";
import { useCatFactsStore } from "../store/catFactsStore";
import { ActivityLayout } from "../../../shared/components/ActivityLayout";
import { LoadingSpinner } from "../../../shared/components/LoadingSpinner";

export function CatFactsPage() {
  const {
    status,
    currentFact,
    isLoading,
    error,
    fetchStatus,
    subscribe,
    unsubscribe,
    fetchRandomFact,
    clearError,
  } = useCatFactsStore();

  const [showSuccess, setShowSuccess] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    fetchStatus();
    fetchRandomFact();
  }, []);

  const handleSubscribe = async () => {
    try {
      await subscribe("09:00:00", "UTC");
      setSuccessMessage("Successfully subscribed to daily cat facts! 🐱");
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 5000);
    } catch (error) {
      // Error is already set in the store
      console.error("Subscribe error:", error);
    }
  };

  const handleUnsubscribe = async () => {
    try {
      await unsubscribe();
      setSuccessMessage("Successfully unsubscribed from daily cat facts 😿");
      setShowSuccess(true);
      setTimeout(() => setShowSuccess(false), 5000);
    } catch (error) {
      console.error("Unsubscribe error:", error);
    }
  };

  const handleGetNewFact = () => {
    fetchRandomFact();
  };

  return (
    <ActivityLayout
      title="Cat Facts Subscription"
      description="Subscribe to receive daily cat facts in your email"
      currentPath="/activities/cat-facts"
    >
      {/* Current Cat Fact Display */}
      <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-6 mb-6 border-2 border-purple-200">
        <div className="flex items-start gap-4">
          <div className="text-5xl">🐱</div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-800 mb-2">
              Random Cat Fact
            </h3>
            {isLoading && !currentFact ? (
              <div className="flex items-center gap-2">
                <LoadingSpinner size="sm" />
                <span className="text-gray-600">Loading cat fact...</span>
              </div>
            ) : currentFact ? (
              <div>
                <p className="text-gray-700 text-base leading-relaxed mb-3">
                  {currentFact.fact}
                </p>
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span>Source: {currentFact.source}</span>
                  <span>•</span>
                  <span>{currentFact.length} characters</span>
                </div>
              </div>
            ) : (
              <p className="text-gray-600">
                Click the button below to fetch a cat fact!
              </p>
            )}
          </div>
        </div>
        <button
          onClick={handleGetNewFact}
          disabled={isLoading}
          className="mt-4 px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          {isLoading ? "Loading..." : "Get New Fact"}
        </button>
      </div>

      {/* Subscription Status Card */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-4">
          Email Subscription
        </h3>

        {status?.subscribed ? (
          <div className="space-y-4">
            <div className="flex items-center gap-2 text-green-600 mb-3">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="font-medium">You're subscribed!</span>
            </div>

            {status.subscription && (
              <div className="bg-gray-50 rounded-lg p-4 space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Preferred Time:</span>
                  <span className="font-medium text-gray-800">
                    {status.subscription.preferred_time}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Timezone:</span>
                  <span className="font-medium text-gray-800">
                    {status.subscription.timezone}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Facts Sent:</span>
                  <span className="font-medium text-gray-800">
                    {status.subscription.total_sent}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Last Sent:</span>
                  <span className="font-medium text-gray-800">
                    {status.subscription.last_sent_at
                      ? new Date(
                          status.subscription.last_sent_at
                        ).toLocaleDateString()
                      : "Never"}
                  </span>
                </div>
              </div>
            )}

            <button
              onClick={handleUnsubscribe}
              disabled={isLoading}
              className="w-full px-6 py-3 bg-red-500 text-white font-medium rounded-lg hover:bg-red-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              {isLoading ? "Processing..." : "Unsubscribe"}
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <p className="text-gray-600">
              Subscribe to receive daily cat facts delivered to your email inbox
              every day at 9:00 AM UTC.
            </p>

            <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
              <div className="flex items-start">
                <div className="text-2xl mr-3">📧</div>
                <div>
                  <h4 className="font-semibold text-blue-800 mb-1">
                    What you'll get:
                  </h4>
                  <ul className="text-sm text-blue-700 space-y-1">
                    <li>• Daily cat facts delivered to your email</li>
                    <li>• Fun and educational content</li>
                    <li>• Unsubscribe anytime</li>
                  </ul>
                </div>
              </div>
            </div>

            <button
              onClick={handleSubscribe}
              disabled={isLoading}
              className="w-full px-6 py-3 bg-purple-500 text-white font-medium rounded-lg hover:bg-purple-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              {isLoading ? "Processing..." : "Subscribe to Daily Cat Facts"}
            </button>
          </div>
        )}
      </div>

      {/* Success Message */}
      {showSuccess && (
        <div className="bg-green-50 border-l-4 border-green-400 p-4 rounded-lg mb-4">
          <div className="flex items-center">
            <svg
              className="w-5 h-5 text-green-600 mr-2"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clipRule="evenodd"
              />
            </svg>
            <p className="text-green-700 font-medium">{successMessage}</p>
          </div>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-lg mb-4">
          <div className="flex items-start justify-between">
            <div className="flex items-center">
              <svg
                className="w-5 h-5 text-red-600 mr-2"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
              <p className="text-red-700 font-medium">{error}</p>
            </div>
            <button
              onClick={clearError}
              className="text-red-600 hover:text-red-800"
            >
              ×
            </button>
          </div>
        </div>
      )}
    </ActivityLayout>
  );
}
