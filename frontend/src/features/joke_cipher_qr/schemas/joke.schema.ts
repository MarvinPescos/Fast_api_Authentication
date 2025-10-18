import { z } from "zod";

export const JokeCipherQRRequestSchema = z.object({
  cipher_type: z.enum(["atbash", "caesar", "vigenere"]).optional(),
  caesar_shift: z.number().min(1).max(25).optional(),
  vigenere_key: z.string().optional(),
});

export const JokeCipherQRResponseSchema = z.object({
  original_joke: z.string(),
  ciphered_joke: z.string().optional(),
  cipher_used: z.string().optional(),
  qr_code_base64: z.string(),
});

export type JokeCipherQRRequestType = z.infer<typeof JokeCipherQRRequestSchema>;
export type JokeCipherQRResponseType = z.infer<
  typeof JokeCipherQRResponseSchema
>;
