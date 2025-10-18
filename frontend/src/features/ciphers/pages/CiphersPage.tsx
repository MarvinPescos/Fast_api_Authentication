import { useNavigate } from "react-router-dom";
import { useCiphersStore } from "../store/ciphersStore";
import { CipherSelector } from "../components/CipherSelector";
import { CipherOptions } from "../components/CipherOptions";
import { TextInput } from "../components/TextInput";
import { LoadingSpinner } from "../../../shared/components/LoadingSpinner";
import { ActivityLayout } from "../../../shared/components/ActivityLayout";

export function CiphersPage() {
  const navigate = useNavigate();
  const {
    inputText,
    outputText,
    selectedCipher,
    caesarShift,
    vigenereKey,
    isLoading,
    error,
    setInputText,
    setSelectedCipher,
    setCaesarShift,
    setVigenereKey,
    processCipher,
    clearText,
    resetState,
  } = useCiphersStore();

  const handleBackToDashboard = () => {
    navigate("/home");
  };

  const handleProcessCipher = () => {
    processCipher();
  };

  const handleClearText = () => {
    clearText();
  };

  const handleResetAll = () => {
    resetState();
  };

  return (
    <ActivityLayout
      title="Text Ciphers"
      description="Encode and decode text using various cipher algorithms"
      currentPath="/activities/ciphers"
    >
      {/* Cipher Type Selection */}
      <CipherSelector
        selectedCipher={selectedCipher}
        onCipherChange={setSelectedCipher}
      />

      {/* Cipher Options */}
      <CipherOptions
        selectedCipher={selectedCipher}
        caesarShift={caesarShift}
        vigenereKey={vigenereKey}
        onCaesarShiftChange={setCaesarShift}
        onVigenereKeyChange={setVigenereKey}
      />

      {/* Input Text */}
      <TextInput
        label="Input Text"
        value={inputText}
        onChange={setInputText}
        placeholder="Enter the text you want to cipher..."
      />

      {/* Action Buttons */}
      <div className="flex justify-center space-x-4 mb-6">
        <button
          onClick={handleProcessCipher}
          disabled={!inputText.trim() || isLoading}
          className="px-6 py-3 bg-amber-500 text-white font-medium rounded-lg hover:bg-amber-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed h-12 flex items-center justify-center"
        >
          <div className="flex items-center space-x-2 h-6">
            {isLoading ? (
              <>
                <LoadingSpinner size="sm" />
                <span>Processing...</span>
              </>
            ) : (
              "Process Cipher"
            )}
          </div>
        </button>

        <button
          onClick={handleClearText}
          className="px-6 py-3 bg-gray-500 text-white font-medium rounded-lg hover:bg-gray-600 transition-colors h-12 flex items-center justify-center"
        >
          <div className="h-6 flex items-center">Clear Text</div>
        </button>

        <button
          onClick={handleResetAll}
          className="px-6 py-3 bg-red-500 text-white font-medium rounded-lg hover:bg-red-600 transition-colors h-12 flex items-center justify-center"
        >
          <div className="h-6 flex items-center">Reset All</div>
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center space-x-2">
            <svg
              className="w-5 h-5 text-red-600"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                clipRule="evenodd"
              />
            </svg>
            <span className="text-red-800 font-medium">{error}</span>
          </div>
        </div>
      )}

      {/* Output Text */}
      {outputText && (
        <TextInput
          label="Ciphered Text"
          value={outputText}
          onChange={() => {}} // Read-only
          placeholder="Ciphered text will appear here..."
        />
      )}

      {/* Copy Button */}
      {outputText && (
        <div className="flex justify-center">
          <button
            onClick={() => navigator.clipboard.writeText(outputText)}
            className="px-4 py-2 bg-green-500 text-white font-medium rounded-lg hover:bg-green-600 transition-colors"
          >
            Copy Result
          </button>
        </div>
      )}
    </ActivityLayout>
  );
}
