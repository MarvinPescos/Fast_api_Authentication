import { create } from "zustand";
import type { QRGeneratorState } from "../types/qr.types";
import { qrGeneratorService } from "../services/qr.service";
import { QRRequestSchema } from "../schemas/qr.schema";
import { ZodError } from "zod";

interface QRGeneratorStore extends QRGeneratorState {
  setInputText: (text: string) => void;
  generateQR: () => Promise<void>;
  downloadQR: () => void;
  reset: () => void;
}

const initialState: QRGeneratorState = {
  inputText: "",
  qrCodeDataUrl: null,
  isLoading: false,
  error: null,
};

export const useQRGeneratorStore = create<QRGeneratorStore>((set, get) => ({
  ...initialState,

  setInputText: (text) => set({ inputText: text }),

  generateQR: async () => {
    set({ isLoading: true, error: null, qrCodeDataUrl: null });
    const { inputText } = get();

    try {
      const payload = QRRequestSchema.parse({ text: inputText });
      const response = await qrGeneratorService.generateQR(payload);

      // Convert base64 to data URL
      const dataUrl = `data:image/png;base64,${response.qr_code_base64}`;

      set({ qrCodeDataUrl: dataUrl, isLoading: false });
    } catch (error) {
      let errorMessage = "Failed to generate QR code.";
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
      link.download = "qr-code.png";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  },

  reset: () => set(initialState),
}));
