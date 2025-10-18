import { z } from "zod";
import { userSchema } from "../../users/schemas/users.schema";

export const loginSchema = z.object({
  email: z.string().email("Invalid Email address"),
  password: z
    .string()
    .min(8, "Password must at least 8 characters")
    .regex(/[A-Z]/, "Password must have at least 1 uppercase Letter")
    .regex(/[a-z]/, "Password must have at least 1 lowercase Letter")
    .regex(/\d/, "Password must have at least 1 number"),
  totp_code: z.string().optional(),
});

export const loginResponseSchema = z.object({
  user: userSchema,
  message: z.string(),
});

export type loginRequest = z.infer<typeof loginSchema>;
export type loginResponse = z.infer<typeof loginResponseSchema>;
