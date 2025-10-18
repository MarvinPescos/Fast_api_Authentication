import React from "react";
import { useJokeCipherQRStore } from "../store/jokeStore";

export function JokeDisplay() {
  const { originalJoke, cipheredJoke, cipherUsed, qrCodeDataUrl, isLoading } =
    useJokeCipherQRStore();

  if (isLoading) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Joke & QR Code
        </h3>
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-full"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  if (!originalJoke) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Joke & QR Code
        </h3>
        <p className="text-gray-500">Generate a joke to see it here</p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Joke & QR Code
      </h3>

      <div className="space-y-6">
        {/* Original Joke */}
        <div>
          <h4 className="text-md font-medium text-gray-800 mb-2">
            Original Joke
          </h4>
          <div className="p-4 bg-gray-50 rounded-lg">
            <p className="text-gray-700">{originalJoke}</p>
          </div>
        </div>

        {/* Ciphered Joke */}
        {cipheredJoke && cipherUsed && (
          <div>
            <h4 className="text-md font-medium text-gray-800 mb-2">
              Ciphered Joke (
              {cipherUsed.charAt(0).toUpperCase() + cipherUsed.slice(1)})
            </h4>
            <div className="p-4 bg-amber-50 rounded-lg">
              <p className="text-gray-700 font-mono">{cipheredJoke}</p>
            </div>
          </div>
        )}

        {/* QR Code */}
        {qrCodeDataUrl && (
          <div>
            <h4 className="text-md font-medium text-gray-800 mb-2">QR Code</h4>
            <div className="flex flex-col items-center space-y-4">
              <img
                src={qrCodeDataUrl}
                alt="Joke QR Code"
                className="max-w-xs border border-gray-200 rounded-lg"
              />
              <button
                onClick={() => useJokeCipherQRStore.getState().downloadQR()}
                className="px-4 py-2 bg-amber-500 text-white font-medium rounded-lg hover:bg-amber-600 transition-colors"
              >
                Download QR Code
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
