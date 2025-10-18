import { create } from "zustand";
import type { CipherState, CipherType } from "../types/ciphers.types";
import { ciphersService } from "../services/ciphers.service";

interface CiphersStore extends CipherState {
  // Actions
  setInputText: (text: string) => void;
  setSelectedCipher: (cipher: CipherType) => void;
  setCaesarShift: (shift: number) => void;
  setVigenereKey: (key: string) => void;
  processCipher: () => Promise<void>;
  clearText: () => void;
  resetState: () => void;
}

const initialState: CipherState = {
  inputText: "",
  outputText: "",
  selectedCipher: "atbash",
  caesarShift: 3,
  vigenereKey: "SECRET",
  isLoading: false,
  error: null,
};

export const useCiphersStore = create<CiphersStore>((set, get) => ({
  ...initialState,

  setInputText: (text: string) => {
    set({ inputText: text, error: null });
  },

  setSelectedCipher: (cipher: CipherType) => {
    set({ selectedCipher: cipher, outputText: "", error: null });
  },

  setCaesarShift: (shift: number) => {
    set({ caesarShift: shift });
  },

  setVigenereKey: (key: string) => {
    set({ vigenereKey: key });
  },

  processCipher: async () => {
    const { inputText, selectedCipher, caesarShift, vigenereKey } = get();

    if (!inputText.trim()) {
      set({ error: "Please enter some text to cipher" });
      return;
    }

    set({ isLoading: true, error: null });

    try {
      let result: string;

      switch (selectedCipher) {
        case "atbash":
          result = await ciphersService.atbashCipher(inputText);
          break;
        case "caesar":
          result = await ciphersService.caesarCipher(inputText, caesarShift);
          break;
        case "vigenere":
          if (!vigenereKey.trim()) {
            throw new Error("Vigenère cipher requires a key");
          }
          result = await ciphersService.vigenereCipher(inputText, vigenereKey);
          break;
        default:
          throw new Error("Invalid cipher type");
      }

      set({ outputText: result, isLoading: false });
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Failed to process cipher",
        isLoading: false,
      });
    }
  },

  clearText: () => {
    set({ inputText: "", outputText: "", error: null });
  },

  resetState: () => {
    set(initialState);
  },
}));
