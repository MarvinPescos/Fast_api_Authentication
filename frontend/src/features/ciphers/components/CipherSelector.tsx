import type { CipherType, CipherInfo } from "../types/ciphers.types";

interface CipherSelectorProps {
  selectedCipher: CipherType;
  onCipherChange: (cipher: CipherType) => void;
}

const cipherInfo: Record<CipherType, CipherInfo> = {
  atbash: {
    name: "Atbash",
    description: "Reverse alphabet cipher (A=Z, B=Y, etc.)",
    example: "hello → svool",
  },
  caesar: {
    name: "Caesar",
    description: "Shift each letter by a fixed amount",
    example: "hello (shift 3) → khoor",
    requiresShift: true,
  },
  vigenere: {
    name: "Vigenère",
    description: "Keyword-based polyalphabetic cipher",
    example: "hello (key 'KEY') → rijvs",
    requiresKey: true,
  },
};

export function CipherSelector({
  selectedCipher,
  onCipherChange,
}: CipherSelectorProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Select Cipher Type
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {Object.entries(cipherInfo).map(([type, info]) => (
          <button
            key={type}
            onClick={() => onCipherChange(type as CipherType)}
            className={`p-4 border rounded-lg text-left transition-all ${
              selectedCipher === type
                ? "border-amber-500 bg-amber-50"
                : "border-gray-200 hover:border-gray-300"
            }`}
          >
            <div className="font-medium text-gray-900 mb-1">{info.name}</div>
            <div className="text-sm text-gray-600 mb-2">{info.description}</div>
            <div className="text-xs text-gray-500 font-mono">
              {info.example}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
