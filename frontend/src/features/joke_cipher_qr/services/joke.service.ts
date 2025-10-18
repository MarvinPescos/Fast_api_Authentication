import api from "../../../shared/services/api";
import type {
  JokeCipherQRRequestType,
  JokeCipherQRResponseType,
} from "../schemas/joke.schema";

export class JokeCipherQRService {
  async generateJokeCipherQR(
    payload: JokeCipherQRRequestType
  ): Promise<JokeCipherQRResponseType> {
    try {
      const response = await api.post(
        "/fullstack_authentication/activities/joke_cipher_qr/generate",
        payload
      );
      return response as JokeCipherQRResponseType;
    } catch (error: any) {
      console.error("Failed to generate joke cipher QR:", error);
      throw new Error("Failed to generate joke cipher QR");
    }
  }
}

export const jokeCipherQRService = new JokeCipherQRService();
