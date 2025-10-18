import type { CipherType } from "../types/ciphers.types";

interface CipherOptionsProps {
  selectedCipher: CipherType;
  caesarShift: number;
  vigenereKey: string;
  onCaesarShiftChange: (shift: number) => void;
  onVigenereKeyChange: (key: string) => void;
}

export function CipherOptions({
  selectedCipher,
  caesarShift,
  vigenereKey,
  onCaesarShiftChange,
  onVigenereKeyChange,
}: CipherOptionsProps) {
  if (selectedCipher === "caesar") {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Caesar Cipher Options
        </h3>

        <div>
          <label
            htmlFor="caesar-shift"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Shift Amount (1-25)
          </label>
          <input
            id="caesar-shift"
            type="number"
            min="1"
            max="25"
            value={caesarShift}
            onChange={(e) => onCaesarShiftChange(parseInt(e.target.value) || 1)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
          />
          <p className="text-xs text-gray-500 mt-1">
            Each letter will be shifted by this amount in the alphabet
          </p>
        </div>
      </div>
    );
  }

  if (selectedCipher === "vigenere") {
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Vigenère Cipher Options
        </h3>

        <div>
          <label
            htmlFor="vigenere-key"
            className="block text-sm font-medium text-gray-700 mb-2"
          >
            Encryption Key
          </label>
          <input
            id="vigenere-key"
            type="text"
            value={vigenereKey}
            onChange={(e) => onVigenereKeyChange(e.target.value)}
            placeholder="Enter encryption key (letters only)"
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
          />
          <p className="text-xs text-gray-500 mt-1">
            Key must contain only letters and spaces
          </p>
        </div>
      </div>
    );
  }

  return null;
}
