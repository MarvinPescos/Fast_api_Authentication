import React from "react";
import { useQRGeneratorStore } from "../store/qrStore";

export function QRCodeDisplay() {
  const { qrCodeDataUrl, isLoading } = useQRGeneratorStore();

  if (isLoading) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">QR Code</h3>
        <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-amber-500"></div>
        </div>
      </div>
    );
  }

  if (!qrCodeDataUrl) {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">QR Code</h3>
        <div className="flex items-center justify-center h-64 bg-gray-50 rounded-lg">
          <p className="text-gray-500">QR code will appear here</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Generated QR Code
      </h3>
      <div className="flex flex-col items-center space-y-4">
        <img
          src={qrCodeDataUrl}
          alt="Generated QR Code"
          className="max-w-xs border border-gray-200 rounded-lg"
        />
        <button
          onClick={() => useQRGeneratorStore.getState().downloadQR()}
          className="px-4 py-2 bg-amber-500 text-white font-medium rounded-lg hover:bg-amber-600 transition-colors"
        >
          Download QR Code
        </button>
      </div>
    </div>
  );
}
