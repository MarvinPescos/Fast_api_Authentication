export interface JokeCipherQRRequest {
  cipher_type?: "atbash" | "caesar" | "vigenere";
  caesar_shift?: number;
  vigenere_key?: string;
}

export interface JokeCipherQRResponse {
  original_joke: string;
  ciphered_joke?: string;
  cipher_used?: string;
  qr_code_base64: string;
}

export interface JokeCipherQRState {
  originalJoke: string;
  cipheredJoke: string | null;
  cipherUsed: string | null;
  qrCodeDataUrl: string | null;
  selectedCipher: "atbash" | "caesar" | "vigenere" | null;
  caesarShift: number;
  vigenereKey: string;
  isLoading: boolean;
  error: string | null;
}
