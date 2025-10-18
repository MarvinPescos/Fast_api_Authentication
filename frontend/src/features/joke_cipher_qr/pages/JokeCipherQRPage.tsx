import React from "react";
import { useNavigate } from "react-router-dom";
import { useJokeCipherQRStore } from "../store/jokeStore";
import { CipherSelector } from "../components/CipherSelector";
import { CipherOptions } from "../components/CipherOptions";
import { JokeDisplay } from "../components/JokeDisplay";
import { LoadingSpinner } from "../../../shared/components/LoadingSpinner";
import { ActivityLayout } from "../../../shared/components/ActivityLayout";

export function JokeCipherQRPage() {
  const navigate = useNavigate();
  const { isLoading, error, generateJokeCipherQR, reset } =
    useJokeCipherQRStore();

  const handleBackToDashboard = () => {
    navigate("/home");
  };

  const handleGenerate = async () => {
    await generateJokeCipherQR();
  };

  const handleReset = () => {
    reset();
  };

  return (
    <ActivityLayout
      title="Joke Cipher QR"
      description="Fetch jokes, apply ciphers, and generate QR codes"
      currentPath="/activities/joke-cipher-qr"
    >
      <CipherSelector />
      <CipherOptions />

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4 mb-6">
        <button
          onClick={handleGenerate}
          disabled={isLoading}
          className="px-6 py-3 bg-amber-500 text-white font-medium rounded-lg hover:bg-amber-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed h-12 flex items-center justify-center"
        >
          <div className="flex items-center space-x-2 h-6">
            {isLoading ? (
              <>
                <LoadingSpinner size="sm" />
                <span>Generating...</span>
              </>
            ) : (
              "Generate Joke & QR"
            )}
          </div>
        </button>

        <button
          onClick={handleReset}
          className="px-6 py-3 bg-gray-500 text-white font-medium rounded-lg hover:bg-gray-600 transition-colors h-12 flex items-center justify-center"
        >
          <div className="h-6 flex items-center">Reset</div>
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center space-x-2">
            <div className="text-red-500">⚠️</div>
            <div>
              <p className="font-medium text-red-800">Error</p>
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      <JokeDisplay />
    </ActivityLayout>
  );
}
