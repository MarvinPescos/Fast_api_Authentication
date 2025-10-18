import api from "../../../shared/services/api";
import type { CipherRequest, CipherResponse } from "../types/ciphers.types";

export class CiphersService {
  /**
   * Encode text using Atbash cipher
   */
  async atbashCipher(text: string): Promise<string> {
    try {
      const response = await api.post(
        "/fullstack_authentication/activities/cipher/atbash",
        {
          text,
        }
      );
      return (response as any).result;
    } catch (error: any) {
      console.error("Failed to process Atbash cipher:", error);
      throw new Error("Failed to process Atbash cipher");
    }
  }

  /**
   * Encode text using Caesar cipher
   */
  async caesarCipher(text: string, shift: number): Promise<string> {
    try {
      const response = await api.post(
        "/fullstack_authentication/activities/cipher/caesar",
        {
          text,
          shift,
        }
      );
      return (response as any).result;
    } catch (error: any) {
      console.error("Failed to process Caesar cipher:", error);
      throw new Error("Failed to process Caesar cipher");
    }
  }

  /**
   * Encode text using Vigenère cipher
   */
  async vigenereCipher(text: string, key: string): Promise<string> {
    try {
      const response = await api.post(
        "/fullstack_authentication/activities/cipher/vigenere",
        {
          text,
          key,
        }
      );
      return (response as any).result;
    } catch (error: any) {
      console.error("Failed to process Vigenère cipher:", error);
      throw new Error("Failed to process Vigenère cipher");
    }
  }
}

export const ciphersService = new CiphersService();
