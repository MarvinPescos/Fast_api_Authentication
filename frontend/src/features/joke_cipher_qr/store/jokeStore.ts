import { create } from "zustand";
import type { JokeCipherQRState } from "../types/joke.types";
import { jokeCipherQRService } from "../services/joke.service";
import { JokeCipherQRRequestSchema } from "../schemas/joke.schema";
import { ZodError } from "zod";

interface JokeCipherQRStore extends JokeCipherQRState {
  setSelectedCipher: (cipher: "atbash" | "caesar" | "vigenere" | null) => void;
  setCaesarShift: (shift: number) => void;
  setVigenereKey: (key: string) => void;
  generateJokeCipherQR: () => Promise<void>;
  downloadQR: () => void;
  reset: () => void;
}

const initialState: JokeCipherQRState = {
  originalJoke: "",
  cipheredJoke: null,
  cipherUsed: null,
  qrCodeDataUrl: null,
  selectedCipher: null,
  caesarShift: 3,
  vigenereKey: "SECRET",
  isLoading: false,
  error: null,
};

export const useJokeCipherQRStore = create<JokeCipherQRStore>((set, get) => ({
  ...initialState,

  setSelectedCipher: (cipher) => set({ selectedCipher: cipher }),
  setCaesarShift: (shift) => set({ caesarShift: shift }),
  setVigenereKey: (key) => set({ vigenereKey: key }),

  generateJokeCipherQR: async () => {
    set({ isLoading: true, error: null });
    const { selectedCipher, caesarShift, vigenereKey } = get();

    try {
      const payload: any = {};

      if (selectedCipher) {
        payload.cipher_type = selectedCipher;
        if (selectedCipher === "caesar") {
          payload.caesar_shift = caesarShift;
        } else if (selectedCipher === "vigenere") {
          payload.vigenere_key = vigenereKey;
        }
      }

      const validatedPayload = JokeCipherQRRequestSchema.parse(payload);
      const response = await jokeCipherQRService.generateJokeCipherQR(
        validatedPayload
      );

      // Convert base64 to data URL
      const dataUrl = `data:image/png;base64,${response.qr_code_base64}`;

      set({
        originalJoke: response.original_joke,
        cipheredJoke: response.ciphered_joke || null,
        cipherUsed: response.cipher_used || null,
        qrCodeDataUrl: dataUrl,
        isLoading: false,
      });
    } catch (error) {
      let errorMessage = "Failed to generate joke cipher QR.";
      if (error instanceof ZodError) {
        errorMessage = error.issues.map((issue) => issue.message).join(", ");
      } else if (error instanceof Error) {
        errorMessage = error.message;
      }
      set({ error: errorMessage, isLoading: false });
    }
  },

  downloadQR: () => {
    const { qrCodeDataUrl } = get();
    if (qrCodeDataUrl) {
      const link = document.createElement("a");
      link.href = qrCodeDataUrl;
      link.download = "joke-qr-code.png";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  },

  reset: () => set(initialState),
}));
