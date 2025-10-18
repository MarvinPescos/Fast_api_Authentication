import React from "react";
import { useJokeCipherQRStore } from "../store/jokeStore";

export function CipherSelector() {
  const { selectedCipher, setSelectedCipher } = useJokeCipherQRStore();

  const cipherOptions = [
    {
      value: null,
      label: "No Cipher",
      description: "Generate QR code directly from joke",
    },
    {
      value: "atbash",
      label: "Atbash Cipher",
      description: "Reverse alphabet cipher (A=Z, B=Y, etc.)",
    },
    {
      value: "caesar",
      label: "Caesar Cipher",
      description: "Shift each letter by a fixed amount",
    },
    {
      value: "vigenere",
      label: "Vigenère Cipher",
      description: "Keyword-based polyalphabetic cipher",
    },
  ];

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Select Cipher Type
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cipherOptions.map((option) => (
          <button
            key={option.value || "none"}
            onClick={() => setSelectedCipher(option.value)}
            className={`p-4 border rounded-lg text-left transition-colors ${
              selectedCipher === option.value
                ? "border-amber-500 bg-amber-50"
                : "border-gray-200 hover:border-gray-300"
            }`}
          >
            <div className="font-medium text-gray-900">{option.label}</div>
            <div className="text-sm text-gray-600 mt-1">
              {option.description}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
