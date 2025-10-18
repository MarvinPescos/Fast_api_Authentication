import api from "../../../shared/services/api";
import type { QRRequestType, QRResponseType } from "../schemas/qr.schema";

export class QRGeneratorService {
  async generateQR(payload: QRRequestType): Promise<QRResponseType> {
    try {
      const response = await api.post(
        "/fullstack_authentication/activities/qr_generator/generate",
        payload
      );
      return response as QRResponseType;
    } catch (error: any) {
      console.error("Failed to generate QR code:", error);
      throw new Error("Failed to generate QR code");
    }
  }
}

export const qrGeneratorService = new QRGeneratorService();
