import { z } from "zod";

export const QRRequestSchema = z.object({
  text: z.string().min(1, "Text cannot be empty"),
});

export const QRResponseSchema = z.object({
  qr_code_base64: z.string(),
});

export type QRRequestType = z.infer<typeof QRRequestSchema>;
export type QRResponseType = z.infer<typeof QRResponseSchema>;
