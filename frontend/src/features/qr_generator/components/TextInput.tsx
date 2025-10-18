import React from "react";
import { useQRGeneratorStore } from "../store/qrStore";

export function TextInput() {
  const { inputText, setInputText } = useQRGeneratorStore();

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Input Text</h3>
      <textarea
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
        placeholder="Enter text or URL to generate QR code..."
        rows={4}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent resize-none"
      />
    </div>
  );
}
