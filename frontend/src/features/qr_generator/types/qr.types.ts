export interface QRRequest {
  text: string;
}

export interface QRResponse {
  qr_code_base64: string;
}

export interface QRGeneratorState {
  inputText: string;
  qrCodeDataUrl: string | null;
  isLoading: boolean;
  error: string | null;
}
