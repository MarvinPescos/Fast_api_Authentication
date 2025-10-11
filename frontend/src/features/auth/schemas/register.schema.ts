import {z} from "zod";

export const registerSchema = z.object({
    username: z
      .string()
      .min(3, "Username must at least 3 characters")
      .regex(/^[a-zA-Z0-9]+$/, "Username must be alphanumeric"),
    email: z.string().email("Invalid Email address"),
    password: z
    .string()
    .min(8, "Password must at least 8 characters")
    .regex(/[A-Z]/, "Password must have at least 1 uppercase Letter")
    .regex(/[a-z]/, "Password must have at least 1 lowercase Letter")
    .regex(/\d/, "Password must have at least 1 number"),
    fullname: z.string().optional()
  })

export type registerRequest = z.infer<typeof registerSchema>;