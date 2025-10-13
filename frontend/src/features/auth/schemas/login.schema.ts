import {z} from "zod";

export const loginSchema = z.object({
    email: z.string().email("Invalid Email address"),
    password: z
     .string()
     .min(8, "Password must at least 8 characters")
     .regex(/[A-Z]/, "Password must have at least 1 uppercase Letter")
     .regex(/[a-z]/, "Password must have at least 1 lowercase Letter")
     .regex(/\d/, "Password must have at least 1 number"),
  });

export const loginResponseSchema = z.object({
    message: z.string(),
    user_id: z.number().optional()
})

export type loginRequest = z.infer<typeof loginSchema>
export type loginResponse = z.infer<typeof loginResponseSchema>

  