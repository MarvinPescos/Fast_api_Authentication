import React from "react";
import { useJokeCipherQRStore } from "../store/jokeStore";

export function CipherOptions() {
  const {
    selectedCipher,
    caesarShift,
    setCaesarShift,
    vigenereKey,
    setVigenereKey,
  } = useJokeCipherQRStore();

  if (!selectedCipher) {
    return null;
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Cipher Options
      </h3>

      {selectedCipher === "caesar" && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Caesar Shift (1-25)
          </label>
          <input
            type="number"
            value={caesarShift}
            onChange={(e) => setCaesarShift(parseInt(e.target.value))}
            min="1"
            max="25"
            className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent"
          />
        </div>
      )}

      {selectedCipher === "vigenere" && (
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Vigenère Key
          </label>
          <input
            type="text"
            value={vigenereKey}
            onChange={(e) => setVigenereKey(e.target.value)}
            className="block w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent"
            placeholder="e.g., SECRET"
          />
        </div>
      )}

      {selectedCipher === "atbash" && (
        <p className="text-sm text-gray-600">
          No specific options for Atbash Cipher.
        </p>
      )}
    </div>
  );
}
