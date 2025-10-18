export interface CipherRequest {
  text: string;
  shift?: number; // For Caesar cipher
  key?: string; // For Vigenère cipher
}

export interface CipherResponse {
  result: string;
}

export interface CipherState {
  inputText: string;
  outputText: string;
  selectedCipher: CipherType;
  caesarShift: number;
  vigenereKey: string;
  isLoading: boolean;
  error: string | null;
}

export type CipherType = "atbash" | "caesar" | "vigenere";

export interface CipherInfo {
  name: string;
  description: string;
  example: string;
  requiresShift?: boolean;
  requiresKey?: boolean;
}
