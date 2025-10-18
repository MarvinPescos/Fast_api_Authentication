import { z } from "zod";

export const emailVerificationSchema = z.object({
  user_id: z.number(),
  code: z.string().length(6, "Code must be 6 digits"),
});

export const resendVerificationSchema = z.object({
  user_id: z.number(),
});

export const emailVerificationResponseSchema = z.object({
  success: z.boolean(),
  message: z.string(),
  user_id: z.number().optional(),
});

export type emailVerificationRequest = z.infer<typeof emailVerificationSchema>;
export type resendVerificationRequest = z.infer<
  typeof resendVerificationSchema
>;
export type emailVerificationResponse = z.infer<
  typeof emailVerificationResponseSchema
>;
