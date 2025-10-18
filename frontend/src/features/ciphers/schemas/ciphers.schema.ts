import { z } from "zod";

export const CipherRequestSchema = z.object({
  text: z.string().min(1, "Text is required"),
  shift: z.number().min(1).max(25).optional(),
  key: z.string().min(1).optional(),
});

export const CipherResponseSchema = z.object({
  result: z.string(),
});

export const CipherStateSchema = z.object({
  inputText: z.string(),
  outputText: z.string(),
  selectedCipher: z.enum(["atbash", "caesar", "vigenere"]),
  caesarShift: z.number(),
  vigenereKey: z.string(),
  isLoading: z.boolean(),
  error: z.string().nullable(),
});

export type CipherRequestType = z.infer<typeof CipherRequestSchema>;
export type CipherResponseType = z.infer<typeof CipherResponseSchema>;
export type CipherStateType = z.infer<typeof CipherStateSchema>;
