import React from "react";
import { useNavigate } from "react-router-dom";
import { useQRGeneratorStore } from "../store/qrStore";
import { TextInput } from "../components/TextInput";
import { QRCodeDisplay } from "../components/QRCodeDisplay";
import { LoadingSpinner } from "../../../shared/components/LoadingSpinner";
import { ActivityLayout } from "../../../shared/components/ActivityLayout";

export function QRGeneratorPage() {
  const navigate = useNavigate();
  const { inputText, isLoading, error, generateQR, reset } =
    useQRGeneratorStore();

  const handleBackToDashboard = () => {
    navigate("/home");
  };

  const handleGenerateQR = async () => {
    await generateQR();
  };

  const handleReset = () => {
    reset();
  };

  return (
    <ActivityLayout
      title="QR Generator"
      description="Generate QR codes from any text or URL"
      currentPath="/activities/qr-generator"
    >
      <TextInput />

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4 mb-6">
        <button
          onClick={handleGenerateQR}
          disabled={!inputText.trim() || isLoading}
          className="px-6 py-3 bg-amber-500 text-white font-medium rounded-lg hover:bg-amber-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed h-12 flex items-center justify-center"
        >
          <div className="flex items-center space-x-2 h-6">
            {isLoading ? (
              <>
                <LoadingSpinner size="sm" />
                <span>Generating...</span>
              </>
            ) : (
              "Generate QR Code"
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

      <QRCodeDisplay />
    </ActivityLayout>
  );
}
